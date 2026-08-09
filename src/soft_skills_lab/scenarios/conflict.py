"""Chapter 10 deterministic conflict scenarios and professional responses."""

from soft_skills_lab.domain.models import (
    ConflictSignal, ConflictStage, ConflictState, DecisionAlternative, DecisionContext, DecisionIssueKind,
    Participant, ProfessionalResponse, RiskLevel, WorkplaceScenario,
)

RELEASE_FACTS = (
    "Friday release has commercial value.", "Manual validation passed.",
    "Automated row-filter coverage is incomplete.", "Export rules affect customer-visible data.",
    "Morgan owns the release decision.",
)
RELEASE_CONFLICT = ConflictState(
    ConflictStage.RISING_TENSION, "Release Friday or delay for automated validation.", RELEASE_FACTS,
    (("Priya", "Manual validation is sufficient for Friday."),
     ("Alex", "Remaining automated validation risk is too high.")),
    (ConflictSignal("Priya", "Every time we get close to shipping, engineering finds another reason to delay.",
                    generalization=True, topic_expansion=True),),
    expanded_issue="Whether engineering habitually delays releases.",
    not_established=("Engineering intentionally delays releases.", "Priya does not care about quality.",
                     "Alex wants to prevent the release."),
)
RELEASE_DECISION = DecisionContext(
    RELEASE_CONFLICT.current_issue, "Morgan", ("Alex", "Priya"),
    "Ship valuable reporting while protecting customer-visible data.",
    (DecisionAlternative("Release Friday", (RELEASE_FACTS[0], RELEASE_FACTS[1])),
     DecisionAlternative("Delay for automated validation", (RELEASE_FACTS[2], RELEASE_FACTS[3]))),
    unresolved_risks=("Commercial delay versus incomplete automated validation.",), issue_kind=DecisionIssueKind.MATERIAL_RISK,
)
RELEASE_VALIDATION = WorkplaceScenario(
    "release-validation", "Release validation conflict",
    "A normal release disagreement broadens into a generalization about engineering.",
    (Participant("Alex", "developer"), Participant("Priya", "product manager"), Participant("Morgan", "engineering manager")),
    RELEASE_FACTS, ("Whether manual validation is sufficient for Friday.",), (), RiskLevel.HIGH,
    decision_context=RELEASE_DECISION, conflict_state=RELEASE_CONFLICT,
)

RELEASE_RESPONSES = {
    "counterattack": ProfessionalResponse("counterattack", "Counterattack", "Product always commits dates without understanding technical risk.", attacks_group=True, generalizes_about_person=True, preserves_material_risk=True),
    "motive-attack": ProfessionalResponse("motive-attack", "Motive attack", "You only care about your date; you don't care if customers get bad data.", personalizes_disagreement=True, attributes_motive_without_evidence=True, preserves_material_risk=True),
    "sarcasm": ProfessionalResponse("sarcasm", "Sarcasm", "Sure, let's ship broken software. Great plan.", uses_sarcasm=True, preserves_material_risk=True),
    "capitulation": ProfessionalResponse("capitulation", "Capitulation", "Fine. Forget I said anything.", ends_argument=True, concedes_decision=True),
    "repeat-louder": ProfessionalResponse("repeat-louder", "Repeat louder", "We need the tests. I've already explained this.", focuses_on_current_decision=True, preserves_material_risk=True, repeats_resolved_argument=True),
    "de-escalate-and-refocus": ProfessionalResponse(
        "de-escalate-and-refocus", "De-escalate and refocus",
        "I understand why another delay is frustrating. Manual checks passed, but row-filter automation for customer data remains incomplete. Morgan, please decide whether Friday's value outweighs that validation risk; I still recommend delaying.",
        captures_explicit_concern=True, acknowledges_legitimate_concern=True, focuses_on_current_decision=True,
        identifies_shared_objective=True, distinguishes_fact_from_interpretation=True,
        restores_shared_facts=True, decision_relevant_evidence=RELEASE_FACTS[1:4], creates_decision_path=True,
        respects_decision_ownership=True, preserves_material_risk=True, states_specific_disagreement=True,
    ),
    "de-escalate-variation": ProfessionalResponse(
        "de-escalate-variation", "Equivalent de-escalation",
        "Two delays make the date pressure real. The choice now is Friday value versus missing automated coverage for customer-data filters. The manual pass is established. I recommend waiting; Morgan owns the call.",
        acknowledges_legitimate_concern=True, focuses_on_current_decision=True, restores_shared_facts=True,
        identifies_shared_objective=True, distinguishes_fact_from_interpretation=True,
        decision_relevant_evidence=RELEASE_FACTS[0:4], creates_decision_path=True, respects_decision_ownership=True,
        preserves_material_risk=True, states_specific_disagreement=True,
    ),
    "pause-and-resume": ProfessionalResponse(
        "pause-and-resume", "Productive pause",
        "We're repeating positions. I'll finish the risk summary by T4; then Morgan can decide whether manual validation is enough for Friday.",
        focuses_on_current_decision=True, restores_shared_facts=True, creates_decision_path=True,
        preserves_material_risk=True, pauses_conversation=True, pause_has_checkpoint=True, pause_names_needed_evidence=True,
        follow_up_point=4, follow_up_commitment="Review the completed risk summary with Morgan at T4.",
    ),
    "avoid-indefinitely": ProfessionalResponse("avoid-indefinitely", "Avoidance", "Let's talk about this some other time.", pauses_conversation=True),
}

def _conflict_scenario(scenario_id: str, title: str, description: str, participants: tuple[Participant, ...],
                       facts: tuple[str, ...], issue: str, issue_kind: DecisionIssueKind = DecisionIssueKind.MAINTAINABILITY,
                       risk: RiskLevel = RiskLevel.MODERATE) -> WorkplaceScenario:
    state = ConflictState(ConflictStage.PERSONALIZED_CONFLICT, issue, facts, (), unresolved_decision=True)
    decision = DecisionContext(issue, participants[-1].name, tuple(p.name for p in participants[:-1]), issue,
                               (DecisionAlternative("Proceed"), DecisionAlternative("Change course")), issue_kind=issue_kind)
    return WorkplaceScenario(scenario_id, title, description, participants, facts, (), (), risk,
                             decision_context=decision, conflict_state=state)

CODE_REVIEW = _conflict_scenario("code-review-conflict", "Code review conflict",
    "Jordan calls the implementation too complicated; Alex asks whether Jordan read the requirements.",
    (Participant("Alex", "developer"), Participant("Jordan", "reviewer")),
    ("The requirement contains three vendor states.",), "Which implementation complexity is required?")
CODE_RESPONSES = {
    "escalate-insult": ProfessionalResponse("escalate-insult", "Escalate insult", "Maybe review code you can understand.", personalizes_disagreement=True),
    "defend-competence": ProfessionalResponse("defend-competence", "Defend competence", "I know how to design this; don't question me.", personalizes_disagreement=True),
    "withdraw": ProfessionalResponse("withdraw", "Withdraw", "Never mind.", ends_argument=True),
    "restore-technical-question": ProfessionalResponse("restore-technical-question", "Repair and restore", "That came out sharper than intended. Three vendor states create most complexity. Which part looks unnecessary?", repairs_own_contribution=True, identifies_own_contribution=True, focuses_on_current_decision=True, restores_shared_facts=True, creates_decision_path=True, preserves_material_risk=True),
}

MANAGER_TRADEOFF = _conflict_scenario("manager-tradeoff-conflict", "Manager pressure: ordinary tradeoff",
    "Morgan asks Alex to stop repeating an ordinary architectural argument and implement the decision.",
    (Participant("Alex", "junior developer"), Participant("Morgan", "engineering manager")),
    ("Alex's concern was heard.", "The architectural choice is reversible."), "Which reversible cache boundary should be used?", risk=RiskLevel.LOW)
MANAGER_TRADEOFF_RESPONSES = {"confirm-and-proceed": ProfessionalResponse("confirm-and-proceed", "Confirm and proceed", "I understand the decision. I'll document the tradeoff and proceed.", focuses_on_current_decision=True, restores_shared_facts=True, creates_decision_path=True, respects_decision_ownership=True, resolves_issue=True, preserves_material_risk=True)}

MANAGER_MATERIAL = _conflict_scenario("manager-material-risk", "Manager pressure: material risk",
    "Morgan asks Alex to stop arguing although the direction could expose customer data.",
    (Participant("Alex", "junior developer"), Participant("Morgan", "engineering manager")),
    ("The proposed export can expose one customer's rows to another customer.",), "May the unsafe export ship?",
    DecisionIssueKind.MATERIAL_RISK, RiskLevel.CRITICAL)
MANAGER_MATERIAL_RESPONSES = {
    "suppress-risk": ProfessionalResponse("suppress-risk", "Suppress risk", "Okay, I'll ship it.", concedes_decision=True, ends_argument=True),
    "document-and-escalate": ProfessionalResponse("document-and-escalate", "Preserve and escalate risk", "I will stop repeating the point, document the customer-data evidence, and use the security escalation path before release.", focuses_on_current_decision=True, restores_shared_facts=True, creates_decision_path=True, preserves_material_risk=True, escalates_material_risk=True),
}

PUBLIC_CONFLICT = _conflict_scenario("public-deadline-conflict", "Public deadline conflict",
    "A team meeting turns into an argument about responsibility for a missed deadline.",
    (Participant("Alex", "developer"), Participant("Priya", "product manager"), Participant("Morgan", "meeting facilitator")),
    ("The deadline was missed.", "A delivery decision is needed today."), "What immediate delivery plan is needed?")
PUBLIC_RESPONSES = {"change-venue": ProfessionalResponse("change-venue", "Change venue without erasing accountability", "Let's decide today's delivery plan now and review evidence about ownership in the incident follow-up at T5.", focuses_on_current_decision=True, restores_shared_facts=True, creates_decision_path=True, pauses_conversation=True, pause_has_checkpoint=True, pause_names_needed_evidence=True, preserves_material_risk=True, follow_up_point=5)}
