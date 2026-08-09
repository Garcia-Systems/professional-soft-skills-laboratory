"""Professional trust represented as a history of observable evidence."""

from dataclasses import dataclass
from enum import Enum


class TrustEventKind(Enum):
    ACTED_WITHIN_AUTHORITY = (1, "Acted within authority")
    MATERIAL_RISK_ESCALATED_WITH_JUDGMENT = (2, "Escalated material risk with judgment")
    REVERSIBLE_EXPERIMENT_USED = (1, "Reversible experiment used")
    BOUNDARY_VIOLATION_REFUSED = (2, "Boundary violation refused")
    TRADEOFF_SURFACED = (1, "Tradeoff surfaced")
    DECISION_ADJUSTED_AFTER_NEW_EVIDENCE = (2, "Decision adjusted after new evidence")
    JUDGMENT_RATIONALE_DOCUMENTED = (1, "Judgment rationale documented")
    UNNECESSARY_ESCALATION = (-1, "Unnecessary escalation")
    MATERIAL_RISK_IGNORED = (-3, "Material risk ignored")
    IRREVERSIBLE_ACTION_UNDER_AMBIGUITY = (-3, "Irreversible action under unresolved ambiguity")
    UNAUTHORIZED_COMMITMENT = (-2, "Unauthorized commitment")
    UNSAFE_SHORTCUT = (-3, "Unsafe shortcut")
    VALIDATION_FALSIFIED = (-3, "Validation falsified")
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
    CONFLICT_REFOCUSED = (2, "Conflict refocused")
    OWN_ESCALATION_REPAIRED = (2, "Own escalation repaired")
    MATERIAL_CONCERN_PRESERVED = (2, "Material concern preserved")
    MOTIVE_ATTACK = (-2, "Motive attack")
    GROUP_GENERALIZATION = (-2, "Group generalization")
    PERSONAL_ATTACK = (-2, "Personal attack")
    CONFLICT_REPEATED_AFTER_RESOLUTION = (-3, "Conflict repeated after resolution")
    ROUTINE_DECISION_OWNED = (1, "Routine decision owned")
    CONSULTATION_THRESHOLD_RESPECTED = (2, "Consultation threshold respected")
    BLOCKER_ESCALATED = (2, "Blocker escalated")
    RECOMMENDATION_PROVIDED = (1, "Recommendation provided")
    RISK_DISCOVERED_BY_MANAGER = (-3, "Manager forced to discover risk")
    ROUTINE_DECISION_DELEGATED_UPWARD = (-1, "Routine decision unnecessarily delegated upward")
    CONSULTATION_BOUNDARY_BYPASSED = (-2, "Consultation boundary bypassed")
    BLOCKER_HIDDEN = (-3, "Blocker hidden")
    UNSTRUCTURED_STATUS_NOISE = (-1, "Repeated unstructured status noise")
    HANDOFF_ACCEPTED = (2, "Handoff accepted")
    PEER_OWNERSHIP_RESPECTED = (1, "Peer ownership respected")
    DEPENDENCY_LEFT_SILENT = (-2, "Dependency left silent")
    BUSINESS_GOAL_CLARIFIED = (1, "Business goal clarified")
    TECHNICAL_RISK_MADE_VISIBLE = (2, "Technical risk made visible")
    TRADEOFF_EXPLAINED = (2, "Tradeoff explained")
    SCOPE_CHANGE_MADE_EXPLICIT = (2, "Scope change made explicit")
    COMMITMENT_ALIGNED_TO_DECISION = (2, "Commitment aligned to decision")
    REQUEST_LITERALIZED_WITHOUT_ANALYSIS = (-2, "Request literalized without analysis")
    SCOPE_CHANGED_SILENTLY = (-3, "Scope changed silently")
    TECHNICAL_CONSTRAINT_HIDDEN = (-2, "Technical constraint hidden")
    STAKEHOLDER_CONTEXT_DISMISSED = (-2, "Stakeholder context dismissed")
    UNSUPPORTED_COMMITMENT_MADE = (-3, "Unsupported commitment made")
    ASSUMPTION_MADE_VISIBLE = (1, "Assumption made visible")
    REQUIREMENT_DECISION_RECORDED = (2, "Requirement decision recorded")
    MATERIAL_SEMANTICS_ASSUMED = (-2, "Material semantics silently assumed")
    INCIDENT_REPORTED_EARLY = (2, "Incident reported early")
    UNCERTAINTY_PRESERVED = (1, "Uncertainty preserved")
    CONTAINMENT_COORDINATED = (2, "Containment coordinated")
    AFFECTED_PARTY_UPDATED = (2, "Affected party updated")
    RECOVERY_VERIFIED = (2, "Recovery verified")
    INCIDENT_HIDDEN = (-3, "Incident hidden")
    BLAME_ASSERTED_WITHOUT_EVIDENCE = (-2, "Blame asserted without evidence")
    IMPACT_MINIMIZED = (-2, "Impact minimized")
    FALSE_RECOVERY_DECLARED = (-3, "False recovery declared")
    STAKEHOLDER_LEFT_UNINFORMED = (-2, "Stakeholder left uninformed")
    PERSONAL_IMPACT_COMMUNICATED = (2, "Personal impact communicated before failure")
    PRIVACY_BOUNDARY_MAINTAINED = (1, "Privacy boundary maintained")
    REALISTIC_COMMITMENT_REVISION = (2, "Realistic commitment revision")
    SPECIFIC_SUPPORT_REQUESTED = (1, "Specific support requested")
    DEPENDENT_PARTY_UPDATED = (2, "Dependent party updated")
    UNSAFE_TASK_REASSIGNED = (2, "Unsafe task reassigned")
    RECURRING_PATTERN_ADDRESSED = (2, "Recurring pattern addressed")
    REVISED_FOLLOW_UP_COMPLETED = (2, "Revised follow-up completed")
    KNOWN_CAPACITY_RISK_HIDDEN = (-3, "Known capacity risk hidden")
    UNSUPPORTED_REASSURANCE_GIVEN = (-2, "Unsupported reassurance given")
    CRITICAL_DEPENDENCY_ABANDONED = (-3, "Critical dependency abandoned without update")
    REPEATED_IMPACT_WITHOUT_PLAN = (-3, "Repeated impact without plan")
    PERFORMANCE_EXPECTATION_CLARIFIED = (1, "Performance expectation clarified")
    RISK_VISIBILITY_IMPROVED = (2, "Risk visibility improved")
    HANDOFF_BEHAVIOR_IMPROVED = (2, "Handoff behavior improved")
    CHECKPOINT_COMPLETED = (1, "Checkpoint completed")
    FEEDBACK_APPLIED = (2, "Feedback applied")
    FACTUAL_DISAGREEMENT_HANDLED_PROFESSIONALLY = (1, "Factual disagreement handled professionally")
    PLAN_BEHAVIOR_SUSTAINED = (2, "Plan behavior sustained")
    SUPPORTED_FEEDBACK_DENIED = (-2, "Supported feedback denied")
    VAGUE_PROMISE_REPEATED = (-1, "Vague promise repeated")
    CHECKPOINT_MISSED_WITHOUT_UPDATE = (-2, "Checkpoint missed without update")
    KNOWN_BEHAVIOR_GAP_REPEATED = (-2, "Known behavior gap repeated")
    PLAN_EXPECTATION_IGNORED = (-2, "Plan expectation ignored")
    MEETING_PREPARED = (1, "Meeting prepared")
    MATERIAL_RISK_SURFACED_IN_DECISION = (2, "Material risk surfaced in decision")
    USEFUL_QUESTION_ASKED = (1, "Useful question asked")
    DECISION_CAPTURED = (2, "Decision captured")
    ACTION_OWNER_CONFIRMED = (1, "Action owner confirmed")
    MEETING_FOLLOW_UP_COMPLETED = (2, "Meeting follow-up completed")
    OWNED_INFORMATION_UNPREPARED = (-2, "Owned information unprepared")
    MATERIAL_FACT_WITHHELD = (-3, "Material fact withheld")
    DECISION_MISREPRESENTED = (-2, "Decision misrepresented")
    ACTION_LEFT_OWNERLESS = (-2, "Action left ownerless")
    REPEATED_MEETING_FOLLOW_UP_MISSED = (-3, "Repeated meeting follow-up missed")
    MATERIAL_WRITTEN_STATE_CLEAR = (2, "Material written state clear")
    DECISION_RECORDED = (2, "Decision recorded")
    HANDOFF_DOCUMENTED = (2, "Handoff documented")
    WRITTEN_ERROR_CORRECTED = (2, "Written error corrected")
    REVIEW_COMMENT_EVIDENCE_BASED = (1, "Review comment evidence based")
    REQUESTED_ACTION_CLOSED = (2, "Requested action closed")
    AMBIGUOUS_WRITTEN_COMMITMENT = (-2, "Ambiguous written commitment")
    MATERIALLY_WRONG_STATE_LEFT_UNCORRECTED = (-3, "Materially wrong state left uncorrected")
    DEPENDENCY_CHANGE_NOT_DOCUMENTED = (-2, "Dependency change not documented")
    UNSUPPORTED_WRITTEN_CLAIM = (-2, "Unsupported written claim")
    ACTION_OWNER_MISSING = (-2, "Action owner missing")

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

CONFLICT_EVENTS = (
    TrustEvent(TrustEventKind.CONFLICT_REFOCUSED, "Alex restored the release decision after personalization."),
    TrustEvent(TrustEventKind.OWN_ESCALATION_REPAIRED, "Alex corrected a sharp code-review reply."),
    TrustEvent(TrustEventKind.MATERIAL_CONCERN_PRESERVED, "Alex lowered friction without hiding customer-data risk."),
    TrustEvent(TrustEventKind.DECISION_SUPPORTED_AFTER_RESOLUTION, "Alex supported the legitimate resolved tradeoff."),
)

MANAGER_AUTONOMY_EVENTS = (
    TrustEvent(TrustEventKind.ROUTINE_DECISION_OWNED, "Alex handled the internal adapter refactor independently."),
    TrustEvent(TrustEventKind.RISK_COMMUNICATED_EARLY, "Alex surfaced material T8 risk at the agreed threshold."),
    TrustEvent(TrustEventKind.CONSULTATION_THRESHOLD_RESPECTED, "Alex consulted before changing Jordan's contract."),
    TrustEvent(TrustEventKind.BLOCKER_ESCALATED, "Alex promptly surfaced the vendor validation blocker."),
    TrustEvent(TrustEventKind.RECOMMENDATION_PROVIDED, "Alex recommended preserving the public contract."),
    TrustEvent(TrustEventKind.FOLLOW_UP_COMPLETED, "Alex completed the promised manager update."),
)

COLLABORATION_EVENTS = (
    TrustEvent(TrustEventKind.DEPENDENCY_ACKNOWLEDGED, "Alex made Jordan's contract dependency explicit."),
    TrustEvent(TrustEventKind.HANDOFF_ACCEPTED, "Jordan confirmed the supplied contract and fixtures were usable."),
    TrustEvent(TrustEventKind.PEER_OWNERSHIP_RESPECTED, "Focused help returned frontend ownership to Jordan."),
    TrustEvent(TrustEventKind.FOLLOW_UP_COMPLETED, "Alex answered the bounded integration follow-up."),
)

STAKEHOLDER_EVENTS = (
    TrustEvent(TrustEventKind.BUSINESS_GOAL_CLARIFIED, "Alex connected the export to customer-review preparation."),
    TrustEvent(TrustEventKind.TECHNICAL_RISK_MADE_VISIBLE, "Alex explained dependency and volume-validation risk."),
    TrustEvent(TrustEventKind.TRADEOFF_EXPLAINED, "Alex made format, date, and validation tradeoffs visible."),
    TrustEvent(TrustEventKind.RECOMMENDATION_PROVIDED, "Alex recommended CSV for the immediate workflow, conditionally."),
    TrustEvent(TrustEventKind.SCOPE_CHANGE_MADE_EXPLICIT, "Scheduling was treated as a decision, not silently absorbed."),
    TrustEvent(TrustEventKind.COMMITMENT_ALIGNED_TO_DECISION, "Alex waited for selected scope before committing."),
    TrustEvent(TrustEventKind.POSITION_UPDATED_AFTER_NEW_EVIDENCE, "Alex changed course when .xlsx became required."),
)

REQUIREMENT_EVENTS = (
    TrustEvent(TrustEventKind.ASSUMPTION_MADE_VISIBLE, "Alex recorded the reversible filename convention and validation point."),
    TrustEvent(TrustEventKind.CONCERN_RAISED_WITH_EVIDENCE, "Alex surfaced format and pending semantics with their evidence."),
    TrustEvent(TrustEventKind.REQUIREMENT_DECISION_RECORDED, "Product decisions and acceptance conditions were added to history."),
    TrustEvent(TrustEventKind.DECISION_SUPPORTED_AFTER_RESOLUTION, "Alex aligned implementation and tests to the explicit contract."),
)

INCIDENT_EVENTS = (
    TrustEvent(TrustEventKind.INCIDENT_REPORTED_EARLY, "Alex surfaced the 18% payment failure rate at T1."),
    TrustEvent(TrustEventKind.UNCERTAINTY_PRESERVED, "Deployment timing and header rejection remained fact and hypothesis."),
    TrustEvent(TrustEventKind.CONTAINMENT_COORDINATED, "Morgan coordinated reversible header disablement."),
    TrustEvent(TrustEventKind.AFFECTED_PARTY_UPDATED, "Dana and support received customer-safe guidance."),
    TrustEvent(TrustEventKind.RECOVERY_VERIFIED, "Rates, transactions, and workflow recovery were checked."),
    TrustEvent(TrustEventKind.RESPONSIBILITY_ACKNOWLEDGED, "After containment Alex acknowledged the skipped test."),
    TrustEvent(TrustEventKind.PREVENTIVE_ACTION_COMPLETED, "Header compatibility became a deployment gate."),
)

PERSONAL_CAPACITY_EVENTS = (
    TrustEvent(TrustEventKind.PERSONAL_IMPACT_COMMUNICATED, "Alex made reduced capacity and delivery risk visible at T5."),
    TrustEvent(TrustEventKind.PRIVACY_BOUNDARY_MAINTAINED, "Alex communicated work effects without recording the private cause."),
    TrustEvent(TrustEventKind.REALISTIC_COMMITMENT_REVISION, "Alex preserved T8 in history and requested review at T9."),
    TrustEvent(TrustEventKind.SPECIFIC_SUPPORT_REQUESTED, "Alex requested a review adjustment that Morgan could decide."),
    TrustEvent(TrustEventKind.DEPENDENT_PARTY_UPDATED, "Jordan received the revised handoff and stable contract."),
    TrustEvent(TrustEventKind.UNSAFE_TASK_REASSIGNED, "A high-risk deployment was reassigned based on declared capacity."),
    TrustEvent(TrustEventKind.RECURRING_PATTERN_ADDRESSED, "Repeated morning impact led to a durable-plan discussion."),
    TrustEvent(TrustEventKind.REVISED_FOLLOW_UP_COMPLETED, "Alex reassessed the revised commitment when later evidence changed."),
)

PERFORMANCE_PLAN_EVENTS = (
    TrustEvent(TrustEventKind.PERFORMANCE_EXPECTATION_CLARIFIED, "Alex and Morgan defined observable risk, handoff, and status behavior."),
    TrustEvent(TrustEventKind.CHECKPOINT_COMPLETED, "Day 7 preserved positive evidence and the unexercised risk gap."),
    TrustEvent(TrustEventKind.RISK_VISIBILITY_IMPROVED, "Alex surfaced the Day 14 material risk before indirect discovery."),
    TrustEvent(TrustEventKind.HANDOFF_BEHAVIOR_IMPROVED, "Material handoffs reached acknowledgement during the plan."),
    TrustEvent(TrustEventKind.FEEDBACK_APPLIED, "Alex corrected an incomplete status update at the next checkpoint."),
    TrustEvent(TrustEventKind.FACTUAL_DISAGREEMENT_HANDLED_PROFESSIONALLY, "Alex corrected the T8 fact while engaging with valid visibility feedback."),
    TrustEvent(TrustEventKind.PLAN_BEHAVIOR_SUSTAINED, "Defined behavior appeared across multiple relevant work events."),
)

MEETING_EVENTS = (
    TrustEvent(TrustEventKind.MEETING_PREPARED, "Alex inspected the owned boundary failure before the decision."),
    TrustEvent(TrustEventKind.MATERIAL_RISK_SURFACED_IN_DECISION, "Alex surfaced the user-visible boundary consequence."),
    TrustEvent(TrustEventKind.USEFUL_QUESTION_ASKED, "Alex tested whether 30 days met Dana's use case."),
    TrustEvent(TrustEventKind.DECISION_CAPTURED, "The confirmed limited release was recorded separately from proposals."),
    TrustEvent(TrustEventKind.ACTION_OWNER_CONFIRMED, "Alex owned the T4 correction and validation."),
)

# Chapter 21 keeps the original event stream above intact while adding domain-specific,
# observer-scoped evidence.  No balance or aggregate score is used by this model.
class TrustDimension(Enum):
    COMMITMENT_RELIABILITY = "commitment-reliability"
    RISK_VISIBILITY = "risk-visibility"
    HANDOFF_RELIABILITY = "handoff-reliability"
    TECHNICAL_JUDGMENT = "technical-judgment"
    OWNERSHIP = "ownership"
    FEEDBACK_RESPONSIVENESS = "feedback-responsiveness"
    INCIDENT_COMMUNICATION = "incident-communication"
    DECISION_CREDIBILITY = "decision-credibility"
    CROSS_TEAM_COORDINATION = "cross-team-coordination"


class TrustState(Enum):
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    DEVELOPING = "DEVELOPING"
    ESTABLISHED = "ESTABLISHED"
    MIXED = "MIXED"
    DEGRADED = "DEGRADED"
    REBUILDING = "REBUILDING"


class EvidencePolarity(Enum):
    POSITIVE = "+"
    NEGATIVE = "-"
    NEUTRAL = " "


class EvidenceProvenance(Enum):
    DIRECT_OBSERVATION = "DIRECT_OBSERVATION"
    SHARED_ARTIFACT = "SHARED_ARTIFACT"
    DOCUMENTED_EVENT = "DOCUMENTED_EVENT"


@dataclass(frozen=True)
class TrustEvidence:
    event_id: str
    time: str
    dimension: TrustDimension
    polarity: EvidencePolarity
    observable_behavior: str
    provenance: EvidenceProvenance
    linked_scenario: str
    observers: tuple[str, ...]


@dataclass(frozen=True)
class DimensionInterpretation:
    state: TrustState
    why: str


@dataclass(frozen=True)
class TrustHistory:
    scenario_id: str
    subject: str
    evidence: tuple[TrustEvidence, ...]
    interpretations: dict[TrustDimension, DimensionInterpretation]

    def for_dimension(self, dimension: TrustDimension, observer: str | None = None) -> tuple[TrustEvidence, ...]:
        events = (event for event in self.evidence if event.dimension is dimension)
        if observer is not None:
            events = (event for event in events if observer.casefold() in {name.casefold() for name in event.observers})
        return tuple(events)

    def state(self, dimension: TrustDimension, observer: str | None = None) -> TrustState:
        events = self.for_dimension(dimension, observer)
        if observer is None:
            authored = self.interpretations.get(dimension)
            return authored.state if authored else TrustState.INSUFFICIENT_EVIDENCE
        # Observer views deliberately require a repeated, consistent pattern. They do
        # not borrow evidence visible to somebody else.
        positive = sum(event.polarity is EvidencePolarity.POSITIVE for event in events)
        negative = sum(event.polarity is EvidencePolarity.NEGATIVE for event in events)
        if len(events) < 2:
            return TrustState.INSUFFICIENT_EVIDENCE
        if positive and negative:
            return TrustState.MIXED
        if positive >= 2:
            return TrustState.ESTABLISHED
        if negative >= 2:
            return TrustState.DEGRADED
        return TrustState.DEVELOPING
