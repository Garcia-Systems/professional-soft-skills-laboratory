"""Small, immutable domain model for workplace exercises."""

from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4


class Outcome(Enum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    FAIL = "FAIL"


class CommitmentStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    AT_RISK = "at_risk"
    COMPLETED = "completed"
    MISSED = "missed"


@dataclass(frozen=True)
class Participant:
    name: str
    role: str


@dataclass(frozen=True)
class Commitment:
    owner: str
    action: str
    due: str


@dataclass(frozen=True)
class ProfessionalCommitment:
    """A responsibility tracked using deterministic simulated time."""

    commitment_id: str
    description: str
    owner: str
    stakeholder: str
    expected_completion: int
    status: CommitmentStatus = CommitmentStatus.PLANNED
    dependencies: tuple[str, ...] = ()
    known_risks: tuple[str, ...] = ()

    def transition(self, status: CommitmentStatus, *, risk: str | None = None) -> "ProfessionalCommitment":
        allowed = {
            CommitmentStatus.PLANNED: {CommitmentStatus.IN_PROGRESS},
            CommitmentStatus.IN_PROGRESS: {
                CommitmentStatus.AT_RISK,
                CommitmentStatus.COMPLETED,
                CommitmentStatus.MISSED,
            },
            CommitmentStatus.AT_RISK: {CommitmentStatus.COMPLETED, CommitmentStatus.MISSED},
            CommitmentStatus.COMPLETED: set(),
            CommitmentStatus.MISSED: set(),
        }
        if status not in allowed[self.status]:
            raise ValueError(f"invalid commitment transition: {self.status.value} -> {status.value}")
        if risk and status is not CommitmentStatus.AT_RISK:
            raise ValueError("a risk can only be added when transitioning to at_risk")
        from dataclasses import replace

        risks = self.known_risks + ((risk,) if risk else ())
        return replace(self, status=status, known_risks=risks)


@dataclass(frozen=True, order=True)
class TimelineEvent:
    point: int
    description: str


@dataclass(frozen=True)
class WorkplaceScenario:
    scenario_id: str
    title: str
    description: str
    participants: tuple[Participant, ...]
    known_facts: tuple[str, ...]
    uncertainties: tuple[str, ...]
    commitments: tuple[Commitment, ...]
    current_risk: RiskLevel


@dataclass(frozen=True)
class ProfessionalResponse:
    response_id: str
    label: str
    message: str
    acknowledged_facts: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    responsibility_statement: str | None = None
    next_action: str | None = None
    escalation_choice: str | None = None
    follow_up_commitment: str | None = None
    assigns_unsupported_blame: bool = False
    claims_cause_without_evidence: bool = False
    communicated_at: int | None = None
    material_risk_communicated: bool = False
    dependency_acknowledged: bool = False
    known_information: tuple[str, ...] = ()
    unknown_information: tuple[str, ...] = ()
    unsupported_promise: bool = False
    follow_up_point: int | None = None
    loop_closed: bool = False
    delivered_on_time: bool | None = None


@dataclass(frozen=True)
class EvaluationCriterion:
    criterion_id: str
    description: str


@dataclass(frozen=True)
class EvaluationResult:
    criterion: EvaluationCriterion
    outcome: Outcome
    explanation: str
    evidence: tuple[str, ...]
