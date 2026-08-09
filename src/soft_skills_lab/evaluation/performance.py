"""Deterministic evaluation of Chapter 17 observable plan behavior."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("identifies-supported-performance-evidence", "Acknowledges examples supported by the record."),
    EvaluationCriterion("corrects-material-inaccuracy", "Can preserve a material factual correction without wholesale rejection."),
    EvaluationCriterion("clarifies-performance-expectation", "Turns broad concern into observable expected behavior."),
    EvaluationCriterion("establishes-measurement", "Defines a reasonable way to inspect improvement."),
    EvaluationCriterion("establishes-checkpoints", "Makes progress reviews explicit."),
    EvaluationCriterion("avoids-vague-improvement-promise", "Avoids an unmeasured promise to do better."),
    EvaluationCriterion("focuses-on-controllable-behavior", "Prefers behavior reasonably within professional control."),
    EvaluationCriterion("tracks-evidence-over-time", "Preserves a pattern rather than one isolated event."),
    EvaluationCriterion("preserves-plan-scope", "Keeps formal changes explicit and traceable."),
    EvaluationCriterion("demonstrates-improvement", "Shows the defined behavior in later work events."),
)

def evaluate_performance_response(scenario: WorkplaceScenario, response: ProfessionalResponse):
    values = {criterion.criterion_id: getattr(response, criterion.criterion_id.replace("-", "_")) for criterion in CRITERIA[:-1]}
    values["demonstrates-improvement"] = response.demonstrates_plan_improvement
    partial = {
        "automatic-confession": {"identifies-supported-performance-evidence", "avoids-vague-improvement-promise"},
        "argue-every-example": {"identifies-supported-performance-evidence"},
        "vague-promise": {"identifies-supported-performance-evidence", "clarifies-performance-expectation", "avoids-vague-improvement-promise"},
        "passive-signoff": {"identifies-supported-performance-evidence"},
    }.get(response.response_id, set())
    applicable = set(values)
    if (response.clarifies_performance_expectation and response.establishes_measurement
            and response.establishes_checkpoints and not response.demonstrates_plan_improvement):
        applicable.remove("demonstrates-improvement")
    results = []
    for criterion in CRITERIA:
        if criterion.criterion_id not in applicable:
            outcome, explanation = Outcome.PARTIAL, "The initial plan is actionable; later work evidence is not part of this response stage."
        elif criterion.criterion_id in partial:
            outcome, explanation = Outcome.PARTIAL, "Some relevant content is present, but it does not complete this behavior."
        else:
            outcome = Outcome.PASS if values[criterion.criterion_id] else Outcome.FAIL
            explanation = "Authored observable behavior satisfies this criterion." if outcome is Outcome.PASS else "The response does not make this behavior visible."
        results.append(EvaluationResult(criterion, outcome, explanation, (response.message,)))
    return tuple(results)
