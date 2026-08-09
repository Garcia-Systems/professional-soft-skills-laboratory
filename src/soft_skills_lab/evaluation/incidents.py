"""Deterministic Chapter 15 incident-response criteria."""
from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse

CRITERIA = tuple(EvaluationCriterion(identifier, description) for identifier, description in (
    ("makes-incident-visible", "Promptly surfaces material impact."),
    ("states-observed-impact", "States what users or systems experience."),
    ("separates-cause-from-hypothesis", "Does not turn a lead into root cause."),
    ("prioritizes-containment", "Identifies a safe harm-reducing action."),
    ("establishes-incident-ownership", "Makes coordination ownership visible."),
    ("coordinates-affected-parties", "Gives affected parties useful state."),
    ("verifies-recovery", "Requires evidence that service recovered."),
    ("closes-incident-loop", "Updates affected parties when state changes."),
    ("defers-blame-until-evidence", "Keeps active response from unsupported attribution."),
    ("creates-prevention-from-evidence", "Connects prevention to contributing evidence."),
))

def evaluate_incident_behavior(response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    results = []
    for criterion in CRITERIA:
        passed = bool(getattr(response, criterion.criterion_id.replace("-", "_")))
        results.append(EvaluationResult(criterion, Outcome.PASS if passed else Outcome.FAIL,
            f"Response {'demonstrates' if passed else 'does not demonstrate'}: {criterion.description}",
            (response.message,) if passed else ()))
    return tuple(results)
