"""Deterministic evaluation of Chapter 8 responsibility responses."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario


CRITERIA = (
    EvaluationCriterion("identifies-own-contribution", "Identifies the specific supported action or omission."),
    EvaluationCriterion("does-not-over-own", "Does not claim responsibility beyond the evidence."),
    EvaluationCriterion("does-not-shift-blame", "Does not use another contributor or process to erase one's part."),
    EvaluationCriterion("preserves-agency", "Does not falsely claim there was no choice."),
    EvaluationCriterion("uses-context-without-erasing-responsibility", "Keeps context compatible with ownership."),
    EvaluationCriterion("acknowledges-impact", "Recognizes relevant effects on customers or collaborators."),
    EvaluationCriterion("prioritizes-containment", "Addresses current harm before only future improvement."),
    EvaluationCriterion("identifies-corrective-action", "Names how the immediate defect or missed handoff will be corrected."),
    EvaluationCriterion("identifies-preventive-action", "Names a credible recurrence-reduction behavior."),
    EvaluationCriterion("avoids-self-condemnation", "Keeps a bounded mistake distinct from an identity judgment."),
)


def evaluate_responsibility_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    """Evaluate authored semantics, never apology wording, emotion, intent, or personality."""
    no_personal_fault = scenario.scenario_id == "unavoidable-outcome"
    own: bool | None = response.identifies_own_contribution
    if no_personal_fault and response.responsibility_statement:
        own = True  # accurately owns recovery while declining unsupported fault
    checks = (
        own,
        not response.over_owns,
        not response.assigns_unsupported_blame,
        response.preserves_agency,
        not response.context_used_as_excuse,
        response.acknowledges_impact,
        response.prioritizes_containment,
        response.identifies_corrective_action,
        response.identifies_preventive_action,
        not response.self_condemnation,
    )
    results = []
    for criterion, passed in zip(CRITERIA, checks, strict=True):
        outcome = Outcome.PASS if passed else Outcome.FAIL
        if (criterion.criterion_id == "identifies-own-contribution" and response.responsibility_statement
                and not passed and not response.over_owns):
            outcome = Outcome.PARTIAL
        if criterion.criterion_id == "acknowledges-impact" and response.acknowledges_feedback and not passed:
            outcome = Outcome.PARTIAL
        if criterion.criterion_id in {"prioritizes-containment", "identifies-corrective-action", "identifies-preventive-action"} and no_personal_fault:
            # Recovery can be professional without inventing an avoidable mistake or prevention prematurely.
            if criterion.criterion_id == "identifies-preventive-action":
                outcome = Outcome.PARTIAL
        evidence = (response.responsibility_statement or response.message,)
        explanation = ("Authored behavior satisfies this observable criterion." if outcome is Outcome.PASS
                       else "The response only partly establishes this behavior." if outcome is Outcome.PARTIAL
                       else criterion.description)
        results.append(EvaluationResult(criterion, outcome, explanation, evidence))
    return tuple(results)
