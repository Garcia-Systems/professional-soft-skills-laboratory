from soft_skills_lab.cli import _status_text, main
from soft_skills_lab.domain.models import Forecast, StatusCategory
from soft_skills_lab.evaluation.status_updates import evaluate_status_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.scenarios.status_updates import DECISION_USEFUL, STATUS_AUDIENCE_UPDATES


def outcomes(scenario_id: str, response_id: str):
    return {r.criterion.criterion_id: r.outcome.value for r in evaluate_status_response(
        get_scenario(scenario_id), get_response(scenario_id, response_id))}


def test_semantic_status_categories_are_explicit():
    assert {item.value for item in StatusCategory} == {"on_track", "at_risk", "blocked", "completed"}


def test_activity_is_not_progress_or_status():
    result = outcomes("integration-delivery", "activity-dump")
    assert result["states-current-state"] == "FAIL"
    assert result["communicates-material-progress"] == "FAIL"


def test_progress_alone_is_not_decision_useful_status():
    result = outcomes("integration-delivery", "over-detailed")
    assert result["communicates-material-progress"] == "PASS"
    assert result["states-current-state"] == "FAIL"
    assert result["avoids-unnecessary-detail"] == "FAIL"


def test_risk_is_needed_before_deadline_is_missed():
    result = outcomes("integration-delivery", "no-update")
    assert result["communicates-risk"] == "FAIL"
    assert result["communicates-dependency-impact"] == "FAIL"


def test_false_green_is_unsupported_certainty():
    response = get_response("integration-delivery", "false-green")
    assert response.unsupported_promise
    assert response.status_update.forecast.guaranteed
    assert outcomes("integration-delivery", "false-green")["provides-forecast-basis"] == "FAIL"


def test_vague_risk_is_partial_behavior():
    result = outcomes("integration-delivery", "vague-risk")
    assert result["communicates-risk"] == "PARTIAL"
    assert result["states-current-state"] == "FAIL"
    assert result["establishes-next-update"] == "FAIL"


def test_decision_useful_status_covers_planning_dimensions():
    result = outcomes("integration-delivery", "decision-useful")
    for criterion in ("states-current-state", "communicates-material-progress", "communicates-risk",
                      "communicates-dependency-impact", "labels-blocker-correctly",
                      "provides-forecast-basis", "establishes-next-update", "avoids-unnecessary-detail"):
        assert result[criterion] == "PASS"


def test_at_risk_is_not_blocked_when_work_can_continue():
    assert DECISION_USEFUL.current_state is StatusCategory.AT_RISK
    assert not DECISION_USEFUL.blockers
    assert DECISION_USEFUL.next_action


def test_forecast_is_not_a_promise():
    forecast = DECISION_USEFUL.forecast
    assert isinstance(forecast, Forecast)
    assert forecast.basis and forecast.condition
    assert not forecast.guaranteed


def test_audience_views_share_facts_and_underlying_status():
    views = tuple(STATUS_AUDIENCE_UPDATES.values())
    assert len({view.communicated_fact_ids for view in views}) == 1
    assert len({view.status_update for view in views}) == 1
    assert {view.response_id for view in views} == {"jordan", "morgan", "business"}


def test_true_blocker_names_ownership_impact_and_requested_action():
    response = get_response("credential-blocker", "actionable-escalation")
    result = outcomes("credential-blocker", "actionable-escalation")
    assert response.status_update.current_state is StatusCategory.BLOCKED
    assert response.status_update.dependency_owner == "Security team"
    assert result["labels-blocker-correctly"] == "PASS"
    assert result["requests-needed-action"] == "PASS"
    assert response.status_update.remaining_work == ("Production-like validation.",)


def test_passive_blocker_status_hides_ownership_and_action():
    result = outcomes("credential-blocker", "passive-status")
    assert result["states-current-state"] == "FAIL"
    assert result["requests-needed-action"] == "FAIL"


def test_completion_requires_loop_closure_for_dependent_teammate():
    assert outcomes("verification-completion", "silent-completion")["closes-loop"] == "FAIL"
    strong = get_response("verification-completion", "closed-loop")
    assert strong.status_update.current_state is StatusCategory.COMPLETED
    assert outcomes("verification-completion", "closed-loop")["closes-loop"] == "PASS"


def test_status_inspection_is_structured_and_deterministic():
    first = _status_text("integration-delivery", "decision-useful")
    assert first == _status_text("integration-delivery", "decision-useful")
    assert "CURRENT STATE\nAt Risk" in first
    assert "NEXT UPDATE\nT5" in first
    assert "Type: evidence-based estimate" in first


def test_cli_primary_comparison_and_blocker_inspection(capsys):
    assert main(["compare", "integration-delivery"]) == 0
    assert "decision-useful" in capsys.readouterr().out
    assert main(["status", "credential-blocker", "actionable-escalation"]) == 0
    output = capsys.readouterr().out
    assert "DEPENDENCY OWNER\nSecurity team" in output
    assert "NEEDED ACTION" in output


def test_different_wording_can_share_behavioral_semantics():
    jordan = STATUS_AUDIENCE_UPDATES["jordan"]
    morgan = STATUS_AUDIENCE_UPDATES["morgan"]
    assert jordan.message != morgan.message
    assert jordan.status_update == morgan.status_update

