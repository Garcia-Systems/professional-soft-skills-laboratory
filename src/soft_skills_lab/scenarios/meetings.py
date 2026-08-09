"""Chapter 19 meeting scenarios using the shared authored behavior model."""
from soft_skills_lab.domain.models import (ActionItem, ContributionType, MeetingContext,
    MeetingContribution, MeetingDecision, MeetingOutcome, Participant, ProfessionalResponse,
    RiskLevel, WorkplaceScenario)

PEOPLE = (Participant("Morgan", "engineering manager"), Participant("Priya", "product manager"),
          Participant("Alex", "backend developer"), Participant("Jordan", "frontend developer"),
          Participant("Dana", "operations stakeholder"))
FACTS = ("Backend implementation is complete.", "Frontend implementation is complete.",
         "Manual validation passed.", "One automated row-filter case still fails at the 90-day boundary.",
         "No evidence shows unauthorized-field exposure.", "Friday has commercial value.")
OUTCOME = MeetingOutcome(
    (MeetingDecision("Release Friday with export limited to 30 days.", "Morgan",
      "The limited scope meets the customer-review need without exposing the known 90-day defect.",
      ("Release full 90-day scope Friday", "Delay the entire release"), "Export ranges up to 30 days", "Friday"),),
    (ActionItem("Fix and validate the 90-day boundary.", "Alex", "T4"),
     ActionItem("Review full-range release after validation.", "Priya", "T5", "Alex's validation result")),
    ("Does the corrected full range pass automated validation?",), "T4 validation result")
RELEASE_MEETING = MeetingContext("release-readiness", "Reporting export release readiness",
    "Decide whether Friday release is acceptable.", PEOPLE,
    ("Current implementation state", "Remaining validation risk", "Friday release decision",
     "Owner/action if release is delayed or conditioned"),
    ("Release Friday?", "Reduce scope?", "Delay for correction?"), FACTS, FACTS,
    ("Whether the corrected 90-day case passes validation.",),
    (("Morgan", "engineering release approval"), ("Priya", "product scope tradeoff")), "Decision required before Friday",
    (("Alex", ("Remaining test failure.", "User-visible consequence.", "Current correction estimate.", "Recommendation.")),),
    (("Alex", ("Full backend architecture walkthrough.", "Unrelated sprint work.", "Dana's customer agenda beyond the pre-read.")),),
    OUTCOME, (("AGENDA 1 — CURRENT STATE", "Status established."),
              ("AGENDA 2 — REMAINING RISK", "Alex owns relevant evidence."),
              ("AGENDA 3 — TRADEOFF", "30-day limited release proposed."),
              ("AGENDA 4 — DECISION", "Release Friday with 30-day limit."),
              ("AGENDA 5 — FOLLOW-UP", "Alex fixes the boundary; Priya reviews full-range release.")))

def c(kind, *, relevant=False, new=False, repeat=False, scope=True, affects=False, evidence=()):
    return MeetingContribution("Alex", kind, "Remaining validation risk", evidence, relevant, new,
                               False, affects, repeat, scope)
def r(rid, label, message, contribution=None, **kw):
    return ProfessionalResponse(rid, label, message, meeting_contribution=contribution, **kw)

RESPONSES = {
 "unprepared-silence": r("unprepared-silence", "Unprepared silence", "I'm not sure. I'll have to look after the meeting.", meeting_prepared=False),
 "silent-relevant-risk": r("silent-relevant-risk", "Silent relevant risk", "Alex does not disclose the known boundary consequence.", meeting_prepared=True, material_information_withheld=True),
 "dominate-meeting": r("dominate-meeting", "Architecture and test-framework dump", "Alex explains architecture, fixtures, queries, and implementation history.", c(ContributionType.EVIDENCE,relevant=True,new=True,scope=False), meeting_prepared=True, material_risk_communicated=True),
 "repeat-existing-point": r("repeat-existing-point", "Repeat established point", "We still have a failing test.", c(ContributionType.STATUS,repeat=True,scope=False), meeting_prepared=True, material_risk_communicated=True),
 "speak-to-be-seen": r("speak-to-be-seen", "Redundant low-value airtime", "Several comments add no fact, clarification, or decision effect.", c(ContributionType.STATUS,repeat=True,scope=False)),
 "useful-contribution": r("useful-contribution", "Concise decision-relevant contribution", "The remaining failure affects the 90-day boundary and may add one day. No unauthorized fields are known. I recommend fixing it; I can validate by T4.", c(ContributionType.RECOMMENDATION,relevant=True,new=True,affects=True,evidence=(FACTS[3],FACTS[4])), meeting_prepared=True, material_risk_communicated=True, preserves_uncertainty=True, recommendation_provided=True, meeting_purpose_matched=True, follow_up_point=4),
 "useful-question": r("useful-question", "Decision-relevant question", "Would a 30-day limit still satisfy the customer-review use case, Dana?", c(ContributionType.QUESTION,relevant=True,new=True,affects=True), meeting_prepared=True, meeting_purpose_matched=True, supplies_question_context=True),
 "summarize-and-close": r("summarize-and-close", "Capture decision and follow-through", "Decision: Friday with 30 days. Alex fixes the boundary by T4; Priya reviews full range at T5. Validation remains open.", c(ContributionType.SUMMARY,relevant=True,affects=True), meeting_prepared=True, meeting_purpose_matched=True, decision_captured=True, action_owner_captured=True, meeting_loop_closed=True),
}
RELEASE = WorkplaceScenario("release-readiness", RELEASE_MEETING.title, RELEASE_MEETING.purpose, PEOPLE, FACTS,
    RELEASE_MEETING.unresolved_questions, (), RiskLevel.HIGH, meeting_context=RELEASE_MEETING)

def focused(sid,title,purpose,responses, facts=("Meeting semantics are explicitly authored.",)):
    ctx=MeetingContext(sid,title,purpose,PEOPLE,(purpose,),(),(),facts,(),(),"Short meeting")
    return WorkplaceScenario(sid,title,purpose,PEOPLE,facts,(),(),RiskLevel.MODERATE,meeting_context=ctx),responses

STANDUP=focused("daily-standup","Daily standup","Coordinate quickly; move problem solving to follow-up.",{
 "task-diary":r("task-diary","Task diary","Alex lists every action from yesterday.",c(ContributionType.STATUS,scope=False)),
 "hidden-blocker":r("hidden-blocker","Hidden credentials blocker","Still working on verification.",material_information_withheld=True),
 "deep-debugging":r("deep-debugging","Debug during standup","Alex begins solving credential setup in the meeting.",c(ContributionType.STATUS,relevant=True,new=True,scope=False)),
 "useful-standup":r("useful-standup","Useful coordination","Verification is blocked on credentials from Operations; Dana owns access. I will follow up after standup, then validate.",c(ContributionType.STATUS,relevant=True,new=True),meeting_purpose_matched=True,dependency_acknowledged=True,follow_up_point=1)})
DESIGN=focused("design-review","Adapter design review","Evaluate an architectural decision.",{
 "purposeful-detail":r("purposeful-detail","Detailed design evidence","Alex explains coupling, failure modes, benchmarks, and interface alternatives needed for the design choice.",c(ContributionType.EVIDENCE,relevant=True,new=True,affects=True),meeting_purpose_matched=True,supports_decision=True)})
STAKEHOLDER=focused("meeting-uncertainty","Stakeholder capacity question","Answer or establish bounded follow-up.",{
 "bluff":r("bluff","Bluff","The maximum is definitely one million rows.",exceeds_available_evidence=True),
 "defer-vaguely":r("defer-vaguely","Vague deferral","I'll look later."),
 "bounded-follow-up":r("bounded-follow-up","Bounded uncertainty","I don't know the current maximum row count offhand. I can verify it and send it by T3.",c(ContributionType.CLARIFICATION,relevant=True,new=True),preserves_uncertainty=True,follow_up_point=3,meeting_purpose_matched=True)})
INTERRUPTION=focused("meeting-interruption","Frontend constraint discussion","Hear the complete constraint before responding.",{
 "interrupt":r("interrupt","Interrupt Jordan","Alex interrupts before the information that answers the concern.",c(ContributionType.DISAGREEMENT,relevant=True),captures_explicit_concern=False),
 "wait-and-respond":r("wait-and-respond","Wait and respond","Alex listens; Jordan's remaining information resolves the concern.",c(ContributionType.CLARIFICATION,relevant=True),captures_explicit_concern=True,meeting_purpose_matched=True),
 "clarify-after-listening":r("clarify-after-listening","Clarify after listening","After Jordan finishes, Alex asks whether the constraint includes cached exports.",c(ContributionType.QUESTION,relevant=True,new=True),captures_explicit_concern=True,meeting_purpose_matched=True)})
RECOVERY=focused("meeting-interrupted-risk","Risk interrupted","Preserve material release information.",{
 "let-point-drop":r("let-point-drop","Let risk disappear","Alex does not return to the decision-relevant boundary risk.",material_information_withheld=True),
 "protect-relevant-point":r("protect-relevant-point","Finish material point","Before we move on, the failing case affects exported date boundaries and changes the release decision.",c(ContributionType.CLARIFICATION,relevant=True,new=True,affects=True),relevant_point_protected=True,material_risk_communicated=True,meeting_purpose_matched=True)})
GROUP=focused("meeting-group-disagreement","Group disagreement","Resolve a release disagreement without an extended duel.",{
 "evidence-once":r("evidence-once","Evidence once, then respect owner","I disagree because the boundary evidence violates the export contract. Morgan owns approval; I will document detail for follow-up.",c(ContributionType.DISAGREEMENT,relevant=True,new=True),respects_decision_ownership=True,meeting_purpose_matched=True),
 "extended-duel":r("extended-duel","Extended duel","Alex repeats the argument after Morgan decides.",c(ContributionType.DISAGREEMENT,repeat=True,scope=False),repeats_resolved_argument=True)})
CONFLICT=focused("meeting-conflict","Release argument","Separate mixed decisions and refocus.",{
 "refocus":r("refocus","Separate the decisions","We're mixing whether Friday matters with whether the 90-day defect is acceptable. Can we separate them?",c(ContributionType.CLARIFICATION,relevant=True,new=True),restores_shared_facts=True,creates_decision_path=True,meeting_purpose_matched=True)})
LOW=focused("operations-support","Operations meeting","Provide technical support only if relevant.",{
 "low-airtime-useful":r("low-airtime-useful","Quiet, available support","Alex confirms one implementation detail when asked; nothing material remains hidden.",c(ContributionType.CLARIFICATION,relevant=True),meeting_prepared=True,meeting_purpose_matched=True)})
REMOTE=focused("remote-decision","Remote release decision","Participate attentively in an agreed decision role.",{
 "missed-question":r("missed-question","Missed direct question","Unrelated work causes Alex to miss a direct risk question and require repetition.",attention_failure=True)})
ASYNC=focused("deployment-success-update","Deployment success notification","Tell everyone the deployment succeeded.",{
 "use-async":r("use-async","Use a written update","No discussion or decision is needed; send the deployment result asynchronously.",async_recommended=True,meeting_purpose_matched=True)})
NO_OWNER=focused("scope-without-owner","Scope tradeoff without owner","Form a recommendation without pretending it is an authorized decision.",{
 "route-recommendation":r("route-recommendation","Identify missing owner","We can recommend 30 days, but Priya is absent and owns scope. Capture this as a recommendation and route it to her.",c(ContributionType.RECOMMENDATION,relevant=True,new=True),respects_decision_ownership=True,decision_captured=True,meeting_purpose_matched=True),
 "pretend-consensus":r("pretend-consensus","Misrepresent consensus","We all agree, so scope is now 30 days.",decision_captured=False)})
SCENARIOS={s.scenario_id:(s,res) for s,res in ( (RELEASE,RESPONSES),STANDUP,DESIGN,STAKEHOLDER,INTERRUPTION,RECOVERY,GROUP,CONFLICT,LOW,REMOTE,ASYNC,NO_OWNER)}
