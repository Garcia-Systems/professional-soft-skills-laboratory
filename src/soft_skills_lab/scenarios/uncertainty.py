"""Deterministic Chapter 6 scenarios: uncertainty remains part of the shared model."""

from soft_skills_lab.domain.models import (
    CommunicationAudience, EvidenceContext, ExplanationContext, Hypothesis, Participant,
    ProfessionalResponse, RiskLevel, Uncertainty, UncertaintyKind, WorkplaceScenario,
)

FACTS = (
    "14 of 1,200 profile updates failed.",
    "Failures began after yesterday's Harbor release.",
    "Failed requests contain downstream identity-service timeout evidence.",
    "Database writes are completing normally.",
    "The external identity service also changed yesterday.",
)
MISSING = (
    "The failure has not been reproduced in a controlled environment.",
    "Two systems changed in the same window.",
    "No controlled comparison has isolated the cause.",
)
HYPOTHESES = (
    Hypothesis("harbor-regression", "Harbor's release introduced a regression.", (FACTS[1],)),
    Hypothesis("identity-change", "The identity-service change introduced the failures.", (FACTS[2], FACTS[4])),
    Hypothesis("interaction", "An interaction between the two changes causes the failures.", (FACTS[1], FACTS[4])),
)
PROFILE_UNCERTAINTY = Uncertainty(
    subject="Was Harbor's release responsible?", kind=UncertaintyKind.UNKNOWN,
    current_evidence=FACTS[1:], missing_evidence=MISSING,
    current_hypotheses=tuple(item.statement for item in HYPOTHESES),
    decision_impact="Do not choose a rollback solely from current causal evidence.",
    next_investigation_steps=("Compare request traces before and after the release.",
                              "Reproduce the failure in a controlled environment.",
                              "Test a rollback or controlled comparison if evidence remains inconclusive."),
    expected_update_point=4,
)
PROFILE_FAILURE = WorkplaceScenario(
    "profile-update-failure", "Intermittent production profile-update failure",
    "At T2 Morgan asks Alex whether Harbor's release caused an intermittent production failure; the cause is not known.",
    (Participant("Alex", "developer"), Participant("Morgan", "engineering manager"),
     Participant("Dana", "business operations director")), FACTS,
    ("Root cause is unknown.", "The failure cannot yet be reproduced locally.",
     "Current evidence cannot distinguish Harbor's release from the identity-service change."), (), RiskLevel.HIGH,
    evidence_context=EvidenceContext(FACTS, HYPOTHESES,
        ("Root cause.", "Whether rollback removes the failures.",
         "Whether every failed request shares the same mechanism."), PROFILE_UNCERTAINTY),
)

PROFILE_RESPONSES = {
    "bluff": ProfessionalResponse("bluff", "Bluff", "Yes, our deployment caused it.",
        exceeds_available_evidence=True, claims_cause_without_evidence=True),
    "defensive-certainty": ProfessionalResponse("defensive-certainty", "Defensive certainty",
        "No. Our code is fine. The external service is causing it.", exceeds_available_evidence=True,
        claims_cause_without_evidence=True, assigns_unsupported_blame=True,
        offered_hypothesis=HYPOTHESES[1].statement),
    "empty-unknown": ProfessionalResponse("empty-unknown", "Truthful but empty unknown", "I don't know.",
        states_uncertainty_explicitly=True, preserves_uncertainty=True),
    "speculative-answer": ProfessionalResponse("speculative-answer", "Unlabeled speculation",
        "It's probably their fault.", offered_hypothesis=HYPOTHESES[1].statement,
        assigns_unsupported_blame=True, exceeds_available_evidence=True),
    "bounded-hypothesis": ProfessionalResponse("bounded-hypothesis", "Labeled bounded hypothesis",
        "My current hypothesis is the external-service path because failures are downstream timeouts, but we cannot rule out our release.",
        states_uncertainty_explicitly=True, preserves_uncertainty=True,
        offered_hypothesis=HYPOTHESES[1].statement, hypothesis_labeled=True,
        evidence_basis=(FACTS[2],), missing_evidence_identified=(MISSING[2],)),
    "investigation-dump": ProfessionalResponse("investigation-dump", "Investigation dump",
        "There were 1,200 requests, 14 failures, timeout spans, normal writes, two deploys, and no local reproduction.",
        acknowledged_facts=FACTS, evidence_basis=FACTS, implementation_details=FACTS),
    "bounded-uncertainty": ProfessionalResponse("bounded-uncertainty", "Bounded uncertainty",
        "We don't know yet whether our release caused this. It remains plausible because failures began afterward. "
        "The failures show identity-service timeouts, writes are normal, and that service also changed. I am comparing "
        "traces; I will update at T4 and, if needed, propose a rollback comparison.",
        acknowledged_facts=FACTS[1:], states_uncertainty_explicitly=True, preserves_uncertainty=True,
        offered_hypothesis=HYPOTHESES[0].statement, hypothesis_labeled=True,
        evidence_basis=FACTS[1:], missing_evidence_identified=MISSING,
        uncertainty_next_action=PROFILE_UNCERTAINTY.next_investigation_steps[0], next_action=PROFILE_UNCERTAINTY.next_investigation_steps[0],
        follow_up_point=4, follow_up_commitment="Update at T4.", decision_impact=PROFILE_UNCERTAINTY.decision_impact),
}

ESTIMATE = WorkplaceScenario(
    "profile-fix-estimate", "Estimate before root cause", "Morgan asks how long the fix will take before reproduction or root cause.",
    (Participant("Alex", "developer"), Participant("Morgan", "engineering manager")),
    ("The failure is confirmed.",), ("Root cause is unknown.", "Multiple causes remain plausible."), (), RiskLevel.HIGH,
    evidence_context=EvidenceContext(("The failure is confirmed.",), HYPOTHESES,
        ("Root cause.", "Reliable final-delivery estimate."),
        Uncertainty("How long will the fix take?", UncertaintyKind.UNKNOWABLE_FROM_CURRENT_EVIDENCE,
                    missing_evidence=("The failure has not been reproduced.",),
                    next_investigation_steps=("Investigate reproduction through T3.",), expected_update_point=3)),
)
ESTIMATE_RESPONSES = {
    "false-estimate": ProfessionalResponse("false-estimate", "Unsupported final estimate", "Two hours.",
        exceeds_available_evidence=True, unsupported_promise=True, estimate_for="final-delivery"),
    "refusal": ProfessionalResponse("refusal", "Refusal to engage", "I have no idea.", states_uncertainty_explicitly=True),
    "broad-range": ProfessionalResponse("broad-range", "Decision-useless broad range", "Somewhere between an hour and a week.", estimate_for="final-delivery"),
    "learning-point": ProfessionalResponse("learning-point", "Estimate for the learning point",
        "I cannot give a reliable fix estimate until I reproduce it. I expect that investigation through T3; then I will estimate the fix or explain what still prevents one.",
        states_uncertainty_explicitly=True, preserves_uncertainty=True,
        missing_evidence_identified=("The failure has not been reproduced.",),
        uncertainty_next_action="Reproduce the failure.", follow_up_point=3, estimate_for="learning-point"),
}

JUDGMENT = WorkplaceScenario(
    "judgment-under-pressure", "Bounded judgment under pressure", "Morgan asks what Alex thinks despite unresolved cause.",
    (Participant("Alex", "developer"), Participant("Morgan", "engineering manager")), FACTS, ("Root cause is unknown.",), (), RiskLevel.HIGH,
    evidence_context=EvidenceContext(FACTS, HYPOTHESES, ("Root cause.",),
        Uncertainty("Which cause is currently more plausible?", UncertaintyKind.UNCERTAIN,
            current_evidence=(FACTS[2], FACTS[4]), missing_evidence=MISSING,
            current_hypotheses=(HYPOTHESES[1].statement,),
            decision_impact="Do not decide rollback from timeout evidence alone.",
            next_investigation_steps=("Compare request traces.",), expected_update_point=4)),
)
JUDGMENT_RESPONSES = {"bounded-judgment": ProfessionalResponse("bounded-judgment", "Bounded professional judgment",
    "Based on timeout evidence, the external-service path is the stronger hypothesis, but I would not make a rollback decision on that alone.",
    states_uncertainty_explicitly=True, preserves_uncertainty=True, offered_hypothesis=HYPOTHESES[1].statement,
    hypothesis_labeled=True, evidence_basis=(FACTS[2],), decision_impact="Do not decide rollback from this evidence alone.")}

MIGRATION_SAFETY = WorkplaceScenario(
    "migration-safety-unknown", "Junior developer asked about migration safety", "Senior manager asks junior Alex if an uninspected migration is safe.",
    (Participant("Alex", "junior developer"), Participant("Morgan", "senior engineering manager")),
    ("Alex has not inspected the migration.",), ("Locking behavior and staging timing are not known."), (), RiskLevel.HIGH,
    evidence_context=EvidenceContext(("Alex has not inspected the migration.",), not_yet_established=("Migration safety.",),
        uncertainty=Uncertainty("Is this database migration safe?", UncertaintyKind.NOT_YET_INVESTIGATED,
            missing_evidence=("Locking behavior has not been reviewed.",),
            next_investigation_steps=("Check the execution plan and staging timing.",))),
)
MIGRATION_SAFETY_RESPONSES = {"inspect-first": ProfessionalResponse("inspect-first", "Inspect before answering",
    "I haven't reviewed locking yet, so I can't say it is safe. I'll check the execution plan and staging timing first.",
    states_uncertainty_explicitly=True, preserves_uncertainty=True,
    missing_evidence_identified=("Locking behavior has not been reviewed.",), uncertainty_next_action="Check execution plan and staging timing.")}

CUSTOMER_PAYMENT = WorkplaceScenario(
    "customer-payment-verification", "Customer-safe payment uncertainty", "A customer asks whether a timed-out payment was lost.",
    (Participant("Alex", "support engineer"), Participant("Customer", "customer")),
    ("The payment request timed out.",), ("The processor's final payment status is unknown.",), (), RiskLevel.HIGH,
    explanation_context=ExplanationContext((CommunicationAudience("customer", "customer", "no internal system context",
        "avoid duplicate charge", ("safe immediate action", "verification status", "next update")),), ()),
    evidence_context=EvidenceContext(("The payment request timed out.",), not_yet_established=("Whether payment completed.",),
        uncertainty=Uncertainty("Did you lose my payment?", UncertaintyKind.UNKNOWABLE_FROM_CURRENT_EVIDENCE,
            missing_evidence=("Processor confirmation is not available yet.",),
            next_investigation_steps=("Check with the payment processor.",), expected_update_point=3)),
)
CUSTOMER_PAYMENT_RESPONSES = {"customer-safe": ProfessionalResponse("customer-safe", "Customer-safe verification",
    "We are verifying the payment with the processor. Please do not retry yet; we will update you at T3.",
    states_uncertainty_explicitly=True, preserves_uncertainty=True,
    communicated_fact_ids=("payment-status-unconfirmed",), uncertainty_next_action="Check with the processor.",
    follow_up_point=3, decision_impact="Customer should not retry yet.", communicates_impact=True, supports_decision=True)}
