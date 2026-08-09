"""Deterministic evaluation of decision-focused professional disagreement."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("captures-explicit-concern", "Understands the concern before responding."),
    EvaluationCriterion("identifies-shared-objective", "Anchors the discussion in the jointly desired outcome."),
    EvaluationCriterion("states-specific-disagreement", "Makes the precise difference clear."),
    EvaluationCriterion("uses-decision-relevant-evidence", "Supports the position with evidence relevant to the choice."),
    EvaluationCriterion("avoids-personalization", "Keeps competence, status, identity, and authorship out of the argument."),
    EvaluationCriterion("distinguishes-preference-from-defect", "Does not present preference as objective failure."),
    EvaluationCriterion("offers-constructive-alternative", "Offers another practical path when appropriate."),
    EvaluationCriterion("respects-decision-ownership", "Recognizes the legitimate final decision after evidence is heard."),
    EvaluationCriterion("updates-position-with-evidence", "Changes position when new evidence warrants it."),
    EvaluationCriterion("escalates-material-risk", "Escalates rather than normalizing a serious boundary risk."),
)


def evaluate_disagreement_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    """Evaluate explicit scenario semantics; no arbitrary prose or emotional state is parsed."""
    context = scenario.decision_context
    if context is None:
        raise ValueError("disagreement evaluation requires a decision context")
    evidence = bool(response.decision_relevant_evidence)
    preference_required = context.issue_kind.value in {"personal preference", "convention"}
    update_required = scenario.scenario_id == "manager-correct"
    escalation_required = context.issue_kind.value == "material risk"
    ownership_applicable = context.final_choice is not None
    alternative_applicable = len(context.alternatives) > 1
    checks: tuple[bool | None, ...] = (
        response.captures_explicit_concern,
        response.identifies_shared_objective,
        response.states_specific_disagreement,
        evidence,
        not response.personalizes_disagreement,
        response.distinguishes_preference_from_defect if preference_required else True,
        bool(response.constructive_alternative) if alternative_applicable else None,
        (response.respects_decision_ownership and not response.repeats_resolved_argument) if ownership_applicable else None,
        response.updates_position_with_evidence if update_required else None,
        response.escalates_material_risk if escalation_required else None,
    )
    results = []
    for criterion, passed in zip(CRITERIA, checks, strict=True):
        if passed is None:
            outcome, explanation = Outcome.PARTIAL, "This dimension is not required by this decision state."
        elif passed:
            outcome, explanation = Outcome.PASS, criterion.description
        else:
            outcome, explanation = Outcome.FAIL, criterion.description
        if criterion.criterion_id == "uses-decision-relevant-evidence" and not evidence and response.implementation_details:
            outcome, explanation = Outcome.PARTIAL, "Technical concepts were supplied without a practical decision consequence."
        item_evidence = response.decision_relevant_evidence if criterion.criterion_id == "uses-decision-relevant-evidence" else (response.message,)
        results.append(EvaluationResult(criterion, outcome, explanation, item_evidence))
    return tuple(results)
