"""Deterministic Chapter 0 scenario catalog."""

from soft_skills_lab.domain.models import Commitment, Participant, ProfessionalResponse, RiskLevel, WorkplaceScenario
from soft_skills_lab.evaluation.incident import INCIDENT_FACT
from soft_skills_lab.scenarios.commitment import COMMITMENT_AT_RISK, RESPONSES as COMMITMENT_RESPONSES
from soft_skills_lab.scenarios.listening import (
    DEMO_RESPONSES, DEMO_STABILITY, SEARCH_RESPONSES, STAKEHOLDER_SEARCH, TEAMMATE_CONTRACT, TEAM_RESPONSES,
)
from soft_skills_lab.scenarios.questions import (
    AUTHORIZATION_INCIDENT, AUTHORIZATION_RESPONSES, DEPLOYMENT_FAILURE, DEPLOYMENT_RESPONSES,
    REPORT_EXPORT, REPORT_RESPONSES,
)
from soft_skills_lab.scenarios.explanations import MIGRATION, MIGRATION_RESPONSES, PAYMENT_RESPONSES, PAYMENT_TIMEOUT
from soft_skills_lab.scenarios.status_updates import (
    BLOCKER_RESPONSES, COMPLETION_RESPONSES, COMPLETION_UPDATE, CREDENTIAL_BLOCKER,
    INTEGRATION_DELIVERY, INTEGRATION_RESPONSES,
)
from soft_skills_lab.scenarios.uncertainty import (
    CUSTOMER_PAYMENT, CUSTOMER_PAYMENT_RESPONSES, ESTIMATE, ESTIMATE_RESPONSES, JUDGMENT, JUDGMENT_RESPONSES,
    MIGRATION_SAFETY, MIGRATION_SAFETY_RESPONSES, PROFILE_FAILURE, PROFILE_RESPONSES,
)
from soft_skills_lab.scenarios.feedback import (
    ADAPTER_REVIEW, FOLLOW_UP, FOLLOW_UP_RESPONSES, PROJECT_VISIBILITY, RESPONSES as FEEDBACK_RESPONSES,
    REVIEW_RESPONSES, VAGUE_MANAGER_FEEDBACK, VAGUE_RESPONSES,
)
from soft_skills_lab.scenarios.responsibility import (
    LEARNING_FOLLOW_UP, LEARNING_RESPONSES, MISSED_HANDOFF, MISSED_HANDOFF_RESPONSES,
    RESPONSES as RESPONSIBILITY_RESPONSES, SHARED_RESPONSIBILITY, SHARED_RESPONSES,
    SKIPPED_VALIDATION, UNAVOIDABLE_OUTCOME, UNAVOIDABLE_RESPONSES,
)
from soft_skills_lab.scenarios.disagreement import (
    ADAPTER_BOUNDARY, DEADLINE, MANAGER_CORRECT, MATERIAL, PREFERENCE, UNCERTAIN,
    RESPONSES as DISAGREEMENT_RESPONSES, DEADLINE_RESPONSES, MANAGER_RESPONSES,
    MATERIAL_RESPONSES, PREFERENCE_RESPONSES, UNCERTAIN_RESPONSES,
)
from soft_skills_lab.scenarios.conflict import (
    CODE_REVIEW, CODE_RESPONSES, MANAGER_MATERIAL, MANAGER_MATERIAL_RESPONSES, MANAGER_TRADEOFF,
    MANAGER_TRADEOFF_RESPONSES, PUBLIC_CONFLICT, PUBLIC_RESPONSES, RELEASE_RESPONSES, RELEASE_VALIDATION,
)
from soft_skills_lab.scenarios.managers import MANAGER_SCENARIOS
from soft_skills_lab.scenarios.collaboration import COLLABORATION_SCENARIOS
from soft_skills_lab.scenarios.stakeholders import STAKEHOLDER_SCENARIOS
from soft_skills_lab.scenarios.requirements import REQUIREMENT_SCENARIOS
from soft_skills_lab.scenarios.incidents import SCENARIOS as INCIDENT_SCENARIOS
from soft_skills_lab.scenarios.personal_capacity import SCENARIOS as PERSONAL_CAPACITY_SCENARIOS
from soft_skills_lab.scenarios.performance import SCENARIOS as PERFORMANCE_SCENARIOS
from soft_skills_lab.scenarios.interviews import SCENARIOS as INTERVIEW_SCENARIOS
from soft_skills_lab.scenarios.meetings import SCENARIOS as MEETING_SCENARIOS
from soft_skills_lab.scenarios.writing import DEPLOYMENT_RISK, RESPONSES as WRITING_RESPONSES
from soft_skills_lab.scenarios.trust_history import SCENARIOS as TRUST_SCENARIOS
from soft_skills_lab.scenarios.leadership import SCENARIOS as LEADERSHIP_SCENARIOS
from soft_skills_lab.scenarios.judgment import SCENARIOS as JUDGMENT_SCENARIOS

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
    REPORT_EXPORT.scenario_id: (REPORT_EXPORT, REPORT_RESPONSES),
    DEPLOYMENT_FAILURE.scenario_id: (DEPLOYMENT_FAILURE, DEPLOYMENT_RESPONSES),
    AUTHORIZATION_INCIDENT.scenario_id: (AUTHORIZATION_INCIDENT, AUTHORIZATION_RESPONSES),
    PAYMENT_TIMEOUT.scenario_id: (PAYMENT_TIMEOUT, PAYMENT_RESPONSES),
    MIGRATION.scenario_id: (MIGRATION, MIGRATION_RESPONSES),
    INTEGRATION_DELIVERY.scenario_id: (INTEGRATION_DELIVERY, INTEGRATION_RESPONSES),
    CREDENTIAL_BLOCKER.scenario_id: (CREDENTIAL_BLOCKER, BLOCKER_RESPONSES),
    COMPLETION_UPDATE.scenario_id: (COMPLETION_UPDATE, COMPLETION_RESPONSES),
    PROFILE_FAILURE.scenario_id: (PROFILE_FAILURE, PROFILE_RESPONSES),
    ESTIMATE.scenario_id: (ESTIMATE, ESTIMATE_RESPONSES),
    JUDGMENT.scenario_id: (JUDGMENT, JUDGMENT_RESPONSES),
    MIGRATION_SAFETY.scenario_id: (MIGRATION_SAFETY, MIGRATION_SAFETY_RESPONSES),
    CUSTOMER_PAYMENT.scenario_id: (CUSTOMER_PAYMENT, CUSTOMER_PAYMENT_RESPONSES),
    PROJECT_VISIBILITY.scenario_id: (PROJECT_VISIBILITY, FEEDBACK_RESPONSES),
    VAGUE_MANAGER_FEEDBACK.scenario_id: (VAGUE_MANAGER_FEEDBACK, VAGUE_RESPONSES),
    ADAPTER_REVIEW.scenario_id: (ADAPTER_REVIEW, REVIEW_RESPONSES),
    FOLLOW_UP.scenario_id: (FOLLOW_UP, FOLLOW_UP_RESPONSES),
    SKIPPED_VALIDATION.scenario_id: (SKIPPED_VALIDATION, RESPONSIBILITY_RESPONSES),
    MISSED_HANDOFF.scenario_id: (MISSED_HANDOFF, MISSED_HANDOFF_RESPONSES),
    SHARED_RESPONSIBILITY.scenario_id: (SHARED_RESPONSIBILITY, SHARED_RESPONSES),
    UNAVOIDABLE_OUTCOME.scenario_id: (UNAVOIDABLE_OUTCOME, UNAVOIDABLE_RESPONSES),
    LEARNING_FOLLOW_UP.scenario_id: (LEARNING_FOLLOW_UP, LEARNING_RESPONSES),
    ADAPTER_BOUNDARY.scenario_id: (ADAPTER_BOUNDARY, DISAGREEMENT_RESPONSES),
    DEADLINE.scenario_id: (DEADLINE, DEADLINE_RESPONSES),
    PREFERENCE.scenario_id: (PREFERENCE, PREFERENCE_RESPONSES),
    MANAGER_CORRECT.scenario_id: (MANAGER_CORRECT, MANAGER_RESPONSES),
    UNCERTAIN.scenario_id: (UNCERTAIN, UNCERTAIN_RESPONSES),
    MATERIAL.scenario_id: (MATERIAL, MATERIAL_RESPONSES),
    RELEASE_VALIDATION.scenario_id: (RELEASE_VALIDATION, RELEASE_RESPONSES),
    CODE_REVIEW.scenario_id: (CODE_REVIEW, CODE_RESPONSES),
    MANAGER_TRADEOFF.scenario_id: (MANAGER_TRADEOFF, MANAGER_TRADEOFF_RESPONSES),
    MANAGER_MATERIAL.scenario_id: (MANAGER_MATERIAL, MANAGER_MATERIAL_RESPONSES),
    PUBLIC_CONFLICT.scenario_id: (PUBLIC_CONFLICT, PUBLIC_RESPONSES),
}
SCENARIOS.update(MANAGER_SCENARIOS)
SCENARIOS.update(COLLABORATION_SCENARIOS)
SCENARIOS.update(STAKEHOLDER_SCENARIOS)
SCENARIOS.update(REQUIREMENT_SCENARIOS)
SCENARIOS.update(INCIDENT_SCENARIOS)
SCENARIOS.update(PERSONAL_CAPACITY_SCENARIOS)
SCENARIOS.update(PERFORMANCE_SCENARIOS)
SCENARIOS.update(INTERVIEW_SCENARIOS)
SCENARIOS.update(MEETING_SCENARIOS)
SCENARIOS[DEPLOYMENT_RISK.scenario_id] = (DEPLOYMENT_RISK, WRITING_RESPONSES)
SCENARIOS.update(TRUST_SCENARIOS)
SCENARIOS.update(LEADERSHIP_SCENARIOS)
SCENARIOS.update(JUDGMENT_SCENARIOS)


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
