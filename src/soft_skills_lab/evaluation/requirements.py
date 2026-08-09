"""Deterministic Chapter 14 behavioral evaluation."""
from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("identifies-material-ambiguity", "Identifies missing information that changes behavior or a decision."),
    EvaluationCriterion("distinguishes-ambiguity-from-low-value-detail", "Does not block on safely deferrable details."),
    EvaluationCriterion("surfaces-contradiction", "Makes conflicting evidence visible."),
    EvaluationCriterion("uses-existing-evidence", "Resolves what authoritative context already resolves."),
    EvaluationCriterion("records-visible-assumption", "Makes any working assumption inspectable."),
    EvaluationCriterion("uses-safe-default", "Uses convention only when low-risk, reversible, and explicit."),
    EvaluationCriterion("requires-decision-for-material-semantics", "Does not silently choose material product meaning."),
    EvaluationCriterion("creates-testable-acceptance-condition", "Produces observable verification conditions."),
    EvaluationCriterion("updates-requirement-history", "Keeps decisions and later changes traceable."),
    EvaluationCriterion("preserves-uncertainty", "Does not present unresolved meaning as fact."),
    EvaluationCriterion("asks-useful-clarification", "Targets decision-relevant uncertainty rather than maximizing questions."),
    EvaluationCriterion("aligns-commitment-with-decision", "Commits only to work supported by current decisions."),
)


def _outcome(value: bool | None) -> Outcome:
    return Outcome.PARTIAL if value is None else Outcome.PASS if value else Outcome.FAIL


def evaluate_requirement_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    if scenario.requirement_context is None:
        raise ValueError("requirement evaluation requires a requirement context")
    contradiction_relevant = bool(scenario.requirement_context.contradictions) or scenario.scenario_id == "transaction-export"
    checks = (
        response.identifies_material_ambiguity,
        response.distinguishes_low_value_detail,
        response.surfaces_contradiction if contradiction_relevant else None,
        response.uses_existing_evidence,
        response.records_visible_assumption,
        response.uses_safe_default,
        response.requires_material_decision,
        response.creates_testable_acceptance_condition,
        response.updates_requirement_history,
        response.preserves_uncertainty and not response.exceeds_available_evidence,
        response.seeks_specific_understanding and not response.question_dump,
        response.aligns_commitment_with_decision,
    )
    return tuple(EvaluationResult(c, _outcome(v), "Not central to this authored path." if v is None else
        "Authored behavioral evidence satisfies the criterion." if v else "Authored behavioral evidence does not satisfy the criterion.",
        (response.message,)) for c, v in zip(CRITERIA, checks, strict=True))
