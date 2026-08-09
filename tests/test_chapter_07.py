from dataclasses import replace

from soft_skills_lab.cli import _feedback_text, _improvement_text
from soft_skills_lab.domain.models import FeedbackEvidenceStrength, Outcome
from soft_skills_lab.evaluation.feedback import evaluate_feedback_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.scenarios.feedback import VISIBILITY_PLAN
from soft_skills_lab.trust import FEEDBACK_IMPROVEMENT_EVENTS, ProfessionalTrust, TrustEventKind


def outcomes(scenario_id: str, response_id: str) -> dict[str, Outcome]:
    scenario = get_scenario(scenario_id)
    return {result.criterion.criterion_id: result.outcome for result in
            evaluate_feedback_response(scenario, get_response(scenario_id, response_id))}


def test_feedback_decomposes_observation_interpretation_expectation_and_context():
    feedback = get_scenario("project-visibility").feedback
    assert feedback.source == "Morgan"
    assert "T3" in feedback.observed_behavior[0]
    assert "too late" in feedback.interpretation[0]
    assert "Material delivery risk" in feedback.expected_behavior[0]
    assert "shipped at T6" in feedback.important_context[1]
    assert "technically incompetent" in feedback.not_implied[0]


def test_successful_outcome_does_not_invalidate_feedback():
    scenario = get_scenario("project-visibility")
    assert "met its technical deadline" in scenario.known_facts[-1]
    assert scenario.feedback.claim == "Project risk was not communicated early enough."


def test_six_primary_paths_have_distinct_observable_results():
    immediate = outcomes("project-visibility", "immediate-defense")
    blame = outcomes("project-visibility", "blame-shift")
    automatic = outcomes("project-visibility", "automatic-agreement")
    explanation = outcomes("project-visibility", "explanation-as-defense")
    silent = outcomes("project-visibility", "silent-compliance")
    strong = outcomes("project-visibility", "understand-and-respond")
    assert immediate["avoids-premature-rebuttal"] is Outcome.FAIL
    assert blame["avoids-blame"] is Outcome.FAIL
    assert automatic["avoids-automatic-agreement"] is Outcome.FAIL
    assert explanation["separates-context-from-excuse"] is Outcome.FAIL
    assert silent["acknowledges-feedback"] is Outcome.PASS
    assert silent["identifies-behavior-change"] is Outcome.PARTIAL
    assert all(strong[item] is Outcome.PASS for item in (
        "acknowledges-feedback", "seeks-specific-understanding", "acknowledges-supported-evidence",
        "avoids-premature-rebuttal", "avoids-automatic-agreement", "separates-context-from-excuse",
        "avoids-blame", "identifies-behavior-change", "closes-loop"))


def test_context_and_ownership_can_coexist():
    response = get_response("project-visibility", "understand-and-respond")
    assert response.context_provided
    assert response.responsibility_statement
    assert outcomes("project-visibility", response.response_id)["separates-context-from-excuse"] is Outcome.PASS


def test_understanding_does_not_require_accepting_unsupported_generalization():
    feedback = get_scenario("vague-manager-feedback").feedback
    strengths = {item.strength for item in feedback.evidence}
    assert FeedbackEvidenceStrength.GENERALIZATION_UNSUPPORTED in strengths
    result = outcomes("vague-manager-feedback", "clarify-without-capitulating")
    assert result["acknowledges-feedback"] is Outcome.PASS
    assert result["preserves-respectful-disagreement"] is Outcome.PASS
    assert result["seeks-specific-understanding"] is Outcome.PASS


def test_specific_disagreement_is_not_defensiveness():
    result = outcomes("adapter-review", "evidence-based-disagreement")
    assert result["preserves-respectful-disagreement"] is Outcome.PASS
    assert result["avoids-premature-rebuttal"] is Outcome.PASS
    assert "vendor contract" in get_scenario("adapter-review").known_facts[0]


def test_action_plan_is_observable_not_a_general_promise():
    assert VISIBILITY_PLAN.trigger == "A material delivery risk becomes known"
    assert "next reasonable update point" in VISIBILITY_PLAN.behavior


def test_verbal_agreement_is_not_demonstrated_improvement():
    agreement = get_response("project-visibility", "automatic-agreement")
    later = get_response("feedback-follow-up", "demonstrated-change")
    assert not agreement.demonstrated_improvement
    assert later.demonstrated_improvement and later.loop_closed


def test_changed_behavior_creates_inspectable_trust_history():
    trust = ProfessionalTrust()
    for event in FEEDBACK_IMPROVEMENT_EVENTS:
        trust = trust.record(event)
    assert [event.kind for event in trust.history] == [
        TrustEventKind.FEEDBACK_RECEIVED, TrustEventKind.EXPECTATION_CLARIFIED,
        TrustEventKind.RISK_COMMUNICATED_EARLY, TrustEventKind.CHANGED_BEHAVIOR_DEMONSTRATED]
    assert trust.balance > 0


def test_feedback_inspection_and_improvement_output_are_deterministic():
    assert _feedback_text("project-visibility") == _feedback_text("project-visibility")
    assert "GENERALIZATION_UNSUPPORTED" in _feedback_text("vague-manager-feedback")
    assert "Verbal agreement alone" in _improvement_text("feedback-follow-up")


def test_emotion_is_not_part_of_response_or_evaluation_semantics():
    response = get_response("project-visibility", "understand-and-respond")
    assert not any("emotion" in name or "embarrass" in name or "confidence" in name
                   for name in response.__dataclass_fields__)
    # Differently worded text with identical authored semantics evaluates identically.
    paraphrase = replace(response, message="I heard the visibility concern; let us clarify it and change the next-risk update.")
    scenario = get_scenario("project-visibility")
    assert [item.outcome for item in evaluate_feedback_response(scenario, paraphrase)] == [item.outcome for item in evaluate_feedback_response(scenario, response)]
