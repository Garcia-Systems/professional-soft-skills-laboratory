"""Deterministic Chapter 1 commitment scenario and reference behaviors."""

from soft_skills_lab.domain.models import (
    Commitment, CommitmentStatus, Participant, ProfessionalCommitment, ProfessionalResponse,
    RiskLevel, TimelineEvent, WorkplaceScenario,
)

VENDOR_FACT = "The vendor API behaves differently from its documentation."

COMMITMENT = ProfessionalCommitment(
    "api-endpoint", "Build the API endpoint for frontend integration", "Alex", "Jordan", 2,
    CommitmentStatus.AT_RISK, ("Jordan's frontend integration",), (VENDOR_FACT,),
)

COMMITMENT_AT_RISK = WorkplaceScenario(
    "commitment-at-risk", "An API commitment becomes at risk",
    "Alex expects an API endpoint by Day 2. On Day 1, undocumented vendor behavior makes that estimate unlikely.",
    (Participant("Alex", "developer"), Participant("Jordan", "frontend teammate")),
    ("Alex estimated delivery by Day 2.", VENDOR_FACT, "Jordan needs the endpoint to integrate the frontend."),
    ("The final completion time.", "How extensive the vendor discrepancy is."),
    (Commitment("Alex", "deliver the API endpoint so Jordan can integrate", "Day 2"),), RiskLevel.HIGH,
)

TIMELINE = (
    TimelineEvent(0, "Alex makes the Day 2 commitment to Jordan."),
    TimelineEvent(1, "Alex discovers the vendor API discrepancy and the estimate becomes at risk."),
    TimelineEvent(2, "The original completion point arrives."),
)

RESPONSES = {
    "silent": ProfessionalResponse(
        "silent", "Silent miss", "Alex says nothing; Jordan asks after Day 2.", delivered_on_time=False,
    ),
    "vague-warning": ProfessionalResponse(
        "vague-warning", "Vague warning", "Running into some issues. Might take longer.",
        communicated_at=1, material_risk_communicated=True, unknown_information=("Completion may be later.",),
        delivered_on_time=False,
    ),
    "premature-promise": ProfessionalResponse(
        "premature-promise", "Premature promise", "I'll definitely still have it done tomorrow.",
        communicated_at=1, material_risk_communicated=True, unsupported_promise=True,
        known_information=(VENDOR_FACT,), delivered_on_time=False,
    ),
    "professional-update": ProfessionalResponse(
        "professional-update", "Professional early update",
        "The vendor behavior differs from its docs, so Day 2 is at risk. I am investigating. Your frontend depends "
        "on this; I do not know the final completion time yet. I will update you at the start of Day 2.",
        communicated_at=1, material_risk_communicated=True, dependency_acknowledged=True,
        known_information=(VENDOR_FACT, "The Day 2 estimate is at risk."),
        unknown_information=("The final completion time is not yet known.",),
        next_action="Investigate the vendor discrepancy and its scope.", follow_up_commitment="Update Jordan at the start of Day 2.",
        follow_up_point=2, loop_closed=True, delivered_on_time=False,
    ),
    "professional-missed": ProfessionalResponse(
        "professional-missed", "Professional behavior, missed outcome", "Early update followed by a final status and revised plan.",
        communicated_at=1, material_risk_communicated=True, dependency_acknowledged=True,
        known_information=(VENDOR_FACT,), unknown_information=("Completion time remained unknown during investigation.",),
        next_action="Investigate and create a revised plan.", follow_up_commitment="Update at the start of Day 2.", follow_up_point=2,
        loop_closed=True, delivered_on_time=False,
    ),
    "hidden-risk-success": ProfessionalResponse(
        "hidden-risk-success", "Hidden risk, successful outcome", "Alex hides the known risk but happens to finish on Day 2.",
        delivered_on_time=True,
    ),
}

PRIMARY_RESPONSE_IDS = ("silent", "vague-warning", "premature-promise", "professional-update")
