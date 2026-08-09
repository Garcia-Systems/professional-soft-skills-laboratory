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


class StatusCategory(Enum):
    """Decision-relevant state, deliberately more precise than traffic-light colors."""

    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BLOCKED = "blocked"
    COMPLETED = "completed"


@dataclass(frozen=True)
class Forecast:
    """An evidence-based estimate, not a promise or numeric probability."""

    target: str
    basis: str
    condition: str | None = None
    guaranteed: bool = False


@dataclass(frozen=True)
class StatusUpdate:
    """Structured status semantics authored by a scenario, never parsed from prose."""

    subject: str
    current_state: StatusCategory | None = None
    completed_work: tuple[str, ...] = ()
    remaining_work: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    uncertainties: tuple[str, ...] = ()
    dependency_impact: tuple[str, ...] = ()
    next_action: str | None = None
    requested_action: str | None = None
    forecast: Forecast | None = None
    next_update_point: int | None = None
    dependency_owner: str | None = None
    decision_point: str | None = None
    activity_details: tuple[str, ...] = ()


class DecisionRelevance(Enum):
    """How strongly an unknown affects the decision currently being made."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    RESOLVED = "resolved"


class InformationSource(Enum):
    SELF_INVESTIGATION = "self investigation"
    TEAMMATE = "teammate"
    MANAGER = "manager"
    STAKEHOLDER = "stakeholder"
    DOCUMENTATION = "documentation"
    EXTERNAL_DEPENDENCY = "external dependency"


@dataclass(frozen=True)
class DecisionUnknown:
    unknown_id: str
    description: str
    relevance: DecisionRelevance
    source: InformationSource
    consequence: str
    blocking: bool = False
    resolved_value: str | None = None

    @property
    def is_resolved(self) -> bool:
        return self.resolved_value is not None or self.relevance is DecisionRelevance.RESOLVED


@dataclass(frozen=True)
class ProfessionalQuestion:
    """Scenario-authored question semantics; message wording is illustrative only."""

    question_id: str
    target_unknowns: tuple[str, ...]
    message: str
    source: InformationSource
    investigation_performed: tuple[str, ...] = ()
    context_supplied: tuple[str, ...] = ()
    answerable: bool = True
    embedded_assumptions: tuple[str, ...] = ()
    non_blocking: bool = False


@dataclass(frozen=True)
class QuestionContext:
    decision: str
    unknowns: tuple[DecisionUnknown, ...]
    available_evidence: tuple[str, ...] = ()


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
class CommunicationContext:
    """Scenario-authored meaning: no meaning is inferred from arbitrary text."""

    explicit_facts: tuple[str, ...]
    expressed_concern: str
    requested_action: str | None = None
    constraints: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    possible_interpretations: tuple[str, ...] = ()
    unsupported_assumptions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ListenerInterpretation:
    """Structured semantic observations attached to a reference response."""

    understood_facts: tuple[str, ...] = ()
    inferred_intent: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    clarification_needed: tuple[str, ...] = ()
    proposed_response: str | None = None


@dataclass(frozen=True)
class CommunicationAudience:
    """A scenario-specific audience; role is context, not a competence proxy."""

    audience_id: str
    role: str
    technical_context: str
    decision_responsibility: str
    information_needs: tuple[str, ...]


@dataclass(frozen=True)
class ExplanationContext:
    """Explicit truth and audience views used for deterministic explanations."""

    audiences: tuple[CommunicationAudience, ...]
    information_layers: tuple[tuple[str, tuple[str, ...]], ...]
    architecture_views: tuple[tuple[str, tuple[str, ...]], ...] = ()


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
    communication_context: CommunicationContext | None = None
    question_context: QuestionContext | None = None
    explanation_context: ExplanationContext | None = None


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
    listener_interpretation: ListenerInterpretation | None = None
    captures_explicit_concern: bool = False
    distinguishes_fact_from_interpretation: bool = False
    clarifies_success_condition: bool = False
    respectful_disagreement: bool = False
    questions: tuple[ProfessionalQuestion, ...] = ()
    investigation_performed: tuple[str, ...] = ()
    supplies_question_context: bool = False
    question_dump: bool = False
    delay_creates_risk: bool = False
    investigation_delay: int = 0
    immediate_escalation: bool = False
    authority_limited: bool = False
    proposed_next_action: bool = False
    problem_first_sequence: bool | None = None
    communicated_fact_ids: tuple[str, ...] = ()
    communicated_need_ids: tuple[str, ...] = ()
    unsupported_claims: tuple[str, ...] = ()
    implementation_details: tuple[str, ...] = ()
    communicates_impact: bool = False
    communicates_scope: bool = False
    preserves_uncertainty: bool = False
    supports_decision: bool = False
    status_update: StatusUpdate | None = None


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
