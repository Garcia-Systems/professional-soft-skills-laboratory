"""Chapter 7 feedback scenarios and authored response semantics."""

from soft_skills_lab.domain.models import (
    BehavioralActionPlan, Commitment, FeedbackEvidence, FeedbackEvidenceStrength as Strength,
    Participant, ProfessionalFeedback, ProfessionalResponse, RiskLevel, WorkplaceScenario,
)


VISIBILITY_FEEDBACK = ProfessionalFeedback(
    source="Morgan", subject="Alex",
    claim="Project risk was not communicated early enough.",
    examples=("Morgan learned at T5 from Jordan that the deadline was at risk.",),
    observed_behavior=("Alex discovered vendor risk at T3.", "Morgan learned about the risk at T5.",
                       "Morgan learned through Jordan."),
    interpretation=("Morgan considers T5 too late for useful project visibility.",),
    expected_behavior=("Material delivery risk should be surfaced before the commitment fails.",),
    requested_change=("Communicate material risk when it becomes known, even while recovery remains likely.",),
    evidence=(
        FeedbackEvidence("Alex knew about the vendor risk at T3.", Strength.DIRECT_OBSERVATION),
        FeedbackEvidence("Morgan learned indirectly at T5.", Strength.SPECIFIC_EXAMPLE),
    ),
    important_context=("Alex believed recovery before T6 remained possible.", "The feature ultimately shipped at T6."),
    not_implied=("Alex is technically incompetent.", "The project failed.", "Alex intended to hide information."),
)

VISIBILITY_PLAN = BehavioralActionPlan(
    owner="Alex", trigger="A material delivery risk becomes known",
    behavior="Communicate it to Morgan at the next reasonable update point rather than waiting until failure appears likely.",
    follow_up="Confirm the working agreement with Morgan and apply it to the next material risk.",
)

PROJECT_VISIBILITY = WorkplaceScenario(
    "project-visibility", "Feedback about missed project visibility",
    "Morgan gives Alex feedback about visibility on an API integration. The integration shipped on time; the feedback concerns when material risk became visible.",
    (Participant("Morgan", "engineering manager"), Participant("Alex", "developer"), Participant("Jordan", "teammate")),
    ("Alex discovered vendor risk at T3.", "Alex did not tell Morgan at T3.", "Alex told Jordan informally at T4.",
     "By T5 the commitment was clearly at risk.", "Morgan learned at T5 from Jordan.",
     "Alex then provided a detailed update.", "The integration shipped at T6 and met its technical deadline."),
    ("Whether Morgan has other examples of inadequate visibility.",),
    (Commitment("Alex", "deliver the API integration", "T6"),), RiskLevel.MODERATE,
    feedback=VISIBILITY_FEEDBACK, action_plan=VISIBILITY_PLAN,
)

RESPONSES = {
    "immediate-defense": ProfessionalResponse(
        "immediate-defense", "Immediate defense", "But I finished it on time. I knew I could get it done, so there was no reason to worry everyone.",
        acknowledged_facts=("The integration shipped at T6.",), premature_rebuttal=True, context_provided=True,
        context_used_as_excuse=True,
    ),
    "blame-shift": ProfessionalResponse(
        "blame-shift", "Blame shift", "Jordan shouldn't have told you. I was handling it.",
        assigns_unsupported_blame=True, premature_rebuttal=True,
    ),
    "automatic-agreement": ProfessionalResponse(
        "automatic-agreement", "Automatic agreement", "You're completely right. My communication was terrible. It won't happen again.",
        acknowledges_feedback=True, automatic_agreement=True, responsibility_statement="My communication was terrible.",
        follow_up_commitment="It won't happen again.",
    ),
    "explanation-as-defense": ProfessionalResponse(
        "explanation-as-defense", "Explanation used as defense",
        "The vendor changed payloads, then tests failed, and I believed I could resolve every technical issue before T6, so withholding an update was reasonable.",
        context_provided=True, context_used_as_excuse=True, premature_rebuttal=True,
        acknowledges_supported_evidence=True,
    ),
    "silent-compliance": ProfessionalResponse(
        "silent-compliance", "Silent compliance", "Okay.", acknowledges_feedback=True,
    ),
    "understand-and-respond": ProfessionalResponse(
        "understand-and-respond", "Understand and respond",
        "I hear that you learned indirectly at T5 about a risk I knew at T3. Is the main concern visibility before T5, or were there other points where you needed an update? I thought recovery was likely, but that did not remove your need for the risk information. Next time I will surface material risk at the next reasonable update even if recovery looks likely, and I will confirm that threshold with you today.",
        acknowledged_facts=("Alex knew at T3.", "Morgan learned indirectly at T5."), acknowledges_feedback=True,
        seeks_specific_understanding=True, acknowledges_supported_evidence=True,
        responsibility_statement="My recovery judgment did not remove Morgan's need for visibility.",
        context_provided=True, identifies_behavior_change=True, next_action=VISIBILITY_PLAN.behavior,
        follow_up_commitment=VISIBILITY_PLAN.follow_up, captures_explicit_concern=True,
        distinguishes_fact_from_interpretation=True,
    ),
}

VAGUE_FEEDBACK = ProfessionalFeedback(
    "Morgan", "Alex", "Alex needs to be more proactive because Morgan always has to chase Alex.",
    ("Alex missed one status update.",), ("Alex missed one status update.",),
    ("Morgan interprets the missed update as insufficient proactivity.", "The word 'always' asserts a pattern."),
    ("Morgan expects status without having to request it.",), ("Clarify and meet an agreed update cadence.",),
    (FeedbackEvidence("One status update was missed.", Strength.SPECIFIC_EXAMPLE),
     FeedbackEvidence("Morgan always has to chase Alex.", Strength.GENERALIZATION_UNSUPPORTED)),
    ("Alex completed three other commitments with appropriate updates.",),
    ("Every commitment required chasing.",),
)
VAGUE_MANAGER_FEEDBACK = WorkplaceScenario(
    "vague-manager-feedback", "Vague and partly unsupported feedback",
    "Morgan says Alex must be more proactive and uses an unsupported 'always' generalization.",
    (Participant("Morgan", "engineering manager"), Participant("Alex", "developer")),
    ("Alex missed one status update.", "Alex completed three other commitments with appropriate updates."),
    ("Whether Morgan has other specific examples.", "What update cadence Morgan expects."), (), RiskLevel.LOW,
    feedback=VAGUE_FEEDBACK,
)
VAGUE_RESPONSES = {
    "clarify-without-capitulating": ProfessionalResponse(
        "clarify-without-capitulating", "Acknowledge the example and clarify the generalization",
        "I missed the last status update, and I understand that made you chase it. Are there other examples, and what cadence would make updates proactive? I don't currently see support for 'always,' but I want to address the specific expectation.",
        acknowledges_feedback=True, seeks_specific_understanding=True, acknowledges_supported_evidence=True,
        responsibility_statement="I missed the last status update.", preserves_respectful_disagreement=True,
        respectful_disagreement=True, identifies_behavior_change=True, next_action="Agree and use a status cadence.",
        captures_explicit_concern=True, distinguishes_fact_from_interpretation=True,
    ),
}

REVIEW_FEEDBACK = ProfessionalFeedback(
    "Reviewer", "Alex", "The implementation is too complicated; remove the adapter layer.", (),
    ("The implementation contains an adapter layer.",), ("The reviewer considers the layer excess complexity.",),
    ("Reduce avoidable complexity.",), ("Remove the adapter layer.",),
    (FeedbackEvidence("The adapter isolates the external vendor contract and tests rely on the boundary.", Strength.SPECIFIC_EXAMPLE),),
)
ADAPTER_REVIEW = WorkplaceScenario(
    "adapter-review", "Disagreeing after understanding code-review feedback",
    "A reviewer proposes removing an adapter; architectural evidence supports preserving the boundary.",
    (Participant("Reviewer", "code reviewer"), Participant("Alex", "developer")),
    ("The adapter isolates an external vendor contract.", "Tests rely on the boundary.",
     "Removing it couples application code directly to vendor payloads."), (), (), RiskLevel.LOW, feedback=REVIEW_FEEDBACK,
)
REVIEW_RESPONSES = {"evidence-based-disagreement": ProfessionalResponse(
    "evidence-based-disagreement", "Evidence-based disagreement",
    "I understand the concern is avoidable complexity. I disagree with removing the boundary because it isolates the vendor payload and our tests depend on it. I am open to simplifying the adapter while preserving that boundary.",
    acknowledges_feedback=True, seeks_specific_understanding=True, acknowledges_supported_evidence=True,
    preserves_respectful_disagreement=True, respectful_disagreement=True, context_provided=True,
    next_action="Explore a simpler adapter that preserves the vendor boundary.", identifies_behavior_change=True,
)}

FOLLOW_UP = WorkplaceScenario(
    "feedback-follow-up", "Later evidence of changed behavior",
    "Two weeks later Alex discovers another material dependency risk at T2, updates Morgan at T2, and follows up at T3.",
    (Participant("Morgan", "engineering manager"), Participant("Alex", "developer")),
    ("Feedback was received.", "The expected risk-update behavior was clarified.", "Risk was discovered at T2.",
     "Alex updated Morgan at T2.", "Alex named the dependency.", "Alex followed up at T3."), (), (), RiskLevel.MODERATE,
)
FOLLOW_UP_RESPONSES = {"demonstrated-change": ProfessionalResponse(
    "demonstrated-change", "Changed behavior demonstrated", "At T2 Alex reports the new dependency risk and promises a T3 follow-up; at T3 Alex sends it.",
    acknowledges_feedback=True, identifies_behavior_change=True, demonstrated_improvement=True,
    material_risk_communicated=True, dependency_acknowledged=True, loop_closed=True, communicated_at=2, follow_up_point=3,
)}

PRIMARY_RESPONSE_IDS = tuple(RESPONSES)

