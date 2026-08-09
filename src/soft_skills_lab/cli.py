"""Command-line interface for the executable textbook."""

import argparse
from collections.abc import Sequence

from soft_skills_lab.evaluation import evaluate_commitment_response, evaluate_explanation, evaluate_incident_response, evaluate_listening_response, evaluate_question_response, evidence_for_commitment
from soft_skills_lab.scenarios import get_response, get_scenario, list_responses
from soft_skills_lab.scenarios.commitment import COMMITMENT, PRIMARY_RESPONSE_IDS, TIMELINE
from soft_skills_lab.scenarios.listening import PRIMARY_RESPONSE_IDS as LISTENING_RESPONSE_IDS
from soft_skills_lab.scenarios.questions import REPORT_ANSWERS, REPORT_EXPORT, REPORT_RESPONSES, apply_answers
from soft_skills_lab.scenarios.explanations import AUDIENCE_EXPLANATIONS, PAYMENT_RESPONSES
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
    scenario = get_scenario(scenario_id)
    if scenario.explanation_context is not None or scenario_id == "database-migration":
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
        else:
            output = _trust_text()
    except KeyError as error:
        build_parser().error(error.args[0])
    print(output)
    return 0
