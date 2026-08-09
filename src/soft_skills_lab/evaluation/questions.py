"""Observable evaluation for question and escalation behavior."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("targets-relevant-unknown", "Targets uncertainty that affects the current decision."),
    EvaluationCriterion("provides-context", "Supplies the recipient with useful decision context."),
    EvaluationCriterion("shows-prior-investigation", "Investigates first when doing so is cheap and safe."),
    EvaluationCriterion("is-answerable", "Asks specific questions that can receive useful answers."),
    EvaluationCriterion("avoids-assumption-disguised-as-question", "Does not embed unsupported conclusions in confirmation questions."),
    EvaluationCriterion("avoids-unnecessary-question", "Does not ask others to retrieve trivially available evidence."),
    EvaluationCriterion("clarifies-decision", "Materially reduces uncertainty about the next action."),
    EvaluationCriterion("avoids-question-dump", "Prioritizes rather than sending an undifferentiated list."),
)


def evaluate_question_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    """Evaluate explicit scenario metadata, not arbitrary natural language."""
    context = scenario.question_context
    if context is None:
        raise ValueError("scenario has no question context")
    unknowns = {item.unknown_id: item for item in context.unknowns}
    targets = tuple(target for question in response.questions for target in question.target_unknowns)
    relevant_targets = tuple(target for target in targets if target in unknowns and unknowns[target].relevance.name in {"HIGH", "MEDIUM"})
    unnecessary = tuple(target for target in targets if target in unknowns and unknowns[target].is_resolved)
    embedded = tuple(item for question in response.questions for item in question.embedded_assumptions)
    emergency = response.immediate_escalation and response.delay_creates_risk and response.authority_limited
    investigated = bool(response.investigation_performed) or emergency
    answerable = bool(response.questions) and all(question.answerable for question in response.questions)
    decision_help = bool(relevant_targets) or response.proposed_next_action or emergency
    checks = (
        (bool(relevant_targets) or emergency, relevant_targets or (("high-risk escalation",) if emergency else ())),
        (response.supplies_question_context or emergency, (response.message,) if response.supplies_question_context or emergency else ()),
        (investigated, response.investigation_performed or (("delay increases harm",) if emergency else ())),
        (answerable or emergency, tuple(question.message for question in response.questions)),
        (not embedded and not response.assumptions, embedded or response.assumptions),
        (not unnecessary, unnecessary),
        (decision_help and not (response.investigation_delay and response.delay_creates_risk), (response.next_action or response.message,)),
        (not response.question_dump, tuple(question.question_id for question in response.questions)),
    )
    pass_text = (
        "The behavior targets decision-relevant uncertainty.", "Useful context is supplied.",
        "Investigation is proportionate to cost, safety, and urgency.", "The request is specific enough to answer.",
        "No unsupported conclusion is hidden in a question.", "Available evidence is not delegated unnecessarily.",
        "The behavior helps determine the next safe action.", "Important uncertainty is prioritized.",
    )
    fail_text = (
        "No decision-relevant unknown is targeted.", "The recipient must reconstruct the situation.",
        "Cheap, safe evidence was not checked, or investigation continued while delay created risk.",
        "The request is absent or too broad to answer usefully.", "The question embeds unsupported conclusions.",
        "The question asks for information already available through reasonable inspection.",
        "The behavior does not resolve or responsibly defer the decision.",
        "A large undifferentiated list shifts prioritization to the recipient.",
    )
    return tuple(EvaluationResult(criterion, Outcome.PASS if passed else Outcome.FAIL,
                                  pass_text[index] if passed else fail_text[index], tuple(evidence))
                 for index, (criterion, (passed, evidence)) in enumerate(zip(CRITERIA, checks, strict=True)))


def evaluate_question_sequence(response: ProfessionalResponse) -> EvaluationResult:
    criterion = EvaluationCriterion("asks-about-problem-before-solution", "Clarifies the problem before selecting a solution.")
    passed = response.problem_first_sequence is True
    return EvaluationResult(criterion, Outcome.PASS if passed else Outcome.FAIL,
        "The sequence narrows the problem before discussing implementation." if passed else
        "The sequence proposes technologies before the problem and success condition are understood.", (response.message,))
