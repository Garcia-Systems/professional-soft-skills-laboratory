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
    FAIL = "FAIL"


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
