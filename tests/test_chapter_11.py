from dataclasses import replace

from soft_skills_lab.cli import _manager_agreement_text, _visibility_text
from soft_skills_lab.domain.models import Outcome, VisibilityThreshold
from soft_skills_lab.evaluation.managers import evaluate_manager_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.trust import MANAGER_AUTONOMY_EVENTS, ProfessionalTrust, TrustEventKind


def results(scenario_id, response_id):
    scenario = get_scenario(scenario_id)
    return {r.criterion.criterion_id: r.outcome for r in evaluate_manager_response(scenario, get_response(scenario_id, response_id))}


def test_working_agreement_represents_contextual_thresholds_and_delegation():
    agreement = get_scenario("project-autonomy").working_agreement
    assert agreement.employee == "Alex" and agreement.manager == "Morgan"
    assert [e.threshold for e in agreement.expectations] == [VisibilityThreshold.ROUTINE, VisibilityThreshold.ROUTINE, VisibilityThreshold.INFORM, VisibilityThreshold.CONSULT, VisibilityThreshold.ESCALATE]
    assert all(e.evidence_of_agreement for e in agreement.expectations)


def test_autonomy_is_not_silence_and_visibility_is_not_permission_seeking():
    silent = results("project-autonomy", "silent-autonomy")
    permission = results("project-autonomy", "permission-for-everything")
    assert silent["acts-within-delegated-autonomy"] is Outcome.PASS
    assert silent["surfaces-threshold-crossing-risk"] is Outcome.FAIL
    assert permission["surfaces-threshold-crossing-risk"] is Outcome.PASS
    assert permission["avoids-unnecessary-upward-delegation"] is Outcome.FAIL


def test_routine_action_is_autonomy_not_insubordination():
    assert results("project-autonomy", "managed-autonomy")["acts-within-delegated-autonomy"] is Outcome.PASS


def test_visibility_is_not_implementation_reporting():
    flood = results("project-autonomy", "status-flood")
    assert flood["surfaces-threshold-crossing-risk"] is Outcome.PARTIAL
    assert flood["maintains-manager-signal"] is Outcome.FAIL


def test_late_and_premature_escalation_cross_different_boundaries():
    assert results("project-autonomy", "late-escalation")["escalates-true-blocker"] is Outcome.FAIL
    premature = results("project-autonomy", "escalate-without-investigation")
    assert premature["acts-within-delegated-autonomy"] is Outcome.FAIL
    assert premature["avoids-unnecessary-upward-delegation"] is Outcome.FAIL


def test_escalation_does_not_mean_an_empty_problem():
    empty = results("deployment-ownership", "empty-escalation")
    owned = results("deployment-ownership", "professional-ownership")
    assert empty["provides-recommendation"] is Outcome.FAIL
    assert owned["provides-recommendation"] is Outcome.PASS
    assert owned["respects-consultation-boundary"] is Outcome.FAIL  # recommendation does not fabricate consultation evidence


def test_managed_autonomy_and_equivalent_wording_are_behaviorally_equivalent():
    a = results("project-autonomy", "managed-autonomy")
    b = results("project-autonomy", "managed-autonomy-variation")
    for criterion in ("acts-within-delegated-autonomy", "surfaces-threshold-crossing-risk", "respects-consultation-boundary", "escalates-true-blocker", "provides-recommendation", "maintains-manager-signal"):
        assert a[criterion] == b[criterion] == Outcome.PASS


def test_recommendation_path_preserves_help_and_autonomy():
    result = results("project-autonomy", "visibility-with-recommendation")
    assert result["provides-recommendation"] is Outcome.PASS
    assert result["acts-within-delegated-autonomy"] is Outcome.PASS


def test_vague_direction_and_micromanagement_are_clarified_without_motive_judgment():
    assert results("vague-manager-direction", "clarify-outcome")["clarifies-working-agreement"] is Outcome.PASS
    assert results("micromanagement-clarification", "clarify-boundaries")["clarifies-working-agreement"] is Outcome.PASS
    assert "no motive is inferred" in get_scenario("micromanagement-clarification").description


def test_reliability_can_support_explicitly_changed_autonomy():
    original = get_scenario("changing-autonomy").working_agreement
    expanded = replace(original, normal_update_cadence="Risk- and decision-based updates.", version=2, supersedes=1)
    assert expanded.version == 2 and expanded.supersedes == original.version
    assert results("changing-autonomy", "expanded-autonomy")["acts-within-delegated-autonomy"] is Outcome.PASS


def test_manager_unavailable_does_not_erase_boundaries():
    result = results("manager-unavailable", "use-boundaries")
    assert result["respects-consultation-boundary"] is Outcome.PASS
    assert result["escalates-true-blocker"] is Outcome.PASS


def test_one_on_one_preparation_preserves_signal():
    assert results("manager-one-on-one", "prepared-topics")["maintains-manager-signal"] is Outcome.PASS
    assert results("manager-one-on-one", "task-dump")["maintains-manager-signal"] is Outcome.FAIL


def test_manager_disagreement_reuses_decision_model_and_authority_does_not_suppress_risk():
    assert get_scenario("manager-tradeoff-conflict").decision_context.owner == "Morgan"
    assert get_response("manager-material-risk", "document-and-escalate").preserves_material_risk


def test_later_feedback_behavior_and_trust_are_observable_history():
    assert get_response("feedback-follow-up", "demonstrated-change").demonstrated_improvement
    trust = ProfessionalTrust()
    for event in MANAGER_AUTONOMY_EVENTS:
        trust = trust.record(event)
    assert trust.balance > 0
    assert {e.kind for e in MANAGER_AUTONOMY_EVENTS} >= {TrustEventKind.ROUTINE_DECISION_OWNED, TrustEventKind.BLOCKER_ESCALATED}


def test_inspection_is_deterministic_and_explicitly_contextual():
    assert _manager_agreement_text("project-autonomy") == _manager_agreement_text("project-autonomy")
    text = _visibility_text("project-autonomy")
    assert text == _visibility_text("project-autonomy")
    assert "Threshold: ROUTINE" in text and "Threshold: ESCALATE" in text
    assert "not universal" in text
