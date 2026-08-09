"""Deterministic Chapter 19 predicates; no word or turn counting."""
from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA=tuple(EvaluationCriterion(*x) for x in (
 ("prepares-for-role","Prepared the information expected from this role."),
 ("contributes-decision-relevant-information","Improves shared understanding or the decision."),
 ("surfaces-relevant-risk","Does not hide material information held by the role."),
 ("avoids-redundant-airtime","Avoids repetition that adds no purpose."),
 ("matches-meeting-purpose","Matches contribution type and detail to the meeting purpose."),
 ("protects-relevant-point","Preserves material information when the conversation shifts."),
 ("captures-decision","Distinguishes a confirmed decision from discussion or suggestion."),
 ("captures-action-owner","Makes action ownership and timing explicit."),
 ("closes-meeting-loop","Leaves a usable outcome and follow-up state."),
 ("uses-async-when-appropriate","Uses asynchronous communication when no interaction is needed.")))

def evaluate_meeting_response(scenario: WorkplaceScenario, response: ProfessionalResponse):
    c=response.meeting_contribution
    prepared=Outcome.PASS if response.meeting_prepared is True else (Outcome.FAIL if response.meeting_prepared is False else Outcome.PARTIAL)
    relevant=Outcome.PASS if c and c.decision_relevant else Outcome.FAIL
    risk=Outcome.FAIL if response.material_information_withheld else (Outcome.PASS if response.material_risk_communicated or scenario.current_risk.value < 3 else Outcome.PARTIAL)
    redundant=Outcome.FAIL if c and c.repeats_established_information else Outcome.PASS
    purpose=Outcome.PASS if response.meeting_purpose_matched else (Outcome.FAIL if c and not c.within_scope else Outcome.PARTIAL)
    outcomes=(prepared,relevant,risk,redundant,purpose,
      Outcome.PASS if response.relevant_point_protected else Outcome.PARTIAL,
      Outcome.PASS if response.decision_captured else Outcome.PARTIAL,
      Outcome.PASS if response.action_owner_captured else Outcome.PARTIAL,
      Outcome.PASS if response.meeting_loop_closed else Outcome.PARTIAL,
      Outcome.PASS if response.async_recommended else Outcome.PARTIAL)
    evidence=(response.message,)
    return tuple(EvaluationResult(k,v,"Authored meeting behavior evaluated without airtime, personality, or wording scores.",evidence) for k,v in zip(CRITERIA,outcomes))
