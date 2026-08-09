from soft_skills_lab.scenarios.trust_history import get_trust_history
from soft_skills_lab.trust import EvidencePolarity, EvidenceProvenance, TrustDimension as D, TrustState as S
from soft_skills_lab.cli import main


def test_six_week_history_is_multidimensional_and_traceable():
    history=get_trust_history("six-week-project")
    assert history.state(D.COMMITMENT_RELIABILITY) is S.ESTABLISHED
    assert history.state(D.RISK_VISIBILITY) is S.ESTABLISHED
    assert history.state(D.HANDOFF_RELIABILITY) is S.REBUILDING
    assert history.state(D.TECHNICAL_JUDGMENT) is S.INSUFFICIENT_EVIDENCE
    events=history.for_dimension(D.HANDOFF_RELIABILITY)
    assert {x.polarity for x in events} == {EvidencePolarity.POSITIVE,EvidencePolarity.NEGATIVE}
    assert all(x.event_id and x.time and x.linked_scenario for x in history.evidence)
    assert all(isinstance(x.provenance,EvidenceProvenance) for x in history.evidence)


def test_one_event_is_not_a_reputation_and_one_mistake_does_not_destroy_it():
    assert get_trust_history("one-success").state(D.COMMITMENT_RELIABILITY) is S.INSUFFICIENT_EVIDENCE
    mistake=get_trust_history("one-mistake")
    assert mistake.state(D.HANDOFF_RELIABILITY) is S.MIXED
    assert mistake.state(D.COMMITMENT_RELIABILITY) is S.ESTABLISHED


def test_recent_pattern_degrades_and_later_observation_rebuilds_without_erasure():
    degraded=get_trust_history("trust-degradation")
    rebuilt=get_trust_history("trust-rebuilding")
    assert degraded.state(D.RISK_VISIBILITY) is S.DEGRADED
    assert rebuilt.state(D.RISK_VISIBILITY) is S.REBUILDING
    assert len(rebuilt.evidence)>len(degraded.evidence)
    assert any(x.polarity is EvidencePolarity.NEGATIVE for x in rebuilt.evidence)


def test_technical_competence_does_not_transfer_to_coordination_or_expanded_scope():
    history=get_trust_history("competence-coordination")
    assert history.state(D.TECHNICAL_JUDGMENT) is S.ESTABLISHED
    assert history.state(D.HANDOFF_RELIABILITY) is S.DEGRADED
    transfer=get_trust_history("domain-transfer")
    assert transfer.state(D.COMMITMENT_RELIABILITY) is S.ESTABLISHED
    assert transfer.state(D.DECISION_CREDIBILITY) is S.INSUFFICIENT_EVIDENCE


def test_observer_view_does_not_gain_global_knowledge():
    history=get_trust_history("six-week-project")
    assert history.state(D.HANDOFF_RELIABILITY,"Jordan") is S.MIXED
    assert history.state(D.HANDOFF_RELIABILITY,"Morgan") is S.INSUFFICIENT_EVIDENCE
    assert history.state(D.RISK_VISIBILITY,"Dana") is S.INSUFFICIENT_EVIDENCE


def test_private_cause_excluded_but_handling_is_evidence():
    history=get_trust_history("capacity-handling")
    text=" ".join(x.observable_behavior for x in history.evidence).casefold()
    assert "private" not in text and "medical" not in text and "family" not in text
    assert history.state(D.COMMITMENT_RELIABILITY) is S.ESTABLISHED


def test_promises_and_apologies_do_not_change_degraded_history():
    history=get_trust_history("trust-degradation")
    assert not any("promise" in x.observable_behavior.casefold() or "apology" in x.observable_behavior.casefold() for x in history.evidence)
    assert history.state(D.RISK_VISIBILITY) is S.DEGRADED


def test_cli_inspections_are_deterministic(capsys):
    assert main(["trust-history","six-week-project"]) == 0
    first=capsys.readouterr().out
    assert "No global score" in first and "State: REBUILDING" in first
    main(["trust-explain","six-week-project","handoff-reliability"])
    assert "One missed handoff" in capsys.readouterr().out
    main(["trust-view","six-week-project","--observer","Dana"])
    assert "No available evidence" in capsys.readouterr().out
