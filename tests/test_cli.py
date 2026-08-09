import pytest

from soft_skills_lab.cli import main


def test_scenario_output_is_stable(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["scenario", "production-incident"]) == 0
    output = capsys.readouterr().out
    assert "Scenario: A feature deployment and a production incident" in output
    assert "Known facts:" in output
    assert "- professional: Investigation-oriented response" in output


def test_evaluation_output_has_explainable_criteria(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["evaluate", "production-incident", "professional"]) == 0
    output = capsys.readouterr().out
    assert output.count("Criterion:") == 6
    assert "Criterion: establishes-follow-up\nPASS" in output
    assert "Evidence: Report initial findings at the 15:00 incident update." in output


def test_trust_demo_output(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["trust-demo"]) == 0
    output = capsys.readouterr().out
    assert "Professional trust is accumulated evidence." in output
    assert "Resulting evidence balance: 4" in output


def test_chapter_one_scenario_evaluation_and_comparison(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["scenario", "commitment-at-risk"]) == 0
    scenario = capsys.readouterr().out
    assert "Participants:" in scenario and "Timeline:" in scenario and "Dependencies:" in scenario
    assert main(["evaluate", "commitment-at-risk", "vague-warning"]) == 0
    evaluation = capsys.readouterr().out
    assert "Criterion: communicates-risk-early\nPASS" in evaluation
    assert "Criterion: distinguishes-known-from-unknown\nPARTIAL" in evaluation
    assert main(["compare", "commitment-at-risk"]) == 0
    comparison = capsys.readouterr().out
    assert "professional-update" in comparison and "not a professionalism score" in comparison


@pytest.mark.parametrize("arguments", [["scenario", "missing"], ["evaluate", "production-incident", "missing"]])
def test_invalid_ids_are_cli_errors(arguments: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(arguments)
    assert error.value.code == 2
    assert "unknown" in capsys.readouterr().err
