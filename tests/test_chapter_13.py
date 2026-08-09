from soft_skills_lab.cli import main
from soft_skills_lab.domain.models import Outcome
from soft_skills_lab.evaluation.stakeholders import evaluate_stakeholder_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.trust import ProfessionalTrust, STAKEHOLDER_EVENTS, TrustEventKind


def results(scenario_id: str, response_id: str) -> dict[str, Outcome]:
    scenario = get_scenario(scenario_id)
    return {x.criterion.criterion_id: x.outcome for x in evaluate_stakeholder_response(scenario, get_response(scenario_id, response_id))}


def test_request_is_decomposed_not_literal_specification():
    request = get_scenario("reporting-export").stakeholder_request
    assert request.stated_request != request.business_outcome
    assert request.preferred_solution not in request.requirements
    assert "Friday" == request.deadline
    assert "Internal-only metadata must not be exposed." in request.constraints
    assert request.acceptance_conditions
    assert dict(request.decision_owners)["Dana"] != dict(request.decision_owners)["Alex"]


def test_primary_paths_reject_blind_yes_no_jargon_dump_and_silent_change():
    assert results("reporting-export", "literal-yes")["communicates-tradeoff"] is Outcome.FAIL
    assert results("reporting-export", "technical-no")["preserves-business-context"] is Outcome.FAIL
    assert results("reporting-export", "jargon-rejection")["avoids-unnecessary-detail"] is Outcome.FAIL
    assert results("reporting-export", "requirement-interrogation")["asks-useful-clarification"] is Outcome.FAIL
    assert results("reporting-export", "silent-scope-reduction")["makes-scope-change-explicit"] is Outcome.FAIL


def test_tradeoff_and_recommendation_paths_are_semantic_and_equivalent():
    tradeoff = results("reporting-export", "outcome-first-tradeoff")
    recommended = results("reporting-export", "recommendation-with-decision")
    equivalent = results("reporting-export", "equivalent-recommendation")
    assert tradeoff["communicates-tradeoff"] is Outcome.PASS
    assert tradeoff["respects-decision-ownership"] is Outcome.PASS
    assert recommended["provides-professional-recommendation"] is Outcome.PASS
    assert recommended == equivalent


def test_csv_xlsx_options_are_transparent_not_numeric():
    options = {x.option_id: x for x in get_scenario("reporting-export").tradeoff_options}
    assert options["csv-by-friday"].technical_risk.startswith("Low")
    assert "Native workbook formatting and features" in options["csv-by-friday"].constraints_not_satisfied
    assert "Friday availability" in options["xlsx-next-iteration"].constraints_not_satisfied
    assert not hasattr(options["xlsx-by-friday"], "score")


def test_new_business_evidence_changes_technical_recommendation():
    request = get_scenario("xlsx-required").stakeholder_request
    response = get_response("xlsx-required", "update-recommendation")
    assert ".xlsx" in request.requirements[0]
    assert response.updates_position_with_evidence
    assert results("xlsx-required", "update-recommendation")["respects-explicit-requirement"] is Outcome.PASS


def test_performance_language_becomes_acceptance_question():
    scenario = get_scenario("stakeholder-search-performance")
    assert "Median is 700 ms." in scenario.stakeholder_request.technical_evidence
    assert "percentile" in scenario.stakeholder_request.open_questions[1]
    assert results(scenario.scenario_id, "clarify-experience")["asks-useful-clarification"] is Outcome.PASS


def test_urgent_request_has_controlled_option_not_automatic_preference():
    scenario = get_scenario("urgent-bulk-upload")
    assert scenario.tradeoff_options[0].option_id == "controlled-import"
    assert "might" in get_response(scenario.scenario_id, "controlled-option").message
    assert scenario.stakeholder_request.business_outcome != scenario.stakeholder_request.preferred_solution


def test_scope_request_is_not_wrongdoing_but_is_explicit_tradeoff():
    scenario = get_scenario("export-scope-change")
    assert scenario.scope_change.requested_addition == "Scheduled email delivery"
    assert len(scenario.scope_change.available_tradeoffs) == 3
    assert results(scenario.scenario_id, "explicit-options")["makes-scope-change-explicit"] is Outcome.PASS
    assert results(scenario.scenario_id, "sure")["preserves-uncertainty"] is Outcome.FAIL


def test_security_constraint_explains_consequence_and_preserves_goal():
    weak = results("export-security-constraint", "mysterious-authority")
    strong = results("export-security-constraint", "safe-alternative")
    assert weak["preserves-business-context"] is Outcome.FAIL
    assert strong["preserves-business-context"] is Outcome.PASS
    assert "not authorized" in get_response("export-security-constraint", "safe-alternative").message


def test_impossible_constraints_never_create_invented_commitment():
    request = get_scenario("impossible-export-constraints").stakeholder_request
    assert len(request.constraints) == 4
    assert get_response("impossible-export-constraints", "fake-promise").unsupported_promise
    assert results("impossible-export-constraints", "surface-conflict")["preserves-uncertainty"] is Outcome.PASS


def test_stakeholder_trust_is_observable_history():
    trust = ProfessionalTrust()
    for event in STAKEHOLDER_EVENTS:
        trust = trust.record(event)
    assert trust.history == STAKEHOLDER_EVENTS
    assert TrustEventKind.BUSINESS_GOAL_CLARIFIED in {x.kind for x in trust.history}
    assert TrustEventKind.POSITION_UPDATED_AFTER_NEW_EVIDENCE in {x.kind for x in trust.history}


def test_cli_inspections_are_deterministic(capsys):
    commands = (("stakeholder-request", "reporting-export"), ("tradeoffs", "reporting-export"),
                ("scope-change", "export-scope-change"), ("stakeholder-trust",),
                ("scenario", "stakeholder-search-performance"), ("scenario", "urgent-bulk-upload"),
                ("scenario", "export-security-constraint"), ("scenario", "xlsx-required"),
                ("scenario", "impossible-export-constraints"))
    for command in commands:
        assert main(command) == 0
    output = capsys.readouterr().out
    assert "BUSINESS OUTCOME" in output
    assert "OPTION: CSV BY FRIDAY" in output
    assert "REQUESTED ADDITION" in output
    assert "STAKEHOLDER COLLABORATION TRUST EVIDENCE" in output


def test_requested_invariants_remain_distinct():
    report = get_scenario("reporting-export")
    assert report.stakeholder_request.stated_request != report.decision_context.decision
    assert report.stakeholder_request.business_outcome != report.tradeoff_options[0].description
    assert get_response("reporting-export", "literal-yes").unsupported_promise  # yes != collaboration
    assert not get_response("reporting-export", "technical-no").preserves_business_context  # no != responsibility
    assert get_response("reporting-export", "outcome-first-tradeoff").supports_decision  # tradeoff != refusal
    assert report.current_risk.name != report.stakeholder_request.deadline  # priority/date != feasibility
