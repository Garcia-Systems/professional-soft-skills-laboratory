"""Chapter 10: observable conflict, de-escalation, repair, and risk preservation."""

from dataclasses import replace

from soft_skills_lab.cli import _conflict_text
from soft_skills_lab.domain.models import ConflictStage, Outcome
from soft_skills_lab.evaluation.conflict import evaluate_conflict_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.trust import CONFLICT_EVENTS, ProfessionalTrust, TrustEventKind


def outcomes(scenario_id: str, response_id: str) -> dict[str, Outcome]:
    return {result.criterion.criterion_id: result.outcome for result in
            evaluate_conflict_response(get_scenario(scenario_id), get_response(scenario_id, response_id))}


def test_conflict_state_tracks_observable_signals_without_emotional_score():
    state = get_scenario("release-validation").conflict_state
    assert state.stage is ConflictStage.RISING_TENSION
    assert state.signals[0].generalization and state.signals[0].topic_expansion
    assert not hasattr(state, "emotion") and not hasattr(state, "intensity")


def test_disagreement_is_distinct_from_conflict_and_tension_proves_no_position_wrong():
    state = get_scenario("release-validation").conflict_state
    assert len(state.positions) == 2
    assert state.stage is not ConflictStage.DISAGREEMENT
    assert state.unresolved_decision  # tension supplies no decision outcome


def test_generalizing_counterattack_and_motive_attribution_are_structured_not_scanned():
    counter = get_response("release-validation", "counterattack")
    motive = get_response("release-validation", "motive-attack")
    assert counter.attacks_group and counter.generalizes_about_person
    assert outcomes("release-validation", "counterattack")["avoids-counterattack"] is Outcome.FAIL
    assert motive.attributes_motive_without_evidence
    assert outcomes("release-validation", "motive-attack")["avoids-unsupported-motive-attribution"] is Outcome.FAIL


def test_sarcasm_and_repetition_do_not_restore_evidence_or_decision_path():
    sarcasm = outcomes("release-validation", "sarcasm")
    repeated = outcomes("release-validation", "repeat-louder")
    assert sarcasm["avoids-counterattack"] is Outcome.FAIL
    assert sarcasm["restores-shared-facts"] is Outcome.FAIL
    assert repeated["refocuses-current-issue"] is Outcome.PASS
    assert repeated["creates-decision-path"] is Outcome.FAIL


def test_capitulation_ends_argument_without_resolving_issue_or_preserving_risk():
    response = get_response("release-validation", "capitulation")
    assert response.ends_argument and not response.resolves_issue
    assert response.concedes_decision and not response.preserves_material_risk


def test_de_escalation_preserves_disagreement_and_is_not_capitulation():
    response = get_response("release-validation", "de-escalate-and-refocus")
    result = outcomes("release-validation", response.response_id)
    assert response.states_specific_disagreement and not response.concedes_decision
    assert response.preserves_material_risk
    for criterion in ("avoids-counterattack", "acknowledges-legitimate-concern", "refocuses-current-issue",
                      "keeps-conflict-scoped", "restores-shared-facts", "creates-decision-path"):
        assert result[criterion] is Outcome.PASS


def test_acknowledgment_is_not_concession():
    response = get_response("release-validation", "de-escalate-and-refocus")
    assert response.acknowledges_legitimate_concern and not response.concedes_decision


def test_behaviorally_equivalent_wording_has_same_core_results():
    first = outcomes("release-validation", "de-escalate-and-refocus")
    variation = outcomes("release-validation", "de-escalate-variation")
    for criterion in ("avoids-counterattack", "refocuses-current-issue", "keeps-conflict-scoped",
                      "restores-shared-facts", "creates-decision-path", "preserves-material-risk"):
        assert first[criterion] == variation[criterion] == Outcome.PASS


def test_productive_pause_is_not_avoidance_and_establishes_follow_up():
    productive = get_response("release-validation", "pause-and-resume")
    avoidant = get_response("release-validation", "avoid-indefinitely")
    assert productive.pauses_conversation and productive.follow_up_point == 4
    assert outcomes("release-validation", "pause-and-resume")["uses-pause-productively"] is Outcome.PASS
    assert outcomes("release-validation", "avoid-indefinitely")["uses-pause-productively"] is Outcome.FAIL
    assert not avoidant.pause_has_checkpoint


def test_code_review_repair_proves_one_bad_response_does_not_prevent_recovery():
    response = get_response("code-review-conflict", "restore-technical-question")
    result = outcomes("code-review-conflict", response.response_id)
    assert response.repairs_own_contribution and response.identifies_own_contribution
    assert result["repairs-own-contribution"] is Outcome.PASS
    assert result["refocuses-current-issue"] is Outcome.PASS


def test_code_review_escalation_defense_and_withdrawal_are_not_repair():
    for response_id in ("escalate-insult", "defend-competence", "withdraw"):
        assert outcomes("code-review-conflict", response_id)["repairs-own-contribution"] is Outcome.FAIL


def test_manager_pressure_changes_with_issue_kind():
    ordinary = get_response("manager-tradeoff-conflict", "confirm-and-proceed")
    material = get_response("manager-material-risk", "document-and-escalate")
    suppressed = get_response("manager-material-risk", "suppress-risk")
    assert ordinary.respects_decision_ownership and ordinary.resolves_issue
    assert material.escalates_material_risk and material.preserves_material_risk
    assert outcomes("manager-material-risk", "document-and-escalate")["preserves-material-risk"] is Outcome.PASS
    assert outcomes("manager-material-risk", "suppress-risk")["preserves-material-risk"] is Outcome.FAIL
    assert suppressed.ends_argument  # manager frustration does not remove escalation duty


def test_public_conflict_changes_venue_without_erasing_accountability():
    response = get_response("public-deadline-conflict", "change-venue")
    assert response.pauses_conversation and response.pause_has_checkpoint
    assert response.follow_up_point == 5 and response.creates_decision_path
    assert outcomes("public-deadline-conflict", "change-venue")["uses-pause-productively"] is Outcome.PASS


def test_conflict_inspection_is_deterministic_and_restores_shared_facts():
    text = _conflict_text("release-validation")
    assert text == _conflict_text("release-validation")
    for heading in ("CURRENT DECISION", "SHARED FACTS", "CURRENT DISAGREEMENT", "CONFLICT-ADDING STATEMENTS", "NOT ESTABLISHED"):
        assert heading in text
    assert "Priya does not care about quality" in text


def test_calm_message_can_hide_risk_and_tension_can_end_in_sound_behavior():
    calm_bad = get_response("manager-material-risk", "suppress-risk")
    tense_good = get_response("release-validation", "de-escalate-and-refocus")
    assert not calm_bad.preserves_material_risk
    assert get_scenario("release-validation").conflict_state.stage is ConflictStage.RISING_TENSION
    assert tense_good.preserves_material_risk and tense_good.creates_decision_path


def test_outcome_is_evaluated_from_metadata_not_message_surface():
    response = replace(get_response("release-validation", "de-escalate-and-refocus"), message="Different authored wording.")
    result = {item.criterion.criterion_id: item.outcome for item in evaluate_conflict_response(get_scenario("release-validation"), response)}
    assert result["refocuses-current-issue"] is Outcome.PASS


def test_constructive_conflict_handling_adds_inspectable_trust_evidence():
    trust = ProfessionalTrust()
    for event in CONFLICT_EVENTS:
        trust = trust.record(event)
    assert trust.history == CONFLICT_EVENTS and trust.balance > 0
    assert {event.kind for event in trust.history} == {
        TrustEventKind.CONFLICT_REFOCUSED, TrustEventKind.OWN_ESCALATION_REPAIRED,
        TrustEventKind.MATERIAL_CONCERN_PRESERVED, TrustEventKind.DECISION_SUPPORTED_AFTER_RESOLUTION,
    }
