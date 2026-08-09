"""Command-line interface for the executable textbook."""

import argparse
from collections.abc import Sequence

from soft_skills_lab.evaluation import evaluate_commitment_response, evaluate_conflict_response, evaluate_disagreement_response, evaluate_explanation, evaluate_feedback_response, evaluate_incident_response, evaluate_listening_response, evaluate_manager_response, evaluate_question_response, evaluate_responsibility_response, evaluate_status_response, evaluate_uncertainty_response, evidence_for_commitment
from soft_skills_lab.scenarios import get_response, get_scenario, list_responses
from soft_skills_lab.scenarios.commitment import COMMITMENT, PRIMARY_RESPONSE_IDS, TIMELINE
from soft_skills_lab.scenarios.listening import PRIMARY_RESPONSE_IDS as LISTENING_RESPONSE_IDS
from soft_skills_lab.scenarios.questions import REPORT_ANSWERS, REPORT_EXPORT, REPORT_RESPONSES, apply_answers
from soft_skills_lab.scenarios.explanations import AUDIENCE_EXPLANATIONS, PAYMENT_RESPONSES
from soft_skills_lab.scenarios.status_updates import INTEGRATION_TIMELINE, PRIMARY_RESPONSE_IDS as STATUS_RESPONSE_IDS, STATUS_AUDIENCE_UPDATES
from soft_skills_lab.scenarios.uncertainty import PROFILE_RESPONSES
from soft_skills_lab.evaluation.uncertainty import CRITERIA as UNCERTAINTY_CRITERIA
from soft_skills_lab.trust import DEMO_EVENTS, DISAGREEMENT_EVENTS, ProfessionalTrust
from soft_skills_lab.scenarios.feedback import PRIMARY_RESPONSE_IDS as FEEDBACK_RESPONSE_IDS
from soft_skills_lab.trust import FEEDBACK_IMPROVEMENT_EVENTS
from soft_skills_lab.scenarios.responsibility import PRIMARY_RESPONSE_IDS as RESPONSIBILITY_RESPONSE_IDS
from soft_skills_lab.trust import RESPONSIBILITY_LEARNING_EVENTS
from soft_skills_lab.scenarios.managers import PROJECT_TIMELINE
from soft_skills_lab.trust import MANAGER_AUTONOMY_EVENTS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="soft-skills-lab")
    commands = parser.add_subparsers(dest="command", required=True)
    scenario = commands.add_parser("scenario", help="inspect a deterministic scenario")
    scenario.add_argument("scenario_id")
    evaluate = commands.add_parser("evaluate", help="evaluate a reference response")
    evaluate.add_argument("scenario_id")
    evaluate.add_argument("response_id")
    compare = commands.add_parser("compare", help="compare reference behaviors without a numeric ranking")
    compare.add_argument("scenario_id")
    interpret = commands.add_parser("interpret", help="inspect the deterministic communication gap")
    interpret.add_argument("scenario_id")
    unknowns = commands.add_parser("unknowns", help="inspect decision relevance and information sources")
    unknowns.add_argument("scenario_id")
    answer = commands.add_parser("answer", help="apply deterministic scenario answers")
    answer.add_argument("scenario_id")
    explain = commands.add_parser("explain", help="render a deterministic audience abstraction")
    explain.add_argument("scenario_id")
    explain.add_argument("--audience", required=True)
    layers = commands.add_parser("layers", help="inspect explicit information layers")
    layers.add_argument("scenario_id")
    status = commands.add_parser("status", help="inspect authored structured status metadata")
    status.add_argument("scenario_id")
    status.add_argument("response_id")
    status.add_argument("--audience", choices=("jordan", "morgan", "business"))
    evidence = commands.add_parser("evidence", help="inspect established facts, hypotheses, and open conclusions")
    evidence.add_argument("scenario_id")
    uncertainty = commands.add_parser("uncertainty", help="inspect authored current knowledge and next evidence")
    uncertainty.add_argument("scenario_id")
    feedback = commands.add_parser("feedback", help="inspect authored feedback layers and evidence")
    feedback.add_argument("scenario_id")
    improvement = commands.add_parser("improvement", help="inspect later observable feedback follow-through")
    improvement.add_argument("scenario_id")
    responsibility = commands.add_parser("responsibility", help="inspect evidence-based responsibility boundaries")
    responsibility.add_argument("scenario_id")
    learning = commands.add_parser("learning", help="inspect later observable responsibility follow-through")
    learning.add_argument("scenario_id")
    decision = commands.add_parser("decision", help="inspect decision ownership, alternatives, and evidence")
    decision.add_argument("scenario_id")
    conflict = commands.add_parser("conflict", help="inspect authored observable conflict state")
    conflict.add_argument("scenario_id")
    commands.add_parser("trust-demo", help="show accumulated trust evidence")
    commands.add_parser("disagreement-trust", help="show constructive disagreement trust evidence")
    agreement = commands.add_parser("manager-agreement", help="inspect explicit manager operating boundaries")
    agreement.add_argument("scenario_id")
    visibility = commands.add_parser("visibility", help="inspect contextual visibility thresholds")
    visibility.add_argument("scenario_id")
    commands.add_parser("manager-trust", help="show manager trust and autonomy evidence")
    return parser


def _scenario_text(scenario_id: str) -> str:
    scenario = get_scenario(scenario_id)
    lines = [f"Scenario: {scenario.title}", scenario.description, f"Risk: {scenario.current_risk.name}", "", "Known facts:"]
    lines.extend(f"- {fact}" for fact in scenario.known_facts)
    lines.append("\nUncertainties:")
    lines.extend(f"- {item}" for item in scenario.uncertainties)
    if scenario_id == "commitment-at-risk":
        lines.append("\nParticipants:")
        lines.extend(f"- {participant.name}: {participant.role}" for participant in scenario.participants)
        lines.extend(("\nCommitment:", f"- {COMMITMENT.description}; owner {COMMITMENT.owner}; expected Day {COMMITMENT.expected_completion}", "\nDependencies:"))
        lines.extend(f"- {item}" for item in COMMITMENT.dependencies)
        lines.append("\nTimeline:")
        lines.extend(f"- Day {event.point}: {event.description}" for event in TIMELINE)
    elif scenario_id == "integration-delivery":
        lines.append("\nTimeline:")
        lines.extend(f"- T{event.point}: {event.description}" for event in INTEGRATION_TIMELINE)
    elif scenario_id == "project-autonomy":
        lines.append("\nTimeline:")
        lines.extend(f"- T{event.point}: {event.description}" for event in PROJECT_TIMELINE)
    lines.append("\nReference responses:")
    lines.extend(f"- {response.response_id}: {response.label}" for response in list_responses(scenario_id))
    return "\n".join(lines)


def _evaluation_text(scenario_id: str, response_id: str) -> str:
    response = get_response(scenario_id, response_id)
    lines = [f"Response: {response.label}", response.message]
    scenario = get_scenario(scenario_id)
    if scenario.working_agreement is not None:
        results = evaluate_manager_response(scenario, response)
    elif scenario.conflict_state is not None:
        results = evaluate_conflict_response(scenario, response)
    elif scenario.decision_context is not None:
        results = evaluate_disagreement_response(scenario, response)
    elif scenario.responsibility_map is not None or scenario_id == "responsibility-follow-up":
        results = evaluate_responsibility_response(scenario, response)
    elif scenario.feedback is not None or scenario_id == "feedback-follow-up":
        results = evaluate_feedback_response(scenario, response)
    elif scenario.evidence_context is not None:
        results = evaluate_uncertainty_response(scenario, response)
    elif scenario_id in ("integration-delivery", "credential-blocker", "verification-completion"):
        results = evaluate_status_response(scenario, response)
    elif scenario.explanation_context is not None or scenario_id == "database-migration":
        results = evaluate_explanation(response)
    elif scenario.question_context:
        results = evaluate_question_response(scenario, response)
    elif scenario.communication_context:
        evaluator = evaluate_listening_response
        results = evaluator(response)
    else:
        evaluator = evaluate_commitment_response if scenario_id == "commitment-at-risk" else evaluate_incident_response
        results = evaluator(response)
    for result in results:
        lines.extend(("", f"Criterion: {result.criterion.criterion_id}", result.outcome.value, result.explanation))
        if result.evidence:
            lines.append("Evidence: " + " | ".join(result.evidence))
    if scenario_id == "commitment-at-risk":
        lines.append("\nProfessional evidence history:")
        events = evidence_for_commitment(response)
        lines.extend(f"- {event.kind.label} ({event.kind.weight:+d}): {event.detail}" for event in events)
        if not events:
            lines.append("- No positive observable evidence was recorded.")
        lines.append(f"Technical outcome: {'delivered by Day 2' if response.delivered_on_time else 'missed Day 2'} (not an evaluation criterion)")
    return "\n".join(lines)


def _comparison_text(scenario_id: str) -> str:
    if scenario_id == "project-autonomy":
        headings = ("AUTONOMY", "VISIBILITY", "THRESHOLDS", "RECOMMENDATION", "FOLLOW-UP")
        dimensions = {
            "permission-for-everything": ("FAIL", "PASS", "PARTIAL", "FAIL", "PARTIAL"),
            "silent-autonomy": ("PASS", "FAIL", "FAIL", "PARTIAL", "FAIL"),
            "status-flood": ("PARTIAL", "PARTIAL", "PARTIAL", "PARTIAL", "PASS"),
            "late-escalation": ("PASS", "FAIL", "FAIL", "PASS", "PARTIAL"),
            "escalate-without-investigation": ("FAIL", "PASS", "FAIL", "FAIL", "PASS"),
            "managed-autonomy": ("PASS", "PASS", "PASS", "PASS", "PASS"),
            "visibility-with-recommendation": ("PASS", "PASS", "PASS", "PASS", "PASS"),
        }
        lines = [f"{'PATH':34} " + " ".join(f"{item:14}" for item in headings)]
        for response_id, outcomes in dimensions.items():
            lines.append(f"{response_id:34} " + " ".join(f"{item:14}" for item in outcomes))
        lines.append("\nDimensions remain separate; there is no manager-relationship or obedience score.")
        return "\n".join(lines)
    if scenario_id == "release-validation":
        headings = ("NO ATTACK", "CURRENT ISSUE", "EVIDENCE", "DECISION PATH", "RISK PRESERVED")
        ids = ("avoids-counterattack", "refocuses-current-issue", "restores-shared-facts", "creates-decision-path", "preserves-material-risk")
        primary = ("counterattack", "motive-attack", "sarcasm", "capitulation", "repeat-louder", "de-escalate-and-refocus", "pause-and-resume")
        lines = [f"{'PATH':25} " + " ".join(f"{heading:14}" for heading in headings)]
        scenario = get_scenario(scenario_id)
        for response_id in primary:
            results = {item.criterion.criterion_id: item.outcome.value for item in evaluate_conflict_response(scenario, get_response(scenario_id, response_id))}
            lines.append(f"{response_id:25} " + " ".join(f"{results[item]:14}" for item in ids))
        lines.append("\nDimensions stay separate: this is not a conflict-skill, calmness, or personality score.")
        return "\n".join(lines)
    if scenario_id == "adapter-boundary":
        headings = ("UNDERSTANDS", "EVIDENCE", "NO-PERSONAL", "ALTERNATIVE", "DECISION")
        ids = ("captures-explicit-concern", "uses-decision-relevant-evidence", "avoids-personalization", "offers-constructive-alternative", "respects-decision-ownership")
        primary = ("passive-agreement", "flat-rejection", "authority-challenge", "defensive-ownership", "jargon-battle", "evidence-based-disagreement", "disagree-and-commit")
        lines = [f"{'PATH':31} " + " ".join(f"{item:13}" for item in headings)]
        scenario = get_scenario(scenario_id)
        for response_id in primary:
            results = {item.criterion.criterion_id: item.outcome.value for item in evaluate_disagreement_response(scenario, get_response(scenario_id, response_id))}
            lines.append(f"{response_id:31} " + " ".join(f"{results[item]:13}" for item in ids))
        lines.append("\nDimensions remain separate; this is not a collaboration, dominance, or personality score.")
        return "\n".join(lines)
    if scenario_id == "skipped-validation":
        headings = ("OWN PART", "NO BLAME", "CONTEXT", "IMPACT", "ACTION")
        ids = ("identifies-own-contribution", "does-not-shift-blame",
               "uses-context-without-erasing-responsibility", "acknowledges-impact",
               "identifies-corrective-action")
        lines = [f"{'PATH':31} " + " ".join(f"{item:11}" for item in headings)]
        scenario = get_scenario(scenario_id)
        for response_id in RESPONSIBILITY_RESPONSE_IDS:
            results = {item.criterion.criterion_id: item.outcome.value for item in
                       evaluate_responsibility_response(scenario, get_response(scenario_id, response_id))}
            lines.append(f"{response_id:31} " + " ".join(f"{results[item]:11}" for item in ids))
        lines.append("\nDimensions preserve responsibility boundaries; they are not an accountability percentage.")
        return "\n".join(lines)
    if scenario_id == "project-visibility":
        headings = ("UNDERSTANDS", "OWNERSHIP", "EVIDENCE", "NO-BLAME", "ACTION")
        ids = ("acknowledges-feedback", "separates-context-from-excuse", "acknowledges-supported-evidence", "avoids-blame", "identifies-behavior-change")
        lines = [f"{'PATH':23} " + " ".join(f"{item:12}" for item in headings)]
        scenario = get_scenario(scenario_id)
        for response_id in FEEDBACK_RESPONSE_IDS:
            results = {item.criterion.criterion_id: item.outcome.value for item in evaluate_feedback_response(scenario, get_response(scenario_id, response_id))}
            lines.append(f"{response_id:23} " + " ".join(f"{results[item]:12}" for item in ids))
        lines.append("\nDimensions describe observable reception; they are not a personality or professionalism score.")
        return "\n".join(lines)
    if scenario_id == "profile-update-failure":
        headings = ("EXPLICIT", "EVIDENCE", "HYPOTHESIS", "BASIS", "MISSING", "ACTION", "FOLLOW-UP", "IMPACT")
        ids = tuple(item.criterion_id for item in UNCERTAINTY_CRITERIA[:8])
        primary_ids = ("bluff", "defensive-certainty", "empty-unknown", "speculative-answer", "investigation-dump", "bounded-uncertainty")
        lines = [f"{'PATH':23} " + " ".join(f"{item:10}" for item in headings)]
        scenario = get_scenario(scenario_id)
        for response_id in primary_ids:
            results = {item.criterion.criterion_id: item.outcome.value for item in evaluate_uncertainty_response(scenario, PROFILE_RESPONSES[response_id])}
            lines.append(f"{response_id:23} " + " ".join(f"{results[item]:10}" for item in ids))
        lines.append("\nTruthful uncertainty is stronger than bluffing; bounded uncertainty also carries a next action.")
        return "\n".join(lines)
    if scenario_id == "integration-delivery":
        headings = ("STATE", "PROGRESS", "RISK", "DEPENDENCY", "BLOCKER", "FORECAST", "FOLLOW-UP", "DETAIL")
        ids = ("states-current-state", "communicates-material-progress", "communicates-risk", "communicates-dependency-impact",
               "labels-blocker-correctly", "provides-forecast-basis", "establishes-next-update", "avoids-unnecessary-detail")
        lines = [f"{'PATH':20} " + " ".join(f"{item:11}" for item in headings)]
        scenario = get_scenario(scenario_id)
        for response_id in STATUS_RESPONSE_IDS:
            results = {item.criterion.criterion_id: item.outcome.value for item in evaluate_status_response(scenario, get_response(scenario_id, response_id))}
            lines.append(f"{response_id:20} " + " ".join(f"{results[item]:11}" for item in ids))
        lines.append("\nUseful status exposes state and decisions; this is not a diary-detail score.")
        return "\n".join(lines)
    if scenario_id == "payment-timeout":
        headings = ("TRUTH", "IMPACT", "UNCERTAINTY", "AUDIENCE", "DECISION")
        ids = ("preserves-technical-truth", "communicates-impact", "preserves-uncertainty", "matches-audience-need", "supports-decision")
        lines = [f"{'PATH':31} " + " ".join(f"{item:12}" for item in headings)]
        for response_id, response in PAYMENT_RESPONSES.items():
            results = {item.criterion.criterion_id: item.outcome.value for item in evaluate_explanation(response)}
            lines.append(f"{response_id:31} " + " ".join(f"{results[item]:12}" for item in ids))
        lines.append("\nDimensions remain separate; this is not a communication score or leaderboard.")
        return "\n".join(lines)
    if scenario_id == "report-export":
        headings = ("RELEVANT", "CONTEXT", "INVESTIGATED", "ANSWERABLE", "NO ASSUMPTION", "NO DUMP")
        criterion_ids = ("targets-relevant-unknown", "provides-context", "shows-prior-investigation", "is-answerable",
                         "avoids-assumption-disguised-as-question", "avoids-question-dump")
        lines = [f"{'PATH':22} " + " ".join(f"{heading:13}" for heading in headings)]
        for response_id in REPORT_RESPONSES:
            results = {item.criterion.criterion_id: item.outcome.value for item in
                       evaluate_question_response(REPORT_EXPORT, REPORT_RESPONSES[response_id])}
            lines.append(f"{response_id:22} " + " ".join(f"{results[item]:13}" for item in criterion_ids))
        lines.append("\nMore questions are not automatically better; outcomes are observable criteria, not a score.")
        return "\n".join(lines)
    if scenario_id == "demo-stability":
        headings = ("CONCERN", "ASSUMPTIONS", "UNKNOWN", "NEXT ACTION", "FOLLOW-UP")
        criterion_ids = ("captures-explicit-concern", "avoids-unsupported-assumption", "identifies-unknowns", "establishes-next-action", "establishes-follow-up")
        lines = [f"{'PATH':25} " + " ".join(f"{heading:12}" for heading in headings)]
        for response_id in LISTENING_RESPONSE_IDS:
            results = {item.criterion.criterion_id: item.outcome.value for item in evaluate_listening_response(get_response(scenario_id, response_id))}
            lines.append(f"{response_id:25} " + " ".join(f"{results[item]:12}" for item in criterion_ids))
        lines.append("\nOutcomes are shown criterion by criterion; this is not a listening or personality score.")
        return "\n".join(lines)
    if scenario_id != "commitment-at-risk":
        raise KeyError(f"comparison unavailable for scenario: {scenario_id}")
    headings = ("EARLY RISK", "DEPENDENCY", "UNCERTAINTY", "FOLLOW-UP")
    criterion_ids = ("communicates-risk-early", "acknowledges-dependency", "distinguishes-known-from-unknown", "establishes-follow-up")
    lines = [f"{'PATH':21} " + " ".join(f"{heading:12}" for heading in headings)]
    for response_id in PRIMARY_RESPONSE_IDS:
        results = {item.criterion.criterion_id: item.outcome.value for item in evaluate_commitment_response(get_response(scenario_id, response_id))}
        lines.append(f"{response_id:21} " + " ".join(f"{results[item]:12}" for item in criterion_ids))
    lines.append("\nOutcomes are shown criterion by criterion; this is not a professionalism score.")
    return "\n".join(lines)


def _interpretation_text(scenario_id: str) -> str:
    context = get_scenario(scenario_id).communication_context
    if context is None:
        raise KeyError(f"interpretation unavailable for scenario: {scenario_id}")
    lines = ["EXPLICITLY COMMUNICATED", ""]
    lines.extend(f"- {item}" for item in context.explicit_facts)
    lines.extend(("", "POSSIBLE INTERPRETATIONS", ""))
    lines.extend(f"- {item}" for item in context.possible_interpretations)
    lines.extend(("", "NOT YET KNOWN", ""))
    lines.extend(f"- {item}" for item in context.unknowns)
    lines.extend(("", "UNSUPPORTED ASSUMPTIONS", ""))
    lines.extend(f"- {item}" for item in context.unsupported_assumptions)
    return "\n".join(lines)


def _unknowns_text(scenario_id: str) -> str:
    context = get_scenario(scenario_id).question_context
    if context is None:
        raise KeyError(f"unknown inspection unavailable for scenario: {scenario_id}")
    lines = [f"Decision: {context.decision}", "", f"{'UNKNOWN':34} {'DECISION RELEVANCE':20} SOURCE"]
    for item in context.unknowns:
        lines.append(f"{item.description:34} {item.relevance.name:20} {item.source.value}")
        lines.append(f"  Why: {item.consequence}")
    return "\n".join(lines)


def _answer_text(scenario_id: str) -> str:
    if scenario_id != "report-export":
        raise KeyError(f"deterministic answers unavailable for scenario: {scenario_id}")
    updated = apply_answers(REPORT_EXPORT)
    lines = ["Deterministic lifecycle: unknown -> question -> answer -> known fact -> decision", "", "Priya's answers:"]
    lines.extend(f"- {key}: {value}" for key, value in REPORT_ANSWERS.items())
    lines.extend(("", "Updated known facts:"))
    lines.extend(f"- {fact}" for fact in updated.known_facts[-len(REPORT_ANSWERS):])
    lines.append(f"\nRemaining unknowns: {len(updated.uncertainties)}")
    lines.append("Decision: implementation can begin using the confirmed export contract.")
    return "\n".join(lines)


def _trust_text() -> str:
    trust = ProfessionalTrust()
    lines = ["Professional trust is accumulated evidence.", "", "Evidence history:"]
    for number, event in enumerate(DEMO_EVENTS, 1):
        trust = trust.record(event)
        lines.append(f"{number}. {event.kind.label} ({event.kind.weight:+d}): {event.detail}")
    lines.extend(("", f"Resulting evidence balance: {trust.balance}", "The history—not likability or personality—explains this state."))
    return "\n".join(lines)


def _disagreement_trust_text() -> str:
    trust = ProfessionalTrust()
    lines = ["CONSTRUCTIVE DISAGREEMENT TRUST EVIDENCE"]
    for event in DISAGREEMENT_EVENTS:
        trust = trust.record(event)
        lines.append(f"- {event.kind.label} ({event.kind.weight:+d}): {event.detail}")
    lines.extend(("", f"Evidence balance: {trust.balance}", "The inspectable history—not agreement or likability—supports trust."))
    return "\n".join(lines)


def _explain_text(scenario_id: str, audience_id: str) -> str:
    if scenario_id != "payment-timeout":
        raise KeyError(f"audience explanation unavailable for scenario: {scenario_id}")
    scenario = get_scenario(scenario_id)
    audiences = {item.audience_id: item for item in scenario.explanation_context.audiences}
    if audience_id not in audiences:
        raise KeyError(f"unknown audience for {scenario_id}: {audience_id}")
    audience, explanation = audiences[audience_id], AUDIENCE_EXPLANATIONS[audience_id]
    return "\n".join((f"Audience: {audience.role}", f"Decision responsibility: {audience.decision_responsibility}",
                      "Information needs: " + ", ".join(audience.information_needs), "", explanation.message,
                      "", "Underlying fact IDs: " + ", ".join(explanation.communicated_fact_ids)))


def _layers_text(scenario_id: str) -> str:
    context = get_scenario(scenario_id).explanation_context
    if context is None:
        raise KeyError(f"information layers unavailable for scenario: {scenario_id}")
    lines: list[str] = []
    for heading, items in context.information_layers:
        lines.extend((heading, ""))
        lines.extend(f"- {item}" for item in items)
        lines.append("")
    return "\n".join(lines).rstrip()


def _status_text(scenario_id: str, response_id: str, audience_id: str | None = None) -> str:
    response = STATUS_AUDIENCE_UPDATES[audience_id] if audience_id and scenario_id == "integration-delivery" else get_response(scenario_id, response_id)
    update = response.status_update
    if update is None:
        raise KeyError(f"structured status unavailable for {scenario_id}: {response_id}")
    lines = ["SUBJECT", update.subject, "", "CURRENT STATE", update.current_state.value.replace("_", " ").title() if update.current_state else "Not stated"]
    sections = (("COMPLETED", update.completed_work), ("REMAINING", update.remaining_work), ("BLOCKERS", update.blockers),
                ("RISK", update.risks), ("UNCERTAINTIES", update.uncertainties), ("DEPENDENCY IMPACT", update.dependency_impact))
    for heading, items in sections:
        if items:
            lines.extend(("", heading, *(f"- {item}" for item in items)))
    singles = (("NEXT ACTION", update.next_action), ("NEEDED ACTION", update.requested_action),
               ("DEPENDENCY OWNER", update.dependency_owner), ("DECISION POINT", update.decision_point))
    for heading, value in singles:
        if value:
            lines.extend(("", heading, value))
    if update.forecast:
        qualifier = f" if {update.forecast.condition}" if update.forecast.condition else ""
        lines.extend(("", "FORECAST", f"{update.forecast.target}{qualifier}", f"Basis: {update.forecast.basis}",
                      "Type: guarantee" if update.forecast.guaranteed else "Type: evidence-based estimate"))
    if update.next_update_point is not None:
        lines.extend(("", "NEXT UPDATE", f"T{update.next_update_point}"))
    if audience_id:
        lines.extend(("", "AUDIENCE VIEW", audience_id, "Underlying fact IDs: " + ", ".join(response.communicated_fact_ids)))
    return "\n".join(lines)


def _evidence_text(scenario_id: str) -> str:
    context = get_scenario(scenario_id).evidence_context
    if context is None:
        raise KeyError(f"evidence inspection unavailable for scenario: {scenario_id}")
    lines = ["ESTABLISHED FACTS", "", *(f"- {item}" for item in context.established_facts),
             "", "CURRENT HYPOTHESES", ""]
    lines.extend(f"- {item.statement}" for item in context.hypotheses)
    lines.extend(("", "NOT YET ESTABLISHED", ""))
    lines.extend(f"- {item}" for item in context.not_yet_established)
    return "\n".join(lines)


def _uncertainty_text(scenario_id: str) -> str:
    context = get_scenario(scenario_id).evidence_context
    uncertainty = context.uncertainty if context else None
    if uncertainty is None:
        raise KeyError(f"uncertainty inspection unavailable for scenario: {scenario_id}")
    answer = uncertainty.kind.value.replace("-", " ").title()
    lines = ["QUESTION", uncertainty.subject, "", "CURRENT ANSWER", answer,
             "", "WHAT IS KNOWN", *(f"- {item}" for item in uncertainty.current_evidence),
             "", "WHY ANSWER IS UNKNOWN", *(f"- {item}" for item in uncertainty.missing_evidence),
             "", "NEXT EVIDENCE", *(f"- {item}" for item in uncertainty.next_investigation_steps)]
    if uncertainty.expected_update_point is not None:
        lines.extend(("", "NEXT UPDATE", f"T{uncertainty.expected_update_point}"))
    return "\n".join(lines)


def _feedback_text(scenario_id: str) -> str:
    feedback = get_scenario(scenario_id).feedback
    if feedback is None:
        raise KeyError(f"feedback inspection unavailable for scenario: {scenario_id}")
    lines = ["FEEDBACK", "", "Claim:", feedback.claim, "", "OBSERVED EVIDENCE"]
    lines.extend(f"- {item}" for item in feedback.observed_behavior)
    for heading, items in (("INTERPRETATION", feedback.interpretation), ("EXPECTATION", feedback.expected_behavior),
                           ("REQUESTED CHANGE", feedback.requested_change), ("IMPORTANT CONTEXT", feedback.important_context),
                           ("NOT IMPLIED", feedback.not_implied)):
        lines.extend(("", heading))
        lines.extend(f"- {item}" for item in items)
    lines.extend(("", "EVIDENCE STATUS"))
    lines.extend(f"- {item.strength.name}: {item.statement}" for item in feedback.evidence)
    return "\n".join(lines)


def _improvement_text(scenario_id: str) -> str:
    if scenario_id != "feedback-follow-up":
        raise KeyError(f"improvement history unavailable for scenario: {scenario_id}")
    trust = ProfessionalTrust()
    lines = ["FEEDBACK FOLLOW-UP", "", "Observable evidence:"]
    for event in FEEDBACK_IMPROVEMENT_EVENTS:
        trust = trust.record(event)
        lines.append(f"- {event.kind.label}: {event.detail}")
    lines.extend(("", "Verbal agreement alone is not demonstrated improvement.",
                  "The later risk update and completed follow-up are evidence of changed behavior."))
    return "\n".join(lines)


def _responsibility_text(scenario_id: str) -> str:
    responsibility = get_scenario(scenario_id).responsibility_map
    if responsibility is None:
        raise KeyError(f"responsibility inspection unavailable for scenario: {scenario_id}")
    lines = ["INCIDENT", responsibility.incident]
    for boundary in responsibility.boundaries:
        lines.extend(("", f"{boundary.actor.upper()}'S CONTRIBUTION"))
        lines.extend(f"- {item}" for item in boundary.contribution)
        if boundary.controlled:
            lines.append("Controlled:")
            lines.extend(f"- {item}" for item in boundary.controlled)
        if boundary.did_not_control:
            lines.append("Did not control:")
            lines.extend(f"- {item}" for item in boundary.did_not_control)
    for heading, items in (("EVIDENCE", responsibility.evidence), ("CONTEXT", responsibility.process_conditions),
                           ("EXTERNAL FACTORS", responsibility.external_factors), ("INCIDENT RESULT", responsibility.results),
                           ("NOT SUPPORTED", responsibility.not_supported),
                           ("IMMEDIATE RESPONSIBILITY", responsibility.immediate_responsibility),
                           ("PREVENTIVE ACTION", responsibility.preventive_action)):
        if items:
            lines.extend(("", heading, *(f"- {item}" for item in items)))
    lines.extend(("", "This educational decomposition is not legal-liability analysis."))
    return "\n".join(lines)


def _learning_text(scenario_id: str) -> str:
    if scenario_id != "responsibility-follow-up":
        raise KeyError(f"responsibility learning unavailable for scenario: {scenario_id}")
    trust = ProfessionalTrust()
    lines = ["RESPONSIBILITY FOLLOW-UP", "", "Observable trust evidence:"]
    for event in RESPONSIBILITY_LEARNING_EVENTS:
        trust = trust.record(event)
        lines.append(f"- {event.kind.label}: {event.detail}")
    lines.extend(("", "Verbal ownership alone is not demonstrated learning.",
                  "Accountability becomes credible when corrective behavior is visible later."))
    return "\n".join(lines)


def _decision_text(scenario_id: str) -> str:
    context = get_scenario(scenario_id).decision_context
    if context is None:
        raise KeyError(f"decision inspection unavailable for scenario: {scenario_id}")
    lines = ["DECISION", context.decision, "", "SHARED OBJECTIVE", context.shared_objective,
             "", "DECISION OWNER", context.owner, "", "CONTRIBUTORS", *(f"- {item}" for item in context.contributors)]
    for alternative in context.alternatives:
        lines.extend(("", f"EVIDENCE FOR {alternative.name.upper()}"))
        lines.extend(f"- {item}" for item in alternative.evidence)
        if not alternative.evidence:
            lines.append("- No differentiating evidence established.")
    if context.constraints:
        lines.extend(("", "CONSTRAINTS", *(f"- {item}" for item in context.constraints)))
    if context.unresolved_risks:
        lines.extend(("", "UNRESOLVED TRADEOFF", *(f"- {item}" for item in context.unresolved_risks)))
    if context.final_choice:
        lines.extend(("", "FINAL CHOICE", context.final_choice))
    if context.rationale:
        lines.extend(("", "RATIONALE", context.rationale))
    lines.extend(("", "ISSUE KIND", context.issue_kind.value, "REVERSIBLE", "yes" if context.reversible else "no"))
    return "\n".join(lines)


def _conflict_text(scenario_id: str) -> str:
    state = get_scenario(scenario_id).conflict_state
    if state is None:
        raise KeyError(f"conflict inspection unavailable for scenario: {scenario_id}")
    lines = ["CONFLICT STAGE", state.stage.value, "", "CURRENT DECISION", state.current_issue,
             "", "SHARED FACTS", *(f"- {fact}" for fact in state.shared_facts), "", "CURRENT DISAGREEMENT"]
    for speaker, position in state.positions:
        lines.extend((f"{speaker}:", position))
    lines.extend(("", "CONFLICT-ADDING STATEMENTS"))
    lines.extend(f'- "{signal.statement}"' for signal in state.signals)
    if state.expanded_issue:
        lines.extend(("", "EXPANDED ISSUE", state.expanded_issue))
    lines.extend(("", "NOT ESTABLISHED", *(f"- {item}" for item in state.not_established), "",
                  "UNRESOLVED DECISION", "yes" if state.unresolved_decision else "no"))
    return "\n".join(lines)


def _manager_agreement_text(scenario_id: str) -> str:
    agreement = get_scenario(scenario_id).working_agreement
    if agreement is None:
        raise KeyError(f"working agreement unavailable for scenario: {scenario_id}")
    lines = ["WORKING AGREEMENT", "", "EMPLOYEE", agreement.employee, "", "MANAGER", agreement.manager,
             "", f"{agreement.employee.upper()} OWNS INDEPENDENTLY"]
    lines.extend(f"- {item}" for item in agreement.responsibilities)
    for threshold, heading in (("INFORM", f"INFORM {agreement.manager.upper()}"), ("CONSULT", "CONSULT BEFORE ACTION"), ("ESCALATE", "ESCALATE")):
        lines.extend(("", heading))
        lines.extend(f"- {item.subject}." for item in agreement.expectations if item.threshold.value == threshold)
    lines.extend(("", "NORMAL EXPECTATION", agreement.normal_update_cadence))
    return "\n".join(lines)


def _visibility_text(scenario_id: str) -> str:
    agreement = get_scenario(scenario_id).working_agreement
    if agreement is None:
        raise KeyError(f"visibility thresholds unavailable for scenario: {scenario_id}")
    lines = ["VISIBILITY THRESHOLDS", "", "These thresholds come from this working agreement; they are not universal."]
    for item in agreement.expectations:
        point = f"T{item.point} " if item.point is not None else ""
        lines.extend(("", f"{point}{item.subject}", f"Threshold: {item.threshold.value}", f"Expected behavior: {item.expected_behavior}"))
    return "\n".join(lines)


def _manager_trust_text() -> str:
    trust = ProfessionalTrust()
    lines = ["MANAGER TRUST AND AUTONOMY EVIDENCE"]
    for event in MANAGER_AUTONOMY_EVENTS:
        trust = trust.record(event)
        lines.append(f"- {event.kind.label} ({event.kind.weight:+d}): {event.detail}")
    lines.extend(("", f"Evidence balance: {trust.balance}", "Repeated visible behavior—not obedience or personality—supports adjusted autonomy."))
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "scenario":
            output = _scenario_text(args.scenario_id)
        elif args.command == "evaluate":
            output = _evaluation_text(args.scenario_id, args.response_id)
        elif args.command == "compare":
            output = _comparison_text(args.scenario_id)
        elif args.command == "interpret":
            output = _interpretation_text(args.scenario_id)
        elif args.command == "unknowns":
            output = _unknowns_text(args.scenario_id)
        elif args.command == "answer":
            output = _answer_text(args.scenario_id)
        elif args.command == "explain":
            output = _explain_text(args.scenario_id, args.audience)
        elif args.command == "layers":
            output = _layers_text(args.scenario_id)
        elif args.command == "status":
            output = _status_text(args.scenario_id, args.response_id, args.audience)
        elif args.command == "evidence":
            output = _evidence_text(args.scenario_id)
        elif args.command == "uncertainty":
            output = _uncertainty_text(args.scenario_id)
        elif args.command == "feedback":
            output = _feedback_text(args.scenario_id)
        elif args.command == "improvement":
            output = _improvement_text(args.scenario_id)
        elif args.command == "responsibility":
            output = _responsibility_text(args.scenario_id)
        elif args.command == "learning":
            output = _learning_text(args.scenario_id)
        elif args.command == "decision":
            output = _decision_text(args.scenario_id)
        elif args.command == "conflict":
            output = _conflict_text(args.scenario_id)
        elif args.command == "manager-agreement":
            output = _manager_agreement_text(args.scenario_id)
        elif args.command == "visibility":
            output = _visibility_text(args.scenario_id)
        elif args.command == "manager-trust":
            output = _manager_trust_text()
        elif args.command == "disagreement-trust":
            output = _disagreement_trust_text()
        else:
            output = _trust_text()
    except KeyError as error:
        build_parser().error(error.args[0])
    print(output)
    return 0
