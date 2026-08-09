"""Explicit Chapter 20 predicates: never grammar, tone, or length scoring."""
from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, MessagePurpose, Outcome

CRITERIA=tuple(EvaluationCriterion(*x) for x in (
 ("makes-purpose-explicit","The expected response kind is visible."),("provides-standalone-context","The intended reader has sufficient context."),
 ("states-current-state","Current professional state is explicit."),("uses-decision-relevant-evidence","Evidence supports the state."),
 ("makes-request-explicit","A required action or decision is explicit."),("identifies-owner","Required action has an owner."),
 ("uses-appropriate-channel-detail","Detail fits channel and audience."),("establishes-next-update","A material open loop has a follow-up."),
 ("preserves-uncertainty","Written certainty does not exceed evidence."),("creates-durable-record","Durable state is preserved where needed.")))

def evaluate_written_response(scenario,response):
    w=response.written_message
    if w is None: raise ValueError("response has no written message")
    ask_needed=w.purpose in (MessagePurpose.REQUEST,MessagePurpose.ESCALATE)
    outcomes=(Outcome.PASS if w.purpose_statement else Outcome.FAIL, Outcome.PASS if w.standalone_context else Outcome.FAIL,
      Outcome.PASS if w.current_state else Outcome.FAIL, Outcome.PASS if w.established_facts else Outcome.FAIL,
      Outcome.PASS if (not ask_needed or (w.request and "advise" not in w.request.lower())) else Outcome.FAIL,
      Outcome.PASS if (not ask_needed or w.owner) else Outcome.FAIL, Outcome.PASS if w.channel_detail_appropriate else Outcome.FAIL,
      Outcome.PASS if w.follow_up_point else Outcome.FAIL, Outcome.FAIL if response.exceeds_available_evidence or response.unsupported_promise or not w.urgency_supported else Outcome.PASS,
      Outcome.PASS if w.durable_record else Outcome.PARTIAL)
    return tuple(EvaluationResult(c,o,"Authored written semantics are evaluated without grammar, vocabulary, formality, or brevity scoring.",(response.message,)) for c,o in zip(CRITERIA,outcomes))
