"""Chapter 17 authored performance-plan scenarios and evidence history."""

from soft_skills_lab.domain.models import (
    BehavioralActionPlan, ImprovementPlan, MeasurementKind, Participant,
    PerformanceCheckpoint, PerformanceConcern, PerformanceMeasurement,
    PerformancePlanStatus, PlanHistoryEvent, ProfessionalResponse, RiskLevel,
    WorkplaceScenario,
)

RISK = PerformanceConcern(
    "risk-visibility", "communication", "Material risk is not always surfaced early enough.",
    ("T3: Alex discovered material schedule risk.", "T5: Morgan learned about the risk through Jordan."),
    ("Alex never communicates.",),
    "Communicate material schedule risk at the next reasonable visibility point.",
    "Dependent plans can discover risk indirectly before Morgan receives an update.",
    "Dependent planning can be surprised.", "Prior simulated work through T8",
    PerformanceMeasurement("Threshold-crossing risks are communicated before indirect discovery or commitment failure.", MeasurementKind.OBSERVABLE_BEHAVIOR, True),
)
HANDOFF = PerformanceConcern(
    "handoff-closure", "handoff", "Dependency handoffs are not consistently closed.",
    ("The API was ready before Jordan was explicitly notified.",), ("Alex cannot work independently.",),
    "Explicitly deliver and close material handoffs.", "Artifact readiness did not reach the dependent teammate explicitly.",
    "Dependent integration work can wait unnecessarily.", "Prior simulated work through T8",
    PerformanceMeasurement("Relevant handoff lifecycle reaches DELIVERED and ACKNOWLEDGED.", MeasurementKind.OBSERVABLE_BEHAVIOR, True),
)
STATUS = PerformanceConcern(
    "status-quality", "status", "Material status updates have not always supplied decision-ready visibility.",
    ("At T3 the status did not expose the known schedule risk.",), (),
    "Material updates identify state, risk, next action, and follow-up.", "Some updates omitted a material risk or follow-up.",
    "Morgan cannot make timely dependency decisions.", "Prior simulated work through T8",
    PerformanceMeasurement("Material updates contain state, risk, next action, and follow-up.", MeasurementKind.OBSERVABLE_BEHAVIOR, True),
)

CHECKPOINTS = (
    PerformanceCheckpoint(7, ("risk-visibility", "handoff-closure", "status-quality"),
        ("Two useful status updates were sent.", "One handoff reached ACKNOWLEDGED.", "No material risk event occurred."),
        ("Status quality improved.", "The handoff was explicitly closed."),
        ("Risk visibility has not yet been exercised under a material risk event.",),
        "This week looks better, but we haven't had a real risk event yet.",
        "The positive evidence is useful; risk behavior still needs a relevant event to be demonstrated.",
        ("Continue structured updates.", "Apply the visibility threshold when a material risk appears.")),
    PerformanceCheckpoint(14, ("risk-visibility", "handoff-closure", "status-quality"),
        ("A material risk appeared and Alex communicated it before indirect discovery.", "Alex corrected the next status update after feedback."),
        ("Risk visibility was demonstrated under relevant conditions.", "Feedback was applied at the next checkpoint."), (),
        "The risk escalation now provides stronger evidence of improvement.",
        "I will keep using the threshold and record the next examples.", ("Continue and assess consistency.")),
    PerformanceCheckpoint(21, ("risk-visibility", "handoff-closure", "status-quality"),
        ("Structured updates continued.", "A second handoff reached ACKNOWLEDGED."),
        ("The defined behavior continued across weeks.",), (), "The pattern is continuing.",
        "I will sustain it through Day 30.", ("Review the complete evidence pattern at Day 30.",)),
    PerformanceCheckpoint(30, ("risk-visibility", "handoff-closure", "status-quality"),
        ("One later handoff was missed after several weeks of demonstrated behavior.", "Earlier risk, status, and handoff evidence remains in history."),
        ("Improvement exists across multiple relevant events.",), ("One missed handoff requires follow-up and is not erased."),
        "Review the whole pattern rather than either one success or one failure.",
        "I acknowledge the missed handoff and will correct it; I also want the full period assessed against each criterion.",
        ("Record the miss.", "Determine plan outcome from the defined criteria and full history.")),
)

PLAN = ImprovementPlan(
    "communication-visibility", "Communication and visibility", "Alex", "Morgan", (RISK, HANDOFF, STATUS),
    (BehavioralActionPlan("Alex", "regular project update", "include state, risk, next action, and follow-up", "weekly checkpoint"),
     BehavioralActionPlan("Alex", "risk crosses the agreed material threshold", "notify Morgan outside the cadence when necessary"),
     BehavioralActionPlan("Alex", "an artifact blocks a teammate", "deliver it explicitly and seek acknowledgement")),
    CHECKPOINTS, 30, PerformancePlanStatus.ACTIVE,
    "Consistent evidence of the defined behaviors across the plan period.",
    ("Technical delivery completed at T8.", "Later incident communication was timely and accurate.",
     "Feedback repair occurred after initial defensiveness.", "Alex has improved when expectations are explicit."),
    ("Alex never communicates.", "Alex cannot work independently."),
    (PlanHistoryEvent(0, "concern defined", "Communication and visibility concern documented."),
     PlanHistoryEvent(0, "expectation clarified", "Risk, handoff, and status behaviors made observable."),
     PlanHistoryEvent(7, "checkpoint completed", "Positive status and handoff evidence; risk not exercised."),
     PlanHistoryEvent(14, "evidence recorded", "Material risk communicated early."),
     PlanHistoryEvent(14, "feedback applied", "Incomplete status pattern corrected."),
     PlanHistoryEvent(30, "evidence recorded", "One missed handoff preserved alongside prior improvement.")),
)

def _response(response_id: str, label: str, message: str, **values) -> ProfessionalResponse:
    return ProfessionalResponse(response_id, label, message, **values)

RESPONSES = {
    "panic-resignation": _response("panic-resignation", "Panic and assumed outcome", "If you're putting me on a PIP, you've already decided to fire me. There's no point."),
    "total-denial": _response("total-denial", "Technical-output denial", "This isn't fair. My work was delivered, so I don't have a performance problem."),
    "automatic-confession": _response("automatic-confession", "Automatic confession", "You're right about everything. I've been terrible at communication.", identifies_supported_performance_evidence=True, automatic_agreement=True),
    "argue-every-example": _response("argue-every-example", "Argue every example", "I dispute the dates, the wording, every example, and the whole history before discussing a plan.", identifies_supported_performance_evidence=True, premature_rebuttal=True),
    "vague-promise": _response("vague-promise", "Vague absolute promise", "I'll communicate more and make sure this never happens again.", identifies_supported_performance_evidence=True, clarifies_performance_expectation=True, unsupported_promise=True),
    "passive-signoff": _response("passive-signoff", "Passive signoff", "Okay. I'll sign it.", identifies_supported_performance_evidence=True),
    "clarify-and-plan": _response("clarify-and-plan", "Clarify evidence and plan", "I recognize the late risk and handoff examples. I do not agree that I never communicate. Can we define the threshold, measures, Day 7/14/21/30 reviews, actions, and successful completion? I will document any factual correction without rejecting the supported concern.", acknowledges_feedback=True, seeks_specific_understanding=True, acknowledges_supported_evidence=True, identifies_behavior_change=True, preserves_respectful_disagreement=True, identifies_supported_performance_evidence=True, corrects_material_inaccuracy=True, clarifies_performance_expectation=True, establishes_measurement=True, establishes_checkpoints=True, avoids_vague_improvement_promise=True, focuses_on_controllable_behavior=True, tracks_evidence_over_time=True, preserves_plan_scope=True),
    "execute-and-demonstrate": _response("execute-and-demonstrate", "Execute and demonstrate", "I surfaced the Day 14 risk early, closed the handoff, applied Morgan's status feedback at the next checkpoint, and recorded the complete evidence pattern.", acknowledges_supported_evidence=True, identifies_behavior_change=True, demonstrated_improvement=True, identifies_supported_performance_evidence=True, corrects_material_inaccuracy=True, clarifies_performance_expectation=True, establishes_measurement=True, establishes_checkpoints=True, avoids_vague_improvement_promise=True, focuses_on_controllable_behavior=True, tracks_evidence_over_time=True, preserves_plan_scope=True, demonstrates_plan_improvement=True, loop_closed=True, material_risk_communicated=True, handoff_explicit=True),
}

COMMUNICATION_VISIBILITY = WorkplaceScenario(
    "communication-visibility", "Formal communication improvement plan",
    "Morgan places Alex on a formal 30-day plan about status, risk escalation, and handoffs. The plan evaluates observable behavior; it neither predicts employment consequences nor settles unsupported claims.",
    (Participant("Alex", "developer"), Participant("Morgan", "engineering manager")),
    ("Alex discovered schedule risk at T3; Morgan learned at T5 through Jordan.", "An API handoff was ready before Jordan was notified.", "Alex repaired a defensive review exchange.", "Technical delivery completed at T8."),
    ("The eventual employment outcome is not established.", "Unsupported generalizations are not established."), (), RiskLevel.HIGH,
    performance_plan=PLAN,
)

def variant(scenario_id: str, title: str, description: str, facts: tuple[str, ...], response: ProfessionalResponse):
    return WorkplaceScenario(scenario_id, title, description, COMMUNICATION_VISIBILITY.participants, facts,
        ("Employment consequences are outside this laboratory.",), (), RiskLevel.HIGH, performance_plan=PLAN), {response.response_id: response}

VAGUE, VAGUE_RESPONSES = variant("vague-performance-plan", "Vague formal plan", "Morgan asks for ownership, urgency, and communication without examples or measurements.", (), _response("clarify-observable-plan", "Clarify vague plan", "Please provide examples, observable expectations, measures, and review points; I will document our understanding.", seeks_specific_understanding=True, clarifies_performance_expectation=True, establishes_measurement=True, establishes_checkpoints=True, avoids_vague_improvement_promise=True, focuses_on_controllable_behavior=True, preserves_plan_scope=True))
FACTUAL, FACTUAL_RESPONSES = variant("performance-factual-error", "Partly inaccurate plan", "The written plan says Alex missed T8, while the record says delivery occurred at T8; late risk visibility remains supported.", ("Delivery completed at T8.", "Schedule risk was surfaced late."), _response("correct-and-engage", "Correct fact and engage", "Delivery completed at T8. I agree risk was surfaced too late; please measure that behavior specifically.", acknowledges_supported_evidence=True, identifies_supported_performance_evidence=True, corrects_material_inaccuracy=True, clarifies_performance_expectation=True, establishes_measurement=True, avoids_vague_improvement_promise=True, focuses_on_controllable_behavior=True, preserves_plan_scope=True))
IMPOSSIBLE, IMPOSSIBLE_RESPONSES = variant("impossible-performance-expectation", "Outcome-only expectation", "The draft says no production incident may occur for 30 days, an outcome not fully controlled by Alex.", ("Incident occurrence has causes beyond one actor's behavior.",), _response("propose-controllable-measures", "Replace outcome-only metric", "I will complete required validation, surface known risk, and follow incident procedures; those are observable and reasonably within my control.", clarifies_performance_expectation=True, establishes_measurement=True, avoids_vague_improvement_promise=True, focuses_on_controllable_behavior=True))
CHANGING, CHANGING_RESPONSES = variant("changing-performance-scope", "New concern mid-plan", "At Day 14 Morgan raises an unrelated concern not in the written plan.", ("The original plan covers risk, status, and handoffs.",), _response("clarify-new-scope", "Preserve explicit scope", "I take the feedback seriously. Is it normal coaching, a new expectation, or formally added to this plan? Please record any formal scope change.", seeks_specific_understanding=True, preserves_plan_scope=True, establishes_checkpoints=True, avoids_vague_improvement_promise=True))
CAPACITY, CAPACITY_RESPONSES = variant("performance-plan-capacity", "Capacity issue during plan", "Alex experiences a personal capacity issue during the plan.", ("A plan is active.", "Capacity now affects a commitment."), _response("update-impact-and-plan", "Update work impact and plan", "My capacity affects this commitment. I am using the support process, revising dependencies and the checkpoint, and preserving the plan evidence accurately.", identifies_work_impact=True, requests_specific_support=True, revises_commitment_explicitly=True, updates_dependencies=True, tracks_evidence_over_time=True, preserves_plan_scope=True))
RATING, RATING_RESPONSES = variant("performance-rating-disagreement", "Checkpoint rating disagreement", "Morgan says improvement is insufficient; Alex believes the recorded evidence supports a different assessment.", ("The plan has explicit criteria.", "Multiple checkpoint events are recorded."), _response("review-criteria-and-continue", "Review criteria without effort-only argument", "Which defined criteria are not met? Let's review the specific evidence, document any unresolved disagreement, and continue the required behavior.", seeks_specific_understanding=True, identifies_supported_performance_evidence=True, establishes_measurement=True, establishes_checkpoints=True, avoids_vague_improvement_promise=True, tracks_evidence_over_time=True, preserves_plan_scope=True))

SCENARIOS = {COMMUNICATION_VISIBILITY.scenario_id: (COMMUNICATION_VISIBILITY, RESPONSES), VAGUE.scenario_id: (VAGUE, VAGUE_RESPONSES), FACTUAL.scenario_id: (FACTUAL, FACTUAL_RESPONSES), IMPOSSIBLE.scenario_id: (IMPOSSIBLE, IMPOSSIBLE_RESPONSES), CHANGING.scenario_id: (CHANGING, CHANGING_RESPONSES), CAPACITY.scenario_id: (CAPACITY, CAPACITY_RESPONSES), RATING.scenario_id: (RATING, RATING_RESPONSES)}
