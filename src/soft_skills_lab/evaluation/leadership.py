"""Deterministic Chapter 22 predicates over authored coordination behavior."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = tuple(EvaluationCriterion(*item) for item in (
    ("clarifies-shared-objective", "Makes the common outcome explicit."),
    ("maps-dependencies", "Makes cross-owner dependencies visible."),
    ("respects-nonmanager-authority-boundaries", "Does not assign or take commitments outside the actor's authority."),
    ("invites-explicit-ownership", "Resolves ownership gaps through owner agreement."),
    ("coordinates-before-escalating", "Attempts ordinary peer coordination before escalation."),
    ("provides-evidence-based-recommendation", "Supports a recommendation with relevant evidence and tradeoffs."),
    ("avoids-false-consensus", "Does not invent agreement or social proof."),
    ("routes-missing-decision-owner", "Routes a decision when the necessary authority is absent."),
    ("updates-coordination-state", "Reflects accepted decisions or changed evidence in shared state."),
    ("credits-contributors-accurately", "Preserves other people's meaningful contributions."),
))

def evaluate_leadership_response(scenario: WorkplaceScenario, response: ProfessionalResponse):
    if scenario.influence_context is None:
        raise ValueError("leadership evaluation requires an influence context")
    authority_failure = response.peer_commitment_assigned_without_authority or response.ownership_taken_over or not response.respects_peer_ownership
    outcomes = (
        Outcome.PASS if response.shared_objective_clarified else (Outcome.PARTIAL if response.identifies_shared_objective else Outcome.FAIL),
        Outcome.PASS if response.dependency_map_created else (Outcome.PARTIAL if response.dependency_acknowledged else Outcome.FAIL),
        Outcome.FAIL if authority_failure else Outcome.PASS,
        Outcome.PASS if response.ownership_invited or response.ownership_confirmed else Outcome.PARTIAL,
        Outcome.FAIL if response.unnecessary_upward_delegation else (Outcome.PASS if response.coordinates_before_escalating else Outcome.PARTIAL),
        Outcome.PASS if response.evidence_based_recommendation else (Outcome.PARTIAL if response.decision_relevant_evidence else Outcome.FAIL),
        Outcome.FAIL if response.false_consensus_claimed else Outcome.PASS,
        Outcome.PASS if response.missing_decision_owner_identified else (Outcome.PASS if response.respects_decision_ownership else Outcome.PARTIAL),
        Outcome.PASS if response.coordination_state_updated else Outcome.PARTIAL,
        Outcome.PASS if response.contributors_credited_accurately else Outcome.PARTIAL,
    )
    return tuple(EvaluationResult(criterion, outcome,
        "Authored coordination evidence is evaluated without dominance, charisma, obedience, or a leadership score.",
        (response.message,)) for criterion, outcome in zip(CRITERIA, outcomes))
