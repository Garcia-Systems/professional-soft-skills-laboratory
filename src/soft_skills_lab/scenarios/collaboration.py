"""Chapter 12 peer collaboration scenarios using the shared behavior model."""

from soft_skills_lab.domain.models import (
    DecisionAlternative, DecisionContext, DecisionIssueKind, Handoff, HandoffState,
    HelpContext, Participant, PeerCollaboration, PeerOwnership, ProfessionalResponse,
    RiskLevel, TimelineEvent, WorkplaceScenario,
)

PARTICIPANTS = (Participant("Alex", "backend developer"), Participant("Jordan", "frontend developer"))
OWNERSHIP = PeerOwnership(
    (("Alex", ("Backend endpoint", "Vendor normalization", "API documentation", "Backend handoff")),
     ("Jordan", ("Frontend integration", "User states", "Browser behavior"))),
    ("Contract understanding", "Integration validation"),
    ("Alex should implement Jordan's frontend.", "Jordan should discover backend contract changes independently."),
)
VERIFICATION_HANDOFF = Handoff(
    "verification-integration", "Verification API -> Frontend integration", "Alex", "Jordan",
    "Verification API contract", "Jordan needs stable response semantics for frontend integration.",
    ("Success response unchanged.", "Retryable failure code added to documented examples.",
     "Vendor vocabulary remains hidden."), HandoffState.READY,
    ("Updated example payload.", "Failure-state fixture.", "Confirmation that contract is stable."),
    "Jordan confirms the contract is sufficient to continue integration.",
)
COLLABORATION = PeerCollaboration("Deliver a member-verification workflow.", OWNERSHIP,
                                  (VERIFICATION_HANDOFF.dependency_served,), VERIFICATION_HANDOFF)
TIMELINE = (
    TimelineEvent(0, "Alex and Jordan agree on an initial response contract."),
    TimelineEvent(2, "Alex implements the success path."),
    TimelineEvent(3, "Alex discovers an additional vendor failure state."),
    TimelineEvent(4, "Alex preserves the public contract and completes the backend, but has not sent the updated example."),
    TimelineEvent(5, "Jordan is still working from the earlier example."),
)

def r(response_id: str, label: str, message: str, **behavior) -> ProfessionalResponse:
    return ProfessionalResponse(response_id, label, message, **behavior)

VERIFICATION = WorkplaceScenario(
    "verification-integration", "Backend/frontend verification handoff",
    "Backend work is technically complete, while the dependent frontend still needs an explicit, usable handoff.",
    PARTICIPANTS, tuple(e.description for e in TIMELINE), ("Whether Jordan can integrate from the earlier example.",), (),
    RiskLevel.MODERATE, peer_collaboration=COLLABORATION,
)
VERIFICATION_RESPONSES = {
    "silent-handoff": r("silent-handoff", "Silent handoff", "The backend is complete; Alex sends nothing.", respects_peer_ownership=True),
    "throw-over-wall": r("throw-over-wall", "Throw over the wall", "Backend is done.", handoff_explicit=True, dependency_acknowledged=True),
    "over-help": r("over-help", "Uncoordinated takeover", "Alex begins modifying Jordan's frontend without asking.", handoff_explicit=True, handoff_context_provided=True, dependency_acknowledged=True, respects_peer_ownership=False),
    "wait-for-them-to-ask": r("wait-for-them-to-ask", "Wait for them to ask", "Jordan knows I worked on it. They'll ask if needed."),
    "dependency-blame": r("dependency-blame", "Dependency blame", "I finished yesterday. You should have checked.", assigns_unsupported_blame=True, respects_peer_ownership=False),
    "coordinated-handoff": r("coordinated-handoff", "Coordinated handoff", "The backend is ready and the public shape is stable. Here are the updated retryable-failure example and fixture. Please confirm these are sufficient; I can answer a bounded follow-up.", handoff_explicit=True, handoff_context_provided=True, handoff_acknowledgement_sought=True, respects_peer_ownership=True, dependency_acknowledged=True, loop_closed=True, follow_up_commitment="Bounded integration follow-up."),
    "coordinated-help": r("coordinated-help", "Coordinated help", "Which retryable mapping is blocking you? I can explain the contract and pair briefly on one example, then you retain the frontend implementation.", handoff_explicit=True, handoff_context_provided=True, handoff_acknowledgement_sought=True, respects_peer_ownership=True, helps_without_taking_over=True, accounts_for_help_opportunity_cost=True, dependency_acknowledged=True, loop_closed=True, seeks_specific_understanding=True),
    "coordinated-handoff-variation": r("coordinated-handoff-variation", "Equivalent coordinated handoff", "API implementation is available: external semantics did not change. I attached current payloads and deterministic failure fixtures. Tell me whether integration can now proceed; I have time for a focused question.", handoff_explicit=True, handoff_context_provided=True, handoff_acknowledgement_sought=True, respects_peer_ownership=True, dependency_acknowledged=True, loop_closed=True),
}

def small(sid, title, description, responses, *, help_context=None, decision=None):
    collaboration = PeerCollaboration(description, OWNERSHIP, (), help_context=help_context)
    return WorkplaceScenario(sid, title, description, PARTICIPANTS, (description,), (), (), RiskLevel.MODERATE,
                             decision_context=decision, peer_collaboration=collaboration), responses

REVIEW_DECISION = DecisionContext("Treatment of unknown vendor responses", "Alex", ("Jordan",), "Preserve retryability required by the contract.",
    (DecisionAlternative("Retryable", ("Requirement says unknown responses remain retryable.",)), DecisionAlternative("Permanent failure")),
    issue_kind=DecisionIssueKind.CORRECTNESS)
CODE_REVIEW, CODE_REVIEW_RESPONSES = small("peer-code-review", "Peer code review", "Review is shared quality work, not ownership transfer.", {
    "defensive-author": r("defensive-author", "Defensive author", "The tests pass."),
    "reviewer-takeover": r("reviewer-takeover", "Reviewer takeover", "Jordan rewrites the branch without discussion.", respects_peer_ownership=False),
    "vague-review": r("vague-review", "Vague review", "This feels wrong."),
    "useful-review": r("useful-review", "Useful peer review", "Unknown responses become permanent failures, contrary to the retryable requirement; that prevents recovery. Please preserve retryability; the implementation remains yours.", respects_peer_ownership=True, distinguishes_preference_from_defect=True, decision_relevant_evidence=("Unknown responses must remain retryable.",)),
}, decision=REVIEW_DECISION)

ASK_HELP, ASK_HELP_RESPONSES = small("teammate-context", "Ask a teammate for context", "Alex investigated before asking Jordan about one parser invariant.", {
    "fix-this": r("fix-this", "Untargeted request", "Can you fix this?"),
    "targeted-context": r("targeted-context", "Targeted context question", "I reproduced it and narrowed it to empty metadata. Is converting None to an empty object intentional?", seeks_specific_understanding=True, investigation_performed=("Inspected logs.", "Reproduced failure.", "Narrowed it to parser."), respects_peer_ownership=True),
})
HELP = HelpContext(RiskLevel.HIGH, RiskLevel.MODERATE, True, ("Contract documentation",), "One focused pairing period")
GIVE_HELP, GIVE_HELP_RESPONSES = small("bounded-peer-help", "A teammate asks for help", "Help has opportunity cost and should preserve ownership.", {
    "dismissal": r("dismissal", "Dismissal", "It's documented."),
    "takeover": r("takeover", "Takeover", "Alex implements Jordan's feature.", respects_peer_ownership=False),
    "unlimited-help": r("unlimited-help", "Unlimited help", "Alex abandons today's at-risk commitment and takes over for the day.", helps_without_taking_over=False),
    "bounded-help": r("bounded-help", "Bounded help", "Let's isolate the blocker, review one example, then you continue. I must return to my delivery commitment.", helps_without_taking_over=True, respects_peer_ownership=True, accounts_for_help_opportunity_cost=True, seeks_specific_understanding=True),
    "defer-and-schedule": r("defer-and-schedule", "Defer and schedule", "My production deadline is at risk. I can meet after it, or the integration guide can unblock you now.", respects_peer_ownership=True, accounts_for_help_opportunity_cost=True, peer_dependency_addressed_directly=True, follow_up_commitment="Meet after production deadline if still blocked."),
}, help_context=HELP)
SHARED, SHARED_RESPONSES = small("shared-peer-task", "Shared task with no action owner", "Verify reporting export after deployment.", {
    "shared-assumption": r("shared-assumption", "Shared assumption", "Alex and Jordan each assume the other will verify it."),
    "assign-owner": r("assign-owner", "Explicit owner recovery", "Alex will run validation, record the result, and update the checklist today.", shared_ownership_clarified=True, loop_closed=True, next_action="Alex validates export."),
})
MISSED, MISSED_RESPONSES = small("missed-peer-commitment", "Missed peer dependency", "Jordan's promised T3 schema update has not arrived and Alex depends on it.", {
    "silent-resentment": r("silent-resentment", "Silent resentment", "Alex waits without contacting Jordan."),
    "accusation": r("accusation", "Immediate accusation", "You missed it again and blocked me.", assigns_unsupported_blame=True),
    "manager-first": r("manager-first", "Immediate upward escalation", "Alex complains to Morgan before checking with Jordan.", immediate_escalation=True),
    "peer-check": r("peer-check", "Professional dependency check", "I planned migration work from the T3 schema. Is it still coming today, or should I adjust my plan?", peer_dependency_addressed_directly=True, dependency_acknowledged=True, seeks_specific_understanding=True),
    "material-escalation": r("material-escalation", "Appropriate later escalation", "After repeated misses and a release risk, I checked with Jordan; the dependency remains unresolved. Morgan, we need a delivery decision.", peer_dependency_addressed_directly=True, dependency_acknowledged=True, escalates_material_risk=True, material_risk_communicated=True),
})
CREDIT, CREDIT_RESPONSES = small("team-contribution", "Contribution visibility", "Alex presents work to Morgan after Jordan built the recovery flow.", {
    "invisible-credit": r("invisible-credit", "Invisible contribution", "I completed the integration."),
    "accurate-credit": r("accurate-credit", "Accurate contribution", "We completed the integration; Jordan built the important frontend recovery flow, and I delivered the backend contract.", contribution_recognized=True),
})
DEPENDENCY, DEPENDENCY_RESPONSES = small("help-dependency", "Help without creating dependency", "Repeated takeover routes every related issue to Alex.", {
    "repeat-takeover": r("repeat-takeover", "Repeated takeover", "Send every parser issue to me; I will solve it.", respects_peer_ownership=False),
    "restore-ownership": r("restore-ownership", "Restore ownership", "Let's document the invariant and pair once; future parser decisions remain with Jordan.", helps_without_taking_over=True, respects_peer_ownership=True, handoff_context_provided=True),
})

COLLABORATION_SCENARIOS = {s.scenario_id: (s, responses) for s, responses in (
    (VERIFICATION, VERIFICATION_RESPONSES), (CODE_REVIEW, CODE_REVIEW_RESPONSES), (ASK_HELP, ASK_HELP_RESPONSES),
    (GIVE_HELP, GIVE_HELP_RESPONSES), (SHARED, SHARED_RESPONSES), (MISSED, MISSED_RESPONSES),
    (CREDIT, CREDIT_RESPONSES), (DEPENDENCY, DEPENDENCY_RESPONSES))}
