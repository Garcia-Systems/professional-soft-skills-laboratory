from soft_skills_lab.cli import _comparison_text, _explain_text, _layers_text, main
from soft_skills_lab.domain.models import Outcome
from soft_skills_lab.evaluation.explanations import evaluate_explanation
from soft_skills_lab.scenarios.explanations import (
    ARCHITECTURE_VIEWS, AUDIENCE_EXPLANATIONS, MIGRATION_RESPONSES, PAYMENT_FACTS, PAYMENT_RESPONSES,
)


def outcomes(response_id: str) -> dict[str, Outcome]:
    return {result.criterion.criterion_id: result.outcome for result in evaluate_explanation(PAYMENT_RESPONSES[response_id])}


def test_technical_correctness_is_not_effective_explanation():
    jargon = outcomes("jargon-dump")
    assert jargon["preserves-technical-truth"] is Outcome.PASS
    assert jargon["matches-audience-need"] is Outcome.PARTIAL
    assert jargon["avoids-unnecessary-detail"] is Outcome.FAIL
    assert jargon["supports-decision"] is Outcome.FAIL


def test_simplicity_is_not_accuracy_and_false_certainty_loses_unknown():
    simple = outcomes("oversimplified")
    certain = outcomes("false-certainty")
    assert simple["preserves-technical-truth"] is Outcome.FAIL
    assert certain["preserves-technical-truth"] is Outcome.FAIL
    assert certain["preserves-uncertainty"] is Outcome.FAIL


def test_correct_without_impact_differs_from_decision_oriented():
    no_impact = outcomes("technically-correct-no-impact")
    good = outcomes("decision-oriented")
    assert no_impact["preserves-technical-truth"] is Outcome.PASS
    assert no_impact["communicates-impact"] is Outcome.FAIL
    for criterion in ("preserves-technical-truth", "matches-audience-need", "communicates-impact",
                      "communicates-scope", "preserves-uncertainty", "supports-decision", "establishes-next-action"):
        assert good[criterion] is Outcome.PASS


def test_audience_views_select_different_detail_without_changing_facts():
    fact_ids = set(PAYMENT_FACTS)
    for explanation in AUDIENCE_EXPLANATIONS.values():
        assert set(explanation.communicated_fact_ids) <= fact_ids
        assert not explanation.unsupported_claims
        assert explanation.preserves_uncertainty
    assert AUDIENCE_EXPLANATIONS["engineer"].implementation_details
    assert not AUDIENCE_EXPLANATIONS["product-manager"].implementation_details
    assert "8%" in AUDIENCE_EXPLANATIONS["product-manager"].message
    assert "pause" in AUDIENCE_EXPLANATIONS["business-operations"].message


def test_architecture_abstractions_preserve_boundaries():
    views = dict(ARCHITECTURE_VIEWS)
    assert views["engineer"] == ("Browser", "Harbor API", "Application Service", "External Verification Provider")
    assert views["business-stakeholder"] == ("Member request", "Harbor", "verification partner", "Harbor result")


def test_database_migration_preserves_estimated_duration_and_decision():
    good = MIGRATION_RESPONSES["decision-oriented"]
    assert good.preserves_uncertainty and good.communicates_impact and good.supports_decision
    assert MIGRATION_RESPONSES["misleading-simplification"].unsupported_claims
    assert MIGRATION_RESPONSES["exaggerated-certainty"].unsupported_claims


def test_output_is_deterministic_and_multidimensional():
    assert _comparison_text("payment-timeout") == _comparison_text("payment-timeout")
    assert "leaderboard" in _comparison_text("payment-timeout")
    assert _explain_text("payment-timeout", "engineer") == _explain_text("payment-timeout", "engineer")
    assert "CURRENT UNKNOWNS" in _layers_text("payment-timeout")


def test_chapter_four_cli_examples(capsys):
    examples = (
        ["scenario", "payment-timeout"], ["evaluate", "payment-timeout", "jargon-dump"],
        ["evaluate", "payment-timeout", "oversimplified"], ["evaluate", "payment-timeout", "false-certainty"],
        ["evaluate", "payment-timeout", "technically-correct-no-impact"],
        ["evaluate", "payment-timeout", "decision-oriented"], ["compare", "payment-timeout"],
        ["explain", "payment-timeout", "--audience", "engineer"],
        ["explain", "payment-timeout", "--audience", "product-manager"],
        ["explain", "payment-timeout", "--audience", "business-operations"],
        ["layers", "payment-timeout"], ["scenario", "database-migration"],
        ["evaluate", "database-migration", "decision-oriented"],
    )
    for argv in examples:
        assert main(argv) == 0
    assert "Decision-oriented" in capsys.readouterr().out


def test_behavioral_equivalence_is_structured_not_wording_based():
    original = PAYMENT_RESPONSES["decision-oriented"]
    from dataclasses import replace
    rewritten = replace(original, message="Different words with the same authored behavior.")
    assert evaluate_explanation(rewritten) == evaluate_explanation(original)
