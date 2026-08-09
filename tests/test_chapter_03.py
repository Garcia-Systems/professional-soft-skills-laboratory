from dataclasses import replace

from soft_skills_lab.cli import main
from soft_skills_lab.domain.models import DecisionRelevance, Outcome
from soft_skills_lab.evaluation.questions import evaluate_question_response, evaluate_question_sequence
from soft_skills_lab.scenarios.questions import (
    AUTHORIZATION_INCIDENT, AUTHORIZATION_RESPONSES, DEPLOYMENT_FAILURE, DEPLOYMENT_RESPONSES,
    REPORT_ANSWERS, REPORT_EXPORT, REPORT_RESPONSES, SEARCH_SEQUENCE_RESPONSES, apply_answers,
)


def outcomes(scenario, response):
    return {result.criterion.criterion_id: result.outcome for result in evaluate_question_response(scenario, response)}


def test_unknowns_explain_relevance_blocking_and_self_investigation() -> None:
    unknowns = {item.unknown_id: item for item in REPORT_EXPORT.question_context.unknowns}
    assert unknowns["export-format"].blocking and unknowns["export-format"].relevance is DecisionRelevance.HIGH
    assert not unknowns["button-icon"].blocking and unknowns["button-icon"].relevance is DecisionRelevance.LOW
    assert unknowns["download-component"].is_resolved


def test_focused_questions_show_context_investigation_and_answerability() -> None:
    result = outcomes(REPORT_EXPORT, REPORT_RESPONSES["focused-questions"])
    assert all(value is Outcome.PASS for value in result.values())


def test_more_questions_are_not_better_questioning() -> None:
    dumped = REPORT_RESPONSES["question-dump"]
    focused = REPORT_RESPONSES["focused-questions"]
    assert len(dumped.questions) > len(focused.questions)
    assert outcomes(REPORT_EXPORT, dumped)["avoids-question-dump"] is Outcome.FAIL
    assert outcomes(REPORT_EXPORT, focused)["avoids-question-dump"] is Outcome.PASS


def test_no_questions_leave_requirement_risk_and_asking_before_looking_is_unnecessary() -> None:
    assert outcomes(REPORT_EXPORT, REPORT_RESPONSES["no-questions"])["clarifies-decision"] is Outcome.FAIL
    result = outcomes(REPORT_EXPORT, REPORT_RESPONSES["ask-before-looking"])
    assert result["shows-prior-investigation"] is Outcome.FAIL
    assert result["avoids-unnecessary-question"] is Outcome.FAIL


def test_leading_question_contains_authored_assumptions() -> None:
    result = outcomes(REPORT_EXPORT, REPORT_RESPONSES["leading-question"])
    assert result["avoids-assumption-disguised-as-question"] is Outcome.FAIL


def test_equivalent_wording_has_equivalent_evaluation() -> None:
    response = REPORT_RESPONSES["focused-questions"]
    rewritten = replace(response, message="Completely different wording with the same authored behavior.")
    assert outcomes(REPORT_EXPORT, response) == outcomes(REPORT_EXPORT, rewritten)


def test_answers_update_unknowns_to_facts_deterministically() -> None:
    first = apply_answers(REPORT_EXPORT)
    second = apply_answers(REPORT_EXPORT)
    assert first == second
    assert first.uncertainties == ("Button icon", "Final button label", "Filename punctuation")
    assert all(item.is_resolved for item in first.question_context.unknowns if item.blocking)
    assert all(any(value in fact for fact in first.known_facts) for value in REPORT_ANSWERS.values())


def test_problem_first_question_sequence_avoids_premature_solution() -> None:
    assert evaluate_question_sequence(SEARCH_SEQUENCE_RESPONSES["solution-first"]).outcome is Outcome.FAIL
    assert evaluate_question_sequence(SEARCH_SEQUENCE_RESPONSES["problem-first"]).outcome is Outcome.PASS


def test_asking_for_help_is_not_helplessness_and_solo_work_is_not_always_better() -> None:
    helpless = outcomes(DEPLOYMENT_FAILURE, DEPLOYMENT_RESPONSES["helpless-escalation"])
    professional = outcomes(DEPLOYMENT_FAILURE, DEPLOYMENT_RESPONSES["professional-question"])
    solo = outcomes(DEPLOYMENT_FAILURE, DEPLOYMENT_RESPONSES["endless-solo-investigation"])
    assert helpless["provides-context"] is Outcome.FAIL
    assert professional["provides-context"] is Outcome.PASS
    assert professional["shows-prior-investigation"] is Outcome.PASS
    assert solo["clarifies-decision"] is Outcome.FAIL


def test_high_risk_and_limited_authority_justify_immediate_escalation() -> None:
    immediate = outcomes(AUTHORIZATION_INCIDENT, AUTHORIZATION_RESPONSES["immediate-escalation"])
    alone = outcomes(AUTHORIZATION_INCIDENT, AUTHORIZATION_RESPONSES["investigate-alone"])
    assert immediate["shows-prior-investigation"] is Outcome.PASS
    assert immediate["clarifies-decision"] is Outcome.PASS
    assert alone["clarifies-decision"] is Outcome.FAIL


def test_chapter_three_cli(capsys) -> None:
    for command in (["scenario", "report-export"], ["unknowns", "report-export"],
                    ["evaluate", "report-export", "focused-questions"], ["compare", "report-export"],
                    ["answer", "report-export"]):
        assert main(command) == 0
    output = capsys.readouterr().out
    assert "Export format" in output and "unknown -> question -> answer -> known fact -> decision" in output
