"""Chapter 23 invariants: judgment is contextual, inspectable, and non-numeric."""
from soft_skills_lab.cli import main
from soft_skills_lab.domain.models import Outcome,ProfessionalChoice
from soft_skills_lab.evaluation.judgment import evaluate_judgment_response,evidence_for_judgment
from soft_skills_lab.scenarios import get_response,get_scenario
from soft_skills_lab.trust import TrustEventKind

def outcomes(sid="production-timeout",rid="act-immediately",at="T2"):
 return {r.criterion.criterion_id:r.outcome for r in evaluate_judgment_response(get_scenario(sid),get_response(sid,rid),at)}

def test_context_represents_explicit_factors():
 c=get_scenario("production-timeout").judgment_contexts[0]
 assert (c.actor,c.time,c.urgency)==("Alex","T2","LOW")
 assert c.unknowns and c.decision_owner and c.delay_cost.startswith("LOW")
 assert "production impact" in c.reversibility
 assert len(c.options)==5

def test_same_action_different_context_changes_judgment():
 assert outcomes(at="T2")["matches-action-to-risk"] is Outcome.FAIL
 assert outcomes(at="T3")["matches-action-to-risk"] is Outcome.PASS

def test_investigate_t2_but_contain_t3():
 assert outcomes(rid="investigate-and-inform",at="T2")["uses-available-evidence-before-acting"] is Outcome.PASS
 assert outcomes(rid="investigate-and-inform",at="T3")["considers-delay-cost"] is Outcome.FAIL

def test_asking_not_always_safer_and_acting_not_universal():
 assert get_response("owned-unit-test","professional").professional_choice is ProfessionalChoice.ACT
 assert get_response("historical-data-cleanup","professional").professional_choice is ProfessionalChoice.PAUSE

def test_higher_risk_justifies_action_before_certainty():
 assert outcomes("risk-metadata-exposure","professional")["acts-before-certainty-when-risk-requires"] is Outcome.PASS

def test_manager_authority_stays_inside_security_boundary():
 assert get_response("manager-cosmetic-ship","professional").professional_choice is ProfessionalChoice.COMMIT
 unsafe=get_response("manager-unsafe-ship","professional")
 assert unsafe.professional_choice is ProfessionalChoice.REFUSE
 assert "refused_boundary_violation" in unsafe.trust_evidence

def test_waiting_is_a_choice_and_reversible_action_can_proceed():
 r=get_response("release-window-uncertainty","professional")
 assert r.professional_choice is ProfessionalChoice.ACT
 assert outcomes("release-window-uncertainty","professional")["considers-delay-cost"] is Outcome.PASS

def test_irreversibility_raises_evidence_threshold():
 r=get_response("historical-data-cleanup","professional")
 assert r.professional_choice is ProfessionalChoice.PAUSE
 assert outcomes("historical-data-cleanup","professional")["considers-reversibility"] is Outcome.PASS

def test_collaboration_commitment_and_safe_default_coexist():
 assert get_response("bounded-teammate-help","professional").professional_choice is ProfessionalChoice.ACT
 assert get_response("safe-default-requirement","professional").professional_choice is ProfessionalChoice.ACT

def test_refusal_differs_from_disagreement_and_no_exposes_tradeoff():
 assert get_response("falsify-validation","professional").professional_choice is ProfessionalChoice.REFUSE
 assert get_response("scheduled-export-scope","professional").professional_choice is ProfessionalChoice.SAY_NO

def test_multiple_options_are_defensible():
 r=outcomes("defensible-implementation","professional")
 assert r["allows-multiple-defensible-options"] is Outcome.PASS

def test_hindsight_does_not_replace_known_at_time():
 assert outcomes("reasonable-bad-outcome","professional")["judges-from-known-at-the-time"] is Outcome.PASS
 assert outcomes("reckless-good-outcome","professional")["judges-from-known-at-the-time"] is Outcome.PASS

def test_record_preserves_decision_time_evidence():
 r=get_scenario("production-timeout").judgment_record
 assert r and r.time=="T2" and r.later_outcome.startswith("At T3")

def test_trust_has_judgment_evidence_without_judgment_score():
 assert TrustEventKind.ACTED_WITHIN_AUTHORITY.weight > 0
 assert TrustEventKind.UNSAFE_SHORTCUT.weight < 0
 assert evidence_for_judgment(get_response("manager-unsafe-ship","professional"))[0].kind is TrustEventKind.BOUNDARY_VIOLATION_REFUSED
 assert not hasattr(get_scenario("production-timeout"),"judgment_score")

def test_cli_inspections_are_deterministic(capsys):
 assert main(["judgment","production-timeout","--at","T2"])==0
 first=capsys.readouterr().out
 assert "INVESTIGATE + INFORM" in first and "DELAY COST" in first
 main(["judgment-options","production-timeout","--at","T2"]); options=capsys.readouterr().out
 assert "Acceptable: FAIL" in options and "not numerically ranked" in options
 main(["judgment-record","production-timeout"]); record=capsys.readouterr().out
 assert "FACTS KNOWN AT THE TIME" in record and "does not retroactively" in record
