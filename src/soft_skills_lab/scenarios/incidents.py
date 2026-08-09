"""Chapter 15 incident scenarios authored on the shared behavior model."""

from soft_skills_lab.domain.models import (
    EvidenceContext, Hypothesis, Incident, IncidentReview, IncidentState, Participant,
    ProfessionalResponse, RecoveryCheck, RiskLevel, WorkplaceScenario,
)

PARTICIPANTS = (Participant("Alex", "developer"), Participant("Jordan", "teammate"),
                Participant("Morgan", "engineering manager"),
                Participant("Dana", "business operations director"))

FACTS = ("Normal failure rate is below 1%; current failure rate is approximately 18%.",
         "Successful authorization requests still exist.",
         "Failure increase began shortly after the T0 deployment.",
         "Failures contain downstream HTTP 400 responses.", "Database writes remain normal.",
         "No evidence currently indicates lost payments.",
         "The provider status page reports no broad outage.",
         "The release added a new optional request header.")
IMPACT = ("Approximately 18% of payment attempts are failing.",
          "Some members receive payment errors.", "Successful requests still exist.",
          "No evidence currently indicates lost payments.")
UNKNOWN = ("Full root cause.", "Whether any other release changes contribute.",
           "Whether affected members retried successfully.")

REVIEW = IncidentReview(
    ("T0 release deployed.", "T1 failures rose.", "T2 support confirmed member errors.",
     "T3 controlled test succeeded without the header.", "T4 header removed and recovery verified."),
    IMPACT, ("Optional header was incompatible with provider validation.",
             "Required provider compatibility test was skipped."),
    ("Alex added the header and skipped the required compatibility test.",
     "Incident coordination ownership did not imply Morgan caused the failure."),
    ("Failure-rate monitoring detected the change.",),
    ("The new header was disabled through coordinated configuration change.",),
    ("The incompatible header was removed.",),
    ("Add a provider-header compatibility test to the deployment gate.",
     "Document the reversible header-disable rollback step."),
)

PAYMENT_INCIDENT = Incident(
    "payment-authorization", "Payment authorization failures", "T1", IncidentState.ACTIVE,
    "Morgan", "Alex", "Dana", "Payment authorization", ("Authorization failures increased.",
    "Downstream responses include HTTP 400."), IMPACT, FACTS,
    ("The new request header may be rejected by the provider.",), UNKNOWN,
    ("Disable the new request header or roll back.",),
    ("Remove the incompatible header after confirmation.",),
    (RecoveryCheck("Failure rate returned below 1%.", False),
     RecoveryCheck("Controlled and member workflows succeed.", False),
     RecoveryCheck("No unresolved uncertain transactions remain.", False),
     RecoveryCheck("Support reports stop increasing.", False)),
    ("Engineering", "Business operations", "Customer support"), "T3", REVIEW)

AUDIENCES = (
    ("engineering", ("18% failures with downstream HTTP 400", "database writes normal",
                     "header is a hypothesis", "disable header or roll back", "Alex owns investigation")),
    ("manager", ("member impact", "ACTIVE state", "no evidence of lost payments",
                 "Morgan coordinates; Alex investigates", "containment decision", "next update T3")),
    ("business", ("some payment attempts fail", "do not continue normal retry guidance",
                  "recovery time is not yet established", "next update T3")),
    ("customer-support", ("Some payment attempts are currently failing.",
                          "Members receiving an error should not repeatedly retry until processing status is confirmed.",
                          "Do not claim all payments are broken or name an unconfirmed cause.", "Next update T3.")),
)

PAYMENT = WorkplaceScenario("payment-authorization", PAYMENT_INCIDENT.title,
    "Harbor submits payment authorizations to an external provider; a release precedes elevated failures.",
    PARTICIPANTS, FACTS + ("At T2 support reports members receiving payment errors.",), UNKNOWN, (),
    RiskLevel.HIGH, evidence_context=EvidenceContext(FACTS,
        (Hypothesis("header-rejection", "The new request header may be rejected by the provider.",
                    ("Timing correlation", "Controlled test succeeds without header")),), UNKNOWN),
    incident=PAYMENT_INCIDENT, incident_audiences=AUDIENCES)

def response(response_id: str, label: str, message: str, **values) -> ProfessionalResponse:
    return ProfessionalResponse(response_id, label, message, **values)

RESPONSES = {
 "hide-and-fix": response("hide-and-fix", "Private debugging", "I think I can fix it quickly.",
     preserves_uncertainty=True, prioritizes_containment=True),
 "blame-first": response("blame-first", "Unsupported vendor blame", "The provider broke something.",
     makes_incident_visible=True, assigns_unsupported_blame=True, claims_cause_without_evidence=True),
 "self-blame-first": response("self-blame-first", "Premature self-blame", "This is my fault. I broke production.",
     makes_incident_visible=True, over_owns=True, self_condemnation=True),
 "investigation-dump": response("investigation-dump", "Technical dump without incident state",
     "Logs, headers, stack traces, request IDs, and code diff follow.", preserves_uncertainty=True,
     implementation_details=("logs", "headers", "stack traces", "request IDs", "diff"), prioritizes_containment=True),
 "premature-root-cause": response("premature-root-cause", "Premature root cause",
     "The new header caused the incident.", makes_incident_visible=True, states_observed_impact=True,
     claims_cause_without_evidence=True, prioritizes_containment=True, coordinates_affected_parties=True),
 "silent-rollback": response("silent-rollback", "Silent rollback", "I rolled back without notifying responders.",
     prioritizes_containment=True, identifies_corrective_action=True),
 "coordinated-incident-response": response("coordinated-incident-response", "Coordinated incident response",
     "Payment failures are about 18% and some members see errors. They rose after deployment; causation is not established. The new header is a lead, database writes are normal, and there is no evidence of lost payments. Recommend disabling the header or rolling back. Morgan coordinates, I own investigation, and I will update at T3.",
     makes_incident_visible=True, states_observed_impact=True, separates_cause_from_hypothesis=True,
     prioritizes_containment=True, establishes_incident_ownership=True, coordinates_affected_parties=True,
     states_uncertainty_explicitly=True, material_risk_communicated=True, follow_up_point=3,
     defers_blame_until_evidence=True, supports_decision=True),
 "containment-then-learning": response("containment-then-learning", "Contain, verify, and learn",
     "Coordinate header removal, verify rates and workflows, update affected teams, then document the supported contribution and add the provider compatibility gate.",
     makes_incident_visible=True, states_observed_impact=True, separates_cause_from_hypothesis=True,
     prioritizes_containment=True, establishes_incident_ownership=True, coordinates_affected_parties=True,
     verifies_recovery=True, closes_incident_loop=True, defers_blame_until_evidence=True,
     creates_prevention_from_evidence=True, identifies_own_contribution=True,
     identifies_corrective_action=True, identifies_preventive_action=True, preserves_uncertainty=True),
 "equivalent-coordinated": response("equivalent-coordinated", "Equivalent coordinated response",
     "Members are seeing an elevated but partial authorization failure. The release timing is a fact, not proof. Morgan will coordinate while I test the header and recommend reversible disablement; operations and support get T3 updates.",
     makes_incident_visible=True, states_observed_impact=True, separates_cause_from_hypothesis=True,
     prioritizes_containment=True, establishes_incident_ownership=True, coordinates_affected_parties=True,
     states_uncertainty_explicitly=True, defers_blame_until_evidence=True, follow_up_point=3,
     supports_decision=True),
}

DATA_EXPOSURE_INCIDENT = Incident("data-exposure-risk", "Possible internal metadata exposure", "T1",
    IncidentState.ACTIVE, "Morgan", "Alex", None, "Member export", ("A fixture response contains an internal risk field.",),
    ("Member-visible internal metadata is possible; production exposure is not confirmed.",),
    ("Endpoint is live.", "One fixture exposes an internal risk field."),
    ("The new projection may include the field in production.",), ("Whether production members received it.",),
    ("Immediately disable or restrict the endpoint and preserve evidence.",), ("Correct the response projection.",),
    (RecoveryCheck("Production responses exclude internal metadata."),), ("Security", "Engineering manager"), "T2")
DATA_EXPOSURE = WorkplaceScenario("data-exposure-risk", DATA_EXPOSURE_INCIDENT.title,
    "A live endpoint may expose internal metadata; high risk justifies containment before full diagnosis.", PARTICIPANTS,
    DATA_EXPOSURE_INCIDENT.established_facts, DATA_EXPOSURE_INCIDENT.unknowns, (), RiskLevel.CRITICAL,
    incident=DATA_EXPOSURE_INCIDENT)

FALSE_ALARM_INCIDENT = Incident("payment-alert-false-alarm", "Duplicated failure alert", "T1",
    IncidentState.RESOLVED, "Morgan", "Alex", None, "Payment authorization",
    ("Exporter reported duplicated failure events.",), ("No customer impact was found.",),
    ("Customer requests succeed normally.", "Metrics exporter duplicated events."), (), (),
    ("Investigate before broad corrective action.",), ("Correct metrics exporter."),
    (RecoveryCheck("Customer requests are succeeding normally.", True),), ("Engineering",), None)
FALSE_ALARM = WorkplaceScenario("payment-alert-false-alarm", FALSE_ALARM_INCIDENT.title,
    "An announced alert is corrected and closed when evidence shows no customer impact.", PARTICIPANTS,
    FALSE_ALARM_INCIDENT.established_facts, (), (), RiskLevel.LOW, incident=FALSE_ALARM_INCIDENT)

SCENARIOS = {PAYMENT.scenario_id: (PAYMENT, RESPONSES),
             DATA_EXPOSURE.scenario_id: (DATA_EXPOSURE, {}),
             FALSE_ALARM.scenario_id: (FALSE_ALARM, {})}
