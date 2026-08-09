"""Chapter 16 scenarios: observable work impact and proportionate boundaries."""

from soft_skills_lab.domain.models import (
    Commitment, CommitmentRevision, Participant, ProfessionalResponse, RiskLevel,
    WorkCapacity, WorkImpactContext, WorkplaceScenario,
)

PEOPLE = (Participant("Alex", "developer"), Participant("Morgan", "engineering manager"),
          Participant("Jordan", "dependent teammate"))

REVISION = CommitmentRevision(
    "Verification integration at T8", "capacity change", "Final review at T9",
    ("Jordan's T8 integration",), "Requested from Morgan; decision pending", "T6",
)
PRIMARY_IMPACT = WorkImpactContext(
    "Alex", "Verification integration at T8",
    ("Internal test checkpoint missed.", "Remaining validation incomplete.", "Delivery confidence reduced."),
    "T4", WorkCapacity.REDUCED,
    ("Exact nature of Alex's personal situation.", "Family or relationship details.",
     "Medical or other sensitive details not needed for the work decision."),
    ("Current capacity is reduced.", "Verification delivery is at risk.",
     "Jordan depends on the T8 handoff.", "Final validation remains incomplete."),
    True, ("Revised checkpoint.", "Temporary workload adjustment.", "Help with one review task."),
    REVISION, ("Jordan plans integration at T8.",), "T6",
    "Some requests exceed a manager's authority and need the organization's formal process.",
)

PERSONAL_CAPACITY = WorkplaceScenario(
    "personal-capacity", "A personal situation affecting delivery",
    "At T5, an abstract personal situation has reduced Alex's capacity and created material verification risk.",
    PEOPLE,
    ("Work was on track at T0.", "Concentration reduced at T4 and an internal test checkpoint was missed.",
     "At T5 failure handling remains unvalidated.", "Jordan depends on the T8 handoff.",
     "Alex no longer has strong evidence that T8 is safe and Morgan has not been told."),
    ("Whether T8 can still be recovered.", "What adjustment Morgan will approve."),
    (Commitment("Alex", "verification integration for Jordan", "T8"),), RiskLevel.HIGH,
    work_impact=PRIMARY_IMPACT,
)

def response(response_id, label, message, **flags):
    return ProfessionalResponse(response_id, label, message, **flags)

RESPONSES = {
    "hide-everything": response("hide-everything", "Hide everything", "This is personal. Work doesn't need to know.",
        preserves_reasonable_privacy=True),
    "overshare": response("overshare", "Unnecessary private detail", "Alex gives a long private history, then vaguely mentions being behind.",
        identifies_work_impact=True, preserves_reasonable_privacy=False, communicates_impact=True),
    "vague-personal-problem": response("vague-personal-problem", "Vague personal problem", "I'm having some personal problems.",
        preserves_reasonable_privacy=True),
    "explanation-without-plan": response("explanation-without-plan", "Explanation without plan",
        "I've had a difficult situation at home and that's why I'm behind.", identifies_work_impact=True,
        preserves_reasonable_privacy=True, dependency_acknowledged=True),
    "unsupported-reassurance": response("unsupported-reassurance", "Unsupported reassurance",
        "I'm dealing with something personal, but don't worry, I'll definitely still finish by T8.",
        identifies_work_impact=True, unsupported_promise=True, preserves_reasonable_privacy=True),
    "disappear": response("disappear", "Disappear", "Alex stops responding without an availability update or handoff.",
        preserves_reasonable_privacy=True),
    "bounded-professional-disclosure": response("bounded-professional-disclosure", "Bounded professional disclosure",
        "A personal situation is affecting my capacity today. The verification work is at risk for T8; failure handling still needs validation. Can we move final review to T9 while Jordan uses the stable contract? I'll update at T6.",
        identifies_work_impact=True, preserves_reasonable_privacy=True, requests_specific_support=True,
        revises_commitment_explicitly=True, updates_dependencies=True, communicates_impact=True,
        material_risk_communicated=True, dependency_acknowledged=True, preserves_uncertainty=True,
        follow_up_point=6, recommendation_provided=True),
    "equivalent-bounded": response("equivalent-bounded", "Equivalent bounded disclosure",
        "My capacity is reduced for a private reason. T8 verification is not a safe forecast: validation remains. I propose T9, Jordan can use the posted contract, and I will reassess at T6.",
        identifies_work_impact=True, preserves_reasonable_privacy=True, requests_specific_support=True,
        revises_commitment_explicitly=True, updates_dependencies=True, communicates_impact=True,
        material_risk_communicated=True, dependency_acknowledged=True, preserves_uncertainty=True,
        follow_up_point=6, recommendation_provided=True),
    "early-support-request": response("early-support-request", "Early, smaller support request",
        "My capacity is reduced today. Before the review slips, can we move one meeting and pair on failure handling? T8 remains at risk; I will update at T6.",
        identifies_work_impact=True, preserves_reasonable_privacy=True, requests_specific_support=True,
        revises_commitment_explicitly=True, updates_dependencies=True, material_risk_communicated=True,
        dependency_acknowledged=True, preserves_uncertainty=True, follow_up_point=6),
}

def small_scenario(sid, title, description, capacity, facts, responses, risk=RiskLevel.MODERATE, formal=None):
    impact = WorkImpactContext("Alex", facts[0], tuple(facts[1:]), "T1", capacity,
        ("The private cause in full detail.",), tuple(facts), True, (), None, (), "next agreed checkpoint", formal)
    return sid, (WorkplaceScenario(sid, title, description, PEOPLE, tuple(facts), (), (), risk, work_impact=impact), responses)

AUXILIARY = dict((small_scenario(
    "one-day-availability", "One-day availability issue", "Alex will be unavailable tomorrow afternoon.", WorkCapacity.UNAVAILABLE,
    ("Review with Jordan tomorrow afternoon.", "Alex will be unavailable then."), {
      "miss-review": response("miss-review", "Say nothing", "Alex misses the review without notice."),
      "proactive-reschedule": response("proactive-reschedule", "Reschedule and preserve the handoff", "I need to be unavailable tomorrow afternoon. Can we move to T4 morning? The API contract is posted.", identifies_work_impact=True, requests_specific_support=True, revises_commitment_explicitly=True, updates_dependencies=True),
    }), small_scenario(
    "high-risk-capacity", "Capacity and a production deployment", "Alex identifies inadequate concentration before a risky deployment.", WorkCapacity.UNSAFE_FOR_HIGH_RISK_TASK,
    ("Production deployment today.", "No deadline has been missed.", "Current capacity is not appropriate for this high-risk task."), {
      "reassign-safely": response("reassign-safely", "Stop and reassign", "I should not execute this deployment in my current capacity. Please assign another qualified reviewer or defer it.", identifies_work_impact=True, answers_legitimate_capacity_question=True, requests_specific_support=True, recognizes_task_safety=True),
    }, RiskLevel.CRITICAL), small_scenario(
    "recurring-capacity-impact", "Recurring work impact", "Morning commitments have repeatedly been missed without a durable plan.", WorkCapacity.REDUCED,
    ("Repeated morning commitments.", "Several one-off explanations have not produced a workable plan."), {
      "durable-plan": response("durable-plan", "Address the pattern", "This pattern is affecting morning commitments. Let's clarify expectations and a sustainable schedule; if beyond your authority I will use the designated formal process.", identifies_work_impact=True, requests_specific_support=True, addresses_recurring_pattern=True, uses_formal_path_when_needed=True),
    }, formal="Some requests exceed a manager's authority and need the organization's formal process."), small_scenario(
    "urgent-personal-absence", "Urgent personal absence", "Alex must leave immediately; communication is proportional to what is feasible.", WorkCapacity.UNAVAILABLE,
    ("Immediate availability.", "Alex must leave now.", "A critical handoff may be affected."), {
      "minimal-handoff": response("minimal-handoff", "Minimal proportional notice", "I must leave for an urgent personal matter. The stable contract is posted for Jordan; I will update Morgan when I can.", identifies_work_impact=True, preserves_reasonable_privacy=True, updates_dependencies=True),
    }), small_scenario(
    "intrusive-peer-question", "Intrusive teammate question", "Jordan asks what exactly is going on.", WorkCapacity.REDUCED,
    ("Jordan's T8 handoff.", "The handoff is moving to T9."), {
      "maintain-boundary": response("maintain-boundary", "Maintain a useful boundary", "It's personal and I'd rather not discuss details. Your handoff moves to T9; I'll send the stable contract today.", identifies_work_impact=True, preserves_reasonable_privacy=True, updates_dependencies=True),
    }), small_scenario(
    "manager-capacity-question", "Legitimate operational question", "Morgan asks whether deployment should be reassigned.", WorkCapacity.UNSAFE_FOR_HIGH_RISK_TASK,
    ("Deployment ownership today.", "Morgan needs an operational capacity answer."), {
      "answer-operationally": response("answer-operationally", "Answer without private cause", "I can do routine work, but not this deployment safely today; please reassign it. I prefer to keep the cause private.", identifies_work_impact=True, preserves_reasonable_privacy=True, answers_legitimate_capacity_question=True, recognizes_task_safety=True, requests_specific_support=True),
    }), small_scenario(
    "revised-commitment-missed", "Revised commitment changes again", "Early support was useful, but later evidence puts T9 at risk too.", WorkCapacity.REDUCED,
    ("Final review revised from T8 to T9.", "New evidence shows T9 will also be missed."), {
      "update-again": response("update-again", "Reassess and update", "The T9 revision is now at risk. Validation still remains; I need another adjustment and will close the T10 checkpoint.", identifies_work_impact=True, requests_specific_support=True, revises_commitment_explicitly=True, updates_dependencies=True, material_risk_communicated=True, follow_up_point=10, loop_closed=True),
    }), small_scenario(
    "formal-capacity-support", "Formal support boundary", "A longer-term request exceeds ordinary manager authority.", WorkCapacity.REDUCED,
    ("Longer-term schedule request.", "Morgan cannot approve the full request alone."), {
      "use-formal-path": response("use-formal-path", "Use designated process", "I will communicate work impact to Morgan and use the organization's designated formal process for the longer request.", identifies_work_impact=True, requests_specific_support=True, uses_formal_path_when_needed=True),
    }, formal="Company policy and local law can affect procedures; this lab gives no legal conclusion.")))

SCENARIOS = {PERSONAL_CAPACITY.scenario_id: (PERSONAL_CAPACITY, RESPONSES), **AUXILIARY}
