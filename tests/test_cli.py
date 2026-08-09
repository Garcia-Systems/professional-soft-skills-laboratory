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


@pytest.mark.parametrize("arguments", [["scenario", "missing"], ["evaluate", "production-incident", "missing"]])
def test_invalid_ids_are_cli_errors(arguments: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(arguments)
    assert error.value.code == 2
    assert "unknown" in capsys.readouterr().err
