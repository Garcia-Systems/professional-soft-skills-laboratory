"""Chapter 14 authored requirements ambiguity scenarios.

The values extend the shared workplace scenario model.  They do not parse prose or
attempt to be a requirements-management system.
"""

from soft_skills_lab.domain.models import (
    AcceptanceCondition, AssumptionRecord, DecisionRelevance, Participant,
    ProfessionalResponse, RequirementAmbiguity, RequirementContext,
    RequirementContradiction, RequirementHistoryEvent, RequirementIssueKind,
    ResolutionSource, RiskLevel, WorkplaceScenario,
)

PARTICIPANTS = (
    Participant("Priya", "product manager"), Participant("Dana", "operations stakeholder"),
    Participant("Alex", "developer"), Participant("Jordan", "frontend developer"),
)

DATE_EVIDENCE = (
    'Requirement document: "Download should match what the member is viewing."',
    "The account UI defaults to 30 days but permits a selected range up to 90 days.",
)

TRANSACTION_CONTEXT = RequirementContext(
    requirement_id="transaction-export",
    stated_request="Let members download recent transaction history from the account page.",
    business_outcome="Members can use their account transaction records outside the application.",
    explicit_requirements=("The download is available to an authorized member from the account page.",),
    constraints=("Internal operational and risk metadata must not be exported.",
                 "The account report supports ranges no longer than 90 days.",
                 "A member may receive only that member's transactions."),
    ambiguities=(
        RequirementAmbiguity("Date range", 'What does "recent" select?', RequirementIssueKind.VAGUE,
            DecisionRelevance.RESOLVED, DATE_EVIDENCE,
            ("Fixed last 30 days", "Active selected range", "Any range up to 90 days"), False,
            ResolutionSource.EXISTING_CONTRACT,
            "Use the member's active report range, subject to the existing 90-day maximum."),
        RequirementAmbiguity("Export format", "No output format is specified.", RequirementIssueKind.INCOMPLETE,
            DecisionRelevance.HIGH,
            ("Spreadsheet use suggests structured data.", "Existing member statements are PDF; operations exports are CSV."),
            ("CSV", "XLSX", "PDF"), False),
        RequirementAmbiguity("Pending transactions", 'Does "transaction history" include pending items?',
            RequirementIssueKind.AMBIGUOUS, DecisionRelevance.BLOCKING,
            ("The page displays pending separately from posted transactions.", "Downstream accounting expectations are unknown."),
            ("Exclude", "Include with pending status", "Include identically to posted"), False),
        RequirementAmbiguity("Internal fields", "Whether internal metadata belongs in a member export.",
            RequirementIssueKind.AMBIGUOUS, DecisionRelevance.RESOLVED,
            ("Security policy prohibits member access to internal risk metadata.",),
            ("Visible member fields only", "Add internal operational metadata"), False,
            ResolutionSource.POLICY, "Only member-visible fields may be exported."),
        RequirementAmbiguity("Filename format", "Exact filename punctuation is unstated.", RequirementIssueKind.INCOMPLETE,
            DecisionRelevance.LOW, ("Existing downloads use date-stamped names.",),
            ("transactions-YYYY-MM-DD.csv", "A product-selected name"), True),
        RequirementAmbiguity("Button icon", "No icon is specified.", RequirementIssueKind.INCOMPLETE,
            DecisionRelevance.LOW, ("The application has an established download-button convention.",),
            ("Existing icon", "No icon", "A new icon"), True),
    ),
    contradictions=(RequirementContradiction("Date-range meaning",
        (("Request", "Recent transaction history"),
         ("Requirement document", "Download should match what the member is viewing."),
         ("UI behavior", "Member can view a default 30 days or select up to 90 days.")),
        "The 30-day UI default is not proof of a 30-day export limit.",
        "Use the active viewed date range, subject to the existing 90-day maximum.",
        ResolutionSource.EXISTING_CONTRACT),),
    defaults=("After CSV is selected, use the existing transactions-YYYY-MM-DD.csv filename convention unless product specifies otherwise.",),
    assumptions=(AssumptionRecord("Use the existing date-stamped filename convention.",
        "It is the established UI convention after CSV is selected.", "Presentation only", "Alex", True,
        "Product review before release", safe_default=True),),
    decisions=("Use the active viewed range up to 90 days.", "Export CSV.",
               "Include posted and pending transactions with explicit status.", "Exclude internal-only fields."),
    acceptance_conditions=(
        AcceptanceCondition("active-range", "Export uses the active member-selected date range.",
                            "Selecting January 1-31 yields only January 1-31 transactions."),
        AcceptanceCondition("range-limit", "Maximum supported range is 90 days.",
                            "A request over 90 days follows the existing report rejection or constraint behavior."),
        AcceptanceCondition("pending-status", "Pending and posted transactions are distinguished explicitly.",
                            "A pending row has status=pending."),
        AcceptanceCondition("visible-fields", "Only member-visible fields are exported.",
                            "The output schema contains no internal risk metadata."),
        AcceptanceCondition("authorization", "The existing authorization boundary remains unchanged.",
                            "Another member's transactions can never appear."),
        AcceptanceCondition("format", "Output format is CSV.", "The result is accepted by the CSV contract fixture."),
    ),
    evidence_sources=("Account-page behavior", "Existing requirement document", "Stakeholder spreadsheet-use note",
                      "Security policy", "Member statement and operations export conventions"),
    history=(
        RequirementHistoryEvent(0, "Request received."),
        RequirementHistoryEvent(1, "Active-range behavior resolved from existing evidence.", ResolutionSource.EXISTING_CONTRACT),
        RequirementHistoryEvent(1, "Internal-field constraint resolved from security policy.", ResolutionSource.POLICY),
        RequirementHistoryEvent(2, "Product selects CSV.", ResolutionSource.PRODUCT_DECISION),
        RequirementHistoryEvent(2, "Product selects pending-with-status.", ResolutionSource.PRODUCT_DECISION),
        RequirementHistoryEvent(3, "Acceptance conditions finalized.", ResolutionSource.PRODUCT_DECISION),
    ),
    safe_work_while_open=("Preserve the existing authorization boundary.", "Build the filtered transaction query.",
                          "Project member-visible fields only."),
)

TRANSACTION_EXPORT = WorkplaceScenario(
    "transaction-export", "Turning an ambiguous transaction export into a contract",
    "Alex must reduce ambiguity until the next responsible decision can be made without inventing product semantics.",
    PARTICIPANTS,
    ("The account page shows posted and pending transactions differently.", *DATE_EVIDENCE,
     "Members need records usable in spreadsheets.", "Security policy prohibits internal operational metadata."),
    ("Export format awaits a product decision.", "Pending-transaction semantics await a product decision."), (),
    RiskLevel.HIGH, requirement_context=TRANSACTION_CONTEXT,
)

RESPONSES = {
    "assume-everything": ProfessionalResponse("assume-everything", "Silent assumptions",
        "I'll build CSV with current filters, 90 days, pending rows, and visible fields.", assumptions=("CSV and pending included",),
        uses_existing_evidence=True),
    "literal-minimum": ProfessionalResponse("literal-minimum", "Default mistaken for requirement",
        "The screen defaults to 30 days, so the export will always contain 30 days.",
        creates_testable_acceptance_condition=True, exceeds_available_evidence=True),
    "block-on-everything": ProfessionalResponse("block-on-everything", "Question maximization",
        "I cannot begin until filename punctuation, icon, column order, seconds, quoting, format, and pending behavior are answered.",
        questions=(), records_visible_assumption=True, identifies_material_ambiguity=True, uses_existing_evidence=True,
        question_dump=True),
    "contradictory-pick": ProfessionalResponse("contradictory-pick", "Hidden conflict resolution",
        "I'll use the 30-day interpretation I prefer.", assumptions=("30 days controls",),
        creates_testable_acceptance_condition=True, exceeds_available_evidence=True),
    "assumption-as-fact": ProfessionalResponse("assumption-as-fact", "Assumption presented as fact",
        "Jordan, the export is CSV and includes pending transactions.", unsupported_claims=("CSV and pending were decided",),
        exceeds_available_evidence=True),
    "resolve-decision-relevant-ambiguity": ProfessionalResponse("resolve-decision-relevant-ambiguity",
        "Focused ambiguity reduction",
        "Evidence supports the active range up to 90 days, and policy excludes internal fields. Priya, please decide CSV versus XLSX/PDF and pending semantics. I will use our reversible filename convention and record the resulting acceptance checks.",
        identifies_material_ambiguity=True, distinguishes_low_value_detail=True, surfaces_contradiction=True,
        uses_existing_evidence=True, records_visible_assumption=True, uses_safe_default=True,
        requires_material_decision=True, creates_testable_acceptance_condition=True, updates_requirement_history=True,
        preserves_uncertainty=True, seeks_specific_understanding=True, respects_explicit_requirement=True,
        aligns_commitment_with_decision=True),
    "progressive-clarification": ProfessionalResponse("progressive-clarification", "Safe incremental progress",
        "While format and pending semantics await Priya, I can implement authorization, the active filtered query, and the member-visible projection. The filename convention is a visible reversible default; acceptance is finalized after those decisions.",
        identifies_material_ambiguity=True, distinguishes_low_value_detail=True, surfaces_contradiction=True,
        uses_existing_evidence=True, records_visible_assumption=True, uses_safe_default=True,
        requires_material_decision=True, creates_testable_acceptance_condition=True, updates_requirement_history=True,
        progresses_safely=True, preserves_uncertainty=True, seeks_specific_understanding=True,
        aligns_commitment_with_decision=True),
    "equivalent-focused": ProfessionalResponse("equivalent-focused", "Equivalent focused response",
        "We can proceed on authorization, filtered querying, and safe fields. Existing evidence resolves active range and policy resolves metadata; product still owns file type and pending meaning. Record the reversible filename default and testable outcomes.",
        identifies_material_ambiguity=True, distinguishes_low_value_detail=True, surfaces_contradiction=True,
        uses_existing_evidence=True, records_visible_assumption=True, uses_safe_default=True,
        requires_material_decision=True, creates_testable_acceptance_condition=True, updates_requirement_history=True,
        progresses_safely=True, preserves_uncertainty=True, seeks_specific_understanding=True,
        aligns_commitment_with_decision=True),
}


def context_scenario(scenario_id: str, title: str, request: str, ambiguities: tuple[RequirementAmbiguity, ...],
                     constraints: tuple[str, ...] = (), decisions: tuple[str, ...] = (),
                     assumptions: tuple[AssumptionRecord, ...] = (), history: tuple[RequirementHistoryEvent, ...] = ()) -> WorkplaceScenario:
    context = RequirementContext(scenario_id, request, request, (), constraints, ambiguities,
                                 assumptions=assumptions, decisions=decisions, history=history)
    response = ProfessionalResponse("classify", "Classify before deciding", "Classify material decisions, constraints, and deferrable details.",
        identifies_material_ambiguity=True, distinguishes_low_value_detail=True, preserves_uncertainty=True)
    return WorkplaceScenario(scenario_id, title, request, PARTICIPANTS, constraints, tuple(a.description for a in ambiguities if not a.is_resolved), (),
                             RiskLevel.MODERATE, requirement_context=context), {"classify": response}

NOTIFICATION = context_scenario("verification-notification", "Verification notification ambiguity",
    "Notify users when their verification is complete.", (
        RequirementAmbiguity("Channel", "Email, in-app, or SMS?", RequirementIssueKind.AMBIGUOUS, DecisionRelevance.HIGH, (), ("email", "in-app", "SMS"), False),
        RequirementAmbiguity("Outcome", "Success only or failure too?", RequirementIssueKind.INCOMPLETE, DecisionRelevance.HIGH, (), ("success", "success and failure"), False),
        RequirementAmbiguity("Timing", "Immediately or next login?", RequirementIssueKind.AMBIGUOUS, DecisionRelevance.MEDIUM, (), ("immediate", "next login"), True),
        RequirementAmbiguity("Content", "What personal data may it contain?", RequirementIssueKind.UNKNOWN, DecisionRelevance.RESOLVED, ("Privacy policy limits notification content.",), ("minimal status",), False, ResolutionSource.POLICY, "Use policy-approved minimal status."),
    ), ("Privacy policy limits notification content.",))

STAKEHOLDER_CONFLICT = context_scenario("contradictory-export-stakeholders", "A constraint resolves stakeholder conflict",
    "Dana asks for all fields; Priya asks for visible fields only.", (
        RequirementAmbiguity("Field set", "Stakeholder requests conflict.", RequirementIssueKind.CONTRADICTORY, DecisionRelevance.RESOLVED,
            ("Security policy prohibits internal risk metadata.",), ("all operational fields", "member-visible fields"), False,
            ResolutionSource.POLICY, "Member-visible fields only; policy removes the internal-fields option."),
    ), ("Internal risk metadata must never be exported to members.",), ("Export member-visible fields only.",))

RETRY = context_scenario("verification-retry", "Implementation-critical retry ambiguity",
    "Retry failed verification requests.", tuple(
        RequirementAmbiguity(subject, description, RequirementIssueKind.INCOMPLETE, relevance, evidence, options, False)
        for subject, description, relevance, evidence, options in (
            ("Retryable failures", "Which failures are safe to retry?", DecisionRelevance.BLOCKING, ("Duplicate external operations are possible.",), ("transient only", "all failures")),
            ("Trigger", "Automatic or user-triggered?", DecisionRelevance.HIGH, (), ("automatic", "user-triggered")),
            ("Retry policy", "Limit and backoff are unspecified.", DecisionRelevance.HIGH, (), ("bounded exponential", "fixed", "unbounded")),
            ("Idempotency", "Duplicate-operation behavior is unknown.", DecisionRelevance.BLOCKING, ("The provider performs an external operation.",), ("idempotency key", "no protection")),
        )))

SAFE_DEFAULT = context_scenario("download-button-default", "A safe reversible UI default", "Add a download button.", (
    RequirementAmbiguity("Label", "Exact label is missing.", RequirementIssueKind.INCOMPLETE, DecisionRelevance.LOW,
        ("Product selected CSV.", "Existing application convention is Download CSV."), ("Download CSV", "Download"), True,
        ResolutionSource.ESTABLISHED_CONVENTION, "Use Download CSV unless product specifies otherwise."),),
    decisions=("CSV is the selected format.",), assumptions=(AssumptionRecord("Use the Download CSV label.",
        "Established convention", "Low-risk presentation", "Alex", True, "Product review", safe_default=True),))

CHANGE = context_scenario("pending-requirement-change", "A later requirement change", "Pending transactions should not be included after all.", (),
    decisions=("Previously: include pending with explicit status.", "Now: exclude pending transactions."),
    history=(RequirementHistoryEvent(2, "Product selected pending-with-status.", ResolutionSource.PRODUCT_DECISION),
             RequirementHistoryEvent(4, "Product changed the accepted behavior to exclude pending; implementation, tests, scope, and commitment require updates.", ResolutionSource.PRODUCT_DECISION)))

REQUIREMENT_SCENARIOS = {
    TRANSACTION_EXPORT.scenario_id: (TRANSACTION_EXPORT, RESPONSES),
    NOTIFICATION[0].scenario_id: NOTIFICATION,
    STAKEHOLDER_CONFLICT[0].scenario_id: STAKEHOLDER_CONFLICT,
    RETRY[0].scenario_id: RETRY,
    SAFE_DEFAULT[0].scenario_id: SAFE_DEFAULT,
    CHANGE[0].scenario_id: CHANGE,
}
