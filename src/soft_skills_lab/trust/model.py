"""Professional trust represented as a history of observable evidence."""

from dataclasses import dataclass
from enum import Enum


class TrustEventKind(Enum):
    PREPARED_FOR_WORK = (1, "Prepared for work")
    RISK_COMMUNICATED_EARLY = (2, "Risk communicated early")
    COMMITMENT_KEPT = (2, "Commitment kept")
    MISTAKE_ACKNOWLEDGED = (1, "Mistake acknowledged")
    FOLLOW_UP_COMPLETED = (2, "Follow-up completed")
    UNSUPPORTED_CLAIM_MADE = (-1, "Unsupported claim made")
    IMPORTANT_RISK_HIDDEN = (-3, "Important risk hidden")
    COMMITMENT_MISSED_WITHOUT_WARNING = (-3, "Commitment missed without warning")
    FOLLOW_UP_MISSED = (-2, "Follow-up missed")
    DEPENDENCY_ACKNOWLEDGED = (1, "Dependency acknowledged")
    EXPECTATION_CLARIFIED = (1, "Expectation clarified")
    CORRECTIVE_ACTION_TAKEN = (1, "Corrective action taken")
    FEEDBACK_RECEIVED = (0, "Feedback received")
    CHANGED_BEHAVIOR_DEMONSTRATED = (2, "Changed behavior demonstrated")
    RESPONSIBILITY_ACKNOWLEDGED = (1, "Responsibility acknowledged")
    PREVENTIVE_ACTION_COMPLETED = (2, "Preventive action completed")
    IMPACTED_PARTY_FOLLOWED_UP = (2, "Impacted party followed up")
    BLAME_SHIFTED = (-1, "Blame shifted")
    KNOWN_RESPONSIBILITY_DENIED = (-2, "Known responsibility denied")
    SAME_AVOIDABLE_FAILURE_REPEATED = (-3, "Same avoidable failure repeated")
    CONCERN_RAISED_WITH_EVIDENCE = (2, "Concern raised with evidence")
    DECISION_SUPPORTED_AFTER_RESOLUTION = (2, "Decision supported after resolution")
    POSITION_UPDATED_AFTER_NEW_EVIDENCE = (2, "Position updated after new evidence")
    MATERIAL_RISK_ESCALATED = (2, "Material risk escalated")
    RELEVANT_CONCERN_WITHHELD = (-2, "Relevant concern withheld")
    DISAGREEMENT_PERSONALIZED = (-2, "Disagreement personalized")
    DECISION_UNDERMINED_AFTER_RESOLUTION = (-3, "Decision undermined after resolution")
    UNSUPPORTED_ARGUMENT_REPEATED = (-2, "Unsupported argument repeated")

    @property
    def weight(self) -> int:
        return self.value[0]

    @property
    def label(self) -> str:
        return self.value[1]


@dataclass(frozen=True)
class TrustEvent:
    kind: TrustEventKind
    detail: str


@dataclass(frozen=True)
class ProfessionalTrust:
    history: tuple[TrustEvent, ...] = ()

    @property
    def balance(self) -> int:
        return sum(event.kind.weight for event in self.history)

    def record(self, event: TrustEvent) -> "ProfessionalTrust":
        return ProfessionalTrust(self.history + (event,))


DEMO_EVENTS = (
    TrustEvent(TrustEventKind.RISK_COMMUNICATED_EARLY, "Warned that migration time threatened the release window."),
    TrustEvent(TrustEventKind.COMMITMENT_KEPT, "Delivered the migration review when promised."),
    TrustEvent(TrustEventKind.MISTAKE_ACKNOWLEDGED, "Reported an incorrect configuration without concealment."),
    TrustEvent(TrustEventKind.FOLLOW_UP_COMPLETED, "Shared the promised corrective-action notes."),
    TrustEvent(TrustEventKind.COMMITMENT_MISSED_WITHOUT_WARNING, "Missed a later review with no advance notice."),
)

FEEDBACK_IMPROVEMENT_EVENTS = (
    TrustEvent(TrustEventKind.FEEDBACK_RECEIVED, "Alex received feedback about surfacing material delivery risk."),
    TrustEvent(TrustEventKind.EXPECTATION_CLARIFIED, "Alex and Morgan clarified the early-risk update expectation."),
    TrustEvent(TrustEventKind.RISK_COMMUNICATED_EARLY, "Alex reported the next material risk when discovered at T2."),
    TrustEvent(TrustEventKind.CHANGED_BEHAVIOR_DEMONSTRATED, "Alex named the dependency at T2 and followed up at T3."),
)

RESPONSIBILITY_LEARNING_EVENTS = (
    TrustEvent(TrustEventKind.RESPONSIBILITY_ACKNOWLEDGED, "Alex acknowledged skipping required staging validation."),
    TrustEvent(TrustEventKind.CORRECTIVE_ACTION_TAKEN, "The endpoint was corrected and validated before redeployment."),
    TrustEvent(TrustEventKind.PREVENTIVE_ACTION_COMPLETED, "Staging validation became a deployment gate."),
    TrustEvent(TrustEventKind.CHANGED_BEHAVIOR_DEMONSTRATED, "Alex ran the gate and stopped a later invalid endpoint before production."),
    TrustEvent(TrustEventKind.IMPACTED_PARTY_FOLLOWED_UP, "Alex reported the stopped deployment and closed the incident follow-up."),
)

DISAGREEMENT_EVENTS = (
    TrustEvent(TrustEventKind.CONCERN_RAISED_WITH_EVIDENCE, "Alex surfaced vendor-change evidence before Morgan's call."),
    TrustEvent(TrustEventKind.DECISION_SUPPORTED_AFTER_RESOLUTION, "Alex documented the tradeoff and implemented the resolved choice."),
    TrustEvent(TrustEventKind.POSITION_UPDATED_AFTER_NEW_EVIDENCE, "Alex withdrew an objection after the benchmark changed the evidence."),
    TrustEvent(TrustEventKind.MATERIAL_RISK_ESCALATED, "Alex escalated customer-data exposure through the appropriate path."),
)
