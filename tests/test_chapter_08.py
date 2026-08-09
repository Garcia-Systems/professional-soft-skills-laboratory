from dataclasses import replace

from soft_skills_lab.cli import _learning_text, _responsibility_text
from soft_skills_lab.domain.models import Outcome
from soft_skills_lab.evaluation.responsibility import evaluate_responsibility_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.scenarios.responsibility import MISSED_HANDOFF_COMMITMENT
from soft_skills_lab.trust import ProfessionalTrust, RESPONSIBILITY_LEARNING_EVENTS, TrustEventKind


def outcomes(scenario_id, response_id):
    return {r.criterion.criterion_id: r.outcome for r in evaluate_responsibility_response(
        get_scenario(scenario_id), get_response(scenario_id, response_id))}


def test_responsibility_decomposes_control_contribution_context_and_result():
    responsibility = get_scenario("skipped-validation").responsibility_map
    alex, jordan = responsibility.boundaries
    assert "Skipped required" in alex.controlled[1]
    assert "Authorship" in alex.did_not_control[0]
    assert "Authored" in jordan.controlled[0]
    assert "manual" in responsibility.process_conditions[0]
    assert "would have detected" in responsibility.results[1]


def test_seven_paths_expose_distinct_observable_behavior():
    assert outcomes("skipped-validation", "deny")["does-not-shift-blame"] is Outcome.FAIL
    assert outcomes("skipped-validation", "blame-process")["identifies-preventive-action"] is Outcome.PASS
    assert outcomes("skipped-validation", "blame-process")["identifies-own-contribution"] is Outcome.FAIL
    assert outcomes("skipped-validation", "excuse-pressure")["preserves-agency"] is Outcome.FAIL
    assert outcomes("skipped-validation", "over-own")["does-not-over-own"] is Outcome.FAIL
    assert outcomes("skipped-validation", "over-own")["avoids-self-condemnation"] is Outcome.FAIL
    assert outcomes("skipped-validation", "empty-apology")["identifies-own-contribution"] is Outcome.PARTIAL
    assert outcomes("skipped-validation", "empty-apology")["identifies-corrective-action"] is Outcome.FAIL
    assert outcomes("skipped-validation", "explanation-without-ownership")["identifies-own-contribution"] is Outcome.FAIL
    strong = outcomes("skipped-validation", "accurate-ownership")
    assert all(value is Outcome.PASS for value in strong.values())


def test_context_and_responsibility_coexist_but_pressure_can_erase_agency():
    assert outcomes("skipped-validation", "accurate-ownership")["uses-context-without-erasing-responsibility"] is Outcome.PASS
    assert outcomes("skipped-validation", "excuse-pressure")["uses-context-without-erasing-responsibility"] is Outcome.FAIL


def test_process_weakness_and_individual_responsibility_both_remain_visible():
    scenario = get_scenario("skipped-validation")
    assert "manual" in scenario.responsibility_map.process_conditions[0]
    assert get_response("skipped-validation", "accurate-ownership").identifies_own_contribution


def test_accidental_outcome_still_has_responsibility_without_malicious_intent():
    responsibility = get_scenario("skipped-validation").responsibility_map
    assert "intended" in responsibility.not_supported[1]
    assert "Skipped" in responsibility.boundaries[0].controlled[1]


def test_corrective_action_hierarchy_is_separate_and_containment_first():
    response = get_response("skipped-validation", "accurate-ownership")
    assert response.prioritizes_containment
    assert response.identifies_corrective_action
    assert response.identifies_preventive_action
    assert not get_response("skipped-validation", "blame-process").prioritizes_containment


def test_missed_handoff_reuses_commitment_and_loop_closure():
    scenario = get_scenario("missed-handoff")
    assert MISSED_HANDOFF_COMMITMENT.expected_completion == 4
    assert scenario.commitments[0].owner == "Alex"
    strong = get_response("missed-handoff", "own-and-recover")
    assert strong.loop_closed and strong.acknowledges_impact
    assert outcomes("missed-handoff", "jordan-could-ask")["does-not-shift-blame"] is Outcome.FAIL


def test_shared_responsibility_does_not_force_total_causation():
    scenario = get_scenario("shared-responsibility")
    assert len(scenario.responsibility_map.boundaries) == 3
    assert "alone" in scenario.responsibility_map.not_supported[0]
    result = outcomes("shared-responsibility", "bounded-ownership")
    assert result["identifies-own-contribution"] is Outcome.PASS
    assert result["does-not-over-own"] is Outcome.PASS


def test_bad_outcome_is_not_proof_of_personal_fault():
    scenario = get_scenario("unavoidable-outcome")
    assert "every required validation" in scenario.known_facts[0]
    result = outcomes("unavoidable-outcome", "evidence-bounded")
    assert result["identifies-own-contribution"] is Outcome.PASS
    assert result["does-not-over-own"] is Outcome.PASS


def test_semantics_not_magic_apology_wording_drive_evaluation():
    original = get_response("skipped-validation", "accurate-ownership")
    paraphrase = replace(original, message="Different words with the same authored professional behavior.")
    scenario = get_scenario("skipped-validation")
    assert [r.outcome for r in evaluate_responsibility_response(scenario, original)] == [
        r.outcome for r in evaluate_responsibility_response(scenario, paraphrase)]
    assert outcomes("skipped-validation", "equivalent-ownership") == outcomes("skipped-validation", "accurate-ownership")


def test_later_behavior_is_stronger_trust_evidence_than_words_alone():
    trust = ProfessionalTrust()
    for event in RESPONSIBILITY_LEARNING_EVENTS:
        trust = trust.record(event)
    assert TrustEventKind.CHANGED_BEHAVIOR_DEMONSTRATED in [e.kind for e in trust.history]
    assert trust.history[-1].kind is TrustEventKind.IMPACTED_PARTY_FOLLOWED_UP
    assert get_response("responsibility-follow-up", "demonstrated-learning").demonstrated_improvement
    assert not get_response("skipped-validation", "accurate-ownership").demonstrated_improvement


def test_responsibility_and_learning_inspection_are_deterministic():
    first = _responsibility_text("skipped-validation")
    assert first == _responsibility_text("skipped-validation")
    assert "ALEX'S CONTRIBUTION" in first and "NOT SUPPORTED" in first
    learning = _learning_text("responsibility-follow-up")
    assert "Verbal ownership alone" in learning and "Changed behavior demonstrated" in learning


def test_model_does_not_score_emotion_personality_or_intent():
    fields = get_response("skipped-validation", "accurate-ownership").__dataclass_fields__
    forbidden = ("guilt", "shame", "confidence", "remorse", "personality", "self_esteem")
    assert not any(term in name for name in fields for term in forbidden)
