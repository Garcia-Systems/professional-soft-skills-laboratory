"""Chapter 9 decisions and authored disagreement behaviors."""

from soft_skills_lab.domain.models import (DecisionAlternative, DecisionContext, DecisionIssueKind, Participant,
    ProfessionalResponse, RiskLevel, WorkplaceScenario)

KEEP_EVIDENCE = (
    "Vendor field names changed across two API versions.",
    "The adapter translates vendor-specific statuses into Harbor domain values.",
    "Application services contain no vendor-specific payload parsing.",
    "Application tests use the adapter contract.",
)
REMOVAL_EVIDENCE = ("The adapter adds approximately 80 lines and another abstraction.", "The current vendor integration is small.")
ADAPTER_DECISION = DecisionContext(
    decision="Keep or remove the verification adapter.", owner="Morgan", contributors=("Alex",),
    shared_objective="Keep the verification integration simple, maintainable, and reliable.",
    alternatives=(DecisionAlternative("Remove the adapter", REMOVAL_EVIDENCE), DecisionAlternative("Keep the adapter boundary", KEEP_EVIDENCE)),
    constraints=("The application integrates with an external identity-verification vendor.",),
    unresolved_risks=("Less code now versus stronger isolation from vendor change.",), final_choice="Remove the adapter",
    rationale="Morgan accepts vendor coupling for lower ceremony now.",
)
ADAPTER_BOUNDARY = WorkplaceScenario("adapter-boundary", "Remove the verification adapter?",
    "Morgan calls the adapter unnecessary abstraction and asks Alex to call the vendor from the application service.",
    (Participant("Alex", "developer"), Participant("Morgan", "engineering manager")), KEEP_EVIDENCE + REMOVAL_EVIDENCE,
    ADAPTER_DECISION.unresolved_risks, (), RiskLevel.MODERATE, decision_context=ADAPTER_DECISION)

common = dict(captures_explicit_concern=True, identifies_shared_objective=True, states_specific_disagreement=True,
              decision_relevant_evidence=KEEP_EVIDENCE, constructive_alternative="Reduce adapter ceremony while retaining its contract boundary.",
              respects_decision_ownership=True)
RESPONSES = {
 "passive-agreement": ProfessionalResponse("passive-agreement", "Passive agreement", "Sure.", automatic_agreement=True),
 "flat-rejection": ProfessionalResponse("flat-rejection", "Flat rejection", "No, that's a bad idea.", states_specific_disagreement=True),
 "authority-challenge": ProfessionalResponse("authority-challenge", "Authority challenge", "You're the manager, but I've worked with more integrations than you have.", states_specific_disagreement=True, personalizes_disagreement=True),
 "defensive-ownership": ProfessionalResponse("defensive-ownership", "Defensive ownership", "I wrote that adapter for a reason. Removing it would undo my work.", captures_explicit_concern=True, states_specific_disagreement=True, personalizes_disagreement=True),
 "jargon-battle": ProfessionalResponse("jargon-battle", "Jargon battle", "Hexagonal architecture, ports and adapters, anti-corruption layers, inversion of control, and dependency inversion require it.", captures_explicit_concern=True, states_specific_disagreement=True, implementation_details=("Architecture terminology without a practical consequence.",)),
 "evidence-based-disagreement": ProfessionalResponse("evidence-based-disagreement", "Evidence-based disagreement", "I agree that abstractions should earn their complexity. I would retain this boundary because vendor fields have changed and it keeps vendor vocabulary out of application services. We can simplify its ceremony and inspect the next vendor change as a decision rule.", **common),
 "evidence-based-variation": ProfessionalResponse("evidence-based-variation", "Equivalent evidence-based wording", "Our shared aim is a simple, reliable integration. I recommend keeping the contract seam: tests use it and two API revisions renamed fields. Let's trim the wrapper rather than spread vendor parsing.", **common),
 "disagree-and-commit": ProfessionalResponse("disagree-and-commit", "Disagree and commit", "My evidence-based recommendation remains to keep the boundary. I understand Morgan owns and has made the acceptable tradeoff; I will document it and implement the direct integration.", **common),
}

DEADLINE = WorkplaceScenario("reporting-deadline", "Friday export validation tradeoff", "Priya asks Alex to skip automated tests to ship Friday.",
 (Participant("Priya", "product manager"), Participant("Alex", "developer")),
 ("The export includes customer data.", "Filtering rules are complex.", "Automated validation takes about one simulated day.", "Friday is commercially valuable."),
 ("Manual verification is less comprehensive.",), (), RiskLevel.HIGH,
 decision_context=DecisionContext("How to deliver the reporting export Friday.", "Priya", ("Alex",), "Deliver commercially useful reporting without exposing incorrect customer rows.",
 (DecisionAlternative("Skip automated tests", ("Preserves Friday scope.",)), DecisionAlternative("Ship CSV with automated validation", ("Preserves Friday date and validation by deferring Excel.",))), constraints=("New implementation",)))
DEADLINE_RESPONSES = {
 "silent-agreement": ProfessionalResponse("silent-agreement", "Silent agreement", "Okay."),
 "emotional-rejection": ProfessionalResponse("emotional-rejection", "Emotional rejection", "Absolutely not. That's reckless.", states_specific_disagreement=True, personalizes_disagreement=True),
 "absolutist": ProfessionalResponse("absolutist", "Absolutist rule", "We can never skip tests.", states_specific_disagreement=True),
 "scope-reduction": ProfessionalResponse("scope-reduction", "Evidence-based scope reduction", "Friday matters. Complex customer-data filters need validation, so ship CSV Friday and defer Excel.", captures_explicit_concern=True, identifies_shared_objective=True, states_specific_disagreement=True, decision_relevant_evidence=("Customer-data filtering is complex.",), constructive_alternative="Ship CSV Friday; defer Excel."),
}

PREFERENCE = WorkplaceScenario("code-review-preference", "Preference is not a defect", "Jordan proposes an equally valid implementation that differs from Alex's preferred style.",
 (Participant("Alex", "developer"), Participant("Jordan", "developer")), ("Both solutions are correct.",), (), (), RiskLevel.LOW,
 decision_context=DecisionContext("Choose between two valid implementations.", "Jordan", ("Alex",), "Keep the code correct and maintainable.", (DecisionAlternative("Jordan's style"), DecisionAlternative("Alex's style")), issue_kind=DecisionIssueKind.PREFERENCE))
PREFERENCE_RESPONSES = {"name-preference": ProfessionalResponse("name-preference", "Name the preference", "Both are valid; mine is a preference, not a defect.", captures_explicit_concern=True, identifies_shared_objective=True, distinguishes_preference_from_defect=True, constructive_alternative="Follow the repository convention."),
 "invent-defect": ProfessionalResponse("invent-defect", "Escalate preference", "My style is the correct one.", states_specific_disagreement=True)}

MANAGER_CORRECT = WorkplaceScenario("manager-correct", "Update a position after investigation", "Alex investigates and discovers Morgan's batching proposal uses fewer calls without added latency.",
 (Participant("Alex", "developer"), Participant("Morgan", "engineering manager")), ("The benchmark shows fewer calls and no added latency.",), (), (), RiskLevel.LOW,
 decision_context=DecisionContext("Use individual or batched requests.", "Morgan", ("Alex",), "Reduce calls without increasing latency.", (DecisionAlternative("Individual"), DecisionAlternative("Batched", ("Benchmark supports batching.",))), final_choice="Batched", rationale="New benchmark evidence."))
MANAGER_RESPONSES = {"update-position": ProfessionalResponse("update-position", "Update position", "The benchmark changes my view. Morgan's batching proposal is better; I withdraw my earlier objection.", captures_explicit_concern=True, identifies_shared_objective=True, decision_relevant_evidence=("Benchmark shows fewer calls without latency.",), respects_decision_ownership=True, updates_position_with_evidence=True)}

UNCERTAIN = WorkplaceScenario("cache-strategy", "Resolve incomplete evidence", "Both cache strategies are plausible and workload evidence is incomplete.",
 (Participant("Alex", "developer"), Participant("Morgan", "engineering manager")), (), ("Production workload is not measured.",), (), RiskLevel.MODERATE,
 decision_context=DecisionContext("Choose a cache strategy.", "Morgan", ("Alex",), "Improve latency without unacceptable invalidation risk.", (DecisionAlternative("Local cache"), DecisionAlternative("Shared cache")), unresolved_risks=("Workload evidence is incomplete.",)))
UNCERTAIN_RESPONSES = {"prototype": ProfessionalResponse("prototype", "Reversible experiment", "Both remain plausible. Let's time-box a benchmark and use a reversible prototype.", captures_explicit_concern=True, identifies_shared_objective=True, states_specific_disagreement=True, decision_relevant_evidence=("Workload evidence is incomplete.",), constructive_alternative="Time-box a benchmark and reversible prototype.", preserves_uncertainty=True)}

MATERIAL = WorkplaceScenario("sensitive-logging", "Sensitive logging boundary", "Morgan says to ship logging that would expose sensitive customer data and clean it up later.",
 (Participant("Alex", "developer"), Participant("Morgan", "engineering manager")), ("The proposed logs expose sensitive customer data.",), (), (), RiskLevel.CRITICAL,
 decision_context=DecisionContext("Ship sensitive logging.", "Morgan", ("Alex",), "Diagnose production safely.", (DecisionAlternative("Ship exposed data"), DecisionAlternative("Redact and use approved diagnostics")), issue_kind=DecisionIssueKind.MATERIAL_RISK, final_choice="Ship exposed data", reversible=False))
MATERIAL_RESPONSES = {"escalate": ProfessionalResponse("escalate", "Escalate material risk", "This exposes sensitive customer data, not an ordinary preference. I will not silently ship it; I am escalating through security and compliance.", captures_explicit_concern=True, identifies_shared_objective=True, states_specific_disagreement=True, decision_relevant_evidence=("Logs expose sensitive customer data.",), constructive_alternative="Redact fields and use approved diagnostics.", escalates_material_risk=True),
 "commit-anyway": ProfessionalResponse("commit-anyway", "Unsafe commit", "I disagree, but I'll ship it.", states_specific_disagreement=True, respects_decision_ownership=True)}
