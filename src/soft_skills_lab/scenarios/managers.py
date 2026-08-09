"""Chapter 11 scenarios reuse the shared professional-behavior model."""

from soft_skills_lab.domain.models import (
    ManagerExpectation, Participant, ProfessionalResponse, RiskLevel, TimelineEvent,
    VisibilityThreshold, WorkingAgreement, WorkplaceScenario,
)

KICKOFF = ("You own the implementation. I don't need every technical detail, but tell me early "
           "if the T8 delivery is at risk, if another team is blocking you, or if you need to "
           "change the API contract Jordan is integrating against.")

EXPECTATIONS = (
    ManagerExpectation("Internal refactor", VisibilityThreshold.ROUTINE, "Act independently", "Alex", KICKOFF, 2),
    ManagerExpectation("Vendor response normalization", VisibilityThreshold.ROUTINE, "Act independently", "Alex", KICKOFF, 3),
    ManagerExpectation("Schedule risk", VisibilityThreshold.INFORM, "Update Morgan", "Alex", KICKOFF, 4),
    ManagerExpectation("API contract change", VisibilityThreshold.CONSULT, "Discuss before changing contract", "Morgan and Jordan", KICKOFF, 5),
    ManagerExpectation("Vendor validation outage", VisibilityThreshold.ESCALATE, "Promptly surface blocker and impact", "Morgan", KICKOFF, 6),
)
PROJECT_AGREEMENT = WorkingAgreement(
    "Morgan", "Alex",
    ("Internal implementation details.", "Refactoring that preserves external behavior.",
     "Vendor normalization behind the existing API contract."), EXPECTATIONS,
    "Risk- and decision-based updates; no implementation-by-implementation approval.",
    ("Jordan depends on the public API contract.", "The vendor test environment is external."),
)
PROJECT_TIMELINE = (
    TimelineEvent(0, "Alex owns day-to-day member-verification implementation."),
    TimelineEvent(2, "Alex refactors an internal adapter without changing external behavior."),
    TimelineEvent(3, "An undocumented vendor response can be normalized safely; T8 remains supported."),
    TimelineEvent(4, "A second vendor issue creates material risk to T8."),
    TimelineEvent(5, "A possible fix would change Jordan's public API contract."),
    TimelineEvent(6, "The vendor test environment is unavailable and validation cannot continue."),
)
PROJECT_AUTONOMY = WorkplaceScenario(
    "project-autonomy", "Project autonomy with manager visibility",
    KICKOFF, (Participant("Morgan", "engineering manager"), Participant("Alex", "developer"),
              Participant("Jordan", "dependent teammate")),
    tuple(event.description for event in PROJECT_TIMELINE), ("Duration of the vendor outage.",), (),
    RiskLevel.HIGH, working_agreement=PROJECT_AGREEMENT,
)

def response(response_id: str, label: str, message: str, **behavior: bool | int | str | tuple) -> ProfessionalResponse:
    return ProfessionalResponse(response_id, label, message, **behavior)

PROJECT_RESPONSES = {
    "permission-for-everything": response("permission-for-everything", "Permission for everything", "May I refactor the helper, rename variables, add an adapter branch, and update fixtures?", threshold_risk_visible=True, unnecessary_upward_delegation=True),
    "silent-autonomy": response("silent-autonomy", "Silent autonomy", "I handled the vendor issues and contract change; Morgan learned later.", owns_delegated_decisions=True, recommendation_provided=True),
    "status-flood": response("status-flood", "Status flood", "Every edit, test fixture, variable rename, risk, and decision follows...", owns_delegated_decisions=True, threshold_risk_visible=True, consultation_boundary_respected=True, true_blocker_escalated=True, recommendation_provided=True, follow_up_commitment="Continue sending every detail."),
    "late-escalation": response("late-escalation", "Late escalation", "After several periods of solo investigation: validation is blocked; preserve the contract.", owns_delegated_decisions=True, threshold_risk_visible=False, consultation_boundary_respected=True, true_blocker_escalated=False, recommendation_provided=True, follow_up_commitment="Update after another investigation period."),
    "escalate-without-investigation": response("escalate-without-investigation", "Escalate without investigation", "I'm blocked. What should I do?", threshold_risk_visible=True, true_blocker_escalated=False, follow_up_commitment="Follow Morgan's instruction.", unnecessary_upward_delegation=True),
    "managed-autonomy": response("managed-autonomy", "Managed autonomy", "I handled T2 and T3. T8 is at risk. Before changing Jordan's contract, let's decide; at T6 vendor validation is blocked. I recommend preserving the contract, will continue independent tests, and update at T7.", owns_delegated_decisions=True, threshold_risk_visible=True, consultation_boundary_respected=True, true_blocker_escalated=True, recommendation_provided=True, manager_signal_preserved=True, material_risk_communicated=True, dependency_acknowledged=True, respects_decision_ownership=True, preserves_uncertainty=True, follow_up_point=7, follow_up_commitment="Update Morgan at T7."),
    "visibility-with-recommendation": response("visibility-with-recommendation", "Visibility with recommendation", "The simplest workaround changes Jordan's contract. I recommend preserving it and normalizing inside the adapter; that may put T8 at risk by one checkpoint. Vendor validation is now blocked; I'll continue local tests and update at T7.", owns_delegated_decisions=True, threshold_risk_visible=True, consultation_boundary_respected=True, true_blocker_escalated=True, recommendation_provided=True, manager_signal_preserved=True, material_risk_communicated=True, dependency_acknowledged=True, respects_decision_ownership=True, preserves_uncertainty=True, follow_up_point=7, follow_up_commitment="Update Morgan at T7."),
    "managed-autonomy-variation": response("managed-autonomy-variation", "Equivalent managed autonomy", "Routine adapter work is complete. Delivery now has vendor risk; the shared contract needs consultation. I advise keeping its shape. Validation is blocked, so I escalated and set a T7 follow-up.", owns_delegated_decisions=True, threshold_risk_visible=True, consultation_boundary_respected=True, true_blocker_escalated=True, recommendation_provided=True, manager_signal_preserved=True, follow_up_point=7),
}

def small(sid: str, title: str, description: str, facts: tuple[str, ...], responses: dict[str, ProfessionalResponse], risk=RiskLevel.MODERATE):
    scenario = WorkplaceScenario(sid, title, description, (Participant("Morgan", "engineering manager"), Participant("Alex", "developer")), facts, (), (), risk, working_agreement=PROJECT_AGREEMENT)
    return scenario, responses

OWNERSHIP, OWNERSHIP_RESPONSES = small("deployment-ownership", "Ownership with recommendation", "Morgan asks Alex to investigate a failed deployment and recommend action.", ("Production impact continues.",), {
    "empty-escalation": response("empty-escalation", "Empty escalation", "What do you want me to do?", unnecessary_upward_delegation=True),
    "invisible-investigation": response("invisible-investigation", "Independent but invisible", "Alex investigates beyond the production update threshold.", owns_delegated_decisions=True),
    "professional-ownership": response("professional-ownership", "Professional ownership", "Rollback is supported by logs; cause remains uncertain. I recommend rollback. Morgan owns that production decision; I will update in 20 minutes.", owns_delegated_decisions=True, threshold_risk_visible=True, recommendation_provided=True, manager_signal_preserved=True, respects_decision_ownership=True, preserves_uncertainty=True, follow_up_point=20),
}, RiskLevel.CRITICAL)
VAGUE, VAGUE_RESPONSES = small("vague-manager-direction", "Vague manager direction", "Morgan says: Make the reporting system more reliable.", ("Recent failure evidence is available.",), {"clarify-outcome": response("clarify-outcome", "Clarify measurable outcome", "Recent failures are delayed exports. Should success mean fewer than one delayed export per month, and which customers are in scope?", working_agreement_clarified=True, investigation_performed=("Inspected recent failure evidence.",), clarifies_success_condition=True)})
CHANGING, CHANGING_RESPONSES = small("changing-autonomy", "Changing autonomy expectations", "After reliable delivery Morgan replaces daily details with risk- and decision-based updates.", ("The change is explicit.", "Organizational context also affects autonomy."), {"expanded-autonomy": response("expanded-autonomy", "Expanded autonomy", "I will own routine work and update when risk or a decision crosses the new boundary.", owns_delegated_decisions=True, working_agreement_clarified=True, manager_signal_preserved=True)})
MICRO, MICRO_RESPONSES = small("micromanagement-clarification", "Clarifying approval expectations", "Approval for every small decision creates latency, duplicate effort, and unclear ownership; no motive is inferred.", ("Alex was assigned implementation ownership.",), {"clarify-boundaries": response("clarify-boundaries", "Clarify boundaries", "For changes that do not affect scope, API contracts, or delivery risk, may I decide independently and summarize them in the normal update?", working_agreement_clarified=True, manager_signal_preserved=True)})
UNAVAILABLE, UNAVAILABLE_RESPONSES = small("manager-unavailable", "Manager unavailable", "Morgan is unavailable during a time-sensitive issue; existing boundaries still apply.", ("Alex may preserve the contract and continue local work.", "A named incident channel is the alternate escalation path."), {"use-boundaries": response("use-boundaries", "Use boundaries and alternate path", "I will preserve the contract, continue local work, defer the scope decision, and send the blocker to the incident channel.", owns_delegated_decisions=True, consultation_boundary_respected=True, true_blocker_escalated=True, manager_signal_preserved=True)})
ONE_ON_ONE, ONE_ON_ONE_RESPONSES = small("manager-one-on-one", "Prepared one-on-one", "Alex has a risk, a decision, a development question, and routine details.", ("Shared time is limited.",), {
    "no-topics": response("no-topics", "No preparation", "What do you want to discuss?"),
    "task-dump": response("task-dump", "Every-task dump", "Here is every implementation detail."),
    "prepared-topics": response("prepared-topics", "Attention-relevant preparation", "I prepared the material risk, the decision you own, and one development question; routine details remain in the normal update.", threshold_risk_visible=True, recommendation_provided=True, manager_signal_preserved=True),
})

MANAGER_SCENARIOS = {s.scenario_id: (s, r) for s, r in ((PROJECT_AUTONOMY, PROJECT_RESPONSES), (OWNERSHIP, OWNERSHIP_RESPONSES), (VAGUE, VAGUE_RESPONSES), (CHANGING, CHANGING_RESPONSES), (MICRO, MICRO_RESPONSES), (UNAVAILABLE, UNAVAILABLE_RESPONSES), (ONE_ON_ONE, ONE_ON_ONE_RESPONSES))}
