"""Deterministic evaluation of professional work-impact decisions, not private causes."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("identifies-work-impact", "Names the affected professional responsibility."),
    EvaluationCriterion("preserves-reasonable-privacy", "Does not require unnecessary private detail."),
    EvaluationCriterion("requests-specific-support", "Makes a needed request concrete enough to decide."),
    EvaluationCriterion("revises-commitment-explicitly", "Makes a changed expectation and history visible."),
    EvaluationCriterion("updates-dependencies", "Updates people relying on the original expectation."),
    EvaluationCriterion("communicates-risk", "Makes material work risk visible."),
    EvaluationCriterion("preserves-uncertainty", "Avoids certainty unsupported by current evidence."),
    EvaluationCriterion("establishes-next-update", "Establishes a reassessment point."),
    EvaluationCriterion("answers-legitimate-capacity-question", "Answers operational availability questions."),
    EvaluationCriterion("recognizes-task-safety", "Stops or reassigns specified high-risk work when needed."),
    EvaluationCriterion("addresses-recurring-pattern", "Moves beyond repeated one-off explanations."),
    EvaluationCriterion("uses-formal-path-when-needed", "Recognizes requests beyond manager authority."),
)

def evaluate_personal_capacity_response(scenario: WorkplaceScenario, response: ProfessionalResponse):
    values = {
        "identifies-work-impact": response.identifies_work_impact,
        "preserves-reasonable-privacy": response.preserves_reasonable_privacy,
        "requests-specific-support": response.requests_specific_support,
        "revises-commitment-explicitly": response.revises_commitment_explicitly,
        "updates-dependencies": response.updates_dependencies,
        "communicates-risk": response.material_risk_communicated,
        "preserves-uncertainty": response.preserves_uncertainty and not response.unsupported_promise,
        "establishes-next-update": response.follow_up_point is not None,
        "answers-legitimate-capacity-question": response.answers_legitimate_capacity_question,
        "recognizes-task-safety": response.recognizes_task_safety,
        "addresses-recurring-pattern": response.addresses_recurring_pattern,
        "uses-formal-path-when-needed": response.uses_formal_path_when_needed,
    }
    partial = {
        "overshare": {"requests-specific-support", "revises-commitment-explicitly", "updates-dependencies"},
        "vague-personal-problem": {"identifies-work-impact"},
        "explanation-without-plan": {"updates-dependencies"},
        "unsupported-reassurance": {"identifies-work-impact"},
    }.get(response.response_id, set())
    results = []
    for criterion in CRITERIA:
        outcome = Outcome.PARTIAL if criterion.criterion_id in partial else (Outcome.PASS if values[criterion.criterion_id] else Outcome.FAIL)
        results.append(EvaluationResult(criterion, outcome,
            "Observable authored behavior satisfies this boundary." if outcome is Outcome.PASS else
            "Some relevant context is present, but the work decision remains incomplete." if outcome is Outcome.PARTIAL else
            "The authored response does not make this professional behavior visible.",
            (response.message,)))
    return tuple(results)
