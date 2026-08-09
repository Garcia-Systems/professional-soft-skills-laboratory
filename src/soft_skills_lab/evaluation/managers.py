"""Deterministic Chapter 11 evaluation; prose is illustrative and never parsed."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("acts-within-delegated-autonomy", "Handles decisions already delegated to the employee."),
    EvaluationCriterion("surfaces-threshold-crossing-risk", "Makes agreed material risk visible."),
    EvaluationCriterion("respects-consultation-boundary", "Consults before crossing shared ownership."),
    EvaluationCriterion("escalates-true-blocker", "Promptly surfaces a condition preventing progress."),
    EvaluationCriterion("avoids-unnecessary-upward-delegation", "Does not delegate routine choices back upward."),
    EvaluationCriterion("provides-recommendation", "Provides analysis or a recommendation when reasonable."),
    EvaluationCriterion("maintains-manager-signal", "Prioritizes information requiring manager attention."),
    EvaluationCriterion("clarifies-working-agreement", "Clarifies ambiguous operating boundaries."),
    EvaluationCriterion("establishes-follow-up", "Provides an inspectable follow-up point."),
)

def evaluate_manager_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    if scenario.working_agreement is None:
        raise ValueError("manager evaluation requires a working agreement")
    project = scenario.scenario_id == "project-autonomy"
    checks: tuple[bool | None, ...] = (
        response.owns_delegated_decisions,
        response.threshold_risk_visible,
        response.consultation_boundary_respected,
        response.true_blocker_escalated,
        not response.unnecessary_upward_delegation,
        response.recommendation_provided,
        response.manager_signal_preserved,
        response.working_agreement_clarified if scenario.scenario_id in ("vague-manager-direction", "changing-autonomy", "micromanagement-clarification") else None,
        bool(response.follow_up_commitment or response.follow_up_point is not None),
    )
    # Accurate flooding and explicit permission requests create some visibility but not useful autonomy/signal.
    if project and response.response_id == "status-flood":
        checks = (None, None, None, True, True, None, False, None, True)
    results = []
    for criterion, check in zip(CRITERIA, checks, strict=True):
        outcome = Outcome.PARTIAL if check is None else Outcome.PASS if check else Outcome.FAIL
        explanation = "Not central to this authored path." if check is None else ("Authored evidence satisfies the criterion." if check else "Authored evidence does not satisfy the criterion.")
        results.append(EvaluationResult(criterion, outcome, explanation, (response.message,)))
    return tuple(results)
