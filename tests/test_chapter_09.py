"""Chapter 9: evidence-based disagreement and decision follow-through."""

from dataclasses import replace

from soft_skills_lab.cli import _decision_text
from soft_skills_lab.domain.models import DecisionIssueKind, Outcome
from soft_skills_lab.evaluation.disagreement import evaluate_disagreement_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.trust import DISAGREEMENT_EVENTS, ProfessionalTrust, TrustEventKind


def outcomes(scenario_id: str, response_id: str) -> dict[str, Outcome]:
    scenario = get_scenario(scenario_id)
    return {r.criterion.criterion_id: r.outcome for r in evaluate_disagreement_response(scenario, get_response(scenario_id, response_id))}


def test_adapter_decision_context_has_objective_owner_contributors_and_both_cases():
    context = get_scenario("adapter-boundary").decision_context
    assert context.shared_objective == "Keep the verification integration simple, maintainable, and reliable."
    assert context.owner == "Morgan" and context.contributors == ("Alex",)
    assert len(context.alternatives) == 2
    assert all(option.evidence for option in context.alternatives)
    assert "80 lines" in context.alternatives[0].evidence[0]
    assert "field names changed" in context.alternatives[1].evidence[0]


def test_primary_bad_extremes_and_personalized_paths_are_not_professional_by_compliance_or_force():
    passive = outcomes("adapter-boundary", "passive-agreement")
    flat = outcomes("adapter-boundary", "flat-rejection")
    authority = outcomes("adapter-boundary", "authority-challenge")
    ownership = outcomes("adapter-boundary", "defensive-ownership")
    assert passive["uses-decision-relevant-evidence"] is Outcome.FAIL  # agreement != professionalism
    assert flat["states-specific-disagreement"] is Outcome.PASS
    assert flat["uses-decision-relevant-evidence"] is Outcome.FAIL
    assert authority["avoids-personalization"] is Outcome.FAIL
    assert ownership["avoids-personalization"] is Outcome.FAIL


def test_jargon_is_not_a_practical_decision_case():
    result = get_response("adapter-boundary", "jargon-battle")
    assert "hexagonal" in result.message.lower()
    assert result.constructive_alternative is None


def test_evidence_based_disagreement_and_equivalent_wording_pass_core_behavior():
    for response_id in ("evidence-based-disagreement", "evidence-based-variation"):
        result = outcomes("adapter-boundary", response_id)
        for criterion in ("captures-explicit-concern", "identifies-shared-objective", "states-specific-disagreement",
                          "uses-decision-relevant-evidence", "avoids-personalization", "offers-constructive-alternative"):
            assert result[criterion] is Outcome.PASS


def test_disagreement_is_not_defensiveness_and_respect_is_not_agreement():
    response = get_response("adapter-boundary", "evidence-based-disagreement")
    assert response.states_specific_disagreement
    assert not response.personalizes_disagreement
    assert not response.automatic_agreement


def test_disagree_and_commit_respects_owner_without_repeating_argument():
    response = get_response("adapter-boundary", "disagree-and-commit")
    result = outcomes("adapter-boundary", "disagree-and-commit")
    assert response.respects_decision_ownership and not response.repeats_resolved_argument
    assert result["respects-decision-ownership"] is Outcome.PASS
    assert get_scenario("adapter-boundary").decision_context.owner == "Morgan"  # expertise != ownership


def test_repetition_after_resolution_is_not_stronger_advocacy():
    scenario = get_scenario("adapter-boundary")
    repeated = replace(get_response("adapter-boundary", "disagree-and-commit"), repeats_resolved_argument=True)
    result = {r.criterion.criterion_id: r.outcome for r in evaluate_disagreement_response(scenario, repeated)}
    assert result["respects-decision-ownership"] is Outcome.FAIL


def test_deadline_tradeoff_preserves_date_with_scope_alternative():
    response = get_response("reporting-deadline", "scope-reduction")
    result = outcomes("reporting-deadline", "scope-reduction")
    assert "CSV" in response.constructive_alternative
    assert result["uses-decision-relevant-evidence"] is Outcome.PASS
    assert outcomes("reporting-deadline", "silent-agreement")["uses-decision-relevant-evidence"] is Outcome.FAIL


def test_preference_is_not_a_defect():
    scenario = get_scenario("code-review-preference")
    assert scenario.decision_context.issue_kind is DecisionIssueKind.PREFERENCE
    assert outcomes("code-review-preference", "name-preference")["distinguishes-preference-from-defect"] is Outcome.PASS
    assert outcomes("code-review-preference", "invent-defect")["distinguishes-preference-from-defect"] is Outcome.FAIL


def test_changing_position_after_new_evidence_is_not_weakness():
    response = get_response("manager-correct", "update-position")
    assert response.updates_position_with_evidence
    assert outcomes("manager-correct", "update-position")["updates-position-with-evidence"] is Outcome.PASS
    # Manager authority alone is not the evidence; the benchmark is.
    assert "Benchmark" in response.decision_relevant_evidence[0]


def test_uncertainty_can_use_a_reversible_experiment_instead_of_more_argument():
    response = get_response("cache-strategy", "prototype")
    assert response.preserves_uncertainty
    assert "reversible" in response.constructive_alternative
    assert get_scenario("cache-strategy").decision_context.unresolved_risks


def test_material_risk_requires_escalation_not_disagree_and_commit():
    scenario = get_scenario("sensitive-logging")
    assert scenario.decision_context.issue_kind is DecisionIssueKind.MATERIAL_RISK
    assert outcomes("sensitive-logging", "escalate")["escalates-material-risk"] is Outcome.PASS
    assert outcomes("sensitive-logging", "commit-anyway")["escalates-material-risk"] is Outcome.FAIL
    # Decision ownership does not permit ignoring evidence.
    assert scenario.decision_context.owner == "Morgan" and not scenario.decision_context.reversible


def test_decision_inspection_is_deterministic():
    first = _decision_text("adapter-boundary")
    assert first == _decision_text("adapter-boundary")
    for text in ("DECISION OWNER", "Morgan", "EVIDENCE FOR REMOVE THE ADAPTER", "UNRESOLVED TRADEOFF", "FINAL CHOICE"):
        assert text in first


def test_constructive_disagreement_adds_inspectable_trust_history():
    trust = ProfessionalTrust()
    for event in DISAGREEMENT_EVENTS:
        trust = trust.record(event)
    assert trust.history == DISAGREEMENT_EVENTS
    assert trust.balance > 0
    assert {event.kind for event in trust.history} == {
        TrustEventKind.CONCERN_RAISED_WITH_EVIDENCE, TrustEventKind.DECISION_SUPPORTED_AFTER_RESOLUTION,
        TrustEventKind.POSITION_UPDATED_AFTER_NEW_EVIDENCE, TrustEventKind.MATERIAL_RISK_ESCALATED,
    }
