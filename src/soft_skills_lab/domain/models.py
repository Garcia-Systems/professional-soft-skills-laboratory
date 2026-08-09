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


class UncertaintyKind(Enum):
    """Why an answer is unavailable; each kind implies a different response."""

    UNKNOWN = "unknown"
    UNCERTAIN = "uncertain"
    NOT_YET_INVESTIGATED = "not-yet-investigated"
    UNKNOWABLE_FROM_CURRENT_EVIDENCE = "unknowable-from-current-evidence"


class FeedbackEvidenceStrength(Enum):
    """An inspectable relationship between feedback and scenario evidence."""

    DIRECT_OBSERVATION = "direct observation"
    SPECIFIC_EXAMPLE = "specific example"
    PATTERN_SUPPORTED = "pattern supported"
    GENERALIZATION_UNSUPPORTED = "generalization unsupported"


@dataclass(frozen=True)
class FeedbackEvidence:
    statement: str
    strength: FeedbackEvidenceStrength


@dataclass(frozen=True)
class BehavioralActionPlan:
    """A future observable rule, distinct from a verbal promise."""

    owner: str
    trigger: str
    behavior: str
    follow_up: str | None = None


@dataclass(frozen=True)
class ResponsibilityBoundary:
    """Evidence-based scope for one actor, not a legal-liability finding."""

    actor: str
    controlled: tuple[str, ...] = ()
    did_not_control: tuple[str, ...] = ()
    contribution: tuple[str, ...] = ()


@dataclass(frozen=True)
class ResponsibilityMap:
    """Deterministic decomposition of an outcome and its responsibility boundaries."""

    incident: str
    boundaries: tuple[ResponsibilityBoundary, ...]
    process_conditions: tuple[str, ...] = ()
    external_factors: tuple[str, ...] = ()
    results: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    not_supported: tuple[str, ...] = ()
    immediate_responsibility: tuple[str, ...] = ()
    preventive_action: tuple[str, ...] = ()


class DecisionIssueKind(Enum):
    """The decision significance of a disputed point, authored rather than inferred."""

    CORRECTNESS = "correctness issue"
    MAINTAINABILITY = "maintainability tradeoff"
    CONVENTION = "convention"
    PREFERENCE = "personal preference"
    MATERIAL_RISK = "material risk"


class ConflictStage(Enum):
    """Observable conversational stage, not an inferred emotional intensity."""

    DISAGREEMENT = "disagreement"
    RISING_TENSION = "rising tension"
    PERSONALIZED_CONFLICT = "personalized conflict"
    DE_ESCALATED = "de-escalated"
    DECISION_RESOLVED = "decision resolved"


class VisibilityThreshold(Enum):
    """Scenario-specific action boundary agreed by an employee and manager."""

    ROUTINE = "ROUTINE"
    INFORM = "INFORM"
    CONSULT = "CONSULT"
    ESCALATE = "ESCALATE"


class HandoffState(Enum):
    """Observable handoff milestones; artifact creation is deliberately not delivery."""

    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ACCEPTED = "ACCEPTED"
    REWORK_REQUIRED = "REWORK REQUIRED"


class IncidentState(Enum):
    """Operational incident milestones, separate from causal conclusions."""

    DETECTED = "DETECTED"
    ACTIVE = "ACTIVE"
    CONTAINED = "CONTAINED"
    RECOVERING = "RECOVERING"
    RESOLVED = "RESOLVED"
    REVIEWED = "REVIEWED"


class WorkCapacity(Enum):
    """Actor-declared or scenario-authored work capacity, never a diagnosis."""

    FULL = "FULL"
    REDUCED = "REDUCED"
    UNAVAILABLE = "UNAVAILABLE"
    UNSAFE_FOR_HIGH_RISK_TASK = "UNSAFE_FOR_HIGH_RISK_TASK"


class DisclosureBoundary(Enum):
    """Educational information boundary; it does not encode law or policy."""

    PRIVATE = "PRIVATE"
    OPTIONAL_CONTEXT = "OPTIONAL_CONTEXT"
    WORK_RELEVANT = "WORK_RELEVANT"
    REQUIRED_FOR_REQUEST = "REQUIRED_FOR_REQUEST"


class MeasurementKind(Enum):
    """Quality of an authored performance measure, not a score for a person."""

    ACTIVITY = "activity"
    PERSONALITY = "personality"
    OUTCOME_ONLY = "outcome-only"
    OBSERVABLE_BEHAVIOR = "observable-behavior"


class PerformancePlanStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    EXTENDED = "EXTENDED"
    UNSATISFACTORY = "UNSATISFACTORY"
    SUPERSEDED = "SUPERSEDED"


@dataclass(frozen=True)
class PerformanceMeasurement:
    statement: str
    kind: MeasurementKind
    within_reasonable_control: bool


@dataclass(frozen=True)
class PerformanceConcern:
    """A claim decomposed into evidence and an observable expectation."""

    concern_id: str
    category: str
    claim: str
    supporting_examples: tuple[str, ...]
    unsupported_generalizations: tuple[str, ...]
    expected_behavior: str
    current_gap: str
    impact: str
    evidence_period: str
    measurement: PerformanceMeasurement


@dataclass(frozen=True, order=True)
class PlanHistoryEvent:
    day: int
    kind: str
    detail: str


@dataclass(frozen=True)
class PerformanceCheckpoint:
    day: int
    concerns_reviewed: tuple[str, ...]
    evidence_since_last: tuple[str, ...]
    improvement_observed: tuple[str, ...]
    unresolved_gaps: tuple[str, ...]
    manager_feedback: str
    employee_response: str
    next_actions: tuple[str, ...]


@dataclass(frozen=True)
class ImprovementPlan:
    """Small shared behavior plan; deliberately not an HR or legal workflow."""

    plan_id: str
    title: str
    participant: str
    manager: str
    concerns: tuple[PerformanceConcern, ...]
    actions: tuple[BehavioralActionPlan, ...]
    checkpoints: tuple[PerformanceCheckpoint, ...]
    duration_days: int
    status: PerformancePlanStatus
    success_condition: str
    positive_evidence: tuple[str, ...] = ()
    unsupported_claims: tuple[str, ...] = ()
    history: tuple[PlanHistoryEvent, ...] = ()


@dataclass(frozen=True)
class CommitmentRevision:
    original_commitment: str
    reason_category: str
    new_commitment: str
    affected_dependencies: tuple[str, ...]
    owner_agreement: str | None
    next_checkpoint: str


@dataclass(frozen=True)
class WorkImpactContext:
    """Observable professional effects; deliberately excludes the private cause."""

    actor: str
    affected_commitment: str
    observed_work_impact: tuple[str, ...]
    impact_start: str
    current_capacity: WorkCapacity
    private_details: tuple[str, ...]
    work_relevant_information: tuple[str, ...]
    manager_visibility_needed: bool
    requested_support: tuple[str, ...]
    revised_commitment: CommitmentRevision | None
    dependencies: tuple[str, ...]
    follow_up_point: str | None
    formal_support_note: str | None = None


@dataclass(frozen=True)
class RecoveryCheck:
    description: str
    verified: bool = False


@dataclass(frozen=True)
class IncidentReview:
    timeline: tuple[str, ...]
    impact: tuple[str, ...]
    contributing_conditions: tuple[str, ...]
    responsibility: tuple[str, ...]
    detection: tuple[str, ...]
    containment: tuple[str, ...]
    correction: tuple[str, ...]
    prevention: tuple[str, ...]


@dataclass(frozen=True)
class Incident:
    """Small authored incident view; not monitoring or causal inference machinery."""

    incident_id: str
    title: str
    detected_at: str
    state: IncidentState
    coordinator: str
    technical_owner: str
    business_owner: str | None
    affected_workflow: str
    symptoms: tuple[str, ...]
    impact: tuple[str, ...]
    established_facts: tuple[str, ...]
    hypotheses: tuple[str, ...]
    unknowns: tuple[str, ...]
    containment_actions: tuple[str, ...]
    corrective_actions: tuple[str, ...]
    recovery_checks: tuple[RecoveryCheck, ...]
    stakeholders: tuple[str, ...]
    next_update_point: str | None
    review: IncidentReview | None = None

    @property
    def recovery_verified(self) -> bool:
        return bool(self.recovery_checks) and all(check.verified for check in self.recovery_checks)

    def transition(self, state: IncidentState) -> "Incident":
        allowed = {
            IncidentState.DETECTED: {IncidentState.ACTIVE},
            IncidentState.ACTIVE: {IncidentState.CONTAINED},
            IncidentState.CONTAINED: {IncidentState.RECOVERING},
            IncidentState.RECOVERING: {IncidentState.RESOLVED},
            IncidentState.RESOLVED: {IncidentState.REVIEWED},
            IncidentState.REVIEWED: set(),
        }
        if state not in allowed[self.state]:
            raise ValueError(f"invalid incident transition: {self.state.value} -> {state.value}")
        if state is IncidentState.RESOLVED and not self.recovery_verified:
            raise ValueError("incident cannot be resolved before recovery is verified")
        if state is IncidentState.REVIEWED and self.review is None:
            raise ValueError("incident cannot be reviewed without an incident review")
        from dataclasses import replace
        return replace(self, state=state)


@dataclass(frozen=True)
class Handoff:
    handoff_id: str
    title: str
    sender: str
    receiver: str
    artifact: str
    dependency_served: str
    agreed_contract: tuple[str, ...]
    state: HandoffState
    required_context: tuple[str, ...]
    acceptance_condition: str
    open_questions: tuple[str, ...] = ()

    def transition(self, state: HandoffState) -> "Handoff":
        allowed = {
            HandoffState.PREPARING: {HandoffState.READY},
            HandoffState.READY: {HandoffState.DELIVERED},
            HandoffState.DELIVERED: {HandoffState.ACKNOWLEDGED, HandoffState.REWORK_REQUIRED},
            HandoffState.ACKNOWLEDGED: {HandoffState.ACCEPTED, HandoffState.REWORK_REQUIRED},
            HandoffState.REWORK_REQUIRED: {HandoffState.READY},
            HandoffState.ACCEPTED: set(),
        }
        if state not in allowed[self.state]:
            raise ValueError(f"invalid handoff transition: {self.state.value} -> {state.value}")
        from dataclasses import replace
        return replace(self, state=state)


@dataclass(frozen=True)
class PeerOwnership:
    owners: tuple[tuple[str, tuple[str, ...]], ...]
    shared: tuple[str, ...]
    not_implied: tuple[str, ...]


@dataclass(frozen=True)
class HelpContext:
    helper_commitment_risk: RiskLevel
    request_urgency: RiskLevel
    requester_blocked: bool
    alternative_sources: tuple[str, ...]
    expected_duration: str


@dataclass(frozen=True)
class PeerCollaboration:
    shared_objective: str
    ownership: PeerOwnership
    dependencies: tuple[str, ...]
    handoff: Handoff | None = None
    help_context: HelpContext | None = None


@dataclass(frozen=True)
class StakeholderRequest:
    """Scenario-authored request decomposition, not a parsed specification."""

    requester: str
    stated_request: str
    business_outcome: str
    deadline: str | None
    constraints: tuple[str, ...]
    preferred_solution: str | None
    requirements: tuple[str, ...]
    acceptance_conditions: tuple[str, ...]
    open_questions: tuple[str, ...]
    decision_owners: tuple[tuple[str, tuple[str, ...]], ...]
    technical_evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class TradeoffOption:
    """A transparent option description; deliberately has no numeric score."""

    option_id: str
    description: str
    business_value: str
    delivery_impact: str
    technical_risk: str
    scope: tuple[str, ...]
    constraints_satisfied: tuple[str, ...]
    constraints_not_satisfied: tuple[str, ...]
    reversibility: str


@dataclass(frozen=True)
class ScopeChange:
    original_scope: tuple[str, ...]
    requested_addition: str
    delivery_impact: str
    available_tradeoffs: tuple[str, ...]
    decision: str | None = None


@dataclass(frozen=True)
class ManagerExpectation:
    subject: str
    threshold: VisibilityThreshold
    expected_behavior: str
    decision_owner: str
    evidence_of_agreement: str
    point: int | None = None


@dataclass(frozen=True)
class WorkingAgreement:
    """Explicit operating boundaries, not a universal policy or HR record."""

    manager: str
    employee: str
    responsibilities: tuple[str, ...]
    expectations: tuple[ManagerExpectation, ...]
    normal_update_cadence: str
    known_dependencies: tuple[str, ...] = ()
    version: int = 1
    supersedes: int | None = None


@dataclass(frozen=True)
class ConflictSignal:
    """Scenario-authored behavior; ``statement`` is illustrative, never parsed."""

    speaker: str
    statement: str
    interruption: bool = False
    generalization: bool = False
    personal_attribution: bool = False
    repeated_unsupported_claim: bool = False
    topic_expansion: bool = False
    threat_or_coercion: bool = False


@dataclass(frozen=True)
class ConflictState:
    """A deterministic view of a tense exchange and its decision boundary."""

    stage: ConflictStage
    current_issue: str
    shared_facts: tuple[str, ...]
    positions: tuple[tuple[str, str], ...]
    signals: tuple[ConflictSignal, ...] = ()
    expanded_issue: str | None = None
    not_established: tuple[str, ...] = ()
    unresolved_decision: bool = True


@dataclass(frozen=True)
class DecisionAlternative:
    name: str
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class DecisionContext:
    """A compact, inspectable decision boundary—not a decision-management system."""

    decision: str
    owner: str
    contributors: tuple[str, ...]
    shared_objective: str
    alternatives: tuple[DecisionAlternative, ...]
    constraints: tuple[str, ...] = ()
    unresolved_risks: tuple[str, ...] = ()
    issue_kind: DecisionIssueKind = DecisionIssueKind.MAINTAINABILITY
    final_choice: str | None = None
    rationale: str | None = None
    reversible: bool = True


@dataclass(frozen=True)
class ProfessionalFeedback:
    """Scenario-authored decomposition; it does not parse arbitrary prose."""

    source: str
    subject: str
    claim: str
    examples: tuple[str, ...]
    observed_behavior: tuple[str, ...]
    interpretation: tuple[str, ...]
    expected_behavior: tuple[str, ...]
    requested_change: tuple[str, ...]
    evidence: tuple[FeedbackEvidence, ...]
    important_context: tuple[str, ...] = ()
    not_implied: tuple[str, ...] = ()


@dataclass(frozen=True)
class Hypothesis:
    """A possible explanation, explicitly distinct from an established fact."""

    hypothesis_id: str
    statement: str
    evidence_basis: tuple[str, ...] = ()


@dataclass(frozen=True)
class Uncertainty:
    """Scenario-authored knowledge state, not inferred from message wording."""

    subject: str
    kind: UncertaintyKind
    current_evidence: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
    current_hypotheses: tuple[str, ...] = ()
    decision_impact: str | None = None
    next_investigation_steps: tuple[str, ...] = ()
    expected_update_point: int | None = None


@dataclass(frozen=True)
class EvidenceContext:
    established_facts: tuple[str, ...]
    hypotheses: tuple[Hypothesis, ...] = ()
    not_yet_established: tuple[str, ...] = ()
    uncertainty: Uncertainty | None = None


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
    BLOCKING = "blocking"
    RESOLVED = "resolved"


class RequirementIssueKind(Enum):
    """Authored requirement defects; these labels are not inferred from prose."""

    VAGUE = "vague"
    AMBIGUOUS = "ambiguous"
    INCOMPLETE = "incomplete"
    CONTRADICTORY = "contradictory"
    UNKNOWN = "unknown"


class ResolutionSource(Enum):
    EXISTING_CONTRACT = "existing contract"
    STAKEHOLDER_DECISION = "stakeholder decision"
    PRODUCT_DECISION = "product decision"
    ENGINEERING_CONSTRAINT = "engineering constraint"
    POLICY = "policy"
    ESTABLISHED_CONVENTION = "established convention"
    EXPERIMENT = "experiment"


class AssumptionStatus(Enum):
    OPEN = "open"
    VALIDATED = "validated"
    REPLACED = "replaced"


@dataclass(frozen=True)
class RequirementAmbiguity:
    subject: str
    description: str
    kind: RequirementIssueKind
    decision_impact: DecisionRelevance
    evidence: tuple[str, ...]
    possible_interpretations: tuple[str, ...]
    safe_to_defer: bool
    resolution_source: ResolutionSource | None = None
    resolution: str | None = None

    @property
    def is_resolved(self) -> bool:
        return self.resolution is not None


@dataclass(frozen=True)
class RequirementContradiction:
    subject: str
    sources: tuple[tuple[str, str], ...]
    interpretation: str
    resolution: str | None = None
    resolution_source: ResolutionSource | None = None


@dataclass(frozen=True)
class AssumptionRecord:
    assumption: str
    reason: str
    impact: str
    owner: str
    reversible: bool
    validation_point: str
    status: AssumptionStatus = AssumptionStatus.OPEN
    safe_default: bool = False


@dataclass(frozen=True)
class AcceptanceCondition:
    """An observable contract outcome, deliberately not an implementation recipe."""

    condition_id: str
    statement: str
    verification: str


@dataclass(frozen=True, order=True)
class RequirementHistoryEvent:
    point: int
    description: str
    source: ResolutionSource | None = None


@dataclass(frozen=True)
class RequirementContext:
    """Small scenario-authored ambiguity view extending the shared behavior model."""

    requirement_id: str
    stated_request: str
    business_outcome: str
    explicit_requirements: tuple[str, ...]
    constraints: tuple[str, ...]
    ambiguities: tuple[RequirementAmbiguity, ...]
    contradictions: tuple[RequirementContradiction, ...] = ()
    defaults: tuple[str, ...] = ()
    assumptions: tuple[AssumptionRecord, ...] = ()
    decisions: tuple[str, ...] = ()
    acceptance_conditions: tuple[AcceptanceCondition, ...] = ()
    evidence_sources: tuple[str, ...] = ()
    history: tuple[RequirementHistoryEvent, ...] = ()
    safe_work_while_open: tuple[str, ...] = ()


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
    evidence_context: EvidenceContext | None = None
    feedback: ProfessionalFeedback | None = None
    action_plan: BehavioralActionPlan | None = None
    responsibility_map: ResponsibilityMap | None = None
    decision_context: DecisionContext | None = None
    conflict_state: ConflictState | None = None
    working_agreement: WorkingAgreement | None = None
    peer_collaboration: PeerCollaboration | None = None
    stakeholder_request: StakeholderRequest | None = None
    tradeoff_options: tuple[TradeoffOption, ...] = ()
    scope_change: ScopeChange | None = None
    requirement_context: RequirementContext | None = None
    incident: Incident | None = None
    incident_audiences: tuple[tuple[str, tuple[str, ...]], ...] = ()
    work_impact: WorkImpactContext | None = None
    performance_plan: ImprovementPlan | None = None


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
    states_uncertainty_explicitly: bool = False
    exceeds_available_evidence: bool = False
    offered_hypothesis: str | None = None
    hypothesis_labeled: bool = False
    evidence_basis: tuple[str, ...] = ()
    missing_evidence_identified: tuple[str, ...] = ()
    uncertainty_next_action: str | None = None
    decision_impact: str | None = None
    estimate_for: str | None = None
    acknowledges_feedback: bool = False
    seeks_specific_understanding: bool = False
    acknowledges_supported_evidence: bool = False
    premature_rebuttal: bool = False
    automatic_agreement: bool = False
    context_provided: bool = False
    context_used_as_excuse: bool = False
    identifies_behavior_change: bool = False
    preserves_respectful_disagreement: bool = False
    demonstrated_improvement: bool = False
    identifies_own_contribution: bool = False
    over_owns: bool = False
    preserves_agency: bool = True
    prioritizes_containment: bool = False
    identifies_corrective_action: bool = False
    identifies_preventive_action: bool = False
    acknowledges_impact: bool = False
    self_condemnation: bool = False
    identifies_shared_objective: bool = False
    states_specific_disagreement: bool = False
    decision_relevant_evidence: tuple[str, ...] = ()
    personalizes_disagreement: bool = False
    distinguishes_preference_from_defect: bool = False
    constructive_alternative: str | None = None
    respects_decision_ownership: bool = False
    updates_position_with_evidence: bool = False
    escalates_material_risk: bool = False
    repeats_resolved_argument: bool = False
    generalizes_about_person: bool = False
    attributes_motive_without_evidence: bool = False
    attacks_group: bool = False
    uses_sarcasm: bool = False
    focuses_on_current_decision: bool = False
    acknowledges_legitimate_concern: bool = False
    concedes_decision: bool = False
    restores_shared_facts: bool = False
    creates_decision_path: bool = False
    preserves_material_risk: bool = False
    ends_argument: bool = False
    resolves_issue: bool = False
    makes_incident_visible: bool = False
    states_observed_impact: bool = False
    separates_cause_from_hypothesis: bool = False
    establishes_incident_ownership: bool = False
    coordinates_affected_parties: bool = False
    verifies_recovery: bool = False
    closes_incident_loop: bool = False
    defers_blame_until_evidence: bool = False
    creates_prevention_from_evidence: bool = False
    pauses_conversation: bool = False
    pause_has_checkpoint: bool = False
    pause_names_needed_evidence: bool = False
    repairs_own_contribution: bool = False
    owns_delegated_decisions: bool = False
    threshold_risk_visible: bool = False
    consultation_boundary_respected: bool = False
    true_blocker_escalated: bool = False
    unnecessary_upward_delegation: bool = False
    recommendation_provided: bool = False
    manager_signal_preserved: bool = False
    working_agreement_clarified: bool = False
    handoff_explicit: bool = False
    handoff_context_provided: bool = False
    handoff_acknowledgement_sought: bool = False
    respects_peer_ownership: bool = True
    helps_without_taking_over: bool = False
    accounts_for_help_opportunity_cost: bool = False
    shared_ownership_clarified: bool = False
    peer_dependency_addressed_directly: bool = False
    contribution_recognized: bool = False
    identifies_business_outcome: bool = False
    separates_outcome_from_solution: bool = False
    respects_explicit_requirement: bool = True
    communicates_tradeoff: bool = False
    makes_scope_change_explicit: bool = False
    provides_professional_recommendation: bool = False
    aligns_commitment_with_decision: bool = False
    preserves_business_context: bool = False
    technical_risk_made_visible: bool = False
    identifies_material_ambiguity: bool = False
    distinguishes_low_value_detail: bool = False
    surfaces_contradiction: bool = False
    uses_existing_evidence: bool = False
    records_visible_assumption: bool = False
    uses_safe_default: bool = False
    requires_material_decision: bool = False
    creates_testable_acceptance_condition: bool = False
    updates_requirement_history: bool = False
    progresses_safely: bool = False
    identifies_work_impact: bool = False
    preserves_reasonable_privacy: bool = True
    answers_legitimate_capacity_question: bool = False
    requests_specific_support: bool = False
    revises_commitment_explicitly: bool = False
    updates_dependencies: bool = False
    recognizes_task_safety: bool = False
    addresses_recurring_pattern: bool = False
    uses_formal_path_when_needed: bool = False
    identifies_supported_performance_evidence: bool = False
    corrects_material_inaccuracy: bool = False
    clarifies_performance_expectation: bool = False
    establishes_measurement: bool = False
    establishes_checkpoints: bool = False
    avoids_vague_improvement_promise: bool = False
    focuses_on_controllable_behavior: bool = False
    tracks_evidence_over_time: bool = False
    preserves_plan_scope: bool = False
    demonstrates_plan_improvement: bool = False


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
