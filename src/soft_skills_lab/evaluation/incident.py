"""Explainable, behavior-based evaluation for the Chapter 0 incident."""

from collections.abc import Callable

from soft_skills_lab.domain.models import (
    EvaluationCriterion,
    EvaluationResult,
    Outcome,
    ProfessionalResponse,
)

INCIDENT_FACT = "A production incident occurred after the feature deployment."

CRITERIA = (
    EvaluationCriterion("acknowledges-impact", "Recognizes the incident and its impact."),
    EvaluationCriterion("avoids-unsupported-claims", "Avoids conclusions before evidence is reviewed."),
    EvaluationCriterion("accepts-owned-responsibility", "Accepts responsibility for clearly owned work."),
    EvaluationCriterion("avoids-blame", "Does not assign unsupported blame."),
    EvaluationCriterion("establishes-next-action", "Identifies a concrete investigation action."),
    EvaluationCriterion("establishes-follow-up", "Establishes when findings will be communicated."),
)

Check = tuple[Callable[[ProfessionalResponse], bool], str, str, Callable[[ProfessionalResponse], tuple[str, ...]]]


def _present(value: str | None) -> bool:
    return bool(value and value.strip())


CHECKS: tuple[Check, ...] = (
    (
        lambda response: INCIDENT_FACT in response.acknowledged_facts,
        "The response recognizes that a production incident occurred and requires attention.",
        "The response does not acknowledge the known incident.",
        lambda response: response.acknowledged_facts,
    ),
    (
        lambda response: not response.claims_cause_without_evidence and not response.assumptions,
        "The response does not claim the feature is innocent or guilty before evidence is reviewed.",
        "The response presents an unverified conclusion or assumption as settled.",
        lambda response: response.assumptions or (response.message,),
    ),
    (
        lambda response: _present(response.responsibility_statement),
        "The response states responsibility for the actor's owned work without accepting unknown causes.",
        "The response does not identify responsibility for any clearly owned work.",
        lambda response: (response.responsibility_statement,) if response.responsibility_statement else (),
    ),
    (
        lambda response: not response.assigns_unsupported_blame,
        "The response avoids assigning fault without evidence.",
        "The response shifts blame before the cause is established.",
        lambda response: (response.message,),
    ),
    (
        lambda response: _present(response.next_action),
        "The response identifies a concrete action to investigate or limit impact.",
        "The response provides no concrete next action.",
        lambda response: (response.next_action,) if response.next_action else (),
    ),
    (
        lambda response: _present(response.follow_up_commitment),
        "The response commits to a defined follow-up after investigation.",
        "The response gives no follow-up point for findings.",
        lambda response: (response.follow_up_commitment,) if response.follow_up_commitment else (),
    ),
)


def evaluate_incident_response(response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    """Evaluate structured behaviors, deliberately ignoring exact message phrasing."""
    results = []
    for criterion, (check, pass_text, fail_text, evidence) in zip(CRITERIA, CHECKS, strict=True):
        passed = check(response)
        results.append(
            EvaluationResult(
                criterion=criterion,
                outcome=Outcome.PASS if passed else Outcome.FAIL,
                explanation=pass_text if passed else fail_text,
                evidence=tuple(item for item in evidence(response) if item),
            )
        )
    return tuple(results)
