"""Command-line interface for the executable textbook."""

import argparse
from collections.abc import Sequence

from soft_skills_lab.evaluation import evaluate_incident_response
from soft_skills_lab.scenarios import get_response, get_scenario, list_responses
from soft_skills_lab.trust import DEMO_EVENTS, ProfessionalTrust


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="soft-skills-lab")
    commands = parser.add_subparsers(dest="command", required=True)
    scenario = commands.add_parser("scenario", help="inspect a deterministic scenario")
    scenario.add_argument("scenario_id")
    evaluate = commands.add_parser("evaluate", help="evaluate a reference response")
    evaluate.add_argument("scenario_id")
    evaluate.add_argument("response_id")
    commands.add_parser("trust-demo", help="show accumulated trust evidence")
    return parser


def _scenario_text(scenario_id: str) -> str:
    scenario = get_scenario(scenario_id)
    lines = [f"Scenario: {scenario.title}", scenario.description, f"Risk: {scenario.current_risk.name}", "", "Known facts:"]
    lines.extend(f"- {fact}" for fact in scenario.known_facts)
    lines.append("\nUncertainties:")
    lines.extend(f"- {item}" for item in scenario.uncertainties)
    lines.append("\nReference responses:")
    lines.extend(f"- {response.response_id}: {response.label}" for response in list_responses(scenario_id))
    return "\n".join(lines)


def _evaluation_text(scenario_id: str, response_id: str) -> str:
    response = get_response(scenario_id, response_id)
    lines = [f"Response: {response.label}", response.message]
    for result in evaluate_incident_response(response):
        lines.extend(("", f"Criterion: {result.criterion.criterion_id}", result.outcome.value, result.explanation))
        if result.evidence:
            lines.append("Evidence: " + " | ".join(result.evidence))
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
        else:
            output = _trust_text()
    except KeyError as error:
        build_parser().error(error.args[0])
    print(output)
    return 0
