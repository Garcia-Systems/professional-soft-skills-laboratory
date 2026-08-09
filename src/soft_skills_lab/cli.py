"""Command-line interface for the executable textbook."""

import argparse
from collections.abc import Sequence

from soft_skills_lab.evaluation import evaluate_commitment_response, evaluate_incident_response, evidence_for_commitment
from soft_skills_lab.scenarios import get_response, get_scenario, list_responses
from soft_skills_lab.scenarios.commitment import COMMITMENT, PRIMARY_RESPONSE_IDS, TIMELINE
from soft_skills_lab.trust import DEMO_EVENTS, ProfessionalTrust


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
    commands.add_parser("trust-demo", help="show accumulated trust evidence")
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
    lines.append("\nReference responses:")
    lines.extend(f"- {response.response_id}: {response.label}" for response in list_responses(scenario_id))
    return "\n".join(lines)


def _evaluation_text(scenario_id: str, response_id: str) -> str:
    response = get_response(scenario_id, response_id)
    lines = [f"Response: {response.label}", response.message]
    evaluator = evaluate_commitment_response if scenario_id == "commitment-at-risk" else evaluate_incident_response
    for result in evaluator(response):
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


def _trust_text() -> str:
    trust = ProfessionalTrust()
    lines = ["Professional trust is accumulated evidence.", "", "Evidence history:"]
    for number, event in enumerate(DEMO_EVENTS, 1):
        trust = trust.record(event)
        lines.append(f"{number}. {event.kind.label} ({event.kind.weight:+d}): {event.detail}")
    lines.extend(("", f"Resulting evidence balance: {trust.balance}", "The history—not likability or personality—explains this state."))
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
        else:
            output = _trust_text()
    except KeyError as error:
        build_parser().error(error.args[0])
    print(output)
    return 0
