import pytest

from soft_skills_lab.cli import main
from soft_skills_lab.domain.models import DisclosureBoundary, WorkCapacity
from soft_skills_lab.evaluation.personal_capacity import evaluate_personal_capacity_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.trust import PERSONAL_CAPACITY_EVENTS


def outcomes(scenario_id, response_id):
    scenario = get_scenario(scenario_id)
    return {result.criterion.criterion_id: result.outcome.value for result in
            evaluate_personal_capacity_response(scenario, get_response(scenario_id, response_id))}


def test_work_impact_keeps_private_cause_out_of_professional_model():
    impact = get_scenario("personal-capacity").work_impact
    assert impact.current_capacity is WorkCapacity.REDUCED
    assert impact.manager_visibility_needed
    assert impact.revised_commitment.original_commitment == "Verification integration at T8"
    assert impact.revised_commitment.new_commitment == "Final review at T9"
    assert impact.revised_commitment.reason_category == "capacity change"
    assert "Exact nature" in impact.private_details[0]
    assert all("diagnosis" not in item.lower() for item in impact.observed_work_impact)
    assert {item.value for item in DisclosureBoundary} == {"PRIVATE", "OPTIONAL_CONTEXT", "WORK_RELEVANT", "REQUIRED_FOR_REQUEST"}


@pytest.mark.parametrize("response_id, expected", [
    ("hide-everything", {"identifies-work-impact": "FAIL", "preserves-reasonable-privacy": "PASS", "updates-dependencies": "FAIL"}),
    ("overshare", {"identifies-work-impact": "PASS", "preserves-reasonable-privacy": "FAIL", "requests-specific-support": "PARTIAL"}),
    ("vague-personal-problem", {"identifies-work-impact": "PARTIAL", "revises-commitment-explicitly": "FAIL"}),
    ("explanation-without-plan", {"identifies-work-impact": "PASS", "revises-commitment-explicitly": "FAIL"}),
    ("unsupported-reassurance", {"preserves-uncertainty": "FAIL", "establishes-next-update": "FAIL"}),
    ("disappear", {"identifies-work-impact": "FAIL", "updates-dependencies": "FAIL"}),
    ("bounded-professional-disclosure", {"identifies-work-impact": "PASS", "preserves-reasonable-privacy": "PASS", "requests-specific-support": "PASS", "revises-commitment-explicitly": "PASS", "updates-dependencies": "PASS", "preserves-uncertainty": "PASS", "establishes-next-update": "PASS"}),
    ("early-support-request", {"communicates-risk": "PASS", "requests-specific-support": "PASS"}),
])
def test_primary_paths(response_id, expected):
    actual = outcomes("personal-capacity", response_id)
    assert all(actual[key] == value for key, value in expected.items())


def test_behavioral_equivalence_is_authored_not_word_matching():
    a = outcomes("personal-capacity", "bounded-professional-disclosure")
    b = outcomes("personal-capacity", "equivalent-bounded")
    for criterion in ("identifies-work-impact", "preserves-reasonable-privacy", "requests-specific-support",
                      "revises-commitment-explicitly", "updates-dependencies", "communicates-risk"):
        assert a[criterion] == b[criterion] == "PASS"


@pytest.mark.parametrize("scenario_id,response_id,criterion", [
    ("one-day-availability", "proactive-reschedule", "updates-dependencies"),
    ("high-risk-capacity", "reassign-safely", "recognizes-task-safety"),
    ("recurring-capacity-impact", "durable-plan", "addresses-recurring-pattern"),
    ("urgent-personal-absence", "minimal-handoff", "preserves-reasonable-privacy"),
    ("intrusive-peer-question", "maintain-boundary", "updates-dependencies"),
    ("manager-capacity-question", "answer-operationally", "answers-legitimate-capacity-question"),
    ("formal-capacity-support", "use-formal-path", "uses-formal-path-when-needed"),
    ("revised-commitment-missed", "update-again", "revises-commitment-explicitly"),
])
def test_secondary_scenarios(scenario_id, response_id, criterion):
    assert outcomes(scenario_id, response_id)[criterion] == "PASS"


def test_capacity_states_are_operational_not_medical():
    assert {state.value for state in WorkCapacity} == {"FULL", "REDUCED", "UNAVAILABLE", "UNSAFE_FOR_HIGH_RISK_TASK"}
    assert get_scenario("high-risk-capacity").work_impact.current_capacity is WorkCapacity.UNSAFE_FOR_HIGH_RISK_TASK
    assert get_scenario("urgent-personal-absence").work_impact.current_capacity is WorkCapacity.UNAVAILABLE


def test_trust_history_contains_behavior_only():
    text = " ".join(event.detail.lower() for event in PERSONAL_CAPACITY_EVENTS)
    assert "private cause" in text
    for sensitive in ("diagnosis", "medical", "family", "substance", "relationship"):
        assert sensitive not in text


def test_deterministic_cli_inspections_and_scenarios(capsys):
    cases = ((["boundary", "personal-capacity"], "PRIVATE DETAILS"),
             (["work-impact", "personal-capacity"], "CURRENT PROFESSIONAL RISK\nAT_RISK"),
             (["compare", "personal-capacity"], "bounded-professional-disclosure"),
             (["evaluate", "one-day-availability", "proactive-reschedule"], "updates-dependencies"),
             (["evaluate", "high-risk-capacity", "reassign-safely"], "recognizes-task-safety"),
             (["evaluate", "urgent-personal-absence", "minimal-handoff"], "preserves-reasonable-privacy"),
             (["evaluate", "intrusive-peer-question", "maintain-boundary"], "updates-dependencies"),
             (["evaluate", "recurring-capacity-impact", "durable-plan"], "addresses-recurring-pattern"),
             (["evaluate", "revised-commitment-missed", "update-again"], "establishes-next-update"),
             (["personal-capacity-trust"], "no private cause is stored"))
    for args, expected in cases:
        assert main(args) == 0
        assert expected in capsys.readouterr().out
