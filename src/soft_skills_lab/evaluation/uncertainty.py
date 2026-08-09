"""Behavioral evaluation of authored uncertainty semantics."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("states-uncertainty-explicitly", "States directly when the answer is not known."),
    EvaluationCriterion("does-not-exceed-evidence", "Does not claim more certainty than available evidence supports."),
    EvaluationCriterion("labels-hypothesis", "Labels an offered hypothesis as a hypothesis rather than fact."),
    EvaluationCriterion("provides-evidence-basis", "Provides evidence supporting current judgment."),
    EvaluationCriterion("identifies-missing-evidence", "Identifies what prevents a confident answer."),
    EvaluationCriterion("connects-uncertainty-to-next-action", "Connects uncertainty to a credible investigation action."),
    EvaluationCriterion("establishes-follow-up", "Establishes the next information point."),
    EvaluationCriterion("communicates-decision-impact", "Explains how to decide or mitigate while uncertainty remains."),
    EvaluationCriterion("distinguishes-known-from-unknown", "Separates established evidence from the unresolved answer."),
    EvaluationCriterion("avoids-unsupported-claim", "Avoids an unsupported causal or delivery claim."),
    EvaluationCriterion("establishes-next-action", "Names the next useful action."),
    EvaluationCriterion("communicates-risk", "Makes the decision risk of uncertainty visible."),
)


def evaluate_uncertainty_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    """Evaluate explicit fields; never parse arbitrary response text."""
    offered = response.offered_hypothesis is not None
    checks = (
        response.states_uncertainty_explicitly,
        not response.exceeds_available_evidence and not response.claims_cause_without_evidence,
        not offered or response.hypothesis_labeled,
        bool(response.evidence_basis),
        bool(response.missing_evidence_identified),
        bool(response.uncertainty_next_action),
        response.follow_up_point is not None,
        bool(response.decision_impact),
        response.states_uncertainty_explicitly and bool(response.evidence_basis),
        not response.exceeds_available_evidence and not response.claims_cause_without_evidence,
        bool(response.uncertainty_next_action),
        bool(response.decision_impact),
    )
    pass_texts = (
        "The unavailable answer is stated directly.", "The response preserves the certainty supported by evidence.",
        "Current judgment is explicitly labeled as a hypothesis.", "The judgment has an explicit evidence basis.",
        "The missing evidence is visible.", "A concrete method for learning more is supplied.",
        "The next information point is explicit.", "The decision impact of remaining uncertainty is explicit.",
        "Known evidence and the unresolved answer remain distinct.", "No unsupported claim is made.",
        "The next action is explicit.", "Decision risk is visible.",
    )
    fail_texts = (
        "The central uncertainty is not answered directly.", "The response converts uncertainty into unsupported certainty.",
        "A possible explanation is presented without clearly labeling it as a hypothesis.",
        "No evidence basis is connected to the response.", "The response does not say what prevents a conclusion.",
        "Uncertainty is not connected to a next investigation.", "No next information point is established.",
        "The recipient is not told how remaining uncertainty affects a decision.",
        "Known evidence is not clearly separated from the unresolved answer.", "An unsupported claim exceeds the evidence.",
        "No next action is established.", "The risk created by uncertainty is not communicated.",
    )
    evidence = response.evidence_basis or response.missing_evidence_identified or ((response.message,) if response.message else ())
    return tuple(EvaluationResult(criterion, Outcome.PASS if check else Outcome.FAIL,
                                  passed if check else failed, evidence)
                 for criterion, check, passed, failed in zip(CRITERIA, checks, pass_texts, fail_texts, strict=True))
