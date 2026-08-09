"""Deterministic stakeholder evaluation over scenario-authored semantics."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("identifies-business-outcome", "Identifies what the stakeholder is trying to accomplish."),
    EvaluationCriterion("separates-outcome-from-solution", "Distinguishes need from requested implementation when appropriate."),
    EvaluationCriterion("respects-explicit-requirement", "Does not silently substitute when a property is required."),
    EvaluationCriterion("communicates-tradeoff", "Explains what is gained and lost across options."),
    EvaluationCriterion("makes-scope-change-explicit", "Surfaces a material change to agreed delivery."),
    EvaluationCriterion("provides-professional-recommendation", "Recommends an option when evidence supports one."),
    EvaluationCriterion("aligns-commitment-with-decision", "Makes commitment follow an explicit decision."),
    EvaluationCriterion("preserves-business-context", "Keeps the business reason visible in technical communication."),
    EvaluationCriterion("asks-useful-clarification", "Asks decision-relevant questions without a question dump."),
    EvaluationCriterion("supports-decision", "Supplies information that enables the decision owner."),
    EvaluationCriterion("avoids-unnecessary-detail", "Uses the audience's decision layer rather than irrelevant internals."),
    EvaluationCriterion("communicates-risk", "Makes relevant technical and delivery risk visible."),
    EvaluationCriterion("preserves-uncertainty", "Does not turn uncertain feasibility into certainty."),
    EvaluationCriterion("respects-decision-ownership", "Separates business, product, and technical decision roles."),
    EvaluationCriterion("updates-position-with-evidence", "Changes a recommendation when material new evidence arrives."),
    EvaluationCriterion("establishes-follow-up", "Makes the decision or follow-up checkpoint explicit."),
)

def _outcome(value: bool | None) -> Outcome:
    return Outcome.PARTIAL if value is None else Outcome.PASS if value else Outcome.FAIL

def evaluate_stakeholder_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    if scenario.stakeholder_request is None:
        raise ValueError("stakeholder evaluation requires a stakeholder request")
    scope_relevant = scenario.scope_change is not None or response.response_id == "silent-scope-reduction"
    recommendation_relevant = scenario.scenario_id in ("reporting-export", "stakeholder-search-performance", "urgent-bulk-upload", "xlsx-required")
    update_relevant = scenario.scenario_id == "xlsx-required"
    checks: tuple[bool | None, ...] = (
        response.identifies_business_outcome,
        response.separates_outcome_from_solution,
        response.respects_explicit_requirement,
        response.communicates_tradeoff,
        response.makes_scope_change_explicit if scope_relevant else None,
        response.provides_professional_recommendation if recommendation_relevant else None,
        response.aligns_commitment_with_decision if scenario.scenario_id in ("reporting-export", "impossible-export-constraints") else None,
        response.preserves_business_context,
        (response.seeks_specific_understanding and not response.question_dump) if scenario.stakeholder_request.open_questions else None,
        response.supports_decision or response.communicates_tradeoff or response.respects_decision_ownership,
        not bool(response.implementation_details),
        response.technical_risk_made_visible,
        not response.unsupported_promise and not response.exceeds_available_evidence,
        response.respects_decision_ownership,
        response.updates_position_with_evidence if update_relevant else None,
        bool(response.follow_up_commitment or response.follow_up_point is not None or response.respects_decision_ownership),
    )
    return tuple(EvaluationResult(criterion, _outcome(check),
        "Not central to this authored path." if check is None else
        "Authored behavioral evidence satisfies the criterion." if check else
        "Authored behavioral evidence does not satisfy the criterion.", (response.message,))
        for criterion, check in zip(CRITERIA, checks, strict=True))
