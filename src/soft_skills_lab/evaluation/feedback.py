"""Deterministic evaluation of observable feedback reception."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("acknowledges-feedback", "Shows that the feedback was heard."),
    EvaluationCriterion("seeks-specific-understanding", "Clarifies broad feedback when needed."),
    EvaluationCriterion("acknowledges-supported-evidence", "Recognizes established evidence."),
    EvaluationCriterion("avoids-premature-rebuttal", "Understands before rebutting."),
    EvaluationCriterion("avoids-automatic-agreement", "Does not accept unsupported claims merely to end discussion."),
    EvaluationCriterion("separates-context-from-excuse", "Context does not erase responsibility."),
    EvaluationCriterion("avoids-blame", "Does not divert feedback through unsupported blame."),
    EvaluationCriterion("identifies-behavior-change", "Names a concrete future behavior."),
    EvaluationCriterion("preserves-respectful-disagreement", "Allows evidence-based disagreement where warranted."),
    EvaluationCriterion("closes-loop", "Establishes follow-up or demonstrates it later."),
)

def evaluate_feedback_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    """Evaluate authored response meaning, never emotions, personality, or keywords."""
    disagreement_needed = bool(scenario.feedback and any(e.strength.name == "GENERALIZATION_UNSUPPORTED" for e in scenario.feedback.evidence)) or scenario.scenario_id == "adapter-review"
    checks: tuple[tuple[bool | None, str, tuple[str, ...]], ...] = (
        (response.acknowledges_feedback, "feedback was explicitly acknowledged", (response.message,)),
        (response.seeks_specific_understanding, "a focused clarification established the claim's scope", (response.message,)),
        (response.acknowledges_supported_evidence, "supported evidence was acknowledged", response.acknowledged_facts or (response.message,)),
        (not response.premature_rebuttal, "the response did not rebut before understanding", (response.message,)),
        (not response.automatic_agreement, "the response did not automatically accept every conclusion", (response.message,)),
        (not response.context_used_as_excuse, "context was absent or remained compatible with ownership", (response.message,)),
        (not response.assigns_unsupported_blame, "the response did not shift unsupported blame", (response.message,)),
        (response.identifies_behavior_change, "a concrete future behavior was identified", (response.next_action,) if response.next_action else ()),
        (response.preserves_respectful_disagreement if disagreement_needed else None,
         "supported disagreement was preserved" if disagreement_needed else "disagreement was not required by this scenario", (response.message,)),
        (bool(response.follow_up_commitment or response.loop_closed), "a follow-up was established or completed", (response.follow_up_commitment or response.message,)),
    )
    results = []
    for criterion, (passed, success, evidence) in zip(CRITERIA, checks, strict=True):
        if passed is None:
            outcome, explanation = Outcome.PARTIAL, success
        elif passed:
            outcome, explanation = Outcome.PASS, success
        else:
            outcome, explanation = Outcome.FAIL, criterion.description
            if criterion.criterion_id in {"acknowledges-feedback", "identifies-behavior-change"} and response.acknowledges_feedback:
                outcome = Outcome.PARTIAL
        results.append(EvaluationResult(criterion, outcome, explanation, evidence))
    return tuple(results)
