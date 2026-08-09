from soft_skills_lab.capstone import PROJECT_ID, build_simulation, get_simulation
from soft_skills_lab.cli import main
from soft_skills_lab.trust import EvidencePolarity, TrustDimension, TrustState


def test_timeline_is_deterministic_and_complete():
    first = build_simulation(); second = build_simulation()
    assert first.events == second.events
    assert tuple(e.time for e in first.events) == ("T0", "T2", "T3", "T4", "T5", "T7", "T9", "T10", "T11", "T12", "T14", "T16", "T17", "T18", "T18.5", "T20", "T24")


def test_existing_public_scenarios_are_composed():
    simulation = build_simulation()
    assert len(simulation.composed_scenarios) == 13
    assert {s.scenario_id for s in simulation.composed_scenarios} >= {"skipped-validation", "payment-authorization", "verification-launch", "release-readiness"}


def test_requirement_resolution_traces_to_launch():
    trace = build_simulation().requirements
    assert "failed members know what to do" in trace.request
    assert "retryable-timeout" in trace.implementation_contract
    assert any("support workflow" in item for item in trace.launch_verification)
    assert all(trace.product_decisions) and all(trace.acceptance_conditions)


def test_explicit_ownership_commitments_and_dependencies():
    simulation = build_simulation()
    owners = {c.owner for c in simulation.commitments}
    assert owners == {"Alex", "Jordan", "Priya", "Dana", "Morgan"}
    assert any(c.commitment_id == "api-contract" and c.expected_completion == 7 for c in simulation.commitments)
    assert ("Jordan frontend", "Alex API contract") in simulation.dependencies


def test_uncertainty_capacity_boundary_and_revision_are_preserved():
    simulation = build_simulation(); t3 = simulation.at("T3")[-1]; t5 = simulation.at("T5")[-1]
    assert "Request may already be processed." in t3.facts
    assert "Blind retry may be unsafe." in t3.risks
    assert "private cause was not recorded" in " ".join(t5.facts)
    assert "commitment revised" in t5.summary
    assert not any(word in " ".join(e.observable_behavior for e in simulation.trust_history.evidence).lower() for word in ("medical", "family", "relationship"))


def test_handoff_requires_usable_acknowledged_dependency():
    event = build_simulation().at("T7")[-1]
    assert "acknowledged" in event.summary
    assert "Fixture" in event.facts[0]


def test_disagreement_scope_status_and_leadership_are_visible():
    simulation = build_simulation()
    summaries = {e.time: e.summary for e in simulation.events}
    assert "disagreement resolved" in summaries["T9"]
    assert "deferred" in summaries["T10"]
    assert "risk reported" in summaries["T11"]
    assert "dependencies aligned" in summaries["T12"]
    assert "peer decision rights" in simulation.trust_history.interpretations[TrustDimension.CROSS_TEAM_COORDINATION].why


def test_mistake_disclosure_incident_responsibility_and_prevention_are_distinct():
    simulation = build_simulation(); by_id = {e.event_id: e for e in simulation.trust_history.evidence}
    assert by_id["validation-skipped"].polarity is EvidencePolarity.NEGATIVE
    assert by_id["incident-response"].polarity is EvidencePolarity.POSITIVE
    assert by_id["responsibility"].time == "T18"  # assigned only after T17 evidence
    assert by_id["prevention"].time == "T24"
    assert "No real members affected." in simulation.at("T17")[-1].facts


def test_feedback_conflict_and_written_decision_are_inspectable():
    simulation = build_simulation(); event = simulation.at("T18")[-1]
    assert any("Conflict was refocused" in fact for fact in event.facts)
    assert "feedback" in event.summary
    assert simulation.written_decision.owners
    assert simulation.written_decision.monitoring
    assert simulation.written_decision.member_support_readiness


def test_both_professionally_defensible_launch_branches_are_deterministic():
    launch = build_simulation("monitor-and-launch"); delay = build_simulation("delay-for-regression")
    assert (launch.launch_time, delay.launch_time) == ("T20", "T22")
    assert launch.project_outcome == delay.project_outcome == "launched successfully"
    assert launch.trust_history == delay.trust_history
    assert launch.decisions[-1].owner == delay.decisions[-1].owner == "Morgan"


def test_outcome_does_not_collapse_professional_evidence_invariants():
    simulation = build_simulation(); polarities = {e.polarity for e in simulation.trust_history.evidence}
    assert simulation.project_outcome == "launched successfully"
    assert {EvidencePolarity.POSITIVE, EvidencePolarity.NEGATIVE} <= polarities
    assert simulation.trust_history.state(TrustDimension.TECHNICAL_JUDGMENT) is TrustState.MIXED
    assert any(e.event_id == "validation-skipped" for e in simulation.trust_history.evidence)  # recovery did not erase it
    assert any(e.event_id == "prevention" for e in simulation.trust_history.evidence)  # recovery adds evidence
    assert not hasattr(simulation, "professionalism_score")


def test_incident_recovery_is_not_learning_until_follow_up():
    before = {e.event_id for event in build_simulation().at("T17") for e in build_simulation().trust_history.evidence if e.event_id in event.evidence_ids}
    assert "incident-response" in before
    assert "prevention" not in before


def test_unknown_project_and_time_are_rejected():
    import pytest
    with pytest.raises(KeyError, match="unknown capstone project"):
        get_simulation("other")
    with pytest.raises(KeyError, match="unknown capstone time"):
        build_simulation().at("T99")


def test_all_cli_reports_are_deterministic(capsys):
    commands = (("capstone",), ("capstone-step", "--at", "T14"), ("capstone-evidence",),
                ("capstone-trust",), ("capstone-requirements",), ("capstone-decisions",), ("capstone-judgment",))
    for command in commands:
        argv = [command[0], PROJECT_ID, *command[1:]]
        assert main(argv) == 0; first = capsys.readouterr().out
        assert main(argv) == 0; second = capsys.readouterr().out
        assert first == second and first.strip()


def test_delayed_cli_branch_reports_t22(capsys):
    main(["capstone", PROJECT_ID, "--launch-decision", "delay-for-regression"])
    output = capsys.readouterr().out
    assert "T22   Launch completed" in output
    assert "launched successfully at T22" in output
