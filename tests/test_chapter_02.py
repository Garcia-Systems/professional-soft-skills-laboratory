from dataclasses import replace

import pytest

from soft_skills_lab.cli import _interpretation_text, main
from soft_skills_lab.domain.models import Outcome, ProfessionalResponse
from soft_skills_lab.evaluation.listening import CRITERIA, evaluate_listening_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.scenarios.listening import DEMO_ASSUMPTIONS, DEMO_FACTS, DEMO_UNKNOWNS


def outcomes(response: ProfessionalResponse) -> dict[str, Outcome]:
    return {result.criterion.criterion_id: result.outcome for result in evaluate_listening_response(response)}


def test_communication_gap_is_explicit_and_deterministic() -> None:
    context = get_scenario("demo-stability").communication_context
    assert context is not None
    assert context.explicit_facts == DEMO_FACTS
    assert context.unknowns == DEMO_UNKNOWNS
    assert context.unsupported_assumptions == DEMO_ASSUMPTIONS
    assert _interpretation_text("demo-stability") == _interpretation_text("demo-stability")


def test_listener_interpretations_distinguish_assumption_and_unknown() -> None:
    defensive = get_response("demo-stability", "defensive-interpretation").listener_interpretation
    clarifying = get_response("demo-stability", "listen-then-clarify").listener_interpretation
    assert defensive and "Morgan is accusing Alex." in defensive.assumptions
    assert clarifying and clarifying.understood_facts == DEMO_FACTS and clarifying.clarification_needed


def test_premature_solution_and_fast_response_are_not_good_listening() -> None:
    result = outcomes(get_response("demo-stability", "premature-solution"))
    assert result["avoids-premature-solution"] is Outcome.FAIL
    assert result["captures-explicit-concern"] is Outcome.FAIL


def test_defensiveness_is_worse_than_partial_acknowledgment() -> None:
    defensive = outcomes(get_response("demo-stability", "defensive-interpretation"))
    passive = outcomes(get_response("demo-stability", "passive-acknowledgment"))
    assert defensive["avoids-unsupported-assumption"] is Outcome.FAIL
    assert passive["avoids-unsupported-assumption"] is Outcome.PASS
    assert passive["captures-explicit-concern"] is Outcome.PARTIAL


def test_useful_clarification_is_not_helplessness() -> None:
    result = outcomes(get_response("demo-stability", "listen-then-clarify"))
    assert all(value is Outcome.PASS for value in result.values())
    assert result["clarifies-success-condition"] is Outcome.PASS
    assert result["establishes-next-action"] is Outcome.PASS


def test_accurate_understanding_is_not_agreement() -> None:
    response = get_response("demo-stability", "understand-then-disagree")
    assert response.respectful_disagreement
    result = outcomes(response)
    assert result["captures-explicit-concern"] is Outcome.PASS
    assert result["avoids-unsupported-assumption"] is Outcome.PASS


def test_equivalent_semantics_not_wording_drive_evaluation() -> None:
    original = get_response("demo-stability", "listen-then-clarify")
    differently_worded = replace(original, response_id="equivalent", message="Different surface wording entirely.")
    assert outcomes(original) == outcomes(differently_worded)


def test_reuses_existing_next_action_and_follow_up_criteria() -> None:
    assert [criterion.criterion_id for criterion in CRITERIA][-2:] == ["establishes-next-action", "establishes-follow-up"]


def test_peer_and_stakeholder_scenarios() -> None:
    peer = outcomes(get_response("teammate-contract", "clarify-contract"))
    stakeholder = outcomes(get_response("stakeholder-search", "measure-and-clarify"))
    assert peer["clarifies-success-condition"] is Outcome.PASS
    assert stakeholder["identifies-unknowns"] is Outcome.PASS
    assert "Acceptable performance." in get_scenario("stakeholder-search").uncertainties


def test_interpret_cli_and_invalid_scenario(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["interpret", "demo-stability"]) == 0
    assert "UNSUPPORTED ASSUMPTIONS\n\n- Morgan is blaming Alex." in capsys.readouterr().out
    with pytest.raises(SystemExit):
        main(["interpret", "production-incident"])
