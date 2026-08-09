"""Deterministic Chapter 2 communication contexts and reference responses."""

from soft_skills_lab.domain.models import (
    CommunicationContext, ListenerInterpretation, Participant, ProfessionalResponse, RiskLevel, WorkplaceScenario,
)

DEMO_FACTS = (
    "Customer demo is Thursday.",
    "Reporting screen failed twice yesterday.",
    "Failures occurred while changing the date range.",
    "Morgan is concerned about safely demonstrating the screen.",
)
DEMO_UNKNOWNS = (
    "Root cause of the failures.", "Reproduction rate.", "Whether a workaround exists.",
    "Whether all reporting behavior must be stable for the demo.", "Whether the demo can avoid the failing interaction.",
)
DEMO_ASSUMPTIONS = (
    "Morgan is blaming Alex.", "The module must be rewritten.", "The demo must be cancelled.", "Alex must work overtime.",
)
DEMO_CONTEXT = CommunicationContext(
    DEMO_FACTS, "Morgan needs enough evidence to decide whether the reporting screen can be demoed safely Thursday.",
    "Determine whether the reporting screen can be safely demonstrated.", ("The customer demo is Thursday.",),
    DEMO_UNKNOWNS, ("The observed instability may threaten the demo.",), DEMO_ASSUMPTIONS,
)
DEMO_STABILITY = WorkplaceScenario(
    "demo-stability", "Listening before responding to a demo concern",
    "Morgan tells Alex: “The customer demo is Thursday, and I'm worried that the reporting screen still isn't stable. "
    "Yesterday I saw it fail twice when changing the date range. I need to know whether we can safely demo this.”",
    (Participant("Morgan", "engineering manager"), Participant("Alex", "developer")), DEMO_FACTS, DEMO_UNKNOWNS,
    (), RiskLevel.HIGH, DEMO_CONTEXT,
)

def interpretation(*, facts=(), intent=(), assumptions=(), questions=(), proposal=None):
    return ListenerInterpretation(facts, intent, assumptions, questions, proposal)

DEMO_RESPONSES = {
    "premature-solution": ProfessionalResponse(
        "premature-solution", "Premature solution", "I'll rewrite the date filtering code today.",
        unsupported_promise=True, next_action="Rewrite date filtering before diagnosing it.",
        listener_interpretation=interpretation(intent=("Morgan wants date filtering rewritten today.",),
            assumptions=("The date filtering code is the cause.", "A rewrite is required."), proposal="Rewrite the code today."),
    ),
    "defensive-interpretation": ProfessionalResponse(
        "defensive-interpretation", "Defensive interpretation",
        "That code was working when I finished it. Someone else changed the reporting module afterward.",
        assumptions=("Morgan blamed Alex.", "Someone else's change caused the failures."), assigns_unsupported_blame=True,
        claims_cause_without_evidence=True,
        listener_interpretation=interpretation(assumptions=("Morgan is accusing Alex.", "Someone else caused the issue.")),
    ),
    "passive-acknowledgment": ProfessionalResponse(
        "passive-acknowledgment", "Passive acknowledgment", "Okay, I'll take a look.",
        next_action="Take an unspecified look at the issue.",
        listener_interpretation=interpretation(proposal="Look at the issue."),
    ),
    "listen-then-clarify": ProfessionalResponse(
        "listen-then-clarify", "Listen, then clarify",
        "The two date-range failures make Thursday's demo risky. I don't know the cause yet. I'll reproduce the "
        "failure and check whether that interaction is required for a safe demo, then update you at 15:00.",
        acknowledged_facts=DEMO_FACTS, known_information=DEMO_FACTS,
        unknown_information=("Root cause of the failures.", "Whether the failing interaction is required in the demo."),
        next_action="Reproduce the date-range failure and assess the demo path.", follow_up_commitment="Update Morgan at 15:00.",
        captures_explicit_concern=True, distinguishes_fact_from_interpretation=True, clarifies_success_condition=True,
        listener_interpretation=interpretation(facts=DEMO_FACTS, intent=(DEMO_CONTEXT.expressed_concern,),
            questions=("Is changing the date range required for the demo?",), proposal="Investigate, then report at 15:00."),
    ),
    "understand-then-disagree": ProfessionalResponse(
        "understand-then-disagree", "Understand, then respectfully disagree",
        "If I understand correctly, the two failures make Thursday's demo risky. We should investigate that risk, "
        "but I don't think we have evidence that the module needs a rewrite. I'll report findings at 15:00.",
        acknowledged_facts=DEMO_FACTS, known_information=DEMO_FACTS,
        unknown_information=("Root cause of the failures.",), next_action="Investigate the observed failures.",
        follow_up_commitment="Report findings at 15:00.", captures_explicit_concern=True,
        distinguishes_fact_from_interpretation=True, clarifies_success_condition=True, respectful_disagreement=True,
        listener_interpretation=interpretation(facts=DEMO_FACTS, intent=(DEMO_CONTEXT.expressed_concern,),
            questions=("What evidence explains the failures?",), proposal="Investigate without assuming a rewrite."),
    ),
}

TEAM_CONTEXT = CommunicationContext(
    ("Jordan is having trouble integrating Alex's endpoint.", "The response differs from the discussed example.",
     "Jordan is spending substantial time adapting the frontend."),
    "Jordan needs the API contract mismatch resolved.", None, (),
    ("Whether the API contract intentionally changed.", "Whether the example is outdated.",
     "Whether the API or frontend should change."),
    ("The discussed example or current endpoint could be authoritative.",),
    ("Jordan wants Alex to implement the frontend.",),
)
TEAMMATE_CONTRACT = WorkplaceScenario(
    "teammate-contract", "Clarifying a teammate's API contract concern",
    "Jordan tells Alex the endpoint response differs from their example and frontend adaptation is consuming time.",
    (Participant("Jordan", "frontend developer"), Participant("Alex", "API developer")),
    TEAM_CONTEXT.explicit_facts, TEAM_CONTEXT.unknowns, (), RiskLevel.MODERATE, TEAM_CONTEXT,
)
TEAM_RESPONSES = {
    "assume-frontend-request": ProfessionalResponse("assume-frontend-request", "Invented implementation request",
        "I'll implement the frontend for you.", assumptions=TEAM_CONTEXT.unsupported_assumptions,
        listener_interpretation=interpretation(assumptions=TEAM_CONTEXT.unsupported_assumptions), unsupported_promise=True),
    "clarify-contract": ProfessionalResponse("clarify-contract", "Clarify the authoritative contract",
        "I understand the mismatch is costing frontend time. Let's compare the endpoint with the agreed contract and "
        "establish whether the example or response is authoritative before either of us changes code.",
        acknowledged_facts=TEAM_CONTEXT.explicit_facts, known_information=TEAM_CONTEXT.explicit_facts,
        unknown_information=TEAM_CONTEXT.unknowns, next_action="Compare the endpoint, example, and agreed contract.",
        captures_explicit_concern=True, distinguishes_fact_from_interpretation=True, clarifies_success_condition=True,
        listener_interpretation=interpretation(facts=TEAM_CONTEXT.explicit_facts, questions=TEAM_CONTEXT.unknowns)),
}

SEARCH_CONTEXT = CommunicationContext(
    ("A stakeholder says search feels slow.", "The stakeholder believes customers will not wait."),
    "The stakeholder is concerned that search performance will lose customers.", None, (),
    ("What ‘slow’ means.", "Which search workflow.", "Observed latency and frequency.", "Device and environment.",
     "Business impact.", "Acceptable performance."),
    ("A search experience may not meet an unstated performance expectation.",), ("The search system must be rewritten.",),
)
STAKEHOLDER_SEARCH = WorkplaceScenario(
    "stakeholder-search", "Clarifying stakeholder language about search",
    "A nontechnical stakeholder says: “Search feels slow. Customers aren't going to wait this long.”",
    (Participant("Riley", "business stakeholder"), Participant("Alex", "developer")), SEARCH_CONTEXT.explicit_facts,
    SEARCH_CONTEXT.unknowns, (), RiskLevel.MODERATE, SEARCH_CONTEXT,
)
SEARCH_RESPONSES = {
    "rewrite-search": ProfessionalResponse("rewrite-search", "Assume a rewrite", "I'll rewrite the search system.",
        assumptions=SEARCH_CONTEXT.unsupported_assumptions, unsupported_promise=True,
        listener_interpretation=interpretation(assumptions=SEARCH_CONTEXT.unsupported_assumptions)),
    "measure-and-clarify": ProfessionalResponse("measure-and-clarify", "Clarify and measure",
        "I understand the concern is customers abandoning slow searches. Which workflow and environment did you "
        "observe, and what response time is acceptable? I'll measure that path before proposing a change.",
        acknowledged_facts=SEARCH_CONTEXT.explicit_facts, known_information=SEARCH_CONTEXT.explicit_facts,
        unknown_information=SEARCH_CONTEXT.unknowns, next_action="Measure the identified search path.",
        captures_explicit_concern=True, distinguishes_fact_from_interpretation=True, clarifies_success_condition=True,
        listener_interpretation=interpretation(facts=SEARCH_CONTEXT.explicit_facts, questions=SEARCH_CONTEXT.unknowns)),
}

PRIMARY_RESPONSE_IDS = ("premature-solution", "defensive-interpretation", "passive-acknowledgment", "listen-then-clarify")
