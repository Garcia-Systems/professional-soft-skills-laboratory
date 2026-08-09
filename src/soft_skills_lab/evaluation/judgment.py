"""Contextual Chapter 23 evaluation using authored factors, never a score."""
from soft_skills_lab.domain.models import EvaluationCriterion,EvaluationResult,Outcome,ProfessionalResponse,WorkplaceScenario
CRITERIA=tuple(EvaluationCriterion(*x) for x in (
("matches-action-to-risk","Chosen response fits potential harm."),("matches-action-to-authority","Actor stays within delegated rights or routes appropriately."),("considers-reversibility","Evidence threshold reflects reversibility."),("considers-delay-cost","Waiting consequences are considered."),("uses-available-evidence-before-acting","Cheap relevant evidence is gathered when time permits."),("acts-before-certainty-when-risk-requires","Material containment does not await perfect certainty."),("refuses-boundary-violation","Explicit safety, security, or integrity constraints are preserved."),("uses-proportional-escalation","Escalation fits the issue."),("allows-multiple-defensible-options","Context may admit more than one acceptable response."),("judges-from-known-at-the-time","Outcome does not rewrite prior evidence.")))
def evaluate_judgment_response(scenario:WorkplaceScenario,response:ProfessionalResponse,at="T2"):
 if not scenario.judgment_contexts: raise ValueError("judgment evaluation requires a judgment context")
 authored=dict(response.judgment_outcomes)
 for point,values in response.contextual_judgment_outcomes:
  if point.upper()==at.upper(): authored=dict(values); break
 if not authored: authored={c.criterion_id:Outcome.PARTIAL for c in CRITERIA}
 return tuple(EvaluationResult(c,authored.get(c.criterion_id,Outcome.PARTIAL),"Evaluated against explicit facts, risk, authority, reversibility, delay, and policy at "+at+"; no judgment score is calculated.",(response.message,)) for c in CRITERIA)

def evidence_for_judgment(response:ProfessionalResponse):
 """Translate authored behavior into the shared observable trust-event history."""
 from soft_skills_lab.trust import TrustEvent,TrustEventKind
 kinds={
  "acted_within_authority":TrustEventKind.ACTED_WITHIN_AUTHORITY,
  "escalated_material_risk":TrustEventKind.MATERIAL_RISK_ESCALATED_WITH_JUDGMENT,
  "used_reversible_experiment":TrustEventKind.REVERSIBLE_EXPERIMENT_USED,
  "refused_boundary_violation":TrustEventKind.BOUNDARY_VIOLATION_REFUSED,
  "surfaced_tradeoff":TrustEventKind.TRADEOFF_SURFACED,
  "adjusted_decision_after_new_evidence":TrustEventKind.DECISION_ADJUSTED_AFTER_NEW_EVIDENCE,
  "documented_rationale":TrustEventKind.JUDGMENT_RATIONALE_DOCUMENTED,
  "unnecessary_escalation":TrustEventKind.UNNECESSARY_ESCALATION,
  "material_risk_ignored":TrustEventKind.MATERIAL_RISK_IGNORED,
  "irreversible_action_under_unresolved_ambiguity":TrustEventKind.IRREVERSIBLE_ACTION_UNDER_AMBIGUITY,
  "unauthorized_commitment":TrustEventKind.UNAUTHORIZED_COMMITMENT,
  "unsafe_shortcut":TrustEventKind.UNSAFE_SHORTCUT,
  "falsified_validation":TrustEventKind.VALIDATION_FALSIFIED,
 }
 return tuple(TrustEvent(kinds[item],f"{response.label}: {item.replace('_',' ')}.") for item in response.trust_evidence if item in kinds)
