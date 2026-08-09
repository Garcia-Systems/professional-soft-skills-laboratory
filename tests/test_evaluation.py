from soft_skills_lab.domain.models import Outcome, ProfessionalResponse
from soft_skills_lab.evaluation import evaluate_incident_response
from soft_skills_lab.evaluation.incident import INCIDENT_FACT
from soft_skills_lab.scenarios import get_response


def result_map(response: ProfessionalResponse) -> dict[str, Outcome]:
    return {result.criterion.criterion_id: result.outcome for result in evaluate_incident_response(response)}


def test_professional_reference_passes_every_criterion() -> None:
    results = evaluate_incident_response(get_response("production-incident", "professional"))
    assert all(result.outcome is Outcome.PASS for result in results)
    assert all(result.explanation for result in results)
    assert all(result.evidence for result in results)


def test_reference_failures_are_behavior_specific() -> None:
    defensive = result_map(get_response("production-incident", "defensive"))
    blame = result_map(get_response("production-incident", "blame-shifting"))
    accepting = result_map(get_response("production-incident", "over-accepting"))
    assert defensive["avoids-unsupported-claims"] is Outcome.FAIL
    assert blame["avoids-blame"] is Outcome.FAIL
    assert accepting["accepts-owned-responsibility"] is Outcome.PASS
    assert accepting["avoids-unsupported-claims"] is Outcome.FAIL


def test_different_wording_with_equivalent_behaviors_has_same_results() -> None:
    fields = dict(
        acknowledged_facts=(INCIDENT_FACT,),
        responsibility_statement="I will examine the work I own.",
        next_action="Review telemetry and changes.",
        follow_up_commitment="Update the team in thirty minutes.",
    )
    terse = ProfessionalResponse("one", "Terse", "Incident noted; investigating.", **fields)
    detailed = ProfessionalResponse(
        "two", "Detailed", "Thank you for raising this. I will carefully collect the available evidence.", **fields
    )
    assert result_map(terse) == result_map(detailed)
    assert all(outcome is Outcome.PASS for outcome in result_map(terse).values())


def test_message_keywords_alone_do_not_pass_structured_behavior_checks() -> None:
    response = ProfessionalResponse(
        "keywords", "Keywords only", "incident responsibility logs follow-up no blame"
    )
    results = result_map(response)
    assert results["acknowledges-impact"] is Outcome.FAIL
    assert results["establishes-next-action"] is Outcome.FAIL
    assert results["establishes-follow-up"] is Outcome.FAIL
