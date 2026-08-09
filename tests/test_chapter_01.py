from dataclasses import FrozenInstanceError, replace

import pytest

from soft_skills_lab.domain.models import CommitmentStatus, Outcome, ProfessionalCommitment, ProfessionalResponse
from soft_skills_lab.evaluation.commitment import evaluate_commitment_response, evidence_for_commitment
from soft_skills_lab.evaluation.preparation import PREPARATION_BEHAVIORS, preparation_evidence
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.scenarios.commitment import TIMELINE, VENDOR_FACT
from soft_skills_lab.trust import TrustEventKind


def outcomes(response: ProfessionalResponse) -> dict[str, Outcome]:
    return {item.criterion.criterion_id: item.outcome for item in evaluate_commitment_response(response)}


def test_commitment_state_transitions_are_explicit_and_immutable() -> None:
    planned = ProfessionalCommitment("c", "work", "Alex", "Jordan", 2)
    active = planned.transition(CommitmentStatus.IN_PROGRESS)
    risky = active.transition(CommitmentStatus.AT_RISK, risk="vendor mismatch")
    assert planned.status is CommitmentStatus.PLANNED
    assert risky.known_risks == ("vendor mismatch",)
    assert risky.transition(CommitmentStatus.MISSED).status is CommitmentStatus.MISSED
    with pytest.raises((FrozenInstanceError, AttributeError)):
        planned.status = CommitmentStatus.COMPLETED  # type: ignore[misc]
    with pytest.raises(ValueError, match="invalid commitment transition"):
        planned.transition(CommitmentStatus.COMPLETED)


def test_simulated_timeline_is_deterministic_integer_time() -> None:
    assert TIMELINE == tuple(sorted(TIMELINE))
    assert [event.point for event in TIMELINE] == [0, 1, 2]
    assert all(isinstance(event.point, int) for event in TIMELINE)


def test_four_paths_have_behavior_specific_results() -> None:
    silent = outcomes(get_response("commitment-at-risk", "silent"))
    vague = outcomes(get_response("commitment-at-risk", "vague-warning"))
    promise = outcomes(get_response("commitment-at-risk", "premature-promise"))
    professional = outcomes(get_response("commitment-at-risk", "professional-update"))
    assert silent["communicates-risk-early"] is Outcome.FAIL
    assert vague["communicates-risk-early"] is Outcome.PASS
    assert vague["distinguishes-known-from-unknown"] is Outcome.PARTIAL
    assert vague["acknowledges-dependency"] is Outcome.FAIL
    assert promise["avoids-unsupported-promise"] is Outcome.FAIL
    assert all(value is Outcome.PASS for value in professional.values())


def test_late_risk_communication_does_not_count_as_early() -> None:
    response = replace(get_response("commitment-at-risk", "professional-update"), communicated_at=2)
    assert outcomes(response)["communicates-risk-early"] is Outcome.FAIL


def test_follow_up_and_loop_closure_are_independent_observations() -> None:
    response = replace(get_response("commitment-at-risk", "professional-update"), follow_up_point=None, loop_closed=False)
    result = outcomes(response)
    assert result["establishes-follow-up"] is Outcome.FAIL
    assert result["closes-loop"] is Outcome.FAIL


def test_equivalent_wording_has_equivalent_evaluation() -> None:
    original = get_response("commitment-at-risk", "professional-update")
    reworded = replace(original, response_id="reworded", message="Different words with the same observed behaviors.")
    assert outcomes(original) == outcomes(reworded)


def test_bad_outcome_is_not_automatically_unprofessional() -> None:
    response = get_response("commitment-at-risk", "professional-missed")
    assert response.delivered_on_time is False
    assert all(value is Outcome.PASS for value in outcomes(response).values())
    kinds = {event.kind for event in evidence_for_commitment(response)}
    assert TrustEventKind.RISK_COMMUNICATED_EARLY in kinds
    assert TrustEventKind.FOLLOW_UP_COMPLETED in kinds


def test_good_outcome_is_not_automatically_professional() -> None:
    response = get_response("commitment-at-risk", "hidden-risk-success")
    assert response.delivered_on_time is True
    assert outcomes(response)["communicates-risk-early"] is Outcome.FAIL
    assert outcomes(response)["acknowledges-dependency"] is Outcome.FAIL
    assert TrustEventKind.COMMITMENT_KEPT in {event.kind for event in evidence_for_commitment(response)}


def test_preparation_is_observable_evidence() -> None:
    assert preparation_evidence(PREPARATION_BEHAVIORS["unreviewed"]) == ()
    assert len(preparation_evidence(PREPARATION_BEHAVIORS["reviewed-no-artifact"])) == 1
    fully = preparation_evidence(PREPARATION_BEHAVIORS["fully-prepared"])
    assert len(fully) == 3
    assert fully[0].kind is TrustEventKind.PREPARED_FOR_WORK


def test_scenario_and_results_are_deterministic() -> None:
    assert get_scenario("commitment-at-risk") == get_scenario("commitment-at-risk")
    assert VENDOR_FACT in get_scenario("commitment-at-risk").known_facts
    first = evaluate_commitment_response(get_response("commitment-at-risk", "vague-warning"))
    assert first == evaluate_commitment_response(get_response("commitment-at-risk", "vague-warning"))


def test_unknown_chapter_one_response() -> None:
    with pytest.raises(KeyError, match="unknown response"):
        get_response("commitment-at-risk", "not-a-path")
