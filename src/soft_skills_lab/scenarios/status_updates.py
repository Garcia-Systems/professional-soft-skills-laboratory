"""Chapter 5 scenarios: deterministic work state and structured updates."""

from soft_skills_lab.domain.models import (
    CommunicationAudience, Commitment, ExplanationContext, Forecast, Participant,
    ProfessionalCommitment, ProfessionalResponse, RiskLevel, StatusCategory, StatusUpdate,
    TimelineEvent, WorkplaceScenario,
)

INTEGRATION_COMMITMENT = ProfessionalCommitment(
    "member-verification", "Provide a usable member-verification endpoint", "Alex", "Jordan", 6,
    dependencies=("External verification provider behavior", "Jordan starts integration at T6"),
    known_risks=("Undocumented provider failure structures",),
)

INTEGRATION_TIMELINE = (
    TimelineEvent(0, "Work begins."),
    TimelineEvent(2, "Request flow and success response are implemented."),
    TimelineEvent(3, "Undocumented provider error structures are discovered; work can continue, but T6 is at risk."),
    TimelineEvent(4, "Two of three observed error forms are normalized; one remains unexplained."),
    TimelineEvent(5, "Vendor support is unavailable and the team must choose limited delivery, fallback behavior, or waiting."),
)

AUDIENCES = (
    CommunicationAudience("jordan", "dependent frontend teammate", "Uses the endpoint contract",
        "Plan and begin frontend integration", ("integration-readiness", "stable-contract", "possible-change", "T6", "parallel-work", "next-update")),
    CommunicationAudience("morgan", "engineering manager", "Needs delivery rather than payload detail",
        "Manage commitment risk and make a delivery decision", ("state", "completed", "risk", "cause", "dependency-impact", "decision", "next-update")),
    CommunicationAudience("business", "business stakeholder", "Needs user-facing delivery implications",
        "Plan feature delivery", ("schedule", "user-scope", "decision", "confidence-point")),
)

INTEGRATION_DELIVERY = WorkplaceScenario(
    "integration-delivery", "Member-verification integration delivery",
    "Alex expects to provide a usable endpoint by T6; Jordan plans frontend integration at T6. At T3 an undocumented provider failure form makes delivery at risk, but work can continue.",
    (Participant("Alex", "backend developer"), Participant("Jordan", "frontend developer"), Participant("Morgan", "engineering manager")),
    ("The success path works.", "Failure normalization is incomplete.", "Two of three observed error forms are understood.",
     "Alex can continue investigation and implementation.", "Jordan plans integration at T6."),
    ("How the third provider error form should be normalized.", "Whether vendor support will respond before T6."),
    (Commitment("Alex", "provide a usable member-verification endpoint", "T6"),), RiskLevel.HIGH,
    explanation_context=ExplanationContext(AUDIENCES, ()),
)

def update(**kwargs: object) -> StatusUpdate:
    return StatusUpdate(subject="Member-verification endpoint", **kwargs)

DECISION_USEFUL = update(
    current_state=StatusCategory.AT_RISK,
    completed_work=("Success path implemented.", "Two known vendor failure forms normalized."),
    remaining_work=("Safe handling for the third failure form.",),
    risks=("Undocumented provider behavior may affect T6 delivery.",),
    uncertainties=("The final provider failure form remains unexplained.",),
    dependency_impact=("Jordan's frontend integration begins at T6 and may be affected.",),
    next_action="Implement a safe fallback and continue investigation.",
    forecast=Forecast("T6", "The success path and two known error forms work", "the fallback safely handles the third form"),
    next_update_point=5,
    decision_point="If unresolved by T5, choose fallback delivery or reduced scope.",
)

INTEGRATION_RESPONSES = {
    "no-update": ProfessionalResponse("no-update", "No update", "Alex says nothing because T6 has not passed."),
    "activity-dump": ProfessionalResponse("activity-dump", "Activity dump",
        "Worked on the API, added tests, refactored the adapter, checked docs, and debugged responses.",
        status_update=update(activity_details=("Added tests", "Refactored adapter", "Checked vendor docs", "Debugged responses"))),
    "false-green": ProfessionalResponse("false-green", "False green", "Everything is on track.", unsupported_promise=True,
        status_update=update(current_state=StatusCategory.ON_TRACK, forecast=Forecast("T6", "No supporting delivery evidence", guaranteed=True))),
    "vague-risk": ProfessionalResponse("vague-risk", "Vague risk", "Running into vendor issues. Might affect the deadline.", material_risk_communicated=True,
        status_update=update(risks=("Vendor issues might affect the deadline.",))),
    "over-detailed": ProfessionalResponse("over-detailed", "Technically exhaustive update",
        "A long account of payloads, stack traces, adapter branches, fixtures, mocks, and test internals.",
        implementation_details=("raw payloads", "stack traces", "adapter branches", "fixtures", "mocks", "test internals"),
        status_update=update(completed_work=("Success path implemented.",), activity_details=("payload bytes", "stack traces", "fixture internals", "mock internals"))),
    "decision-useful": ProfessionalResponse("decision-useful", "Decision-useful status",
        "Success works; failure normalization is incomplete, putting T6 at risk but not blocking work. Jordan may be affected. I am adding a safe fallback, will update at T5, and then we may need a scope decision.",
        material_risk_communicated=True, dependency_acknowledged=True, preserves_uncertainty=True,
        supports_decision=True, next_action=DECISION_USEFUL.next_action, follow_up_point=5,
        status_update=DECISION_USEFUL),
}

# All views select from the same authored facts; only decision-relevant detail differs.
STATUS_AUDIENCE_UPDATES = {
    "jordan": ProfessionalResponse("jordan", "Jordan view", "Endpoint is not ready to integrate; success contract is stable, errors may change. Continue UI work and expect T5 update.",
        communicated_fact_ids=("success-path", "failure-incomplete", "T6-risk", "jordan-T6"), status_update=DECISION_USEFUL),
    "morgan": ProfessionalResponse("morgan", "Morgan view", "T6 is at risk due to one unknown failure form; fallback work continues and a T5 delivery choice may be needed.",
        communicated_fact_ids=("success-path", "failure-incomplete", "T6-risk", "jordan-T6"), status_update=DECISION_USEFUL),
    "business": ProfessionalResponse("business", "Business view", "Schedule is at risk; user scope is not changed yet. Confidence improves at T5, when a fallback decision may be needed.",
        communicated_fact_ids=("success-path", "failure-incomplete", "T6-risk", "jordan-T6"), status_update=DECISION_USEFUL),
}

CREDENTIAL_BLOCKER = WorkplaceScenario(
    "credential-blocker", "Production-like credential dependency",
    "Alex requested a production-like credential at T1. At T3 security has not supplied it, so validation cannot continue and T5 release confidence is affected.",
    (Participant("Alex", "backend developer"), Participant("Security team", "credential owner"), Participant("Morgan", "engineering manager")),
    ("Credential requested at T1.", "Security owns issuance.", "Validation cannot continue without it.", "Alex can continue documentation."),
    ("When security will issue the credential.",), (Commitment("Alex", "complete validation", "T5"),), RiskLevel.HIGH,
)
BLOCKER_RESPONSES = {
    "silent-blocking": ProfessionalResponse("silent-blocking", "Silent blocking", "Alex waits without communicating."),
    "passive-status": ProfessionalResponse("passive-status", "Passive status", "Still waiting on credentials.",
        status_update=StatusUpdate("Production-like validation", blockers=("Credential unavailable.",))),
    "actionable-escalation": ProfessionalResponse("actionable-escalation", "Actionable escalation",
        "Validation is blocked on the T1 security credential request. Security owns it; T5 confidence is affected. Morgan, please escalate. I can continue documentation, but not validation.",
        material_risk_communicated=True, dependency_acknowledged=True, supports_decision=True,
        status_update=StatusUpdate("Production-like validation", StatusCategory.BLOCKED,
            completed_work=("Credential request submitted at T1.",), remaining_work=("Production-like validation.",),
            blockers=("Validation cannot continue without the credential.",), risks=("T5 release confidence is affected.",),
            dependency_impact=("Validation cannot continue.",), next_action="Continue documentation while waiting.",
            requested_action="Morgan should help escalate the credential request.", dependency_owner="Security team")),
}

COMPLETION_UPDATE = WorkplaceScenario(
    "verification-completion", "Verification endpoint completion",
    "The endpoint is complete, but Jordan cannot update the integration plan until Alex closes the communication loop.",
    (Participant("Alex", "backend developer"), Participant("Jordan", "frontend developer")),
    ("Endpoint is ready.", "Contract is unchanged.", "Tests pass.", "Unknown-error fallback is included."), (),
    (Commitment("Alex", "provide the endpoint", "T6"),), RiskLevel.LOW,
)
COMPLETION_RESPONSES = {
    "silent-completion": ProfessionalResponse("silent-completion", "Silent completion", "Work finishes, but Alex does not tell Jordan."),
    "closed-loop": ProfessionalResponse("closed-loop", "Completion loop closed",
        "Verification endpoint is ready for integration. The contract is unchanged, tests pass, and the unknown-error fallback is included.",
        loop_closed=True, dependency_acknowledged=True,
        status_update=StatusUpdate("Member-verification endpoint", StatusCategory.COMPLETED,
            completed_work=("Endpoint ready.", "Contract unchanged.", "Tests passing.", "Unknown-error fallback included."))),
}

PRIMARY_RESPONSE_IDS = tuple(INTEGRATION_RESPONSES)
