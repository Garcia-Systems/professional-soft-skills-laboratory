from dataclasses import replace

import pytest

from soft_skills_lab.cli import main
from soft_skills_lab.domain.models import MeasurementKind, PerformancePlanStatus, ProfessionalResponse
from soft_skills_lab.evaluation.performance import evaluate_performance_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.scenarios.performance import PLAN
from soft_skills_lab.trust import PERFORMANCE_PLAN_EVENTS


def outcomes(scenario_id, response_id):
    scenario = get_scenario(scenario_id)
    return {r.criterion.criterion_id: r.outcome.value for r in evaluate_performance_response(scenario, get_response(scenario_id, response_id))}


def test_performance_concern_and_plan_are_distinct_and_observable():
    concern = PLAN.concerns[0]
    assert concern.claim != concern.supporting_examples[0]
    assert concern.expected_behavior != concern.measurement.statement
    assert concern.unsupported_generalizations == ("Alex never communicates.",)
    assert concern.measurement.kind is MeasurementKind.OBSERVABLE_BEHAVIOR
    assert concern.measurement.within_reasonable_control
    assert PLAN.status is PerformancePlanStatus.ACTIVE
    assert PLAN.duration_days == 30
    assert [c.day for c in PLAN.checkpoints] == [7, 14, 21, 30]


@pytest.mark.parametrize("kind,statement", [
    (MeasurementKind.ACTIVITY, "Send five status messages per day."),
    (MeasurementKind.PERSONALITY, "Show more confidence."),
    (MeasurementKind.OUTCOME_ONLY, "Never miss a deadline."),
])
def test_weak_measurement_kinds_are_not_behavior_measurements(kind, statement):
    assert kind is not MeasurementKind.OBSERVABLE_BEHAVIOR
    assert statement != PLAN.concerns[0].measurement.statement


@pytest.mark.parametrize("response_id", ["panic-resignation", "total-denial"])
def test_assumed_outcome_and_denial_do_not_build_a_plan(response_id):
    result = outcomes("communication-visibility", response_id)
    assert set(result.values()) == {"FAIL"}


@pytest.mark.parametrize("response_id", ["automatic-confession", "argue-every-example", "vague-promise", "passive-signoff"])
def test_incomplete_paths_do_not_establish_measurement_or_checkpoints(response_id):
    result = outcomes("communication-visibility", response_id)
    assert result["establishes-measurement"] == "FAIL"
    assert result["establishes-checkpoints"] == "FAIL"


def test_clarification_and_execution_have_different_stages():
    clarified = outcomes("communication-visibility", "clarify-and-plan")
    executed = outcomes("communication-visibility", "execute-and-demonstrate")
    assert clarified["establishes-measurement"] == "PASS"
    assert clarified["demonstrates-improvement"] == "PARTIAL"
    assert set(executed.values()) == {"PASS"}


def test_behaviorally_equivalent_wording_uses_structured_semantics():
    original = get_response("communication-visibility", "clarify-and-plan")
    rewritten = replace(original, response_id="rewritten", message="Different words, same authored behavior.")
    assert [r.outcome for r in evaluate_performance_response(get_scenario("communication-visibility"), original)] == [r.outcome for r in evaluate_performance_response(get_scenario("communication-visibility"), rewritten)]


def test_vague_plan_is_not_actionable_until_clarified():
    scenario = get_scenario("vague-performance-plan")
    assert not scenario.known_facts
    result = outcomes(scenario.scenario_id, "clarify-observable-plan")
    assert result["clarifies-performance-expectation"] == result["establishes-measurement"] == "PASS"


def test_factual_correction_does_not_reject_supported_feedback():
    response = get_response("performance-factual-error", "correct-and-engage")
    assert response.corrects_material_inaccuracy
    assert response.acknowledges_supported_evidence
    assert outcomes("performance-factual-error", response.response_id)["clarifies-performance-expectation"] == "PASS"


def test_outcome_only_expectation_is_replaced_with_controllable_behavior():
    result = outcomes("impossible-performance-expectation", "propose-controllable-measures")
    assert result["focuses-on-controllable-behavior"] == "PASS"
    assert result["establishes-measurement"] == "PASS"


def test_personal_capacity_updates_work_without_erasing_plan_history():
    response = get_response("performance-plan-capacity", "update-impact-and-plan")
    assert response.identifies_work_impact and response.revises_commitment_explicitly
    assert response.tracks_evidence_over_time and response.preserves_plan_scope


def test_new_formal_expectation_must_remain_explicit():
    assert outcomes("changing-performance-scope", "clarify-new-scope")["preserves-plan-scope"] == "PASS"


def test_checkpoint_rating_disagreement_uses_criteria_and_history_not_effort():
    response = get_response("performance-rating-disagreement", "review-criteria-and-continue")
    assert response.seeks_specific_understanding
    assert response.tracks_evidence_over_time and response.preserves_plan_scope
    assert "trying" not in response.message.lower()


def test_checkpoint_history_distinguishes_absence_from_demonstration_and_patterns():
    day7, day14, day30 = PLAN.checkpoints[0], PLAN.checkpoints[1], PLAN.checkpoints[3]
    assert "not yet been exercised" in day7.unresolved_gaps[0]
    assert "relevant conditions" in day14.improvement_observed[0]
    assert day30.improvement_observed and day30.unresolved_gaps
    assert len(PLAN.history) > 1


def test_effort_and_message_volume_are_not_demonstrated_improvement():
    effort = ProfessionalResponse("effort", "Effort", "I'm trying hard.")
    result = {r.criterion.criterion_id: r.outcome.value for r in evaluate_performance_response(get_scenario("communication-visibility"), effort)}
    assert result["demonstrates-improvement"] == "FAIL"
    assert PLAN.concerns[2].measurement.statement != "Send five status messages per day."


def test_plan_has_no_termination_prediction_and_acceptance_is_not_total_agreement():
    scenario = get_scenario("communication-visibility")
    assert any("not established" in item for item in scenario.uncertainties)
    assert get_response(scenario.scenario_id, "clarify-and-plan").preserves_respectful_disagreement
    assert "Technical delivery completed" in PLAN.positive_evidence[0]
    assert PLAN.concerns  # technical success and communication gaps coexist


def test_trust_records_behavior_not_emotion():
    labels = " ".join(event.kind.label.lower() for event in PERFORMANCE_PLAN_EVENTS)
    assert "anxiety" not in labels and "fear" not in labels and "confidence" not in labels
    assert "risk visibility improved" in labels and "feedback applied" in labels


@pytest.mark.parametrize("argv,expected", [
    (["performance-plan", "communication-visibility"], "SUCCESS CONDITION"),
    (["performance-evidence", "communication-visibility"], "UNSUPPORTED OR OVERBROAD CLAIMS"),
    (["checkpoint", "communication-visibility", "--day", "14"], "material risk"),
    (["compare", "communication-visibility"], "execute-and-demonstrate"),
])
def test_deterministic_inspection_commands(capsys, argv, expected):
    main(argv)
    first = capsys.readouterr().out
    main(argv)
    second = capsys.readouterr().out
    assert first == second
    assert expected.lower() in first.lower()
