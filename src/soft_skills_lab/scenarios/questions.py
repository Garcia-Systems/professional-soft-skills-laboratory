"""Deterministic Chapter 3 question scenarios and knowledge updates."""

from dataclasses import replace

from soft_skills_lab.domain.models import (
    DecisionRelevance, DecisionUnknown, InformationSource, Participant, ProfessionalQuestion,
    ProfessionalResponse, QuestionContext, RiskLevel, WorkplaceScenario,
)

DOWNLOAD_EVIDENCE = (
    "GenericDownloadComponent exists in the repository.",
    "GenericDownloadComponent supports streamed browser downloads.",
    "The component does not decide business-specific formats or columns.",
)

REPORT_UNKNOWNS = (
    DecisionUnknown("export-format", "Export format", DecisionRelevance.HIGH, InformationSource.STAKEHOLDER,
                    "The serialization contract cannot be selected safely.", True),
    DecisionUnknown("filter-scope", "Filters affect exported rows", DecisionRelevance.HIGH, InformationSource.STAKEHOLDER,
                    "The exported population may differ from what the user expects.", True),
    DecisionUnknown("allowed-fields", "Allowed export fields", DecisionRelevance.HIGH, InformationSource.STAKEHOLDER,
                    "Internal information could be exposed or required information omitted.", True),
    DecisionUnknown("maximum-range", "Maximum export size", DecisionRelevance.MEDIUM, InformationSource.STAKEHOLDER,
                    "An unconstrained export may create product or engineering risk."),
    DecisionUnknown("download-component", "Existing download component", DecisionRelevance.RESOLVED,
                    InformationSource.SELF_INVESTIGATION, "Asking transfers trivial repository inspection to Priya.",
                    resolved_value="GenericDownloadComponent supports streamed browser downloads."),
    DecisionUnknown("button-icon", "Button icon", DecisionRelevance.LOW, InformationSource.STAKEHOLDER,
                    "This non-blocking presentation detail can be decided later."),
    DecisionUnknown("button-label", "Final button label", DecisionRelevance.LOW, InformationSource.STAKEHOLDER,
                    "This non-blocking presentation detail can be decided later."),
    DecisionUnknown("filename-punctuation", "Filename punctuation", DecisionRelevance.LOW, InformationSource.STAKEHOLDER,
                    "This non-blocking detail does not prevent initial implementation."),
)

REPORT_CONTEXT = QuestionContext("Can implementation begin safely?", REPORT_UNKNOWNS, DOWNLOAD_EVIDENCE)
REPORT_EXPORT = WorkplaceScenario(
    "report-export", "Asking focused questions about an ambiguous report export",
    "Priya asks Alex: “Add an export option to the customer activity report so account managers can use the data outside the application.”",
    (Participant("Priya", "product manager"), Participant("Alex", "developer")),
    ("The report is a table with approximately 15 columns.", "Users can filter by date range.",
     "Account managers are the primary users.") + DOWNLOAD_EVIDENCE,
    tuple(item.description for item in REPORT_UNKNOWNS if not item.is_resolved), (), RiskLevel.MODERATE,
    question_context=REPORT_CONTEXT,
)

def question(question_id: str, targets: tuple[str, ...], message: str, **kwargs: object) -> ProfessionalQuestion:
    return ProfessionalQuestion(question_id, targets, message, InformationSource.STAKEHOLDER, **kwargs)

FOCUSED_QUESTIONS = (
    question("format", ("export-format",), "Which export format should account managers receive?"),
    question("filters", ("filter-scope",), "Should active report filters define the exported rows?"),
    question("fields", ("allowed-fields",), "Which member-visible fields are allowed in the export?"),
    question("range", ("maximum-range",), "Does the export need a date-range or size constraint?"),
)

REPORT_RESPONSES = {
    "no-questions": ProfessionalResponse("no-questions", "Begin with unverified assumptions",
        "I'll build CSV using current filters, visible columns, and an unlimited date range.",
        assumptions=("CSV is required.", "Current filters apply.", "Visible columns only.", "No date limit."),
        next_action="Implement the assumed contract."),
    "question-dump": ProfessionalResponse("question-dump", "Undifferentiated question dump",
        "CSV or Excel? Button label and color? Timestamps, email, PDF, shortcuts, schedules, icon, or alternating row colors?",
        questions=FOCUSED_QUESTIONS + tuple(question(f"low-{n}", (target,), text, non_blocking=True) for n, (target, text) in enumerate((
            ("button-label", "What should the button say?"), ("button-icon", "What color and icon?"),
            ("filename-punctuation", "How should filenames be punctuated?"), ("button-icon", "Keyboard shortcut?"),
            ("button-icon", "Should exports be scheduled?"), ("button-icon", "Alternating row colors?")), 1)),
        question_dump=True, supplies_question_context=False),
    "ask-before-looking": ProfessionalResponse("ask-before-looking", "Ask before inspecting available evidence",
        "Does the application already have a download component?",
        questions=(question("component", ("download-component",), "Does a download component exist?"),)),
    "leading-question": ProfessionalResponse("leading-question", "Assumptions disguised as confirmation",
        "You want this as a CSV of the currently filtered visible columns, right?",
        questions=(question("leading", ("export-format", "filter-scope", "allowed-fields"),
            "CSV of currently filtered visible columns, right?", embedded_assumptions=("CSV", "filters apply", "visible columns only")),)),
    "focused-questions": ProfessionalResponse("focused-questions", "Investigate, then ask focused questions",
        "I found our generic streamed-download component and can reuse it. Before implementation, I need to confirm the format, filter scope, allowed fields, and size constraint.",
        questions=FOCUSED_QUESTIONS, investigation_performed=DOWNLOAD_EVIDENCE,
        supplies_question_context=True, next_action="Apply Priya's answers to the export contract."),
}

REPORT_ANSWERS = {"export-format": "CSV", "filter-scope": "Current filters apply",
                  "allowed-fields": "Only member-visible report fields", "maximum-range": "Maximum 90-day export"}


def apply_answers(scenario: WorkplaceScenario, answers: dict[str, str] = REPORT_ANSWERS) -> WorkplaceScenario:
    """Return updated immutable knowledge; applying the same answers is deterministic."""
    if scenario.question_context is None:
        raise ValueError("scenario has no question context")
    updated = tuple(replace(item, relevance=DecisionRelevance.RESOLVED, resolved_value=answers[item.unknown_id])
                    if item.unknown_id in answers else item for item in scenario.question_context.unknowns)
    facts = scenario.known_facts + tuple(f"{item.description}: {answers[item.unknown_id]}"
                                        for item in scenario.question_context.unknowns
                                        if item.unknown_id in answers and f"{item.description}: {answers[item.unknown_id]}" not in scenario.known_facts)
    return replace(scenario, known_facts=facts,
                   uncertainties=tuple(item.description for item in updated if not item.is_resolved),
                   question_context=replace(scenario.question_context, unknowns=updated))

# Problem-first sequencing extends Chapter 2's search scenario semantics.
SEARCH_SEQUENCE_RESPONSES = {
    "solution-first": ProfessionalResponse("solution-first", "Solution-first questions",
        "Redis, Elasticsearch, or a query rewrite?", problem_first_sequence=False,
        assumptions=("A particular implementation change is already warranted.",)),
    "problem-first": ProfessionalResponse("problem-first", "Problem-first questions",
        "Which workflow is slow, what latency occurs, what is acceptable, and under which conditions?",
        problem_first_sequence=True),
}

DEPLOYMENT_FAILURE = WorkplaceScenario(
    "deployment-failure", "Asking a manager after proportionate investigation",
    "An unfamiliar migration failure occurs before a production deadline.",
    (Participant("Alex", "developer"), Participant("Sam", "engineering manager")),
    ("The failing command and error X are available.", "Deployment logs, a runbook, and prior deployments are available."),
    ("Whether the manager recognizes error X.", "Whether rollback path Z should begin."), (), RiskLevel.HIGH,
    question_context=QuestionContext("How should the failed deployment proceed safely?", (
        DecisionUnknown("migration-failure", "Cause and safe response to migration error X", DecisionRelevance.HIGH,
                        InformationSource.MANAGER, "The team must choose recovery or rollback before the deadline.", True),
    )),
)
DEPLOYMENT_RESPONSES = {
    "helpless-escalation": ProfessionalResponse("helpless-escalation", "Helpless escalation", "Deployment failed. What do I do?",
        questions=(question("help", (), "What do I do?", answerable=False),)),
    "endless-solo-investigation": ProfessionalResponse("endless-solo-investigation", "Excessive solo investigation",
        "Alex keeps investigating silently past the production decision point.", investigation_delay=180, delay_creates_risk=True),
    "professional-question": ProfessionalResponse("professional-question", "Professional manager question",
        "Migration Y fails with X. I checked the runbook and two deployments; the connection succeeds and no changes applied. Seen this, or should I use rollback Z?",
        questions=(ProfessionalQuestion("migration", ("migration-failure",), "Recognize X or use rollback Z?", InformationSource.MANAGER,
            ("runbook", "last two deployments", "logs"), ("migration step", "error X", "connection succeeds")),),
        investigation_performed=("runbook", "last two deployments", "logs"), supplies_question_context=True,
        proposed_next_action=True, next_action="Rollback path Z if directed."),
}

AUTHORIZATION_INCIDENT = WorkplaceScenario(
    "authorization-risk", "Immediate escalation of authorization exposure risk",
    "Alex discovers a production authorization problem that could expose customer information.",
    (Participant("Alex", "developer"), Participant("Sam", "manager")),
    ("Customer information may be exposed.", "Alex lacks authority to manage the incident alone."),
    ("Scope of exposure.",), (), RiskLevel.CRITICAL,
    question_context=QuestionContext("How can potential exposure be contained?", (
        DecisionUnknown("exposure-response", "Authorized containment response", DecisionRelevance.HIGH,
                        InformationSource.MANAGER, "Delay may increase customer harm.", True),
    )),
)
AUTHORIZATION_RESPONSES = {
    "immediate-escalation": ProfessionalResponse("immediate-escalation", "Immediate high-risk escalation",
        "Potential customer-data authorization exposure detected; initiating the incident path now.",
        immediate_escalation=True, delay_creates_risk=True, authority_limited=True,
        next_action="Initiate the security incident path and avoid unsafe experimentation."),
    "investigate-alone": ProfessionalResponse("investigate-alone", "Unsafe solo experimentation",
        "Alex experiments alone for hours before notifying anyone.", investigation_delay=180, delay_creates_risk=True,
        authority_limited=True),
}
