from dataclasses import FrozenInstanceError

import pytest

from soft_skills_lab.domain.models import RiskLevel
from soft_skills_lab.scenarios import get_response, get_scenario, list_responses


def test_scenario_loading_is_deterministic() -> None:
    first = get_scenario("production-incident")
    second = get_scenario("production-incident")
    assert first == second
    assert first.current_risk is RiskLevel.CRITICAL
    assert tuple(response.response_id for response in list_responses(first.scenario_id)) == (
        "defensive", "blame-shifting", "over-accepting", "professional"
    )


def test_domain_values_are_immutable() -> None:
    scenario = get_scenario("production-incident")
    with pytest.raises(FrozenInstanceError):
        scenario.title = "changed"  # type: ignore[misc]


def test_unknown_scenario() -> None:
    with pytest.raises(KeyError, match="unknown scenario: missing"):
        get_scenario("missing")


def test_unknown_response() -> None:
    with pytest.raises(KeyError, match="unknown response"):
        get_response("production-incident", "missing")
