"""Deterministic evaluation of scenario-authored peer collaboration behavior."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("makes-handoff-explicit", "Communicates that an artifact is ready for dependency use."),
    EvaluationCriterion("provides-handoff-context", "Provides the information needed to use the artifact."),
    EvaluationCriterion("seeks-handoff-acknowledgement", "Confirms a consequential receiver can proceed."),
    EvaluationCriterion("respects-peer-ownership", "Avoids silently taking over a peer's work."),
    EvaluationCriterion("helps-without-taking-over", "Addresses a blocker while returning appropriate ownership."),
    EvaluationCriterion("accounts-for-help-opportunity-cost", "Considers the helper's existing commitments."),
    EvaluationCriterion("clarifies-shared-ownership", "Turns ambiguous shared responsibility into action ownership."),
    EvaluationCriterion("addresses-peer-dependency-directly", "Checks with the peer before escalation when appropriate."),
    EvaluationCriterion("recognizes-contribution", "Accurately represents a meaningful teammate contribution."),
    EvaluationCriterion("acknowledges-dependency", "Makes the effect on dependent work explicit."),
    EvaluationCriterion("closes-loop", "Establishes or completes the required peer follow-up."),
    EvaluationCriterion("avoids-blame", "Keeps dependency coordination factual rather than blaming."),
    EvaluationCriterion("distinguishes-preference-from-defect", "Distinguishes material defects from personal preference."),
    EvaluationCriterion("uses-decision-relevant-evidence", "Connects a review or disagreement to decision evidence."),
)

def evaluate_collaboration_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    if scenario.peer_collaboration is None:
        raise ValueError("collaboration evaluation requires peer collaboration context")
    sid = scenario.scenario_id
    relevant = {
        "verification-integration": {0, 1, 2, 3, 4, 9, 10, 11},
        "peer-code-review": {3, 11, 12, 13}, "teammate-context": {3}, "bounded-peer-help": {3, 4, 5},
        "shared-peer-task": {6, 10}, "missed-peer-commitment": {7, 9, 11},
        "team-contribution": {8}, "help-dependency": {1, 3, 4},
    }[sid]
    values = (
        response.handoff_explicit, response.handoff_context_provided, response.handoff_acknowledgement_sought,
        response.respects_peer_ownership, response.helps_without_taking_over,
        response.accounts_for_help_opportunity_cost, response.shared_ownership_clarified,
        response.peer_dependency_addressed_directly, response.contribution_recognized,
        response.dependency_acknowledged, response.loop_closed, not response.assigns_unsupported_blame,
        response.distinguishes_preference_from_defect, bool(response.decision_relevant_evidence),
    )
    results = []
    for index in sorted(relevant):
        value = values[index]
        # A notified but context-free handoff and uncoordinated helping expose partial progress.
        partial = sid == "verification-integration" and response.response_id in ("throw-over-wall", "over-help") and index in ({9, 10} if response.response_id == "throw-over-wall" else {0, 1, 10})
        outcome = Outcome.PARTIAL if partial else Outcome.PASS if value else Outcome.FAIL
        explanation = "Authored behavior partially advances this dimension." if partial else ("Authored behavior satisfies this criterion." if value else "Authored behavior leaves this criterion unsatisfied.")
        results.append(EvaluationResult(CRITERIA[index], outcome, explanation, (response.message,)))
    return tuple(results)
