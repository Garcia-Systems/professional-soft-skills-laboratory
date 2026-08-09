"""Chapter 13 stakeholder scenarios using the shared professional-behavior model."""

from soft_skills_lab.domain.models import (
    CommunicationAudience, DecisionAlternative, DecisionContext, DecisionIssueKind,
    ExplanationContext, Participant, ProfessionalResponse, RiskLevel, ScopeChange,
    StakeholderRequest, TradeoffOption, WorkplaceScenario,
)

PARTICIPANTS = (
    Participant("Priya", "product manager"), Participant("Dana", "business operations director"),
    Participant("Alex", "developer"),
)

REPORT_REQUEST = StakeholderRequest(
    requester="Dana",
    stated_request="Export the reporting screen to Excel by Friday.",
    business_outcome="Account managers need report data outside the application for next week's customer review.",
    deadline="Friday",
    constraints=("Report can contain up to 50,000 rows.", "Internal-only metadata must not be exposed.",
                 "Current filters should define the user's report context."),
    preferred_solution="Excel workbook.",
    requirements=("Users need a downloadable representation of the filtered report.",),
    acceptance_conditions=("Export uses active report filters.", "Only user-visible fields are included.",
                           "File opens in common spreadsheet tools.", "The agreed row limit is supported.",
                           "Deterministic validation passes."),
    open_questions=("Is Excel specifically required, or is spreadsheet-compatible output sufficient?",
                    "How much of the report must be available by Friday?",
                    "Is large-volume export required for the customer review?"),
    decision_owners=(("Dana", ("Business need", "Operational priority", "Whether CSV satisfies the workflow")),
                     ("Priya", ("Product scope", "Release tradeoff")),
                     ("Alex", ("Technical approach recommendation", "Feasibility evidence", "Technical risk")),
                     ("Morgan", ("Engineering risk above agreed thresholds",))),
    technical_evidence=("CSV can reuse existing streaming infrastructure.",
                        "CSV can likely be implemented and validated by Friday.",
                        "Native XLSX introduces a dependency and high-volume performance uncertainty."),
)

REPORT_OPTIONS = (
    TradeoffOption("csv-by-friday", "CSV by Friday", "External analysis before the review.",
                   "Available Friday with high relative confidence.", "Low relative implementation risk.",
                   ("Active filters", "Visible fields only", "Agreed row limit"),
                   ("External analysis", "Friday availability", "Current filters", "Visible fields only"),
                   ("Native workbook formatting and features",), "A later XLSX increment remains possible."),
    TradeoffOption("xlsx-by-friday", "Native XLSX by Friday", "Native workbook format immediately.",
                   "Friday is a target with lower delivery confidence.",
                   "New dependency and unvalidated memory/performance behavior at 50,000 rows.",
                   ("Native workbook", "Active filters", "Visible fields only"),
                   ("Native workbook format", "Friday target if implementation succeeds"),
                   ("No new dependency", "No performance uncertainty"), "Dependency choice is costly to reverse."),
    TradeoffOption("xlsx-next-iteration", "Native XLSX next iteration", "Validated native workbook format.",
                   "Misses Friday's preparation window.", "Lower after full volume validation.",
                   ("Native workbook", "Full volume validation", "Visible fields only"),
                   ("Native workbook format", "Full validation"), ("Friday availability",),
                   "Delivery can be stopped before dependency adoption."),
    TradeoffOption("reduced-xlsx-friday", "Reduced-volume XLSX by Friday", "Native format for a narrower workflow.",
                   "Friday may be feasible if the accepted row limit is reduced.", "Moderate; volume uncertainty is bounded.",
                   ("Native workbook", "Reduced agreed row limit", "Visible fields only"),
                   ("Native workbook format", "Friday target"), ("Full 50,000-row scope",),
                   "Row limit can be expanded after testing."),
)

REPORT_DECISION = DecisionContext(
    "Format and scope for Friday's reporting export", "Priya", ("Dana", "Alex"),
    "Give account managers usable report data before the customer review.",
    tuple(DecisionAlternative(o.description, (o.business_value, o.delivery_impact, o.technical_risk)) for o in REPORT_OPTIONS),
    REPORT_REQUEST.constraints, ("Whether native XLSX is required", "Validated high-volume XLSX behavior"),
    DecisionIssueKind.MATERIAL_RISK,
)

REPORTING_EXPORT = WorkplaceScenario(
    "reporting-export", "Reporting export request",
    "Dana requests Excel by Friday for a customer review; the request contains an outcome, preference, deadline, and reason.",
    PARTICIPANTS,
    ("Account managers need analysis outside the application.", "The customer review is next week.",
     "CSV reuses a streaming component.", "The report can contain 50,000 rows.",
     "Some stored fields are internal-only."),
    ("Whether native workbook behavior is required.", "The required row volume for this review."), (), RiskLevel.HIGH,
    explanation_context=ExplanationContext(
        (CommunicationAudience("dana", "business operations director", "Owns workflow context, not presumed technical ignorance.",
                               "Operational priority and whether an option serves the workflow.",
                               ("Outcome", "delivery confidence", "scope", "business consequences")),),
        (("Business decision layer", ("Outcome", "deadline", "options", "gains and losses")),
         ("Technical evidence layer", ("Streaming reuse", "dependency", "volume performance"))),
    ), decision_context=REPORT_DECISION, stakeholder_request=REPORT_REQUEST, tradeoff_options=REPORT_OPTIONS,
)

def response(response_id: str, label: str, message: str, **behavior: object) -> ProfessionalResponse:
    return ProfessionalResponse(response_id, label, message, **behavior)

REPORT_RESPONSES = {
    "literal-yes": response("literal-yes", "Literal yes", "Sure, I'll build Excel export by Friday.",
                            unsupported_promise=True, identifies_business_outcome=False),
    "technical-no": response("technical-no", "Technical no", "Excel is a bad format. We should use CSV.",
                              constructive_alternative="CSV", provides_professional_recommendation=True,
                              communicates_tradeoff=False, preserves_business_context=False),
    "jargon-rejection": response("jargon-rejection", "Jargon rejection",
        "XLSX is ZIP-packaged XML; worksheet DOM allocation, library transitive dependencies, streaming internals, and PHP memory limits make it wrong.",
        implementation_details=("ZIP container", "XML worksheets", "library dependency", "memory limits"),
        technical_risk_made_visible=True),
    "requirement-interrogation": response("requirement-interrogation", "Requirement interrogation",
        "Which Excel version? Formatting? Formulas? Tabs? Encoding? Row cap? Macros? Pivot tables? Refresh?",
        question_dump=True, seeks_specific_understanding=True),
    "silent-scope-reduction": response("silent-scope-reduction", "Silent scope reduction",
        "Alex decides CSV is close enough and ships it without telling Dana or Priya.",
        identifies_business_outcome=True, separates_outcome_from_solution=True, communicates_tradeoff=True,
        respects_explicit_requirement=False, preserves_business_context=True),
    "outcome-first-tradeoff": response("outcome-first-tradeoff", "Outcome-first tradeoff",
        "You need filtered, user-visible report data outside the system before the review. Is native workbook behavior required? CSV by Friday has lower delivery risk; XLSX needs dependency and volume testing. We could instead deliver XLSX later or a reduced-volume XLSX Friday. Dana, can CSV serve the workflow, and Priya, which release scope should we select?",
        identifies_business_outcome=True, separates_outcome_from_solution=True, seeks_specific_understanding=True,
        communicates_tradeoff=True, communicates_scope=True, preserves_business_context=True,
        technical_risk_made_visible=True, supports_decision=True, respects_decision_ownership=True,
        respects_explicit_requirement=True),
    "recommendation-with-decision": response("recommendation-with-decision", "Recommendation with decision",
        "Because the immediate goal is analysis before next week's review, I recommend filtered, visible-fields-only CSV by Friday. It opens in spreadsheet tools, reuses our streaming path, and avoids an unvalidated high-volume dependency. If native workbook features matter, schedule validated XLSX next; Dana can confirm workflow fit and Priya can choose release scope before I commit.",
        identifies_business_outcome=True, separates_outcome_from_solution=True, seeks_specific_understanding=True,
        communicates_tradeoff=True, communicates_scope=True, preserves_business_context=True,
        technical_risk_made_visible=True, supports_decision=True, respects_decision_ownership=True,
        provides_professional_recommendation=True, recommendation_provided=True,
        aligns_commitment_with_decision=True, respects_explicit_requirement=True),
    "equivalent-recommendation": response("equivalent-recommendation", "Equivalent recommendation",
        "For preparation next week, my recommendation is the filtered safe columns as CSV on Friday; that is our proven path. A native workbook needs volume validation. Please confirm spreadsheet-compatible output meets operations' need, then Priya can approve that scope and we will record the commitment.",
        identifies_business_outcome=True, separates_outcome_from_solution=True, seeks_specific_understanding=True,
        communicates_tradeoff=True, communicates_scope=True, preserves_business_context=True,
        technical_risk_made_visible=True, supports_decision=True, respects_decision_ownership=True,
        provides_professional_recommendation=True, recommendation_provided=True,
        aligns_commitment_with_decision=True, respects_explicit_requirement=True),
}

def small(sid: str, title: str, request: StakeholderRequest, facts: tuple[str, ...], responses: dict[str, ProfessionalResponse],
          *, options: tuple[TradeoffOption, ...] = (), scope_change: ScopeChange | None = None) -> tuple[WorkplaceScenario, dict[str, ProfessionalResponse]]:
    return WorkplaceScenario(sid, title, request.stated_request, PARTICIPANTS, facts, request.open_questions, (), RiskLevel.HIGH,
                             stakeholder_request=request, tradeoff_options=options, scope_change=scope_change), responses

SEARCH_REQUEST = StakeholderRequest("Dana", "Search is too slow. We need it under one second.",
    "Prevent customers waiting unacceptably during search.", None, ("Large date ranges are slow.",), "Every search under one second.",
    ("An agreed user workflow meets an agreed latency percentile.",), ("Target workflow and percentile are agreed.",),
    ("Which workflow matters?", "Which percentile does the target apply to: median, p95, or every request?"),
    (("Dana", ("Important customer experience",)), ("Alex", ("Measurement and implementation",))),
    ("Median is 700 ms.", "p95 is 3.8 seconds.", "Large date ranges dominate slow requests."))
SEARCH, SEARCH_RESPONSES = small("stakeholder-search-performance", "Clarify experienced performance pain", SEARCH_REQUEST,
    SEARCH_REQUEST.technical_evidence, {
    "already-meets": response("already-meets", "Literal metric defense", "Median is already below one second.", preserves_business_context=False),
    "redis": response("redis", "Solution jump", "We need Redis.", separates_outcome_from_solution=False),
    "unrealistic": response("unrealistic", "Reflexive rejection", "One second is unrealistic.", preserves_business_context=False),
    "clarify-experience": response("clarify-experience", "Clarify user experience", "I see the customer wait. Normal searches have a 700 ms median, while p95 is 3.8 seconds and large ranges are slow. Which workflow and percentile must meet one second? Then I can recommend an approach.", identifies_business_outcome=True, separates_outcome_from_solution=True, seeks_specific_understanding=True, preserves_business_context=True, technical_risk_made_visible=True, provides_professional_recommendation=True),
})

UPLOAD_REQUEST = StakeholderRequest("Priya", "Sales needs bulk customer upload this week or we might lose a deal.",
    "Preserve an important sales opportunity by loading customer data this week.", "This week", ("Security and validation cannot be bypassed.",),
    "Reusable bulk-upload UI.", ("Required customer records are loaded safely.",), ("Agreed volume imports with validation and authorization.",),
    ("How important is the deal?", "What is the minimum workflow and volume?", "Could controlled operational support serve once?"),
    (("Priya", ("Deal and product priority", "Product scope")), ("Alex", ("Safe implementation options",))))
UPLOAD_OPTIONS = (TradeoffOption("controlled-import", "Controlled one-time import", "May serve this deal this week.",
    "Does not deliver reusable UI.", "Requires reviewed validation, authorization, audit, and operational ownership.",
    ("One approved dataset", "Controlled execution"), ("Immediate safe data load",), ("Reusable self-service workflow",),
    "Does not prevent later product work."),)
UPLOAD, UPLOAD_RESPONSES = small("urgent-bulk-upload", "Urgent feature request", UPLOAD_REQUEST, (), {
    "controlled-option": response("controlled-option", "Controlled option, not automatic workaround", "Let's confirm deal value, minimum volume, validation, and security. A reviewed one-time import might serve this deal while we design reusable upload, but Priya should choose after seeing both options.", identifies_business_outcome=True, separates_outcome_from_solution=True, communicates_tradeoff=True, preserves_business_context=True, respects_decision_ownership=True, provides_professional_recommendation=True),
}, options=UPLOAD_OPTIONS)

SCOPE = ScopeChange(("Filtered visible-field export by Friday",), "Scheduled email delivery",
    "Scheduling adds delivery, authorization, failure-handling, and operational work to the Friday commitment.",
    ("Keep Friday export and defer scheduling", "Move the deadline", "Reduce other scope"))
SCOPE_REQUEST = StakeholderRequest("Dana", "Can we also include scheduled email delivery? It should be quick.",
    "Reduce manual report delivery.", "Friday", (), "Scheduled email", ("A schedule delivers an authorized export reliably.",), (), (),
    (("Dana", ("Business value",)), ("Priya", ("Scope tradeoff",)), ("Alex", ("Impact evidence",))))
SCOPE_SCENARIO, SCOPE_RESPONSES = small("export-scope-change", "Stakeholder changes scope", SCOPE_REQUEST, (), {
    "sure": response("sure", "Automatic yes", "Sure.", unsupported_promise=True),
    "scope-creep": response("scope-creep", "Weaponized scope label", "That's scope creep.", preserves_business_context=False),
    "explicit-options": response("explicit-options", "Explicit scope tradeoff", "Scheduled delivery could reduce manual work. It is new scope and adds authorization, scheduling, and failure handling, so it changes Friday confidence. We can keep Friday export and defer it, move the date, or reduce other scope; Priya should select the release tradeoff.", identifies_business_outcome=True, communicates_tradeoff=True, makes_scope_change_explicit=True, preserves_business_context=True, respects_decision_ownership=True, technical_risk_made_visible=True),
}, scope_change=SCOPE)

SECURITY_REQUEST = StakeholderRequest("Dana", "Include the internal risk field in the export.", "Support account review decisions.", None,
    ("Internal risk metadata is not authorized for the requesting user role.",), "Export internal risk metadata.",
    ("Users receive decision-useful, authorized data.",), ("No internal-only field is exposed.",), (),
    (("Dana", ("Business need",)), ("Alex", ("Security constraint and safe alternatives",))))
SECURITY, SECURITY_RESPONSES = small("export-security-constraint", "Explain an engineering constraint", SECURITY_REQUEST, (), {
    "mysterious-authority": response("mysterious-authority", "Mysterious authority", "Security won't allow it."),
    "safe-alternative": response("safe-alternative", "Decision-relevant constraint", "That field contains internal risk metadata this user role is not authorized to receive. I cannot expose it, but we can provide the authorized customer-status field if that supports the review decision.", identifies_business_outcome=True, respects_explicit_requirement=True, communicates_tradeoff=True, preserves_business_context=True, technical_risk_made_visible=True),
})

XLSX_REQUIRED = StakeholderRequest("Dana", "The customer workbook is uploaded into a system that accepts only .xlsx.",
    "Produce a file accepted by the customer's downstream system.", "Friday", ("Downstream system accepts only .xlsx.",),
    "Native XLSX", ("Delivered file is .xlsx and accepted by the downstream system.",),
    ("Validated file is accepted by the downstream system.",), (),
    (("Dana", ("Downstream workflow evidence",)), ("Alex", ("Updated technical recommendation",)), ("Priya", ("Scope and date",))))
NEW_EVIDENCE, NEW_EVIDENCE_RESPONSES = small("xlsx-required", "New business evidence changes recommendation", XLSX_REQUIRED, (), {
    "update-recommendation": response("update-recommendation", "Update with evidence", "That makes .xlsx an acceptance requirement, so CSV no longer meets the outcome. I withdraw that recommendation. We should choose between reduced-volume XLSX Friday and validated full-volume XLSX later.", identifies_business_outcome=True, separates_outcome_from_solution=True, respects_explicit_requirement=True, communicates_tradeoff=True, updates_position_with_evidence=True, provides_professional_recommendation=True, preserves_business_context=True),
})

IMPOSSIBLE_REQUEST = StakeholderRequest("Dana", "Deliver full XLSX, 50,000 rows, Friday, with no new dependency and no performance risk.",
    "Prepare complete native workbooks by Friday.", "Friday", ("Full XLSX", "50,000 rows", "No new dependencies", "No performance risk"),
    "Full XLSX", ("All stated properties hold.",), (), ("Which constraint can move?",),
    (("Dana", ("Operational priority",)), ("Priya", ("Scope/date tradeoff",)), ("Alex", ("Feasibility evidence",))))
IMPOSSIBLE, IMPOSSIBLE_RESPONSES = small("impossible-export-constraints", "Impossible constraint combination", IMPOSSIBLE_REQUEST, (), {
    "fake-promise": response("fake-promise", "Invented commitment", "Yes, all of that will be ready Friday.", unsupported_promise=True),
    "surface-conflict": response("surface-conflict", "Surface incompatible constraints", "Those constraints cannot all hold: native XLSX needs a dependency, and 50,000-row behavior is not yet validated as risk-free by Friday. I cannot make that commitment. We need a priority choice: format, volume, date, or risk/dependency constraint must move.", identifies_business_outcome=True, communicates_tradeoff=True, technical_risk_made_visible=True, respects_decision_ownership=True, aligns_commitment_with_decision=True, preserves_uncertainty=True),
})

STAKEHOLDER_SCENARIOS = {s.scenario_id: (s, responses) for s, responses in (
    (REPORTING_EXPORT, REPORT_RESPONSES), (SEARCH, SEARCH_RESPONSES), (UPLOAD, UPLOAD_RESPONSES),
    (SCOPE_SCENARIO, SCOPE_RESPONSES), (SECURITY, SECURITY_RESPONSES),
    (NEW_EVIDENCE, NEW_EVIDENCE_RESPONSES), (IMPOSSIBLE, IMPOSSIBLE_RESPONSES),
)}
