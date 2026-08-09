"""Observable, deterministic evaluation of Chapter 2 listening behavior."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse
from soft_skills_lab.evaluation.commitment import CRITERIA as COMMITMENT_CRITERIA

_REUSED = {criterion.criterion_id: criterion for criterion in COMMITMENT_CRITERIA}
CRITERIA = (
    EvaluationCriterion("captures-explicit-concern", "Correctly identifies the concern the speaker expressed."),
    EvaluationCriterion("distinguishes-fact-from-interpretation", "Keeps observations distinct from interpretation."),
    EvaluationCriterion("avoids-unsupported-assumption", "Does not invent motives, blame, requirements, or causes."),
    EvaluationCriterion("avoids-premature-solution", "Does not commit to a solution before understanding the problem."),
    EvaluationCriterion("identifies-unknowns", "Makes important missing information visible."),
    EvaluationCriterion("clarifies-success-condition", "Clarifies the outcome needed before committing."),
    _REUSED["establishes-next-action"],
    _REUSED["establishes-follow-up"],
)


def evaluate_listening_response(response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    """Evaluate scenario-authored semantics, never keywords in ``message``."""
    interpretation = response.listener_interpretation
    assumptions = response.assumptions + (interpretation.assumptions if interpretation else ())
    unknowns = response.unknown_information or (interpretation.clarification_needed if interpretation else ())
    checks = (
        (response.captures_explicit_concern, "The expressed concern is accurately represented.",
         "The response does not show that the speaker's actual concern was understood.", response.acknowledged_facts),
        (response.distinguishes_fact_from_interpretation, "Observed facts remain distinct from causes or conclusions.",
         "The response does not distinguish observations from interpretation.", response.known_information),
        (not assumptions and not response.assigns_unsupported_blame and not response.claims_cause_without_evidence,
         "No unsupported motive, blame, requirement, or cause is introduced.",
         "The response goes beyond the available evidence.", assumptions or (response.message,)),
        (not response.unsupported_promise, "No solution is promised before diagnosis or clarification.",
         "A solution or commitment is selected before the problem is understood.", (response.message,)),
        (bool(unknowns), "Important unknown information is identified.",
         "Important ambiguity remains unacknowledged.", tuple(unknowns)),
        (response.clarifies_success_condition, "The response seeks or establishes the outcome needed.",
         "The meaning of success remains unclear.", (response.message,)),
        (bool(response.next_action), "A concrete next action is established.",
         "No concrete next action is established.", (response.next_action,) if response.next_action else ()),
        (bool(response.follow_up_commitment), "A follow-up point tells the speaker when information is coming.",
         "No follow-up point is established.", (response.follow_up_commitment,) if response.follow_up_commitment else ()),
    )
    results = []
    for criterion, (passed, pass_text, fail_text, evidence) in zip(CRITERIA, checks, strict=True):
        # Acknowledging and taking an action has partial value even when clarification is absent.
        outcome = Outcome.PASS if passed else Outcome.FAIL
        if not passed and criterion.criterion_id == "captures-explicit-concern" and response.next_action and not assumptions:
            outcome = Outcome.PARTIAL
        results.append(EvaluationResult(criterion, outcome, pass_text if passed else fail_text, tuple(evidence)))
    return tuple(results)
