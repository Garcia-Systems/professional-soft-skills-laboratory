"""Small observable preparation example for Chapter 1."""

from dataclasses import dataclass

from soft_skills_lab.trust import TrustEvent, TrustEventKind


@dataclass(frozen=True)
class PreparationBehavior:
    behavior_id: str
    reviewed_material: bool
    brought_requested_artifact: bool
    prepared_question: bool


PREPARATION_BEHAVIORS = {
    "unreviewed": PreparationBehavior("unreviewed", False, False, False),
    "reviewed-no-artifact": PreparationBehavior("reviewed-no-artifact", True, False, False),
    "fully-prepared": PreparationBehavior("fully-prepared", True, True, True),
}


def preparation_evidence(behavior: PreparationBehavior) -> tuple[TrustEvent, ...]:
    evidence: list[TrustEvent] = []
    if behavior.reviewed_material:
        evidence.append(TrustEvent(TrustEventKind.PREPARED_FOR_WORK, "Reviewed the T0 agenda before the T2 review."))
    if behavior.brought_requested_artifact:
        evidence.append(TrustEvent(TrustEventKind.PREPARED_FOR_WORK, "Brought the explicitly requested artifact."))
    if behavior.prepared_question:
        evidence.append(TrustEvent(TrustEventKind.EXPECTATION_CLARIFIED, "Identified one question in advance."))
    return tuple(evidence)
