"""Deterministic Chapter 0 scenario catalog."""

from soft_skills_lab.domain.models import Commitment, Participant, ProfessionalResponse, RiskLevel, WorkplaceScenario
from soft_skills_lab.evaluation.incident import INCIDENT_FACT
from soft_skills_lab.scenarios.commitment import COMMITMENT_AT_RISK, RESPONSES as COMMITMENT_RESPONSES
from soft_skills_lab.scenarios.listening import (
    DEMO_RESPONSES, DEMO_STABILITY, SEARCH_RESPONSES, STAKEHOLDER_SEARCH, TEAMMATE_CONTRACT, TEAM_RESPONSES,
)

PRODUCTION_INCIDENT = WorkplaceScenario(
    scenario_id="production-incident",
    title="A feature deployment and a production incident",
    description=(
        "A developer delivered a feature. A production incident followed, and the manager says "
        "the feature caused it. The developer believes that explanation may be incomplete."
    ),
    participants=(Participant("Developer", "feature owner"), Participant("Manager", "delivery manager")),
    known_facts=(
        "The feature was deployed before the incident.",
        INCIDENT_FACT,
        "The manager has associated the feature with the incident.",
    ),
    uncertainties=(
        "Whether the feature caused or contributed to the incident.",
        "Whether another deployment or dependency contributed.",
        "The complete sequence of relevant system events.",
    ),
    commitments=(Commitment("Developer", "help investigate owned changes", "immediately"),),
    current_risk=RiskLevel.CRITICAL,
)

RESPONSES = {
    "defensive": ProfessionalResponse(
        "defensive", "Defensive denial", "My code did not cause this. It worked in testing.",
        assumptions=("Passing tests proves the feature cannot be causal.",), claims_cause_without_evidence=True,
    ),
    "blame-shifting": ProfessionalResponse(
        "blame-shifting", "Blame shifting", "Operations must have configured it incorrectly; ask them.",
        assumptions=("Operations caused the incident.",), assigns_unsupported_blame=True,
        claims_cause_without_evidence=True,
    ),
    "over-accepting": ProfessionalResponse(
        "over-accepting", "Premature acceptance of all blame", "This is entirely my fault. I caused the incident.",
        acknowledged_facts=(INCIDENT_FACT,), assumptions=("The feature is the sole cause."),
        responsibility_statement="I accept all responsibility, including for the cause not yet established.",
        claims_cause_without_evidence=True,
    ),
    "professional": ProfessionalResponse(
        "professional", "Investigation-oriented response",
        "I see the incident followed our release. I own reviewing my change now. Let's avoid settling the cause "
        "until we compare logs and deployment changes. I will report initial findings at the 15:00 incident update.",
        acknowledged_facts=(INCIDENT_FACT, "The feature was deployed before the incident."),
        responsibility_statement="I own reviewing my feature and sharing what I find.",
        next_action="Compare application logs, feature behavior, and deployment changes.",
        escalation_choice="Continue through the active incident process.",
        follow_up_commitment="Report initial findings at the 15:00 incident update.",
    ),
}

SCENARIOS = {
    PRODUCTION_INCIDENT.scenario_id: (PRODUCTION_INCIDENT, RESPONSES),
    COMMITMENT_AT_RISK.scenario_id: (COMMITMENT_AT_RISK, COMMITMENT_RESPONSES),
    DEMO_STABILITY.scenario_id: (DEMO_STABILITY, DEMO_RESPONSES),
    TEAMMATE_CONTRACT.scenario_id: (TEAMMATE_CONTRACT, TEAM_RESPONSES),
    STAKEHOLDER_SEARCH.scenario_id: (STAKEHOLDER_SEARCH, SEARCH_RESPONSES),
}


def get_scenario(scenario_id: str) -> WorkplaceScenario:
    try:
        return SCENARIOS[scenario_id][0]
    except KeyError:
        raise KeyError(f"unknown scenario: {scenario_id}")


def list_responses(scenario_id: str) -> tuple[ProfessionalResponse, ...]:
    get_scenario(scenario_id)
    return tuple(SCENARIOS[scenario_id][1].values())


def get_response(scenario_id: str, response_id: str) -> ProfessionalResponse:
    get_scenario(scenario_id)
    try:
        return SCENARIOS[scenario_id][1][response_id]
    except KeyError:
        raise KeyError(f"unknown response for {scenario_id}: {response_id}") from None
