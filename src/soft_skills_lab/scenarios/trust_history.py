"""Chapter 21 deterministic reputation histories built on professional trust evidence."""
from soft_skills_lab.domain.models import Participant, ProfessionalResponse, RiskLevel, WorkplaceScenario
from soft_skills_lab.trust.model import (DimensionInterpretation, EvidencePolarity as P,
    EvidenceProvenance as Source, TrustDimension as D, TrustEvidence as E, TrustHistory, TrustState as S)

OBS=("Morgan","Jordan")
def e(event_id,time,dimension,polarity,behavior,observers=OBS,source=Source.DIRECT_OBSERVATION,scenario="six-week-project"):
    return E(event_id,time,dimension,polarity,behavior,source,scenario,observers)

SIX_WEEK_EVIDENCE=(
 e("w1-commitment","Week 1",D.COMMITMENT_RELIABILITY,P.POSITIVE,"Commitment kept."),
 e("w1-handoff","Week 1",D.HANDOFF_RELIABILITY,P.POSITIVE,"Handoff explicitly closed.",("Jordan",)),
 e("w2-risk","Week 2",D.RISK_VISIBILITY,P.POSITIVE,"Material schedule risk communicated before the deadline."),
 e("w2-reforecast","Week 2",D.COMMITMENT_RELIABILITY,P.POSITIVE,"Revised forecast communicated and follow-up completed."),
 e("w3-missed","Week 3",D.HANDOFF_RELIABILITY,P.NEGATIVE,"Minor handoff missed; Jordan had to ask.",("Jordan",)),
 e("w3-owned","Week 3",D.OWNERSHIP,P.POSITIVE,"Mistake acknowledged without blame."),
 e("w3-corrected","Week 3",D.HANDOFF_RELIABILITY,P.POSITIVE,"Corrective handoff process completed.",("Jordan",)),
 e("w4-incident","Week 4",D.INCIDENT_COMMUNICATION,P.POSITIVE,"Incident communicated accurately with uncertainty preserved.",("Morgan",),Source.DOCUMENTED_EVENT),
 e("w4-ownership","Week 4",D.OWNERSHIP,P.POSITIVE,"Contribution handled accurately and containment supported.",("Morgan",),Source.DOCUMENTED_EVENT),
 e("w4-recovery","Week 4",D.INCIDENT_COMMUNICATION,P.POSITIVE,"Recovery follow-up completed.",("Morgan",),Source.SHARED_ARTIFACT),
 e("w5-evidence","Week 5",D.TECHNICAL_JUDGMENT,P.POSITIVE,"Architecture concern supported with evidence.",("Morgan",)),
 e("w5-commit","Week 5",D.DECISION_CREDIBILITY,P.POSITIVE,"Resolved decision supported after disagreement.",("Morgan",),Source.SHARED_ARTIFACT),
 e("w6-commitment","Week 6",D.COMMITMENT_RELIABILITY,P.POSITIVE,"Important commitment completed."),
 e("w6-risk","Week 6",D.RISK_VISIBILITY,P.POSITIVE,"Dependency change communicated early."),
 e("w6-handoff","Week 6",D.HANDOFF_RELIABILITY,P.POSITIVE,"Dependency handoff completed proactively.",("Jordan",)),
)
SIX_WEEK=TrustHistory("six-week-project","Alex",SIX_WEEK_EVIDENCE,{
 D.COMMITMENT_RELIABILITY:DimensionInterpretation(S.ESTABLISHED,"Repeated commitments and a realistic reforecast were completed."),
 D.RISK_VISIBILITY:DimensionInterpretation(S.ESTABLISHED,"Material risk was surfaced early in two different weeks."),
 D.HANDOFF_RELIABILITY:DimensionInterpretation(S.REBUILDING,"One missed handoff weakened confidence, but acknowledged correction and later proactive closure show change without erasing the miss."),
 D.TECHNICAL_JUDGMENT:DimensionInterpretation(S.INSUFFICIENT_EVIDENCE,"One evidence-based architecture event is positive, not an established pattern."),
 D.OWNERSHIP:DimensionInterpretation(S.ESTABLISHED,"A mistake and an incident contribution were handled accurately."),
 D.INCIDENT_COMMUNICATION:DimensionInterpretation(S.ESTABLISHED,"Accurate incident communication was followed by documented recovery."),
 D.DECISION_CREDIBILITY:DimensionInterpretation(S.INSUFFICIENT_EVIDENCE,"One constructive decision event is positive but insufficient for an established pattern."),
})

def derived(scenario_id, additions, states):
    return TrustHistory(scenario_id,"Alex",tuple(E(x.event_id,x.time,x.dimension,x.polarity,x.observable_behavior,x.provenance,scenario_id,x.observers) for x in SIX_WEEK_EVIDENCE)+additions,states)

DEGRADATION=derived("trust-degradation",(
 e("d1","Week 7",D.RISK_VISIBILITY,P.NEGATIVE,"Known risk hidden.",scenario="trust-degradation"),
 e("d2","Week 8",D.RISK_VISIBILITY,P.NEGATIVE,"A second known risk was hidden.",scenario="trust-degradation"),
 e("d3","Week 9",D.COMMITMENT_RELIABILITY,P.NEGATIVE,"Commitment missed without warning.",scenario="trust-degradation"),
 e("d4","Week 9",D.HANDOFF_RELIABILITY,P.NEGATIVE,"Critical handoff left open.",scenario="trust-degradation"),),{
 D.COMMITMENT_RELIABILITY:DimensionInterpretation(S.DEGRADED,"Prior strong history remains, but a recent unwarned miss conflicts with it."),
 D.RISK_VISIBILITY:DimensionInterpretation(S.DEGRADED,"Two recent hidden risks conflict with the earlier visible-risk pattern."),
 D.HANDOFF_RELIABILITY:DimensionInterpretation(S.DEGRADED,"A recent critical open handoff follows earlier mixed evidence."),
 D.OWNERSHIP:SIX_WEEK.interpretations[D.OWNERSHIP],})
REBUILDING=derived("trust-rebuilding",DEGRADATION.evidence[len(SIX_WEEK_EVIDENCE):]+(
 e("r1","Week 10",D.RISK_VISIBILITY,P.POSITIVE,"Risk communicated early after feedback.",scenario="trust-rebuilding"),
 e("r2","Week 11",D.RISK_VISIBILITY,P.POSITIVE,"Second risk communicated early.",scenario="trust-rebuilding"),
 e("r3","Week 12",D.RISK_VISIBILITY,P.POSITIVE,"Third risk communicated early.",scenario="trust-rebuilding"),
 e("r4","Week 12",D.HANDOFF_RELIABILITY,P.POSITIVE,"Critical handoff acknowledged and closed.",scenario="trust-rebuilding"),
 e("r5","Week 12",D.COMMITMENT_RELIABILITY,P.POSITIVE,"Revised commitment completed.",scenario="trust-rebuilding"),),{
 D.COMMITMENT_RELIABILITY:DimensionInterpretation(S.REBUILDING,"Observed completion begins repair; a promise or apology alone would not."),
 D.RISK_VISIBILITY:DimensionInterpretation(S.REBUILDING,"Three later visible risks demonstrate change, while degraded history remains."),
 D.HANDOFF_RELIABILITY:DimensionInterpretation(S.REBUILDING,"Later closure is positive behavioral evidence, not instant restoration."),
 D.OWNERSHIP:SIX_WEEK.interpretations[D.OWNERSHIP],})

HISTORIES={x.scenario_id:x for x in (SIX_WEEK,DEGRADATION,REBUILDING)}

def get_trust_history(scenario_id):
    try:return HISTORIES[scenario_id]
    except KeyError:raise KeyError(f"trust history unavailable for scenario: {scenario_id}") from None

def _scenario(sid,title,description):
    return WorkplaceScenario(sid,title,description,(Participant("Alex","engineer"),Participant("Morgan","manager"),Participant("Jordan","teammate")),
      ("Trust conclusions retain observable positive and negative evidence.",),("Future behavior remains unknown.",),(),RiskLevel.MODERATE)
SCENARIOS={
 "six-week-project":(_scenario("six-week-project","Six-week project trust history","Repeated commitments, risk updates, handoffs, incident work, and disagreement create domain-specific evidence."),{}),
 "trust-degradation":(_scenario("trust-degradation","Trust degradation","Recent repeated contradictory behavior degrades relevant dimensions without erasing prior evidence."),{}),
 "trust-rebuilding":(_scenario("trust-rebuilding","Trust rebuilding","Observed corrected behavior starts repair; promises and apologies alone do not alter reliability history."),{}),
}

ONE_SUCCESS=TrustHistory("one-success","Alex",(
 e("s1","Week 1",D.COMMITMENT_RELIABILITY,P.POSITIVE,"First assigned task completed.",("Morgan",),scenario="one-success"),),{
 D.COMMITMENT_RELIABILITY:DimensionInterpretation(S.INSUFFICIENT_EVIDENCE,"One success is positive evidence, not an established reputation."),})
ONE_MISTAKE=derived("one-mistake",(
 e("m1","Week 7",D.HANDOFF_RELIABILITY,P.NEGATIVE,"Significant handoff error reported immediately.",scenario="one-mistake"),
 e("m2","Week 7",D.OWNERSHIP,P.POSITIVE,"Error owned, corrected, and recurrence prevention documented.",scenario="one-mistake"),),{
 **SIX_WEEK.interpretations,
 D.HANDOFF_RELIABILITY:DimensionInterpretation(S.MIXED,"The significant mistake matters, while reporting, correction, prior history, and prevention keep it from becoming a universal reputation."),})
COMPETENCE_BOUNDARY=TrustHistory("competence-coordination","Alex",(
 e("c1","Week 1",D.TECHNICAL_JUDGMENT,P.POSITIVE,"Hard production fault diagnosed accurately.",scenario="competence-coordination"),
 e("c2","Week 2",D.TECHNICAL_JUDGMENT,P.POSITIVE,"High-quality fix passed review and validation.",scenario="competence-coordination"),
 e("c3","Week 3",D.HANDOFF_RELIABILITY,P.NEGATIVE,"Handoff missed.",scenario="competence-coordination"),
 e("c4","Week 4",D.HANDOFF_RELIABILITY,P.NEGATIVE,"Status and interface change arrived late.",scenario="competence-coordination"),
 e("c5","Week 4",D.DECISION_CREDIBILITY,P.NEGATIVE,"Unsupported estimate was contradicted by the outcome.",scenario="competence-coordination"),),{
 D.TECHNICAL_JUDGMENT:DimensionInterpretation(S.ESTABLISHED,"Repeated diagnoses and validated fixes support technical judgment."),
 D.HANDOFF_RELIABILITY:DimensionInterpretation(S.DEGRADED,"Repeated missed coordination evidence remains separate from technical quality."),
 D.DECISION_CREDIBILITY:DimensionInterpretation(S.INSUFFICIENT_EVIDENCE,"One contradicted claim is retained but does not define a complete reputation."),})
DOMAIN_TRANSFER=TrustHistory("domain-transfer", "Alex", SIX_WEEK.evidence, {
 D.COMMITMENT_RELIABILITY:SIX_WEEK.interpretations[D.COMMITMENT_RELIABILITY],
 D.RISK_VISIBILITY:SIX_WEEK.interpretations[D.RISK_VISIBILITY],
 D.HANDOFF_RELIABILITY:SIX_WEEK.interpretations[D.HANDOFF_RELIABILITY],
 D.DECISION_CREDIBILITY:DimensionInterpretation(S.INSUFFICIENT_EVIDENCE,"Current-scope IC reliability is established; cross-team leadership and high-impact architecture remain unobserved."),})
CAPACITY_HANDLING=TrustHistory("capacity-handling","Alex",(
 e("p1","Week 1",D.RISK_VISIBILITY,P.POSITIVE,"Capacity impact communicated before delivery risk.",("Morgan",),scenario="capacity-handling"),
 e("p2","Week 1",D.COMMITMENT_RELIABILITY,P.POSITIVE,"Realistic revised commitment recorded.",("Morgan","Jordan"),Source.SHARED_ARTIFACT,"capacity-handling"),
 e("p3","Week 2",D.COMMITMENT_RELIABILITY,P.POSITIVE,"Revised follow-up completed.",("Morgan","Jordan"),Source.SHARED_ARTIFACT,"capacity-handling"),),{
 D.RISK_VISIBILITY:DimensionInterpretation(S.INSUFFICIENT_EVIDENCE,"Professional impact was visible; private cause was neither needed nor recorded."),
 D.COMMITMENT_RELIABILITY:DimensionInterpretation(S.ESTABLISHED,"Revision and later follow-through are observable professional handling evidence."),})
AUTONOMY_EXPANSION=TrustHistory("autonomy-expansion","Alex",SIX_WEEK.evidence,{
 D.COMMITMENT_RELIABILITY:SIX_WEEK.interpretations[D.COMMITMENT_RELIABILITY],
 D.RISK_VISIBILITY:SIX_WEEK.interpretations[D.RISK_VISIBILITY],
 D.DECISION_CREDIBILITY:DimensionInterpretation(S.INSUFFICIENT_EVIDENCE,"Morgan may reduce routine updates based on relevant IC evidence, while preserving consultation thresholds; expansion is not guaranteed."),})

HISTORIES.update({x.scenario_id:x for x in (ONE_SUCCESS,ONE_MISTAKE,COMPETENCE_BOUNDARY,DOMAIN_TRANSFER,CAPACITY_HANDLING,AUTONOMY_EXPANSION)})
SCENARIOS.update({
 "one-success":(_scenario("one-success","One success","A first success is evidence, not an established pattern."),{}),
 "one-mistake":(_scenario("one-mistake","One handled mistake","A mistake and its reporting, ownership, correction, and prevention all remain evidence."),{}),
 "competence-coordination":(_scenario("competence-coordination","Competence and coordination","Strong technical judgment coexists with weak handoff reliability."),{}),
 "domain-transfer":(_scenario("domain-transfer","Trust transfer boundary","Established individual-contributor evidence does not prove first-time cross-team leadership."),{}),
 "capacity-handling":(_scenario("capacity-handling","Private boundary and professional handling","Only capacity impact, revision, and follow-through enter trust history; private cause does not."),{}),
 "autonomy-expansion":(_scenario("autonomy-expansion","Evidence-linked autonomy","Repeated routine ownership and risk visibility can support fewer routine updates while consultation boundaries remain."),{}),
})
