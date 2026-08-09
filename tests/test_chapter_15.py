from dataclasses import replace
import pytest
from soft_skills_lab.cli import main
from soft_skills_lab.domain.models import IncidentState, RecoveryCheck
from soft_skills_lab.evaluation.incidents import evaluate_incident_behavior
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.trust import INCIDENT_EVENTS, TrustEventKind


def outcomes(response_id):
    return {x.criterion.criterion_id: x.outcome.value for x in evaluate_incident_behavior(get_response("payment-authorization", response_id))}


def test_incident_representation_keeps_distinctions_and_ownership():
    incident = get_scenario("payment-authorization").incident
    assert incident.state is IncidentState.ACTIVE
    assert incident.symptoms != incident.impact
    assert incident.established_facts != incident.hypotheses
    assert incident.coordinator == "Morgan" and incident.technical_owner == "Alex"
    assert "Full root cause." in incident.unknowns
    assert incident.coordinator not in " ".join(incident.hypotheses)


def test_lifecycle_requires_verified_recovery_and_review():
    active = get_scenario("payment-authorization").incident
    contained = active.transition(IncidentState.CONTAINED)
    recovering = contained.transition(IncidentState.RECOVERING)
    with pytest.raises(ValueError, match="recovery"):
        recovering.transition(IncidentState.RESOLVED)
    verified = replace(recovering, recovery_checks=tuple(RecoveryCheck(x.description, True) for x in recovering.recovery_checks))
    resolved = verified.transition(IncidentState.RESOLVED)
    assert resolved.transition(IncidentState.REVIEWED).state is IncidentState.REVIEWED
    with pytest.raises(ValueError):
        active.transition(IncidentState.RESOLVED)


@pytest.mark.parametrize("response_id, expected", [
    ("hide-and-fix", {"makes-incident-visible": "FAIL", "prioritizes-containment": "PASS"}),
    ("blame-first", {"separates-cause-from-hypothesis": "FAIL", "defers-blame-until-evidence": "FAIL"}),
    ("self-blame-first", {"prioritizes-containment": "FAIL"}),
    ("investigation-dump", {"states-observed-impact": "FAIL", "coordinates-affected-parties": "FAIL"}),
    ("premature-root-cause", {"separates-cause-from-hypothesis": "FAIL"}),
    ("silent-rollback", {"prioritizes-containment": "PASS", "makes-incident-visible": "FAIL"}),
    ("coordinated-incident-response", {"makes-incident-visible": "PASS", "prioritizes-containment": "PASS", "establishes-incident-ownership": "PASS"}),
    ("containment-then-learning", {"verifies-recovery": "PASS", "closes-incident-loop": "PASS", "creates-prevention-from-evidence": "PASS"}),
])
def test_primary_paths(response_id, expected):
    actual = outcomes(response_id)
    assert all(actual[key] == value for key, value in expected.items())


def test_behavioral_equivalence_not_word_matching():
    first = outcomes("coordinated-incident-response")
    second = outcomes("equivalent-coordinated")
    for criterion in ("makes-incident-visible", "states-observed-impact", "separates-cause-from-hypothesis",
                      "prioritizes-containment", "establishes-incident-ownership", "coordinates-affected-parties"):
        assert first[criterion] == second[criterion] == "PASS"


def test_containment_precedes_root_cause_and_rollback_is_judgment():
    incident = get_scenario("payment-authorization").incident
    assert incident.containment_actions and "Full root cause." in incident.unknowns
    assert "roll back" in incident.containment_actions[0]


def test_audience_views_share_truth_and_support_is_customer_safe(capsys):
    scenario = get_scenario("payment-authorization")
    views = dict(scenario.incident_audiences)
    assert set(views) == {"engineering", "manager", "business", "customer-support"}
    assert "HTTP 400" in " ".join(views["engineering"])
    assert "Members" in " ".join(views["customer-support"])
    assert "header is causing" not in " ".join(views["customer-support"])
    assert main(["incident-audience", "payment-authorization", "--audience", "customer-support"]) == 0
    assert "Next update T3" in capsys.readouterr().out


def test_high_risk_can_be_contained_before_diagnosis():
    scenario = get_scenario("data-exposure-risk")
    assert scenario.current_risk.name == "CRITICAL"
    assert scenario.incident.unknowns and "Immediately disable" in scenario.incident.containment_actions[0]


def test_false_alarm_closes_without_customer_impact():
    incident = get_scenario("payment-alert-false-alarm").incident
    assert incident.state is IncidentState.RESOLVED
    assert incident.recovery_verified
    assert incident.impact == ("No customer impact was found.",)


def test_supported_own_mistake_and_teammate_blame_are_phase_separated():
    review = get_scenario("payment-authorization").incident.review
    assert "Alex added" in review.responsibility[0]
    assert any("did not imply" in item for item in review.responsibility)
    assert get_response("payment-authorization", "containment-then-learning").identifies_own_contribution
    assert get_response("payment-authorization", "coordinated-incident-response").defers_blame_until_evidence


def test_review_prevention_and_conflict_connections():
    review = get_scenario("payment-authorization").incident.review
    assert review.timeline and review.detection and review.containment and review.correction
    assert any("compatibility" in action for action in review.prevention)
    response = get_response("payment-authorization", "coordinated-incident-response")
    assert response.defers_blame_until_evidence


def test_incident_trust_is_observable_history():
    kinds = {event.kind for event in INCIDENT_EVENTS}
    assert {TrustEventKind.INCIDENT_REPORTED_EARLY, TrustEventKind.UNCERTAINTY_PRESERVED,
            TrustEventKind.CONTAINMENT_COORDINATED, TrustEventKind.AFFECTED_PARTY_UPDATED,
            TrustEventKind.RECOVERY_VERIFIED, TrustEventKind.RESPONSIBILITY_ACKNOWLEDGED,
            TrustEventKind.PREVENTIVE_ACTION_COMPLETED} <= kinds


def test_deterministic_inspections(capsys):
    for args, expected in ((["incident", "payment-authorization"], "STATE\nACTIVE"),
                           (["recovery", "payment-authorization"], "RECOVERY VERIFIED\nno"),
                           (["incident-review", "payment-authorization"], "PREVENTION"),
                           (["compare", "payment-authorization"], "coordinated-incident-response"),
                           (["incident", "data-exposure-risk"], "Possible internal metadata exposure"),
                           (["incident", "payment-alert-false-alarm"], "RESOLVED"),
                           (["incident-trust"], "Recovery verified")):
        assert main(args) == 0
        assert expected in capsys.readouterr().out
