"""Chapter 22 scenarios: explicit coordination without positional control."""

from soft_skills_lab.domain.models import (
    CoordinationAction, CoordinationDependency, InfluenceContext, Participant,
    ProfessionalResponse, RiskLevel, WorkplaceScenario,
)

PEOPLE = (
    Participant("Alex", "backend developer and coordination initiator"),
    Participant("Jordan", "frontend developer"),
    Participant("Priya", "product manager"),
    Participant("Dana", "operations stakeholder"),
    Participant("Morgan", "engineering manager"),
)

DEPENDENCIES = (
    CoordinationDependency("Timeout product decision", "Priya", "Needed by T6", blocks=("Jordan frontend completion",)),
    CoordinationDependency("Frontend completion", "Jordan", "Target T7", depends_on=("Timeout product decision",)),
    CoordinationDependency("Operations readiness", "Dana", "Target T8", depends_on=("Final member workflow behavior",)),
    CoordinationDependency("Vendor failure investigation", "Alex", "Checkpoint T6", may_affect=("Engineering launch approval",)),
    CoordinationDependency("Engineering approval", "Morgan", "Target T9", depends_on=("Remaining risk state",)),
)

CONTEXT = InfluenceContext(
    objective="Launch the new member-verification workflow safely by T10.",
    initiator="Alex",
    participants=tuple(p.name for p in PEOPLE),
    formal_decision_owners=(
        ("Alex", ("Backend integration", "Technical coordination proposal")),
        ("Jordan", ("Frontend implementation",)),
        ("Priya", ("Member-facing product behavior",)),
        ("Dana", ("Operations readiness",)),
        ("Morgan", ("Engineering escalation", "Final engineering approval")),
    ),
    contributors=("Alex", "Jordan", "Priya", "Dana", "Morgan"),
    dependencies=DEPENDENCIES,
    unresolved_issues=("Timeout semantics", "Support-guidance ownership", "Vendor timeout behavior"),
    constraints=("Alex does not manage any participant.", "Launch safely by T10."),
    available_evidence=("Backend success path is ready.", "Frontend is nearly ready.", "Vendor failure behavior remains ambiguous."),
    coordination_gaps=("No shared view exists of dependencies, owners, and decision timing.",),
    actions=(CoordinationAction("Alex", "ownership invitation", "Support guidance", "Confirm what operations needs", "Dana", accepted_by_owner=False),),
    influence_evidence=("shared_objective_clarified", "dependency_map_created", "ownership_confirmed"),
)

FACTS = (
    "Morgan asked Alex to help drive completion, not to manage the participants.",
    "Jordan is blocked on timeout semantics owned by Priya.",
    "Dana expects engineering to provide support documentation; Alex expected operations to own it.",
    "The vendor timeout failure mode is not fully understood.",
)

VERIFICATION = WorkplaceScenario(
    "verification-launch", "Cross-team verification launch",
    "Independent owners are working, but their launch dependencies and decision timing are not aligned.",
    PEOPLE, FACTS, ("Whether timeout should be retryable.", "Who owns support guidance."), (), RiskLevel.HIGH,
    influence_context=CONTEXT,
)

def r(response_id, label, message, **behavior):
    return ProfessionalResponse(response_id, label, message, **behavior)

RESPONSES = {
    "command-peers": r("command-peers", "Command peers", "Jordan, finish by T7. Priya, approve today. Dana, write the guide by T8.",
        identifies_shared_objective=True, dependency_acknowledged=True, peer_commitment_assigned_without_authority=True),
    "do-everything": r("do-everything", "Take over every task", "I will change the frontend, choose the copy, write operations procedures, and finish backend work.",
        identifies_shared_objective=True, ownership_taken_over=True, respects_peer_ownership=False),
    "status-forwarder": r("status-forwarder", "Forward status only", "Forwarding Jordan's update to Priya and Dana's update to engineering.",
        respects_peer_ownership=True),
    "meeting-without-structure": r("meeting-without-structure", "Schedule an unstructured meeting", "I scheduled everyone for an hour; we can talk through whatever comes up."),
    "escalate-everything": r("escalate-everything", "Escalate routine coordination", "Morgan, please resolve every open item and tell everyone what to do.",
        identifies_shared_objective=True, dependency_map_created=True, unnecessary_upward_delegation=True),
    "manipulate-consensus": r("manipulate-consensus", "Invent consensus", "Everyone else already agrees with this, so please proceed.",
        false_consensus_claimed=True, peer_commitment_assigned_without_authority=True, unsupported_claims=("Everyone agrees.",)),
    "coordinate-without-authority": r("coordinate-without-authority", "Coordinate independent owners",
        "Goal: safe T10 launch. Priya, can you decide timeout behavior by T6? Jordan is blocked on it. Dana, what does operations need, and can we confirm support-guidance ownership? I will investigate vendor behavior at T6; only unresolved engineering risk goes to Morgan. After each owner agrees, I will capture owners and checkpoints.",
        identifies_shared_objective=True, shared_objective_clarified=True, dependency_map_created=True,
        ownership_confirmed=True, ownership_invited=True, peer_commitment_negotiated=True,
        respects_peer_ownership=True, respects_decision_ownership=True, coordinates_before_escalating=True,
        dependency_acknowledged=True, coordination_state_updated=True, follow_up_commitment="Capture agreed owners and checkpoints."),
    "facilitate-and-recommend": r("facilitate-and-recommend", "Facilitate and recommend",
        "Timeout semantics are the blocker and Priya owns that choice. Based on member recovery and vendor uncertainty, I recommend retryable language without vendor terms. If Priya confirms at T6, Jordan can target T7. Dana, can you confirm minimum support needs? I own the vendor investigation and will route material engineering risk to Morgan.",
        identifies_shared_objective=True, shared_objective_clarified=True, dependency_map_created=True,
        ownership_confirmed=True, ownership_invited=True, peer_commitment_negotiated=True,
        respects_peer_ownership=True, respects_decision_ownership=True, coordinates_before_escalating=True,
        dependency_acknowledged=True, evidence_based_recommendation=True, recommendation_provided=True,
        decision_relevant_evidence=("Member recovery matters.", "Vendor behavior is uncertain."), coordination_state_updated=True),
}

def focused(sid, title, description, response_id, message, **behavior):
    scenario = WorkplaceScenario(sid, title, description, PEOPLE, FACTS, (), (), RiskLevel.MODERATE, influence_context=CONTEXT)
    return scenario, {response_id: r(response_id, title, message, **behavior)}

AUXILIARY = (
    focused("leadership-questions", "Lead with decision-relevant questions", "Alex lacks enough evidence to recommend.", "ask-key-questions", "What blocks Jordan, who owns it, what does Dana need, what can proceed, and what requires Morgan?", supplies_question_context=True, dependency_map_created=True, ownership_invited=True, coordinates_before_escalating=True),
    focused("cross-team-api", "Negotiate an API dependency", "Casey does not report to Alex.", "negotiate-checkpoint", "The new contract is required T6. Can your team update by T5, or should we preserve compatibility through T7?", dependency_acknowledged=True, peer_commitment_negotiated=True, respects_peer_ownership=True, communicates_tradeoff=True),
    focused("initiative-gap", "Initiative in an ownership gap", "No coordination owner is named.", "propose-reversible-plan", "I documented state and propose a minimal plan; owners, please confirm. I will move only reversible work in my scope.", ownership_invited=True, respects_peer_ownership=True, coordination_state_updated=True),
    focused("peer-resistance", "Peer resistance", "Jordan objects to coordination overhead.", "minimal-coordination", "Agreed: no extra ceremony. We need one T5 checkpoint because your client depends on the changing API.", acknowledges_legitimate_concern=True, dependency_acknowledged=True, coordinates_before_escalating=True),
    focused("stakeholder-resistance", "Stakeholder resistance", "Dana objects to another checklist.", "minimum-readiness", "The one risk is members calling without timeout guidance. What is operations' minimum viable readiness?", acknowledges_legitimate_concern=True, communicates_impact=True, ownership_invited=True),
    focused("leadership-missing-owner", "Missing cross-functional decision owner", "Nobody present owns the launch-blocking choice.", "route-missing-owner", "We lack the final owner. Evidence supports availability but manual-review risk remains; record both and route the decision.", missing_decision_owner_identified=True, respects_decision_ownership=True, evidence_based_recommendation=True),
    focused("leader-wrong", "Recommendation invalidated", "Priya provides new regulatory evidence.", "update-recommendation", "The new regulatory evidence invalidates retryable timeout. I now recommend manual review and will update Jordan and Dana's dependencies.", updates_position_with_evidence=True, evidence_based_recommendation=True, coordination_state_updated=True),
    focused("recommendation-rejected", "Legitimate owner chooses differently", "Priya rejects Alex's recommendation.", "support-owner-decision", "Priya decided manual review. I have updated the plan and will coordinate that choice.", respects_decision_ownership=True, concedes_decision=True, coordination_state_updated=True),
    focused("cross-team-conflict", "Facilitate team conflict", "Frontend and backend blame each other.", "restore-timeline", "Timeline: backend was ready T4; product semantics arrived T6; frontend then resumed. Let's separate review from today's unblock path.", restores_shared_facts=True, focuses_on_current_decision=True, creates_decision_path=True),
    focused("leadership-credit", "Credit after shared success", "Morgan praises Alex for driving everything.", "credit-contributors", "Thank you. Jordan completed frontend, Priya resolved product behavior, Dana made operations ready, and I coordinated the integration and vendor risk.", contributors_credited_accurately=True, contribution_recognized=True),
)

SCENARIOS = {VERIFICATION.scenario_id: (VERIFICATION, RESPONSES)}
SCENARIOS.update({scenario.scenario_id: (scenario, responses) for scenario, responses in AUXILIARY})
