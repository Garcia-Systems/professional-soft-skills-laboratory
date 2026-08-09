"""Chapter 8 scenarios: evidence-based responsibility as observable behavior."""

from soft_skills_lab.domain.models import (
    Commitment, Participant, ProfessionalCommitment, ProfessionalResponse,
    ResponsibilityBoundary, ResponsibilityMap, RiskLevel, WorkplaceScenario,
)


SKIPPED_VALIDATION_MAP = ResponsibilityMap(
    incident="Payment-service deployment failure",
    boundaries=(
        ResponsibilityBoundary("Alex", ("Chose to deploy.", "Skipped required staging payment validation."),
                               ("Authorship of the incorrect configuration.", "Original vendor behavior."),
                               ("An avoidable validation control was bypassed before deployment.",)),
        ResponsibilityBoundary("Jordan", ("Authored the configuration change.",),
                               ("Final deployment decision.", "Whether staging validation was run."),
                               ("The authored configuration contained an incorrect endpoint.",)),
    ),
    process_conditions=("Staging validation was manual.", "The release schedule created pressure."),
    results=("Incorrect configuration reached production.",
             "Required validation would have detected it.",
             "Customers received errors for 18 minutes and had to retry; no payments were lost."),
    evidence=("Procedure required validation.", "Alex knew the procedure.",
              "Validation would have revealed the incorrect endpoint."),
    not_supported=("Alex authored the incorrect endpoint.", "Alex intended to create the incident.",
                   "Alex was the only contributor."),
    immediate_responsibility=("Acknowledge skipped validation.", "Support rollback and verification.",
                              "Communicate corrected deployment plan."),
    preventive_action=("Make validation harder to bypass.",),
)

SKIPPED_VALIDATION = WorkplaceScenario(
    "skipped-validation", "Skipped staging validation",
    "Morgan asks Alex what happened after a payment-service deployment caused an 18-minute incident.",
    (Participant("Alex", "developer"), Participant("Jordan", "teammate"),
     Participant("Morgan", "engineering manager")),
    ("Jordan authored a configuration change containing an incorrect endpoint.",
     "Alex reviewed and deployed the release.",
     "Procedure required staging payment validation and Alex knew it.",
     "Unit and integration tests passed.", "The release was under schedule pressure.",
     "Alex chose to skip the manual staging validation to save time.",
     "The staging validation would have exposed the incorrect endpoint.",
     "Production requests failed for 18 minutes before monitoring prompted rollback.",
     "No payments were lost; some customers received errors and had to retry."),
    ("Whether undocumented vendor behavior also contributed.",),
    (Commitment("Alex", "verify payment behavior before redeployment", "before redeployment"),),
    RiskLevel.CRITICAL, responsibility_map=SKIPPED_VALIDATION_MAP,
)

RESPONSES = {
    "deny": ProfessionalResponse("deny", "Deny contribution", "I didn't cause this. Jordan wrote the configuration.",
        assigns_unsupported_blame=True),
    "blame-process": ProfessionalResponse("blame-process", "Blame the process",
        "The release process is bad. If staging validation were automated, this wouldn't have happened.",
        context_provided=True, context_used_as_excuse=True, assigns_unsupported_blame=True,
        identifies_preventive_action=True, acknowledges_impact=True),
    "excuse-pressure": ProfessionalResponse("excuse-pressure", "Use pressure as an excuse",
        "We were under a lot of pressure to release, so I didn't really have a choice.",
        context_provided=True, context_used_as_excuse=True, preserves_agency=False, acknowledges_impact=True),
    "over-own": ProfessionalResponse("over-own", "Accept all blame", "This entire incident is my fault. I completely failed the team.",
        responsibility_statement="I accept responsibility for the entire incident.", over_owns=True,
        self_condemnation=True, acknowledges_impact=True, identifies_own_contribution=False),
    "empty-apology": ProfessionalResponse("empty-apology", "Apology without specifics", "I'm sorry. It won't happen again.",
        acknowledges_feedback=True, responsibility_statement="I am sorry.", acknowledges_impact=True),
    "explanation-without-ownership": ProfessionalResponse("explanation-without-ownership", "Context without ownership",
        "Tests passed, the release was under pressure, Jordan authored the config, and staging validation is manual.",
        context_provided=True, acknowledges_impact=True, identifies_preventive_action=True),
    "accurate-ownership": ProfessionalResponse("accurate-ownership", "Accurate ownership and action",
        "I deployed and chose to skip the required staging payment validation. Pressure influenced my decision but did not remove it; the check would have caught the endpoint. Rollback contained the errors. I will correct the endpoint, run validation before redeploying, and propose a mandatory automated gate.",
        acknowledged_facts=("Alex deployed.", "Alex skipped the required validation.",
                            "The validation would have detected the endpoint."),
        responsibility_statement="I chose to skip the required validation.", context_provided=True,
        identifies_own_contribution=True, prioritizes_containment=True, identifies_corrective_action=True,
        identifies_preventive_action=True, acknowledges_impact=True, identifies_behavior_change=True,
        next_action="Correct the endpoint and validate before redeployment.",
        follow_up_commitment="Propose a mandatory automated validation gate."),
    "equivalent-ownership": ProfessionalResponse("equivalent-ownership", "Equivalent ownership wording",
        "The part I own is bypassing the staging check required by our procedure. Rollback stopped the impact; I will fix and validate the endpoint, then add a deployment gate.",
        responsibility_statement="I bypassed the required check.", context_provided=True,
        identifies_own_contribution=True, prioritizes_containment=True, identifies_corrective_action=True,
        identifies_preventive_action=True, acknowledges_impact=True, identifies_behavior_change=True),
}
PRIMARY_RESPONSE_IDS = ("deny", "blame-process", "excuse-pressure", "over-own", "empty-apology",
                        "explanation-without-ownership", "accurate-ownership")

MISSED_HANDOFF_COMMITMENT = ProfessionalCommitment("api-contract-handoff", "Send updated API schema", "Alex", "Jordan", 4)
MISSED_HANDOFF = WorkplaceScenario(
    "missed-handoff", "Missed API contract handoff",
    "Alex completed an API contract at T3 but forgot the owned T4 handoff; Jordan waited until T5 and lost a day.",
    (Participant("Alex", "API owner"), Participant("Jordan", "dependent teammate")),
    ("Alex completed the schema at T3.", "Alex owned sending it by T4.",
     "No external blocker prevented communication.", "Jordan waited until T5 and lost a day."), (),
    (Commitment("Alex", "send updated API schema", "T4"),), RiskLevel.MODERATE,
    responsibility_map=ResponsibilityMap("Missed API schema handoff", (
        ResponsibilityBoundary("Alex", ("Complete and send the schema.",), (), ("Forgot to send it by T4.",)),
        ResponsibilityBoundary("Jordan", ("Use the schema after receipt.",), ("Alex's handoff closure.",), ()),),
        results=("Jordan lost one day.",), immediate_responsibility=("Send the schema immediately.",),
        preventive_action=("Track explicit handoff closure.",)),
)
MISSED_HANDOFF_RESPONSES = {
    "jordan-could-ask": ProfessionalResponse("jordan-could-ask", "Shift handoff ownership", "Jordan could have asked.", assigns_unsupported_blame=True),
    "busy-excuse": ProfessionalResponse("busy-excuse", "Use workload as excuse", "I was busy.", context_provided=True, context_used_as_excuse=True),
    "vague-apology": ProfessionalResponse("vague-apology", "Vague apology", "Sorry; it won't happen again.", acknowledges_impact=True),
    "own-and-recover": ProfessionalResponse("own-and-recover", "Own and recover", "I completed it but missed my T4 handoff, which cost Jordan a day. I am sending it now and will track handoff acknowledgment next time.",
        responsibility_statement="I missed my T4 handoff.", identifies_own_contribution=True, acknowledges_impact=True,
        prioritizes_containment=True, identifies_corrective_action=True, identifies_preventive_action=True,
        identifies_behavior_change=True, loop_closed=True),
}

SHARED_RESPONSIBILITY = WorkplaceScenario(
    "shared-responsibility", "Ambiguous timezone release",
    "An ambiguous timezone requirement and three separate decisions contribute to a failed release.",
    (Participant("Priya", "product owner"), Participant("Alex", "developer"), Participant("Morgan", "approver")),
    ("Priya did not specify timezone behavior.", "Alex noticed the omission and assumed UTC without clarifying.",
     "Morgan approved without reviewing the unresolved requirement."), (), (), RiskLevel.HIGH,
    responsibility_map=ResponsibilityMap("Timezone behavior release failure", (
        ResponsibilityBoundary("Priya", ("Specify timezone behavior.",), (), ("Left the behavior ambiguous.",)),
        ResponsibilityBoundary("Alex", ("Clarify before implementation.",), (), ("Assumed UTC instead of clarifying.",)),
        ResponsibilityBoundary("Morgan", ("Review unresolved release requirements.",), (), ("Approved without that review.",))),
        results=("Incorrect timezone behavior reached release.",),
        not_supported=("Alex alone caused the failure.",)),
)
SHARED_RESPONSES = {"bounded-ownership": ProfessionalResponse("bounded-ownership", "Bounded shared ownership",
    "I noticed timezone behavior was unspecified and assumed UTC instead of clarifying. That decision is my part; it does not make me the only contributor.",
    responsibility_statement="I assumed instead of clarifying.", identifies_own_contribution=True, acknowledges_impact=True)}

UNAVOIDABLE_OUTCOME = WorkplaceScenario(
    "unavoidable-outcome", "Undocumented vendor behavior",
    "A release fails despite all required validations because of undocumented vendor behavior no reasonable pre-deployment test could detect.",
    (Participant("Alex", "deployer"), Participant("Morgan", "engineering manager")),
    ("Alex completed every required validation.", "Available evidence supported deployment.",
     "Undocumented vendor behavior caused the failure.", "No reasonable pre-deployment test could detect it."), (), (), RiskLevel.CRITICAL,
    responsibility_map=ResponsibilityMap("Vendor behavior outage", (
        ResponsibilityBoundary("Alex", ("Run required checks.", "Help investigate and recover."),
                               ("Undocumented vendor behavior.",), ("Deployed based on passing required checks.",)),),
        external_factors=("Undocumented vendor behavior caused the failure.",),
        not_supported=("Alex made an avoidable deployment error.",)),
)
UNAVOIDABLE_RESPONSES = {"evidence-bounded": ProfessionalResponse("evidence-bounded", "Evidence-bounded recovery",
    "I deployed based on passing required checks. I am responsible for investigation and recovery, but there is no evidence I made an avoidable deployment error.",
    responsibility_statement="I own investigation and recovery, not an unsupported error.", prioritizes_containment=True,
    identifies_corrective_action=True, preserves_respectful_disagreement=True)}

LEARNING_FOLLOW_UP = WorkplaceScenario(
    "responsibility-follow-up", "Demonstrated learning on the next release",
    "A new gate catches another invalid endpoint; Alex performs the check, stops deployment, and reports it.",
    (Participant("Alex", "developer"), Participant("Morgan", "engineering manager")),
    ("Staging validation became a deployment gate.", "Alex performed it on the next release.",
     "It detected an invalid endpoint before production.", "Alex stopped deployment and reported it."), (), (), RiskLevel.LOW,
)
LEARNING_RESPONSES = {"demonstrated-learning": ProfessionalResponse("demonstrated-learning", "Learning demonstrated",
    "Alex ran the new gate, stopped the invalid release, and reported the finding.", demonstrated_improvement=True,
    prioritizes_containment=True, identifies_preventive_action=True, loop_closed=True)}
