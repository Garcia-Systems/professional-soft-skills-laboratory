"""Multidimensional evaluation of scenario-authored technical explanations."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse

CRITERIA = (
    EvaluationCriterion("preserves-technical-truth", "Remains consistent with established technical facts."),
    EvaluationCriterion("matches-audience-need", "Includes information required for this audience's decision."),
    EvaluationCriterion("communicates-impact", "Connects the technical condition to its consequence."),
    EvaluationCriterion("communicates-scope", "Describes affected and unaffected scope when relevant."),
    EvaluationCriterion("preserves-uncertainty", "Does not convert an unknown into an established fact."),
    EvaluationCriterion("avoids-unnecessary-detail", "Omits detail that does not help this audience's decision."),
    EvaluationCriterion("supports-decision", "Makes an available action or decision visible."),
    EvaluationCriterion("establishes-next-action", "States what happens next."),
)


def evaluate_explanation(response: ProfessionalResponse, required_needs: tuple[str, ...] =
                         ("impact", "duplicate-risk", "scope", "pause", "next-update")) -> tuple[EvaluationResult, ...]:
    """Evaluate explicit semantics; deliberately performs no prose or style scoring."""
    coverage = len(set(required_needs) & set(response.communicated_need_ids))
    need_outcome = Outcome.PASS if coverage == len(required_needs) else Outcome.PARTIAL if coverage else Outcome.FAIL
    detail_outcome = Outcome.FAIL if len(response.implementation_details) > 3 else Outcome.PARTIAL if response.implementation_details else Outcome.PASS
    truth = Outcome.FAIL if response.unsupported_claims else Outcome.PASS
    impact = Outcome.PASS if response.communicates_impact else Outcome.PARTIAL if "duplicate-risk" in response.communicated_fact_ids else Outcome.FAIL
    uncertainty = Outcome.PASS if response.preserves_uncertainty else Outcome.FAIL
    decision = Outcome.PASS if response.supports_decision and "pause" in response.communicated_need_ids else Outcome.PARTIAL if response.supports_decision else Outcome.FAIL
    outcomes = (truth, need_outcome, impact, Outcome.PASS if response.communicates_scope else Outcome.FAIL,
                uncertainty, detail_outcome, decision, Outcome.PASS if response.next_action else Outcome.FAIL)
    explanations = (
        "The authored claims preserve established facts." if truth is Outcome.PASS else "An authored claim asserts more than the evidence establishes.",
        f"The explanation covers {coverage} of {len(required_needs)} scenario-specific audience needs.",
        "The consequence is explicit." if impact is Outcome.PASS else "The consequence is incomplete or absent.",
        "Affected and unaffected scope is explicit." if response.communicates_scope else "Relevant scope is not communicated.",
        "Unknown provider state remains unknown." if uncertainty is Outcome.PASS else "The explanation loses or converts material uncertainty.",
        "Implementation detail is proportionate." if detail_outcome is Outcome.PASS else "Implementation detail is present and may not serve this audience's decision.",
        "The available decision is clear." if decision is Outcome.PASS else "The available decision is incomplete or absent.",
        "A next action is established." if response.next_action else "No next action or follow-up is established.",
    )
    return tuple(EvaluationResult(criterion, outcome, explanation,
                                  response.unsupported_claims or response.communicated_fact_ids)
                 for criterion, outcome, explanation in zip(CRITERIA, outcomes, explanations, strict=True))
