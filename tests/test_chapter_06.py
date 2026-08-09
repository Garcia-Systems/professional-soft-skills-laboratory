from dataclasses import replace

from soft_skills_lab.cli import _comparison_text, _evidence_text, _uncertainty_text
from soft_skills_lab.domain.models import Outcome, ProfessionalResponse, UncertaintyKind
from soft_skills_lab.evaluation import evaluate_uncertainty_response
from soft_skills_lab.scenarios import get_response, get_scenario


def outcomes(scenario_id: str, response_id: str) -> dict[str, Outcome]:
    scenario = get_scenario(scenario_id)
    return {result.criterion.criterion_id: result.outcome
            for result in evaluate_uncertainty_response(scenario, get_response(scenario_id, response_id))}


def test_uncertainty_kinds_remain_distinct():
    assert get_scenario("profile-update-failure").evidence_context.uncertainty.kind is UncertaintyKind.UNKNOWN
    assert get_scenario("profile-fix-estimate").evidence_context.uncertainty.kind is UncertaintyKind.UNKNOWABLE_FROM_CURRENT_EVIDENCE
    assert get_scenario("migration-safety-unknown").evidence_context.uncertainty.kind is UncertaintyKind.NOT_YET_INVESTIGATED
    assert get_scenario("judgment-under-pressure").evidence_context.uncertainty.kind is UncertaintyKind.UNCERTAIN


def test_facts_and_hypotheses_are_separate_and_deterministic():
    context = get_scenario("profile-update-failure").evidence_context
    assert context.established_facts[0] == "14 of 1,200 profile updates failed."
    assert context.hypotheses[0].statement not in context.established_facts
    assert _evidence_text("profile-update-failure") == _evidence_text("profile-update-failure")
    assert "CURRENT HYPOTHESES" in _evidence_text("profile-update-failure")


def test_bluff_and_defensive_certainty_exceed_evidence():
    assert outcomes("profile-update-failure", "bluff")["does-not-exceed-evidence"] is Outcome.FAIL
    assert outcomes("profile-update-failure", "defensive-certainty")["does-not-exceed-evidence"] is Outcome.FAIL
    assert get_response("profile-update-failure", "defensive-certainty").assigns_unsupported_blame


def test_empty_unknown_is_truthful_not_incompetent_but_does_not_stop_the_work():
    result = outcomes("profile-update-failure", "empty-unknown")
    assert result["states-uncertainty-explicitly"] is Outcome.PASS
    assert result["does-not-exceed-evidence"] is Outcome.PASS
    assert result["connects-uncertainty-to-next-action"] is Outcome.FAIL


def test_hypothesis_requires_label_and_basis():
    speculative = outcomes("profile-update-failure", "speculative-answer")
    bounded = outcomes("profile-update-failure", "bounded-hypothesis")
    assert speculative["labels-hypothesis"] is Outcome.FAIL
    assert bounded["labels-hypothesis"] is Outcome.PASS
    assert bounded["provides-evidence-basis"] is Outcome.PASS


def test_more_detail_does_not_remove_uncertainty():
    result = outcomes("profile-update-failure", "investigation-dump")
    assert get_response("profile-update-failure", "investigation-dump").implementation_details
    assert result["states-uncertainty-explicitly"] is Outcome.FAIL


def test_bounded_uncertainty_carries_missing_evidence_action_and_update():
    result = outcomes("profile-update-failure", "bounded-uncertainty")
    assert all(value is Outcome.PASS for value in result.values())
    text = _uncertainty_text("profile-update-failure")
    assert text == _uncertainty_text("profile-update-failure")
    assert "CURRENT ANSWER\nUnknown" in text and "NEXT UPDATE\nT4" in text


def test_behavioral_equivalence_does_not_depend_on_wording():
    original = get_response("profile-update-failure", "bounded-uncertainty")
    paraphrase = replace(original, message="Cause remains open; here is the evidence and my T4 investigation update.")
    assert evaluate_uncertainty_response(get_scenario("profile-update-failure"), original) == evaluate_uncertainty_response(get_scenario("profile-update-failure"), paraphrase)


def test_learning_point_estimate_is_not_final_delivery_estimate():
    learning = get_response("profile-fix-estimate", "learning-point")
    false = get_response("profile-fix-estimate", "false-estimate")
    assert learning.estimate_for == "learning-point"
    assert false.estimate_for == "final-delivery"
    assert outcomes("profile-fix-estimate", "learning-point")["establishes-follow-up"] is Outcome.PASS
    assert outcomes("profile-fix-estimate", "false-estimate")["does-not-exceed-evidence"] is Outcome.FAIL


def test_judgment_can_coexist_with_uncertainty_under_pressure():
    response = get_response("judgment-under-pressure", "bounded-judgment")
    result = outcomes("judgment-under-pressure", "bounded-judgment")
    assert response.offered_hypothesis and response.preserves_uncertainty
    assert result["labels-hypothesis"] is Outcome.PASS
    assert result["communicates-decision-impact"] is Outcome.PASS


def test_authority_does_not_create_evidence_or_require_junior_bluffing():
    scenario = get_scenario("migration-safety-unknown")
    response = get_response("migration-safety-unknown", "inspect-first")
    assert scenario.participants[0].role == "junior developer"
    assert scenario.participants[1].role == "senior engineering manager"
    assert not response.exceeds_available_evidence
    assert response.uncertainty_next_action


def test_customer_adaptation_preserves_truth_and_gives_safe_action():
    scenario = get_scenario("customer-payment-verification")
    response = get_response("customer-payment-verification", "customer-safe")
    assert scenario.evidence_context.uncertainty.kind is UncertaintyKind.UNKNOWABLE_FROM_CURRENT_EVIDENCE
    assert response.preserves_uncertainty and response.supports_decision
    assert "do not retry" in response.message.lower() and response.follow_up_point == 3


def test_primary_comparison_includes_all_six_paths():
    text = _comparison_text("profile-update-failure")
    for response_id in ("bluff", "defensive-certainty", "empty-unknown", "speculative-answer", "investigation-dump", "bounded-uncertainty"):
        assert response_id in text
