import pytest

from soft_skills_lab.cli import main
from soft_skills_lab.domain.models import HandoffState, Outcome
from soft_skills_lab.evaluation.collaboration import evaluate_collaboration_response
from soft_skills_lab.scenarios import get_response, get_scenario

def outcomes(sid, rid):
    return {r.criterion.criterion_id: r.outcome for r in evaluate_collaboration_response(get_scenario(sid), get_response(sid, rid))}

def test_peer_ownership_and_dependency_are_explicit():
    context = get_scenario("verification-integration").peer_collaboration
    assert dict(context.ownership.owners)["Alex"][-1] == "Backend handoff"
    assert "Jordan needs stable response semantics" in context.dependencies[0]
    assert "Contract understanding" in context.ownership.shared

def test_handoff_lifecycle_distinguishes_creation_delivery_understanding_and_acceptance():
    handoff = get_scenario("verification-integration").peer_collaboration.handoff
    assert handoff.state is HandoffState.READY
    delivered = handoff.transition(HandoffState.DELIVERED)
    acknowledged = delivered.transition(HandoffState.ACKNOWLEDGED)
    assert acknowledged.transition(HandoffState.ACCEPTED).state is HandoffState.ACCEPTED
    with pytest.raises(ValueError):
        handoff.transition(HandoffState.ACCEPTED)

def test_rework_returns_to_ready():
    handoff = get_scenario("verification-integration").peer_collaboration.handoff
    rework = handoff.transition(HandoffState.DELIVERED).transition(HandoffState.REWORK_REQUIRED)
    assert rework.transition(HandoffState.READY).state is HandoffState.READY

@pytest.mark.parametrize("rid,criterion,expected", [
    ("silent-handoff", "makes-handoff-explicit", Outcome.FAIL),
    ("throw-over-wall", "provides-handoff-context", Outcome.FAIL),
    ("over-help", "respects-peer-ownership", Outcome.FAIL),
    ("wait-for-them-to-ask", "acknowledges-dependency", Outcome.FAIL),
    ("dependency-blame", "avoids-blame", Outcome.FAIL),
    ("coordinated-handoff", "closes-loop", Outcome.PASS),
    ("coordinated-help", "helps-without-taking-over", Outcome.PASS),
])
def test_primary_paths(rid, criterion, expected):
    assert outcomes("verification-integration", rid)[criterion] is expected

def test_equivalent_wording_has_equivalent_handoff_semantics():
    assert outcomes("verification-integration", "coordinated-handoff") == outcomes("verification-integration", "coordinated-handoff-variation")

def test_targeted_context_question_is_investigated_not_incompetence():
    response = get_response("teammate-context", "targeted-context")
    assert response.seeks_specific_understanding and len(response.investigation_performed) == 3
    assert outcomes("teammate-context", "targeted-context")["respects-peer-ownership"] is Outcome.PASS

def test_review_correctness_is_not_ownership_transfer_or_preference():
    scenario = get_scenario("peer-code-review")
    useful = get_response("peer-code-review", "useful-review")
    assert scenario.decision_context.issue_kind.value == "correctness issue"
    assert useful.distinguishes_preference_from_defect and useful.decision_relevant_evidence
    assert outcomes("peer-code-review", "reviewer-takeover")["respects-peer-ownership"] is Outcome.FAIL

def test_bounded_help_accounts_for_both_commitments():
    scenario = get_scenario("bounded-peer-help")
    assert scenario.peer_collaboration.help_context.helper_commitment_risk.name == "HIGH"
    result = outcomes("bounded-peer-help", "bounded-help")
    assert result["helps-without-taking-over"] is result["accounts-for-help-opportunity-cost"] is Outcome.PASS
    assert outcomes("bounded-peer-help", "takeover")["respects-peer-ownership"] is Outcome.FAIL
    assert outcomes("bounded-peer-help", "unlimited-help")["accounts-for-help-opportunity-cost"] is Outcome.FAIL

def test_defer_and_schedule_can_be_professional_help():
    response = get_response("bounded-peer-help", "defer-and-schedule")
    assert response.follow_up_commitment and response.accounts_for_help_opportunity_cost

def test_shared_responsibility_is_not_shared_assumption():
    assert outcomes("shared-peer-task", "shared-assumption")["clarifies-shared-ownership"] is Outcome.FAIL
    assert outcomes("shared-peer-task", "assign-owner")["clarifies-shared-ownership"] is Outcome.PASS

def test_peer_first_check_precedes_proportionate_escalation():
    assert outcomes("missed-peer-commitment", "peer-check")["addresses-peer-dependency-directly"] is Outcome.PASS
    assert outcomes("missed-peer-commitment", "manager-first")["addresses-peer-dependency-directly"] is Outcome.FAIL
    escalated = get_response("missed-peer-commitment", "material-escalation")
    assert escalated.peer_dependency_addressed_directly and escalated.escalates_material_risk

def test_crediting_teammate_preserves_both_contributions():
    response = get_response("team-contribution", "accurate-credit")
    assert response.contribution_recognized and "I delivered" in response.message

def test_repeated_takeover_creates_dependency_but_documentation_restores_ownership():
    assert outcomes("help-dependency", "repeat-takeover")["respects-peer-ownership"] is Outcome.FAIL
    restored = outcomes("help-dependency", "restore-ownership")
    assert restored["helps-without-taking-over"] is restored["provides-handoff-context"] is Outcome.PASS

@pytest.mark.parametrize("args,expected", [
    (["handoff", "verification-integration"], "READY BUT NOT YET ACKNOWLEDGED"),
    (["ownership", "verification-integration"], "ALEX OWNS"),
    (["compare", "verification-integration"], "coordinated-help"),
    (["scenario", "verification-integration"], "T5:"),
    (["evaluate", "peer-code-review", "useful-review"], "distinguishes-preference-from-defect"),
    (["evaluate", "teammate-context", "targeted-context"], "respects-peer-ownership"),
    (["evaluate", "bounded-peer-help", "bounded-help"], "accounts-for-help-opportunity-cost"),
    (["evaluate", "shared-peer-task", "assign-owner"], "clarifies-shared-ownership"),
    (["evaluate", "missed-peer-commitment", "peer-check"], "addresses-peer-dependency-directly"),
    (["evaluate", "team-contribution", "accurate-credit"], "recognizes-contribution"),
    (["collaboration-trust"], "Handoff accepted"),
])
def test_cli_examples_are_deterministic(args, expected, capsys):
    assert main(args) == 0
    assert expected in capsys.readouterr().out
