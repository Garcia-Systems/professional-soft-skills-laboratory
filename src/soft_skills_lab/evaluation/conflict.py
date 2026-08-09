"""Chapter 10 evaluation of authored, observable conflict behavior."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("avoids-blame", "Avoids unsupported blame while addressing the work."),
    EvaluationCriterion("identifies-shared-objective", "Connects the response to the objective participants share."),
    EvaluationCriterion("uses-decision-relevant-evidence", "Uses evidence that can inform the current choice."),
    EvaluationCriterion("respects-decision-ownership", "Names or follows the legitimate decision path."),
    EvaluationCriterion("establishes-follow-up", "When deferring, establishes an inspectable next point."),
    EvaluationCriterion("distinguishes-fact-from-interpretation", "Restores facts without presenting accusations as facts."),
    EvaluationCriterion("avoids-counterattack", "Avoids answering personalization with another attack."),
    EvaluationCriterion("avoids-unsupported-motive-attribution", "Does not invent another person's motive."),
    EvaluationCriterion("acknowledges-legitimate-concern", "Recognizes legitimate pressure without requiring concession."),
    EvaluationCriterion("refocuses-current-issue", "Returns to the specific issue being decided."),
    EvaluationCriterion("keeps-conflict-scoped", "Does not expand the dispute to people, groups, or unrelated history."),
    EvaluationCriterion("restores-shared-facts", "Restores established evidence rather than accusation."),
    EvaluationCriterion("creates-decision-path", "Names how or when the unresolved issue will be decided."),
    EvaluationCriterion("uses-pause-productively", "If pausing, supplies a checkpoint and needed evidence."),
    EvaluationCriterion("repairs-own-contribution", "If repair is needed, acknowledges and corrects one's contribution."),
    EvaluationCriterion("preserves-material-risk", "Does not suppress an important concern to end friction."),
)


def evaluate_conflict_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    """Inspect semantic fields only; message wording and emotional state are not analyzed."""
    if scenario.conflict_state is None:
        raise ValueError("conflict evaluation requires a conflict state")
    repair_required = scenario.scenario_id == "code-review-conflict"
    pause = response.pauses_conversation
    checks: tuple[bool | None, ...] = (
        not (response.assigns_unsupported_blame or response.attributes_motive_without_evidence or response.attacks_group),
        response.identifies_shared_objective,
        bool(response.decision_relevant_evidence) or response.restores_shared_facts,
        response.respects_decision_ownership or response.creates_decision_path,
        (response.pause_has_checkpoint and bool(response.follow_up_commitment or response.follow_up_point is not None)) if pause else None,
        response.distinguishes_fact_from_interpretation or response.restores_shared_facts,
        not (response.generalizes_about_person or response.attacks_group or response.personalizes_disagreement or response.uses_sarcasm),
        not response.attributes_motive_without_evidence,
        response.acknowledges_legitimate_concern,
        response.focuses_on_current_decision,
        not (response.generalizes_about_person or response.attacks_group) and response.focuses_on_current_decision,
        response.restores_shared_facts,
        response.creates_decision_path,
        (response.pause_has_checkpoint and response.pause_names_needed_evidence) if pause else None,
        response.repairs_own_contribution if repair_required else None,
        response.preserves_material_risk,
    )
    results = []
    for criterion, check in zip(CRITERIA, checks, strict=True):
        outcome = Outcome.PARTIAL if check is None else Outcome.PASS if check else Outcome.FAIL
        explanation = "Not applicable to this response path." if check is None else (
            "The authored behavior satisfies this criterion." if check else "The authored behavior does not satisfy this criterion."
        )
        results.append(EvaluationResult(criterion, outcome, explanation, (response.message,)))
    return tuple(results)
