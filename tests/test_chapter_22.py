"""Chapter 22 invariants and deterministic coordination behavior."""

from dataclasses import replace

import pytest

from soft_skills_lab.cli import _comparison_text, _coordination_map_text, _leadership_text
from soft_skills_lab.domain.models import Outcome
from soft_skills_lab.evaluation.leadership import evaluate_leadership_response
from soft_skills_lab.scenarios import get_response, get_scenario


def outcomes(scenario_id, response_id):
    scenario = get_scenario(scenario_id)
    return {result.criterion.criterion_id: result.outcome for result in evaluate_leadership_response(scenario, get_response(scenario_id, response_id))}


def test_influence_context_has_explicit_objective_people_authority_and_gaps():
    context = get_scenario("verification-launch").influence_context
    assert context.objective == "Launch the new member-verification workflow safely by T10."
    assert context.initiator == "Alex" and context.participants == ("Alex", "Jordan", "Priya", "Dana", "Morgan")
    assert dict(context.formal_decision_owners)["Priya"] == ("Member-facing product behavior",)
    assert "Alex does not manage any participant." in context.constraints
    assert context.coordination_gaps


def test_dependency_map_preserves_owner_timing_and_relationships():
    dependencies = {item.item: item for item in get_scenario("verification-launch").influence_context.dependencies}
    assert dependencies["Timeout product decision"].owner == "Priya"
    assert dependencies["Timeout product decision"].blocks == ("Jordan frontend completion",)
    assert dependencies["Frontend completion"].depends_on == ("Timeout product decision",)
    assert dependencies["Engineering approval"].owner == "Morgan"


@pytest.mark.parametrize("response_id", ("command-peers", "do-everything", "manipulate-consensus"))
def test_authority_crossing_paths_fail_nonmanager_boundary(response_id):
    assert outcomes("verification-launch", response_id)["respects-nonmanager-authority-boundaries"] is Outcome.FAIL


def test_status_forwarding_and_unstructured_meeting_do_not_map_dependencies():
    assert outcomes("verification-launch", "status-forwarder")["maps-dependencies"] is not Outcome.PASS
    assert outcomes("verification-launch", "meeting-without-structure")["maps-dependencies"] is Outcome.FAIL


def test_escalating_everything_does_not_coordinate_first():
    assert outcomes("verification-launch", "escalate-everything")["coordinates-before-escalating"] is Outcome.FAIL


def test_false_consensus_fails_evidence_based_influence_and_consensus():
    result = outcomes("verification-launch", "manipulate-consensus")
    assert result["avoids-false-consensus"] is Outcome.FAIL
    assert result["provides-evidence-based-recommendation"] is Outcome.FAIL


@pytest.mark.parametrize("response_id", ("coordinate-without-authority", "facilitate-and-recommend"))
def test_strong_primary_paths_clarify_map_respect_invite_and_coordinate(response_id):
    result = outcomes("verification-launch", response_id)
    for criterion in ("clarifies-shared-objective", "maps-dependencies", "respects-nonmanager-authority-boundaries", "invites-explicit-ownership", "coordinates-before-escalating", "avoids-false-consensus", "updates-coordination-state"):
        assert result[criterion] is Outcome.PASS


def test_recommendation_is_supported_but_does_not_take_priyas_decision():
    response = get_response("verification-launch", "facilitate-and-recommend")
    assert response.evidence_based_recommendation
    assert response.respects_decision_ownership
    assert not response.ownership_taken_over


def test_proposed_coordination_action_is_not_accepted_commitment():
    action = get_scenario("verification-launch").influence_context.actions[0]
    assert action.proposed_owner == "Dana"
    assert action.action_type == "ownership invitation"
    assert not action.accepted_by_owner


@pytest.mark.parametrize("scenario_id,response_id,field", (
    ("leadership-questions", "ask-key-questions", "supplies_question_context"),
    ("cross-team-api", "negotiate-checkpoint", "peer_commitment_negotiated"),
    ("initiative-gap", "propose-reversible-plan", "ownership_invited"),
    ("peer-resistance", "minimal-coordination", "acknowledges_legitimate_concern"),
    ("stakeholder-resistance", "minimum-readiness", "ownership_invited"),
    ("leadership-missing-owner", "route-missing-owner", "missing_decision_owner_identified"),
    ("leader-wrong", "update-recommendation", "updates_position_with_evidence"),
    ("recommendation-rejected", "support-owner-decision", "concedes_decision"),
    ("cross-team-conflict", "restore-timeline", "restores_shared_facts"),
    ("leadership-credit", "credit-contributors", "contributors_credited_accurately"),
))
def test_secondary_leadership_behaviors_are_explicit(scenario_id, response_id, field):
    assert getattr(get_response(scenario_id, response_id), field)


def test_updated_recommendation_and_rejected_recommendation_preserve_authority():
    changed = get_response("leader-wrong", "update-recommendation")
    rejected = get_response("recommendation-rejected", "support-owner-decision")
    assert changed.updates_position_with_evidence and changed.coordination_state_updated
    assert rejected.respects_decision_ownership and rejected.coordination_state_updated


def test_influence_evidence_supports_credibility_without_creating_authority():
    context = get_scenario("verification-launch").influence_context
    assert "dependency_map_created" in context.influence_evidence
    assert "Alex does not manage any participant." in context.constraints


def test_inspection_and_map_are_deterministic():
    assert _leadership_text("verification-launch") == _leadership_text("verification-launch")
    assert "AUTHORITY BOUNDARY" in _leadership_text("verification-launch")
    assert "TIMEOUT PRODUCT DECISION" in _coordination_map_text("verification-launch")
    assert "Owner: Priya" in _coordination_map_text("verification-launch")


def test_comparison_has_all_paths_and_no_single_score():
    text = _comparison_text("verification-launch")
    assert all(path in text for path in ("command-peers", "do-everything", "status-forwarder", "meeting-without-structure", "escalate-everything", "manipulate-consensus", "coordinate-without-authority", "facilitate-and-recommend"))
    assert "no leadership" in text


def test_differently_worded_equivalent_behavior_has_same_evaluation():
    scenario = get_scenario("verification-launch")
    original = get_response("verification-launch", "coordinate-without-authority")
    paraphrase = replace(original, message="T10 is shared. Here are the owners, blockers, agreed checkpoints, and the one risk to route.")
    assert [(x.criterion.criterion_id, x.outcome) for x in evaluate_leadership_response(scenario, original)] == [(x.criterion.criterion_id, x.outcome) for x in evaluate_leadership_response(scenario, paraphrase)]


def test_core_distinctions_are_represented_as_invariants():
    context = get_scenario("verification-launch").influence_context
    strong = get_response("verification-launch", "facilitate-and-recommend")
    assert context.initiator == "Alex" and "Alex does not manage any participant." in context.constraints  # leadership != title
    assert strong.recommendation_provided and strong.respects_decision_ownership  # influence/recommendation != authority
    assert not strong.peer_commitment_assigned_without_authority  # peer leadership != commands
    assert not strong.ownership_taken_over  # coordination != takeover
    assert strong.coordinates_before_escalating  # escalation != first response
    assert not strong.false_consensus_claimed  # false consensus != influence
    assert set(context.contributors) == {"Alex", "Jordan", "Priya", "Dana", "Morgan"}  # objective != identical roles
