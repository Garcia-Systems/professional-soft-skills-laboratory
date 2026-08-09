"""Chapter 24: deterministic composition of the Volume I domain models.

The capstone deliberately contains no new evaluator.  Its events point to the
existing scenarios whose public models/evaluators supply the meaning of each
professional behavior.  This module only orders those results and renders
project-level traces.
"""

from dataclasses import dataclass
from typing import Literal

from soft_skills_lab.domain.models import ProfessionalCommitment
from soft_skills_lab.scenarios import get_scenario
from soft_skills_lab.trust import (
    DimensionInterpretation, EvidencePolarity, EvidenceProvenance, TrustDimension,
    TrustEvidence, TrustHistory, TrustState,
)

PROJECT_ID = "member-verification-launch"
LaunchDecision = Literal["monitor-and-launch", "delay-for-regression"]


@dataclass(frozen=True)
class ProjectEvent:
    time: str
    summary: str
    state: str
    facts: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    open_decisions: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectDecision:
    time: str
    subject: str
    owner: str
    choice: str
    rationale: str


@dataclass(frozen=True)
class RequirementTrace:
    request: str
    product_decisions: tuple[str, ...]
    acceptance_conditions: tuple[str, ...]
    implementation_contract: tuple[str, ...]
    launch_verification: tuple[str, ...]


@dataclass(frozen=True)
class DecisionRecord:
    decision: str
    rationale: str
    residual_risk: str
    owners: tuple[str, ...]
    monitoring: str
    member_support_readiness: str


@dataclass(frozen=True)
class ProfessionalProjectSimulation:
    """An ordered project view over existing chapter concepts."""

    project_id: str
    objective: str
    participants: tuple[tuple[str, str], ...]
    commitments: tuple[ProfessionalCommitment, ...]
    dependencies: tuple[tuple[str, str], ...]
    requirements: RequirementTrace
    decisions: tuple[ProjectDecision, ...]
    events: tuple[ProjectEvent, ...]
    trust_history: TrustHistory
    written_decision: DecisionRecord
    launch_decision: LaunchDecision
    launch_time: str
    project_outcome: str
    composed_scenarios: tuple[object, ...]

    def at(self, time: str) -> tuple[ProjectEvent, ...]:
        order = {event.time: index for index, event in enumerate(self.events)}
        if time not in order:
            raise KeyError(f"unknown capstone time: {time}")
        return self.events[: order[time] + 1]


def _evidence() -> tuple[TrustEvidence, ...]:
    def e(event_id, time, dimension, polarity, behavior, provenance=EvidenceProvenance.DOCUMENTED_EVENT,
          observers=("Morgan", "Jordan", "Priya", "Dana")):
        return TrustEvidence(event_id, time, dimension, polarity, behavior, provenance, PROJECT_ID, observers)
    return (
        e("capacity-risk", "T5", TrustDimension.RISK_VISIBILITY, EvidencePolarity.POSITIVE,
          "Material capacity and T7 delivery risk communicated without disclosing a private cause."),
        e("commitment-revised", "T5", TrustDimension.COMMITMENT_RELIABILITY, EvidencePolarity.POSITIVE,
          "API checkpoint was revised explicitly and the dependent party was updated."),
        e("handoff-accepted", "T7", TrustDimension.HANDOFF_RELIABILITY, EvidencePolarity.POSITIVE,
          "Stable normalized contract and fixture were delivered and Jordan acknowledged usability."),
        e("adapter-evidence", "T9", TrustDimension.TECHNICAL_JUDGMENT, EvidencePolarity.POSITIVE,
          "Adapter boundary was defended with vendor-change and test evidence."),
        e("coordination-gap", "T12", TrustDimension.CROSS_TEAM_COORDINATION, EvidencePolarity.POSITIVE,
          "The missing operations-script owner was resolved while peer decision rights remained intact."),
        e("validation-skipped", "T14", TrustDimension.TECHNICAL_JUDGMENT, EvidencePolarity.NEGATIVE,
          "Required staging compatibility validation was skipped under schedule pressure."),
        e("readiness-disclosure", "T16", TrustDimension.RISK_VISIBILITY, EvidencePolarity.POSITIVE,
          "Skipped validation was surfaced before final launch approval."),
        e("incident-response", "T17", TrustDimension.INCIDENT_COMMUNICATION, EvidencePolarity.POSITIVE,
          "Compatibility failures were reported, contained, and recovery was verified without premature blame."),
        e("responsibility", "T18", TrustDimension.OWNERSHIP, EvidencePolarity.POSITIVE,
          "Alex accurately owned adding the header and skipping the check after evidence confirmed contribution."),
        e("feedback", "T18", TrustDimension.FEEDBACK_RESPONSIVENESS, EvidencePolarity.POSITIVE,
          "Supported feedback was acknowledged and converted into a specific validation behavior."),
        e("decision-record", "T18.5", TrustDimension.DECISION_CREDIBILITY, EvidencePolarity.POSITIVE,
          "Launch tradeoffs, residual risk, owners, monitoring, and support readiness were recorded."),
        e("prevention", "T24", TrustDimension.TECHNICAL_JUDGMENT, EvidencePolarity.POSITIVE,
          "Provider compatibility validation became a mandatory release gate."),
        e("follow-through", "T24", TrustDimension.COMMITMENT_RELIABILITY, EvidencePolarity.POSITIVE,
          "Preventive action and stakeholder acceptance follow-ups were completed."),
    )


def _history() -> TrustHistory:
    interpretations = {
        TrustDimension.COMMITMENT_RELIABILITY: DimensionInterpretation(TrustState.ESTABLISHED, "An at-risk commitment was revised and later follow-through completed."),
        TrustDimension.RISK_VISIBILITY: DimensionInterpretation(TrustState.ESTABLISHED, "Material T5 and T16 risks became visible before their decision points."),
        TrustDimension.HANDOFF_RELIABILITY: DimensionInterpretation(TrustState.ESTABLISHED, "Jordan acknowledged a usable contract and fixture."),
        TrustDimension.TECHNICAL_JUDGMENT: DimensionInterpretation(TrustState.MIXED, "Good boundary reasoning, a harmful validation shortcut, and later prevention coexist."),
        TrustDimension.OWNERSHIP: DimensionInterpretation(TrustState.ESTABLISHED, "Responsibility followed evidence rather than blame."),
        TrustDimension.FEEDBACK_RESPONSIVENESS: DimensionInterpretation(TrustState.DEVELOPING, "Feedback was accepted and a first concrete change followed."),
        TrustDimension.INCIDENT_COMMUNICATION: DimensionInterpretation(TrustState.ESTABLISHED, "The incident was made visible, contained, and verified."),
        TrustDimension.DECISION_CREDIBILITY: DimensionInterpretation(TrustState.ESTABLISHED, "The launch record makes rationale and residual risk inspectable."),
        TrustDimension.CROSS_TEAM_COORDINATION: DimensionInterpretation(TrustState.ESTABLISHED, "A cross-owner gap was closed while preserving peer decision rights rather than taking peers' work."),
    }
    return TrustHistory(PROJECT_ID, "Alex", _evidence(), interpretations)


def build_simulation(launch_decision: LaunchDecision = "monitor-and-launch") -> ProfessionalProjectSimulation:
    if launch_decision not in ("monitor-and-launch", "delay-for-regression"):
        raise KeyError(f"unknown launch decision: {launch_decision}")
    launch_time = "T20" if launch_decision == "monitor-and-launch" else "T22"
    requirements = RequirementTrace(
        "Member verification in account opening by T20; failed members know what to do next.",
        ("Timeout is retryable with Harbor-safe language.", "Vendor vocabulary remains hidden.",
         "Permanent failure blocks opening and provides a support next step."),
        ("Success permits account opening.", "Timeout presents safe retry guidance.",
         "Permanent failure blocks opening and names support.", "Operations escalation is documented."),
        ("success", "retryable-timeout", "permanent-failure"),
        ("All three normalized states pass controlled validation.", "Frontend and backend contracts align.",
         "Dana confirms the support workflow is usable."),
    )
    decisions = (
        ProjectDecision("T4", "timeout semantics", "Priya", "retryable with Harbor-safe language", "A possibly processed vendor request makes blind retry unsafe; product owns member semantics."),
        ProjectDecision("T9", "adapter boundary", "Morgan", "retain and simplify adapter", "The boundary hides changing vendor vocabulary and preserves vendor-independent services."),
        ProjectDecision("T10", "completion email", "Priya", "defer to next increment", "It is useful but not required and would reduce an already narrow validation margin."),
        ProjectDecision("T17", "incident containment", "Morgan", "disable optional header", "Reversible containment protects validation while root cause remains a hypothesis."),
        ProjectDecision("T18.5", "launch timing", "Morgan", launch_decision,
                        "Acceptance conditions pass; monitoring limits residual risk, while extra regression can reduce uncertainty at real delay cost."),
    )
    commitments = tuple(ProfessionalCommitment(key, desc, owner, recipient, due) for key, desc, owner, recipient, due in (
        ("product-semantics", "Decide timeout and permanent-failure semantics", "Priya", "Alex", 4),
        ("api-contract", "Deliver stable normalized API contract", "Alex", "Jordan", 7),
        ("frontend", "Complete frontend integration", "Jordan", "Morgan", 11),
        ("operations", "Complete support readiness", "Dana", "Morgan", 14),
        ("validation", "Complete engineering validation", "Alex", "Morgan", 17),
        ("launch-decision", "Approve launch timing", "Morgan", "Team", 19),
    ))
    # References are real Chapter 5/7/8/9/10/12/13/15/16/19/20/22/23 scenario
    # objects. The orchestrator does not copy their evaluators or trust rules.
    composed = tuple(get_scenario(s) for s in (
        "integration-delivery", "project-visibility", "skipped-validation", "adapter-boundary",
        "release-validation", "verification-integration", "export-scope-change", "payment-authorization",
        "personal-capacity", "release-readiness", "deployment-risk", "verification-launch",
        "release-window-uncertainty",
    ))
    events = (
        ProjectEvent("T0", "Requirement received", "Ambiguous request", ("Vendor returns success, timeout, or permanent failure.",), (), ("Member failure and operations semantics",)),
        ProjectEvent("T2", "Ownership and dependencies established", "Planned", ("Named owners accepted project responsibilities.",)),
        ProjectEvent("T3", "Vendor timeout ambiguity identified", "Investigating", ("Timeout payload differs from documentation.", "Request may already be processed."), ("Blind retry may be unsafe.",), ("Timeout normalization",)),
        ProjectEvent("T4", "Product semantics decided", "Acceptance conditions explicit", requirements.product_decisions),
        ProjectEvent("T5", "Delivery risk communicated and commitment revised", "API contract at risk", ("Internal checkpoint was missed.", "Work impact was communicated; private cause was not recorded."), ("T7 contract timing threatens Jordan."), (), ("capacity-risk", "commitment-revised")),
        ProjectEvent("T7", "API contract handed off and acknowledged", "Dependency usable", ("Fixture covers retryable and permanent states.",), (), (), ("handoff-accepted",)),
        ProjectEvent("T9", "Adapter disagreement resolved", "Boundary retained and simplified", ("Vendor fields changed; tests rely on the boundary.",), (), (), ("adapter-evidence",)),
        ProjectEvent("T10", "Scope addition deferred", "Original launch scope preserved", ("Completion email is useful but not required.",), ("Schedule risk is moderate.",)),
        ProjectEvent("T11", "Integration edge-case risk reported", "Launch possible; margin shrinking", ("Timeout and permanent states work.",), ("Browser retry after navigation can stick in loading.",)),
        ProjectEvent("T12", "Cross-team dependencies aligned", "Operations-script owner confirmed", ("Priya owns final member language; Dana owns operational procedure; Alex supplies fixture." ,), (), (), ("coordination-gap",)),
        ProjectEvent("T14", "Required compatibility validation skipped", "Release candidate incomplete", ("Unit and integration tests pass.", "Alex changed the optional header and skipped staging."), ("Vendor compatibility is unverified.",), (), ("validation-skipped",)),
        ProjectEvent("T16", "Skipped validation disclosed in readiness meeting", "Approval awaits compatibility check", ("Core, frontend, and operations work are ready.",), ("Required compatibility check is missing.",), (), ("readiness-disclosure",)),
        ProjectEvent("T17", "Compatibility incident contained", "Recovered in controlled validation", ("Vendor rejects the header.", "No real members affected.", "Header disabled and recovery verified."), (), (), ("incident-response",)),
        ProjectEvent("T18", "Responsibility acknowledged and feedback converted to action", "Recovery reviewed", ("Validation would have exposed the failure.", "Conflict was refocused on release recovery."), (), (), ("responsibility", "feedback")),
        ProjectEvent("T18.5", "Launch decision made and recorded", "Decision owned by Morgan", ("Corrected validation passes; acceptance conditions are satisfied.",), ("Additional regression would reduce residual uncertainty.",), (), ("decision-record",)),
        ProjectEvent(launch_time, "Launch completed", "Successful launch", requirements.launch_verification),
        ProjectEvent("T24", "Preventive action and follow-up verified", "Project closed", ("Compatibility gate is mandatory.", "Jordan, Dana, and Priya confirmed acceptance."), (), (), ("prevention", "follow-through")),
    )
    record = DecisionRecord(launch_decision,
        "Required acceptance and corrected compatibility validation pass; the selected timing makes the uncertainty/cost tradeoff explicit.",
        "External-vendor behavior can still vary; additional regression reduces but cannot eliminate that uncertainty.",
        ("Morgan: launch approval", "Alex: monitoring and rollback", "Dana: member support"),
        "Monitor verification failure rate and disable the optional header through the verified rollback path.",
        "Dana confirmed the support script for retryable and permanent failures.")
    return ProfessionalProjectSimulation(PROJECT_ID, "Launch Harbor's new member-verification workflow safely and usefully by T20.",
        (("Alex", "developer"), ("Jordan", "frontend developer"), ("Priya", "product manager"),
         ("Morgan", "engineering manager"), ("Dana", "operations stakeholder")), commitments,
        (("Jordan frontend", "Alex API contract"), ("Dana support", "Priya member semantics"),
         ("Morgan approval", "engineering validation and operations readiness")), requirements, decisions,
        events, _history(), record, launch_decision, launch_time, "launched successfully", composed)


def get_simulation(project_id: str, launch_decision: LaunchDecision = "monitor-and-launch") -> ProfessionalProjectSimulation:
    if project_id != PROJECT_ID:
        raise KeyError(f"unknown capstone project: {project_id}")
    return build_simulation(launch_decision)
