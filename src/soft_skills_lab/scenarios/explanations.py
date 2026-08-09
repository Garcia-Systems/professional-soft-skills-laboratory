"""Chapter 4 deterministic technical realities and audience abstractions."""

from soft_skills_lab.domain.models import (
    CommunicationAudience, ExplanationContext, Participant, ProfessionalResponse, RiskLevel, WorkplaceScenario,
)

PAYMENT_FACTS = {
    "request": "Harbor sends payment authorization requests to an external provider.",
    "normal": "The provider normally responds within 2 seconds.",
    "timeout": "Some requests now exceed Harbor's 10-second timeout.",
    "unknown-state": "A timeout does not reveal whether the provider processed the request.",
    "duplicate-risk": "Retrying an uncertain request could create a duplicate payment attempt.",
    "success-unaffected": "Successful responses are unaffected.",
    "scope": "Approximately 8% of attempts during the incident have timed out.",
    "pause": "Engineering can temporarily disable new payment submissions.",
    "investigation": "Engineering is checking provider status and reconciling uncertain transactions.",
}

AUDIENCES = (
    CommunicationAudience("engineer", "engineer", "Works with request boundaries and transaction state",
        "Diagnose and recover safely", ("timeout", "unknown-state", "duplicate-risk", "investigation", "diagnostics")),
    CommunicationAudience("product-manager", "product manager", "Understands the workflow and product constraints",
        "Choose and communicate product mitigation", ("workflow", "impact", "scope", "unknown-state", "mitigation", "decision")),
    CommunicationAudience("business-operations", "business operations director", "Understands operations and customer risk",
        "Choose an operational risk control", ("impact", "duplicate-risk", "scope", "pause", "next-update")),
)

PAYMENT_LAYERS = (
    ("TECHNICAL FACTS", (PAYMENT_FACTS["normal"], PAYMENT_FACTS["timeout"], PAYMENT_FACTS["unknown-state"], PAYMENT_FACTS["success-unaffected"])),
    ("CUSTOMER IMPACT", ("Some customers may not receive immediate confirmation.", "Blind retry could create duplicate attempts.")),
    ("BUSINESS IMPACT", ("Approximately 8% of attempts are currently uncertain.", "Operations may choose to pause new submissions.")),
    ("ENGINEERING DETAIL", ("Request correlation IDs support reconciliation.", "Retry middleware is disabled for this operation.", "Transaction state is checked before replay.")),
    ("CURRENT UNKNOWNS", ("Root cause at the provider.", "Exact provider state for timed-out requests.", "Duration of the incident.")),
)

ARCHITECTURE_VIEWS = (
    ("engineer", ("Browser", "Harbor API", "Application Service", "External Verification Provider")),
    ("business-stakeholder", ("Member request", "Harbor", "verification partner", "Harbor result")),
)

PAYMENT_TIMEOUT = WorkplaceScenario(
    "payment-timeout", "Explaining a payment-provider timeout",
    "Dana asks Alex: “Why can't we just retry the failed payments?” The decision is whether to pause submissions while uncertain transactions are reconciled.",
    (Participant("Alex", "developer"), Participant("Priya", "product manager"),
     Participant("Morgan", "engineering manager"), Participant("Dana", "business operations director")),
    tuple(PAYMENT_FACTS.values()),
    ("Provider root cause.", "Provider state for each timed-out request.", "Incident duration."), (), RiskLevel.HIGH,
    explanation_context=ExplanationContext(AUDIENCES, PAYMENT_LAYERS, ARCHITECTURE_VIEWS),
)

def response(response_id: str, label: str, message: str, facts: tuple[str, ...], needs: tuple[str, ...], **kwargs: object) -> ProfessionalResponse:
    return ProfessionalResponse(response_id, label, message, communicated_fact_ids=facts,
                                communicated_need_ids=needs, **kwargs)

PAYMENT_RESPONSES = {
    "jargon-dump": response("jargon-dump", "Accurate implementation jargon dump",
        "The Guzzle client throws a timeout exception at 10 seconds; request IDs, workers, retry middleware, idempotency keys, and transaction tables govern replay.",
        ("timeout", "unknown-state", "duplicate-risk"), ("duplicate-risk",), preserves_uncertainty=True,
        implementation_details=("HTTP client", "exception class", "request IDs", "workers", "retry middleware", "idempotency keys", "database table")),
    "oversimplified": response("oversimplified", "Simple but inaccurate", "The payment provider is down, so retries don't work.",
        (), ("impact",), unsupported_claims=("The provider is down.",), communicates_impact=True),
    "false-certainty": response("false-certainty", "Impact stated with false certainty", "Retrying would charge customers twice.",
        ("duplicate-risk",), ("impact", "duplicate-risk"), unsupported_claims=("Every retry would charge a customer twice.",),
        communicates_impact=True, supports_decision=True),
    "technically-correct-no-impact": response("technically-correct-no-impact", "Correct timeout behavior without impact",
        "Some provider requests exceed our 10-second timeout, and their provider-side authorization state remains unknown.",
        ("timeout", "unknown-state"), ("unknown-state",), preserves_uncertainty=True),
    "decision-oriented": response("decision-oriented", "Decision-oriented explanation",
        "Some payment attempts are timing out, so we do not know whether the provider processed them. Retrying now could duplicate an attempt. Successful payments are unaffected; about 8% are uncertain. We are reconciling them, and operations can pause new submissions as a risk control while we investigate.",
        ("timeout", "unknown-state", "duplicate-risk", "success-unaffected", "scope", "pause", "investigation"),
        ("impact", "duplicate-risk", "scope", "pause", "next-update"), communicates_impact=True,
        communicates_scope=True, preserves_uncertainty=True, supports_decision=True, next_action="Reconcile uncertain transactions and report the next incident update."),
}

AUDIENCE_EXPLANATIONS = {
    "engineer": response("engineer", "Engineer view",
        "Authorization requests normally return within 2 seconds; affected calls cross the 10-second client boundary, leaving provider state unknown. Keep automatic retry disabled, correlate request IDs, and reconcile transaction state before replay while checking provider diagnostics.",
        ("normal", "timeout", "unknown-state", "duplicate-risk", "investigation"), AUDIENCES[0].information_needs,
        preserves_uncertainty=True, supports_decision=True, implementation_details=("client boundary", "request IDs", "transaction state")),
    "product-manager": response("product-manager", "Product manager view",
        "About 8% of payment attempts are not receiving confirmation; successful payments are unaffected. We cannot yet tell whether the provider processed each timed-out attempt, so blind retry risks duplicates. We are reconciling transactions and can pause submissions to reduce customer risk.",
        ("scope", "success-unaffected", "unknown-state", "duplicate-risk", "investigation", "pause"), AUDIENCES[1].information_needs,
        communicates_impact=True, communicates_scope=True, preserves_uncertainty=True, supports_decision=True),
    "business-operations": PAYMENT_RESPONSES["decision-oriented"],
}

MIGRATION = WorkplaceScenario(
    "database-migration", "Explaining a release migration",
    "A planned release needs a large-table migration. A product manager asks why it cannot run during business hours.",
    (Participant("Alex", "developer"), Participant("Priya", "product manager")),
    ("The migration can lock a large table and prevent normal writes for several minutes.",
     "The duration is an estimate, not a guarantee.", "A lower-traffic window reduces customer risk."),
    ("Exact lock duration under production load.",), (), RiskLevel.HIGH,
)
MIGRATION_RESPONSES = {
    "database-jargon": response("database-jargon", "Database jargon", "The DDL takes an ACCESS EXCLUSIVE lock while tuples and indexes are rewritten.", ("lock",), ()),
    "misleading-simplification": response("misleading-simplification", "Misleading simplification", "The database will be offline.", (), ("impact",), unsupported_claims=("The database will be offline.",)),
    "exaggerated-certainty": response("exaggerated-certainty", "Exaggerated certainty", "Writes will stop for exactly five minutes.", (), ("impact",), unsupported_claims=("The lock lasts exactly five minutes.",)),
    "decision-oriented": response("decision-oriented", "Decision-oriented migration explanation", "The change can temporarily prevent normal writes, which could interrupt the customer workflow. Several minutes is an estimate, not a guarantee. A lower-traffic deployment reduces that risk, so engineering recommends that window.", ("lock", "estimated-duration", "lower-traffic"), ("impact", "uncertainty", "decision"), communicates_impact=True, preserves_uncertainty=True, supports_decision=True),
}
