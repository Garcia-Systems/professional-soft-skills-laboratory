from soft_skills_lab.cli import main
from soft_skills_lab.domain.models import (
    DecisionRelevance, Outcome, RequirementIssueKind, ResolutionSource,
)
from soft_skills_lab.evaluation.requirements import evaluate_requirement_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.trust import ProfessionalTrust, REQUIREMENT_EVENTS, TrustEventKind


def outcomes(response_id: str) -> dict[str, Outcome]:
    scenario = get_scenario("transaction-export")
    return {r.criterion.criterion_id: r.outcome for r in
            evaluate_requirement_response(scenario, get_response(scenario.scenario_id, response_id))}


def test_requirement_context_preserves_core_distinctions():
    context = get_scenario("transaction-export").requirement_context
    kinds = {a.kind for a in context.ambiguities}
    assert {RequirementIssueKind.VAGUE, RequirementIssueKind.INCOMPLETE, RequirementIssueKind.AMBIGUOUS} <= kinds
    assert context.contradictions[0].subject == "Date-range meaning"
    assert context.stated_request != context.business_outcome
    assert context.explicit_requirements and context.constraints and context.evidence_sources
    assert context.decisions and context.acceptance_conditions


def test_materiality_is_effect_based_not_a_numeric_personality_score():
    ambiguities = {a.subject: a for a in get_scenario("transaction-export").requirement_context.ambiguities}
    assert ambiguities["Pending transactions"].decision_impact is DecisionRelevance.BLOCKING
    assert ambiguities["Export format"].decision_impact is DecisionRelevance.HIGH
    assert ambiguities["Filename format"].decision_impact is DecisionRelevance.LOW
    assert ambiguities["Filename format"].safe_to_defer
    assert not hasattr(ambiguities["Export format"], "score")


def test_existing_evidence_resolves_range_but_default_is_not_requirement():
    date_range = get_scenario("transaction-export").requirement_context.ambiguities[0]
    assert date_range.resolution_source is ResolutionSource.EXISTING_CONTRACT
    assert "active report range" in date_range.resolution
    assert "30-day UI default is not proof" in get_scenario("transaction-export").requirement_context.contradictions[0].interpretation


def test_safe_default_is_a_visible_reversible_assumption_not_authority():
    context = get_scenario("download-button-default").requirement_context
    assumption = context.assumptions[0]
    assert assumption.safe_default and assumption.reversible
    assert assumption.validation_point == "Product review"
    assert context.decisions == ("CSV is the selected format.",)  # convention follows, never overrides, the decision


def test_unsafe_customer_semantics_are_not_silently_assumed():
    pending = {a.subject: a for a in get_scenario("transaction-export").requirement_context.ambiguities}["Pending transactions"]
    assert not pending.safe_to_defer
    assert pending.resolution is None
    assert outcomes("assume-everything")["requires-decision-for-material-semantics"] is Outcome.FAIL
    assert outcomes("assumption-as-fact")["preserves-uncertainty"] is Outcome.FAIL


def test_primary_failure_and_strong_paths_remain_multidimensional():
    assert outcomes("literal-minimum")["uses-existing-evidence"] is Outcome.FAIL
    assert outcomes("block-on-everything")["asks-useful-clarification"] is Outcome.FAIL
    assert outcomes("contradictory-pick")["surfaces-contradiction"] is Outcome.FAIL
    focused = outcomes("resolve-decision-relevant-ambiguity")
    assert all(value is Outcome.PASS for value in focused.values())
    assert outcomes("progressive-clarification") == outcomes("equivalent-focused")


def test_progress_can_continue_while_nonblocking_ambiguity_remains():
    context = get_scenario("transaction-export").requirement_context
    assert len(context.safe_work_while_open) == 3
    assert get_response("transaction-export", "progressive-clarification").progresses_safely
    assert any(a.safe_to_defer and not a.is_resolved for a in context.ambiguities)


def test_acceptance_conditions_are_observable_not_implementation_details():
    conditions = get_scenario("transaction-export").requirement_context.acceptance_conditions
    assert {c.condition_id for c in conditions} == {"active-range", "range-limit", "pending-status", "visible-fields", "authorization", "format"}
    assert "January 1-31" in conditions[0].verification
    assert not hasattr(conditions[0], "implementation")


def test_notification_classifies_product_decisions_and_privacy_constraint():
    items = {a.subject: a for a in get_scenario("verification-notification").requirement_context.ambiguities}
    assert items["Channel"].decision_impact is DecisionRelevance.HIGH
    assert items["Timing"].safe_to_defer
    assert items["Content"].resolution_source is ResolutionSource.POLICY


def test_security_constraint_removes_stakeholder_option_without_compromise():
    scenario = get_scenario("contradictory-export-stakeholders")
    field_set = scenario.requirement_context.ambiguities[0]
    assert field_set.resolution_source is ResolutionSource.POLICY
    assert "removes" in field_set.resolution
    assert "must never" in scenario.requirement_context.constraints[0]


def test_retry_ambiguity_is_implementation_critical():
    items = get_scenario("verification-retry").requirement_context.ambiguities
    assert {a.subject for a in items if a.decision_impact is DecisionRelevance.BLOCKING} == {"Retryable failures", "Idempotency"}
    assert any("Duplicate external operations" in evidence for a in items for evidence in a.evidence)


def test_later_clarification_is_recorded_as_change_not_mistake():
    context = get_scenario("pending-requirement-change").requirement_context
    assert context.history[0].point == 2 and context.history[-1].point == 4
    assert "changed" in context.history[-1].description
    assert "tests" in context.history[-1].description


def test_requirement_trust_is_visible_evidence_history():
    trust = ProfessionalTrust()
    for event in REQUIREMENT_EVENTS:
        trust = trust.record(event)
    assert trust.history == REQUIREMENT_EVENTS
    assert {TrustEventKind.ASSUMPTION_MADE_VISIBLE, TrustEventKind.REQUIREMENT_DECISION_RECORDED} <= {e.kind for e in trust.history}


def test_cli_inspections_and_all_scenarios_are_deterministic(capsys):
    commands = (
        ("scenario", "transaction-export"), ("compare", "transaction-export"),
        ("ambiguities", "transaction-export"), ("contradictions", "transaction-export"),
        ("acceptance", "transaction-export"), ("requirement-history", "transaction-export"),
        ("scenario", "verification-notification"), ("ambiguities", "verification-notification"),
        ("scenario", "contradictory-export-stakeholders"), ("scenario", "verification-retry"),
        ("scenario", "download-button-default"), ("scenario", "pending-requirement-change"),
    )
    for command in commands:
        assert main(command) == 0
    output = capsys.readouterr().out
    assert "UNRESOLVED HIGH-VALUE DECISIONS" in output
    assert "The 30-day UI default is not proof" in output
    assert "ACCEPTANCE CONDITIONS" in output
    assert "REQUIREMENT DECISION HISTORY" in output
    assert "progressive-clarification" in output


def test_more_questions_is_not_better_and_ambiguity_is_not_failure():
    scenario = get_scenario("transaction-export")
    assert scenario.requirement_context.ambiguities  # ambiguity is represented, not itself failed
    assert outcomes("block-on-everything")["identifies-material-ambiguity"] is Outcome.PASS
    assert outcomes("block-on-everything")["asks-useful-clarification"] is Outcome.FAIL
