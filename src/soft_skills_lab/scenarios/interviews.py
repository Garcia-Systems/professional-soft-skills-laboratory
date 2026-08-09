"""Chapter 18 authored interview questions, evidence, and reference answers."""
from soft_skills_lab.domain.models import (ExperienceEvidence, InterviewAnswer, InterviewFollowUp,
    InterviewQuestion, Participant, ProfessionalResponse, RiskLevel, WorkplaceScenario)

ALEX = Participant("Alex", "candidate")
INCIDENT = ExperienceEvidence(
    "skipped-validation-incident", "Payment-service release.", ("Alex", "Jordan", "release team"),
    ("Alex deployed a configuration change.", "Required staging validation was skipped.",
     "An incorrect endpoint reached production.", "Rollback contained the incident.", "No payments were lost."),
    ("Alex alone decided to skip the required staging validation under schedule pressure.",),
    ("The team performed the rollback.", "Alex helped the team add the validation gate."),
    ("Alex deployed the change.", "Alex initiated rollback and verified service."),
    ("A short production incident occurred.", "Rollback restored service; no payments were lost."),
    ("Validation became a mandatory deployment gate.", "Alex now treats schedule pressure as a reason to surface risk, not skip validation."),
    ("Failure rate rose to about 18% during the incident.",),
    competencies=("responsibility", "recovery", "learning", "process improvement"))
ADAPTER = ExperienceEvidence("adapter-boundary-decision", "Adapter design review.", ("Alex", "Morgan"),
    ("Morgan was concerned about delivery complexity.", "Alex presented coupling and test evidence.", "Morgan owned the final decision."),
    ("Alex proposed keeping the boundary.",), ("Morgan chose the final design; the team implemented it.",),
    ("Alex asked for a decision against the shared delivery objective.",), ("The boundary was retained with a smaller interface.",),
    competencies=("influence without authority", "disagreement", "decision quality"))
SOLO = ExperienceEvidence("solo-debugging", "A solo debugging task.", ("Alex",), ("Alex found a cache defect."),
    ("Alex owned the investigation." ,), (), ("Alex fixed the defect.",), ("The test passed.",), competencies=("debugging",))

FOLLOWUPS = (
    InterviewFollowUp("why-skip-validation", "Why did you skip the validation?", ("Schedule pressure influenced Alex's decision but did not remove Alex's agency.",)),
    InterviewFollowUp("immediate-response", "What did you do immediately after discovering the issue?", ("Alex initiated rollback and verified service.",)),
    InterviewFollowUp("proof-of-learning", "How did you know the new process worked?", ("The gate caught another invalid endpoint before production.",)),
    InterviewFollowUp("different-now", "What would you do differently now?", ("Surface schedule risk and run required validation.",)),
)

def q(qid, prompt, competencies, evidence, risks=(), followups=()):
    return InterviewQuestion(qid, prompt, competencies, evidence, risks, followups)
def a(qid, **kw): return InterviewAnswer(question_id=qid, **kw)
def r(rid, label, message, answer): return ProfessionalResponse(rid, label, message, interview_answer=answer)
def scenario(sid, title, question, responses, evidence=()):
    return WorkplaceScenario(sid, title, question.prompt, (ALEX,), tuple(x for e in evidence for x in e.facts), (), (), RiskLevel.LOW,
        interview_question=question, experience_evidence=evidence), responses

MISTAKE_Q = q("mistake", "Tell me about a mistake you made at work and how you handled it.",
    ("Responsibility", "Judgment", "Recovery", "Learning", "Communication"),
    ("Specific decision Alex owned", "Actual impact", "Containment", "Corrective action", "Demonstrated later behavior"),
    ("Blame shifting", "Fake weakness", "Excessive self-condemnation", "Technical detail without professional reflection", "Unsupported claims of permanent improvement"), FOLLOWUPS)
base = dict(experience_id=INCIDENT.experience_id, context=INCIDENT.context)
MISTAKE_RESPONSES = {
 "fake-non-mistake": r("fake-non-mistake", "Fake non-mistake", "I sometimes care too much about quality and spend too much time making things perfect.", a("mistake", answers_directly=False, privacy_preserved=True)),
 "blame-story": r("blame-story", "Blame story", "Jordan wrote the bad configuration. It caused an incident.", a("mistake", **base, evidence=(INCIDENT.facts[2],), outcome="A short incident occurred.", answers_directly=True, ownership_accurate=False)),
 "self-destruction": r("self-destruction", "Self-condemnation", "I caused a production outage because I was careless. It was a terrible failure and I felt awful.", a("mistake", **base, evidence=(INCIDENT.facts[2],), outcome="A short incident occurred.", answers_directly=True, ownership_accurate=False, unsupported_claims=("Alex's identity is careless.",))),
 "technical-dump": r("technical-dump", "Technical dump", "The YAML endpoint, deploy command, validator classes, fixtures, and test internals took several minutes to explain.", a("mistake", **base, evidence=(INCIDENT.facts[2],), irrelevant_detail=("endpoint values", "configuration formats", "deployment commands", "test internals"), answers_directly=False)),
 "vague-learning": r("vague-learning", "Vague learning", "I skipped validation, rolled back the bad endpoint, and learned to be more careful.", a("mistake", **base, responsibility="Skipped required staging validation.", recovery="Rollback restored service.", outcome="Incorrect endpoint reached production.", evidence=(INCIDENT.facts[1], INCIDENT.facts[2]), learning_action="Be more careful.", answers_directly=True, ownership_accurate=True)),
 "overclaim-learning": r("overclaim-learning", "Overclaimed learning", "I skipped validation and rolled back. After that, I made sure deployment mistakes could never happen again.", a("mistake", **base, responsibility="Skipped required staging validation.", recovery="Rollback restored service.", outcome="Incorrect endpoint reached production.", evidence=(INCIDENT.facts[1],), learning_action="Added a gate.", unsupported_claims=("Deployment mistakes can never happen again.",), answers_directly=True, ownership_accurate=True)),
}
strong = a("mistake", **base, responsibility="Skipped required staging validation.", actions=("Initiated rollback.", "Verified service."), reasoning=("Schedule pressure influenced but did not remove the decision.",), outcome="Incorrect endpoint reached production and caused a short incident.", recovery="Rollback restored service.", evidence=INCIDENT.facts, team_contribution=INCIDENT.team_contribution, learning_action="Validation became a mandatory deployment gate.", later_evidence=("The gate later caught another invalid endpoint before production.",), supported_metrics=INCIDENT.supported_metrics, ownership_claim="Alex alone made the deployment decision.", followup_ownership_claims=(("why-skip-validation", "Alex alone made the deployment decision."),), answers_directly=True, ownership_accurate=True)
MISTAKE_RESPONSES["evidence-based-mistake"] = r("evidence-based-mistake", "Evidence-based mistake", "I skipped required staging validation under schedule pressure. The bad endpoint reached production; I initiated rollback and verified service. I helped add a mandatory gate, which later caught another bad endpoint before production.", strong)
MISTAKE_RESPONSES["concise-evidence-based"] = r("concise-evidence-based", "Concise evidence-based", "I skipped required validation, causing a bad endpoint to reach production. We rolled back, and I helped add a required gate that later caught the same class of error.", strong)
MISTAKE = scenario("interview-mistake", "Interview: a mistake", MISTAKE_Q, MISTAKE_RESPONSES, (INCIDENT,))

# Additional focused scenarios exercise the same answer metadata rather than separate engines.
def strong_response(rid, qid, msg, **kw): return r(rid, rid.replace('-', ' ').title(), msg, a(qid, answers_directly=True, ownership_accurate=True, evidence=(msg,), **kw))
DISAGREE_Q=q("disagreement","Tell me about a time you disagreed with your manager.",( "Collaboration","Decision quality"),("Shared objective","Manager concern","Evidence","Decision process","Outcome"),("Victory story",))
DISAGREE=scenario("interview-disagreement","Interview: manager disagreement",DISAGREE_Q,{"collaborative-decision":strong_response("collaborative-decision","disagreement","Morgan was concerned about delivery complexity. I shared coupling and test evidence against our delivery objective. Morgan retained a smaller boundary; I committed to the decision and the team implemented it.",experience_id=ADAPTER.experience_id,reasoning=("Compared options against the shared objective.",),outcome="A smaller adapter boundary was retained.",team_contribution=ADAPTER.team_contribution)},(ADAPTER,))
CONFLICT_Q=q("conflict","Tell me about a difficult conflict with a teammate or stakeholder.",( "De-escalation","Resolution"),("Observable tension","Own contribution","Resolution"))
CONFLICT=scenario("interview-conflict","Interview: conflict",CONFLICT_Q,{"de-escalate-and-resolve":strong_response("de-escalate-and-resolve","conflict","The release discussion became personal after I repeated my position. I acknowledged that contribution, restored the shared validation facts, and we paused until the owner resolved the release decision.",reasoning=("De-escalated to recover a decision process.",),outcome="The decision was resolved without portraying anyone as irrational.")})
FAIL_Q=q("failure","Tell me about a failure.",( "Judgment","Learning"),("Intended outcome","Responsible work","External condition"))
FAIL=scenario("interview-failure","Interview: failure without invented fault",FAIL_Q,{"responsible-failure":strong_response("responsible-failure","failure","We completed the required integration and validation, but the partner discontinued its API, so the initiative did not achieve adoption. I documented the reusable work and learned to add an earlier external-dependency checkpoint.",outcome="The initiative failed to achieve adoption.",learning_action="Add earlier external-dependency checkpoints.")})
WEAK_Q=q("weakness","What is your weakness?",("Self-awareness","Improvement"),("Bounded development area","Past impact","Method","Progress"),("Canned strength","Claiming elimination"))
WEAK=scenario("interview-weakness","Interview: weakness",WEAK_Q,{"perfectionist":r("perfectionist","Canned answer","I'm a perfectionist.",a("weakness")),"evidence-based-weakness":strong_response("evidence-based-weakness","weakness","I used to wait too long to surface schedule risks because I thought I could recover alone. Now I separate risk visibility from delivery confidence, report material risk earlier, and set explicit follow-ups.",learning_action="Report material risk earlier with explicit follow-ups.",later_evidence=("Alex sent the next material risk update before the deadline.",))})
LEAVE_Q=q("leaving","Why did you leave your last job?",("Clarity","Relevance"),("Factual reason","Forward relevance"),("Attack","Oversharing","Evasion"))
LEAVE=scenario("interview-layoff","Interview: fictional restructuring",LEAVE_Q,{"bitter-attack":r("bitter-attack","Bitter attack","Leadership was incompetent.",a("leaving",answers_directly=True)),"concise-forward":strong_response("concise-forward","leaving","My fictional role ended as part of a restructuring. Since then I have strengthened reliability and stakeholder communication, which are relevant to this role.",outcome="Role ended in restructuring.")})
GAP_Q=q("gap","Can you explain this employment gap?",("Timeline clarity","Readiness"),("Concise fact","True activity","Forward focus"),("Invented story","Required private detail"))
GAP=scenario("interview-resume-gap","Interview: fictional resume gap",GAP_Q,{"bounded-gap":strong_response("bounded-gap","gap","I took a planned break for a private family matter; I don't need to share the private details. I completed a reliability course, and I am now available for this role.",outcome="Candidate is available.",privacy_preserved=True)})
TECH_Q=q("technical-unknown","How does this exact storage-engine mechanism work?",("Truthfulness","Reasoning"),("Knowledge boundary","Current understanding","Verification"),("Bluff","Rambling","Stopping without useful reasoning"))
TECH=scenario("interview-technical-unknown","Interview: technical uncertainty",TECH_Q,{"bluff":r("bluff","Bluff","It definitely uses consensus in every case.",a("technical-unknown",answers_directly=True,unsupported_claims=("Exact mechanism is known.",))),"bounded-reasoning":strong_response("bounded-reasoning","technical-unknown","I haven't implemented that exact mechanism. My current understanding is that it uses a write-ahead log, but I would verify its durability guarantees before choosing an approach.",uncertainty=("Exact mechanism not implemented before.",),reasoning=("Verify durability guarantees.",))})
EST_Q=q("estimate","How long would you estimate this project takes?",("Planning","Uncertainty"),("Critical unknowns","Assumptions","Conditional range","Confidence improvement"),("False precision","Refusal"))
EST=scenario("interview-estimation","Interview: incomplete estimate",EST_Q,{"conditional-estimate":strong_response("conditional-estimate","estimate","Assuming one existing integration and unchanged compliance scope, I would estimate four to six weeks. Integration count and security review are open; a discovery spike and stakeholder decision would narrow the range.",uncertainty=("Integration count","Security-review scope"),reasoning=("Range is conditional on stated assumptions.",))})
PROJECT_Q=q("project-not-planned","Tell me about a project that did not go as planned.",( "Adaptation","Learning"),("Change","Response","Partial outcome","Remaining tradeoff"))
PROJECT=scenario("interview-imperfect-outcome","Interview: no movie ending",PROJECT_Q,{"partial-success":strong_response("partial-success","project-not-planned","A partner delay removed half our launch window. We reduced scope transparently and delivered the highest-value workflow, but deferred automation remained. The later planning process added partner checkpoints.",outcome="The core workflow shipped; automation remained deferred.",learning_action="Add partner checkpoints.")})
SELECTION_Q=q("influence","Tell me about a time you influenced a decision without authority.",( "Influence without authority",),("Shared decision","Evidence","No direct authority","Influence"))
SELECTION=scenario("interview-story-selection","Interview: story selection",SELECTION_Q,{"select-adapter-boundary":strong_response("select-adapter-boundary","influence","The adapter-boundary story is most relevant because it contains a shared decision, evidence, influence, and no direct authority.",experience_id=ADAPTER.experience_id)},(INCIDENT,ADAPTER,SOLO))
SCENARIOS=dict((s[0].scenario_id,s) for s in (MISTAKE,DISAGREE,CONFLICT,FAIL,WEAK,LEAVE,GAP,TECH,EST,PROJECT,SELECTION))

def get_question(qid):
    for sc,_ in SCENARIOS.values():
        if sc.interview_question.question_id == qid: return sc.interview_question
    raise KeyError(f"unknown interview question: {qid}")
def get_answer(qid,rid):
    q=get_question(qid)
    for sc,responses in SCENARIOS.values():
        if sc.interview_question == q and rid in responses: return responses[rid].interview_answer
    raise KeyError(f"unknown answer for {qid}: {rid}")
def select_story(question_id):
    if question_id != "influence": raise KeyError(f"story selection unavailable for: {question_id}")
    return ADAPTER
