"""Explicit, multidimensional evaluation for Chapter 5 status semantics."""

from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome, ProfessionalResponse, StatusCategory, WorkplaceScenario

CRITERIA = (
    EvaluationCriterion("states-current-state", "States the semantic commitment state."),
    EvaluationCriterion("communicates-material-progress", "Reports meaningful completed or remaining state, not activity alone."),
    EvaluationCriterion("communicates-risk", "Makes known material risk visible."),
    EvaluationCriterion("communicates-dependency-impact", "Makes effects on another person's plan visible."),
    EvaluationCriterion("labels-blocker-correctly", "Distinguishes a blocker from a problem or risk."),
    EvaluationCriterion("provides-forecast-basis", "Bases a forecast on evidence without guaranteeing it."),
    EvaluationCriterion("requests-needed-action", "Names needed action when another owner must act."),
    EvaluationCriterion("establishes-next-update", "Sets a useful follow-up point."),
    EvaluationCriterion("avoids-unnecessary-detail", "Keeps detail proportional to the decision."),
    EvaluationCriterion("closes-loop", "Tells a dependent recipient when completed work is ready."),
)

def evaluate_status_response(scenario: WorkplaceScenario, response: ProfessionalResponse) -> tuple[EvaluationResult, ...]:
    u = response.status_update
    state = Outcome.PASS if u and u.current_state else Outcome.FAIL
    progress = Outcome.PASS if u and (u.completed_work or u.remaining_work) else Outcome.FAIL
    risk_required = scenario.scenario_id != "verification-completion"
    risk = Outcome.PASS if u and u.risks else Outcome.FAIL if risk_required else Outcome.PASS
    impact = Outcome.PASS if u and u.dependency_impact else Outcome.FAIL
    true_blocker = scenario.scenario_id == "credential-blocker"
    blocker_correct = bool(u and u.current_state is StatusCategory.BLOCKED and u.blockers) if true_blocker else not (u and u.current_state is StatusCategory.BLOCKED)
    forecast = Outcome.PASS if u and u.forecast and u.forecast.basis and not u.forecast.guaranteed else Outcome.FAIL
    action_needed = true_blocker
    requested = Outcome.PASS if u and u.requested_action and u.dependency_owner else Outcome.FAIL if action_needed else Outcome.PASS
    follow_up = Outcome.PASS if u and u.next_update_point is not None else Outcome.FAIL
    detail = Outcome.FAIL if len(response.implementation_details) > 3 or (u and len(u.activity_details) > 3) else Outcome.PASS
    closure_required = scenario.scenario_id == "verification-completion"
    closure = Outcome.PASS if response.loop_closed else Outcome.FAIL if closure_required else Outcome.PASS
    # Vague risk is explicitly partial rather than equivalent to silence.
    if response.material_risk_communicated and risk is Outcome.PASS and state is Outcome.FAIL:
        risk = Outcome.PARTIAL
    outcomes = (state, progress, risk, impact, Outcome.PASS if blocker_correct else Outcome.FAIL,
                forecast, requested, follow_up, detail, closure)
    explanations = (
        "The semantic work state is explicit." if state is Outcome.PASS else "The recipient cannot tell whether work is on track, at risk, blocked, or complete.",
        "Meaningful completed or remaining work is explicit." if progress is Outcome.PASS else "Activity does not establish meaningful progress or remaining state.",
        "Material risk is visible." if risk is Outcome.PASS else "Material risk is missing or too vague to establish status.",
        "A dependent plan's impact is explicit." if impact is Outcome.PASS else "Dependency impact is not made visible.",
        "The blocker label matches whether progress can continue." if blocker_correct else "The authored state hides or mislabels a true blocker.",
        "The forecast has a stated evidence basis and remains conditional." if forecast is Outcome.PASS else "No evidence-based conditional forecast is supplied.",
        "Needed action and ownership are explicit." if requested is Outcome.PASS else "The external owner and requested action are missing.",
        "A next update point is explicit." if follow_up is Outcome.PASS else "No next update point is established.",
        "Detail is proportionate." if detail is Outcome.PASS else "Implementation detail obscures state and action.",
        "The dependent recipient receives completion evidence." if closure is Outcome.PASS else "Completion is not communicated to the dependent recipient.",
    )
    evidence = response.communicated_fact_ids or ((response.message,) if response.message else ())
    return tuple(EvaluationResult(c, o, e, evidence) for c, o, e in zip(CRITERIA, outcomes, explanations, strict=True))
