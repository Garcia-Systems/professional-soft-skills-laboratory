"""Behavior-based evaluation for a commitment that becomes at risk."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse
from soft_skills_lab.trust import TrustEvent, TrustEventKind

DEADLINE = 2

CRITERIA = (
    EvaluationCriterion("communicates-risk-early", "Communicates material risk before the deadline."),
    EvaluationCriterion("acknowledges-dependency", "Recognizes work that depends on the commitment."),
    EvaluationCriterion("distinguishes-known-from-unknown", "Separates known facts from uncertainty."),
    EvaluationCriterion("avoids-unsupported-promise", "Avoids certainty unsupported by evidence."),
    EvaluationCriterion("establishes-next-action", "States the next action."),
    EvaluationCriterion("establishes-follow-up", "Sets a specific follow-up point."),
    EvaluationCriterion("closes-loop", "Communicates the resulting status without being chased."),
)


def _result(criterion: EvaluationCriterion, outcome: Outcome, passed: str, failed: str, evidence: tuple[str, ...]) -> EvaluationResult:
    return EvaluationResult(criterion, outcome, passed if outcome is Outcome.PASS else failed, evidence)


def evaluate_commitment_response(response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    """Evaluate structured observations, never message wording or delivery success."""
    early = response.material_risk_communicated and response.communicated_at is not None and response.communicated_at < DEADLINE
    uncertainty = bool(response.known_information and response.unknown_information)
    checks = (
        (Outcome.PASS if early else Outcome.FAIL,
         "Material risk was communicated before Day 2.", "Material risk was not communicated before the commitment failed.",
         (f"Communicated at Day {response.communicated_at}",) if response.communicated_at is not None else ()),
        (Outcome.PASS if response.dependency_acknowledged else Outcome.FAIL,
         "Jordan's frontend dependency is explicitly acknowledged.", "The update does not help Jordan understand the effect on dependent work.",
         ("Jordan's frontend depends on the endpoint.",) if response.dependency_acknowledged else ()),
        ((Outcome.PASS if uncertainty else Outcome.PARTIAL if response.material_risk_communicated and not response.unsupported_promise else Outcome.FAIL),
         "Known facts and remaining uncertainty are both visible.", "The response does not clearly separate what is known from what remains uncertain.",
         response.known_information + response.unknown_information),
        (Outcome.FAIL if response.unsupported_promise else Outcome.PASS,
         "The response makes no unsupported delivery promise.", "The response promises delivery despite insufficient evidence.",
         (response.message,) if response.unsupported_promise else ("No unsupported promise observed.",)),
        (Outcome.PASS if response.next_action else Outcome.FAIL,
         "The response identifies a concrete next action.", "The response gives no concrete next action.",
         (response.next_action,) if response.next_action else ()),
        (Outcome.PASS if response.follow_up_point is not None else Outcome.FAIL,
         "The response establishes a specific next update point.", "The response gives no specific follow-up point.",
         (f"Next update: Day {response.follow_up_point}",) if response.follow_up_point is not None else ()),
        (Outcome.PASS if response.loop_closed else Outcome.FAIL,
         "Alex proactively communicates the resulting status and plan.", "Jordan has to discover or request the resulting status.",
         ("Final status communicated.",) if response.loop_closed else ()),
    )
    return tuple(_result(criterion, *check) for criterion, check in zip(CRITERIA, checks, strict=True))


def evidence_for_commitment(response: ProfessionalResponse) -> tuple[TrustEvent, ...]:
    """Translate observations into an explainable evidence history."""
    events: list[TrustEvent] = []
    early = response.material_risk_communicated and response.communicated_at is not None and response.communicated_at < DEADLINE
    if early:
        events.append(TrustEvent(TrustEventKind.RISK_COMMUNICATED_EARLY, "Alex raised the Day 2 risk before it failed."))
    else:
        events.append(TrustEvent(TrustEventKind.IMPORTANT_RISK_HIDDEN, "A known material delivery risk was not made visible."))
        if response.delivered_on_time is not True:
            events.append(TrustEvent(TrustEventKind.COMMITMENT_MISSED_WITHOUT_WARNING, "Jordan learned only after the deadline."))
    if response.dependency_acknowledged:
        events.append(TrustEvent(TrustEventKind.DEPENDENCY_ACKNOWLEDGED, "Jordan's frontend dependency was recognized."))
    if response.loop_closed:
        events.append(TrustEvent(TrustEventKind.FOLLOW_UP_COMPLETED, "Alex communicated the final status and revised plan."))
    if response.delivered_on_time is True:
        events.append(TrustEvent(TrustEventKind.COMMITMENT_KEPT, "The endpoint was delivered by Day 2."))
    return tuple(events)
