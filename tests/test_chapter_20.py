from soft_skills_lab.cli import main
from soft_skills_lab.domain.models import MessagePurpose, ReviewIntent, StatusCategory, WrittenChannel
from soft_skills_lab.evaluation.writing import evaluate_written_response
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.scenarios.writing import ARTIFACTS
from soft_skills_lab.trust import TrustEventKind


def results(response_id):
    scenario=get_scenario("deployment-risk")
    return {x.criterion.criterion_id:x.outcome.value for x in evaluate_written_response(scenario,get_response(scenario.scenario_id,response_id))}


def test_written_representation_and_primary_truth():
    w=get_response("deployment-risk","decision-useful").written_message
    assert w.channel is WrittenChannel.CHAT and w.purpose is MessagePurpose.REQUEST
    assert w.current_state is StatusCategory.AT_RISK and w.owner == "Alex" and w.follow_up_point == "T5"
    assert "Production is unaffected now." in w.impact


def test_short_is_not_automatically_clear_and_long_is_not_complete():
    assert results("context-free")["provides-standalone-context"] == "FAIL"
    assert results("wall-of-text")["uses-appropriate-channel-detail"] == "FAIL"
    assert results("concise-decision-useful")["provides-standalone-context"] == "PASS"


def test_activity_alarm_reassurance_and_ambiguous_ask_fail_distinct_dimensions():
    assert results("activity-only")["states-current-state"] == "FAIL"
    assert results("alarm-without-evidence")["preserves-uncertainty"] == "FAIL"
    assert results("false-reassurance")["preserves-uncertainty"] == "FAIL"
    assert results("ambiguous-request")["makes-request-explicit"] == "FAIL"


def test_decision_useful_variants_are_behaviorally_equivalent():
    a,b=results("decision-useful"),results("concise-decision-useful")
    assert a == b
    assert all(a[x] == "PASS" for x in ("provides-standalone-context","states-current-state","uses-decision-relevant-evidence","makes-request-explicit","establishes-next-update"))


def test_decision_record_review_ticket_handoff_and_disagreement():
    decision=ARTIFACTS["release-readiness-recap"]
    assert decision.decision and decision.owner and decision.durable_record
    review=ARTIFACTS["verification-pr-review"]
    assert review.review_intent is ReviewIntent.BLOCKING and review.established_facts
    assert ARTIFACTS["adapter-disagreement"].review_intent is ReviewIntent.SUGGESTION
    assert ARTIFACTS["verification-ticket"].uncertainty and ARTIFACTS["verification-ticket"].follow_up_point
    assert ARTIFACTS["api-handoff"].acknowledgement_required


def test_escalation_correction_audience_and_no_ritual_reply():
    assert ARTIFACTS["security-escalation"].purpose is MessagePurpose.ESCALATE
    assert ARTIFACTS["material-correction"].material_correction
    assert ARTIFACTS["informational-no-reply"].acknowledgement_required is False
    eng,ops=ARTIFACTS["engineering-incident"],ARTIFACTS["operations-incident"]
    assert eng.channel is not ops.channel
    assert eng.established_facts[0] == ops.established_facts[0]
    assert ARTIFACTS["forwardable-deployment"].standalone_context
    assert ARTIFACTS["low-impact-clarification"].audience == ("Jordan",)
    assert ARTIFACTS["contract-reply-draft"].durable_record is False
    assert ARTIFACTS["contract-reply-final"].durable_record is True


def test_trust_events_do_not_score_style_or_verbosity():
    names={x.name for x in TrustEventKind}
    assert {"MATERIAL_WRITTEN_STATE_CLEAR","WRITTEN_ERROR_CORRECTED","UNSUPPORTED_WRITTEN_CLAIM"} <= names
    assert not any(word in name for name in names for word in ("GRAMMAR","VOCABULARY","VERBOSITY","FORMALITY"))


def test_cli_is_deterministic(capsys):
    main(["written-message","deployment-risk","decision-useful"]); first=capsys.readouterr().out
    main(["written-message","deployment-risk","decision-useful"]); assert capsys.readouterr().out == first
    assert "CURRENT STATE\nAT_RISK" in first and "NEXT UPDATE\nT5" in first
    main(["written-artifact","verification-pr-review"]); assert "REVIEW INTENT\nBlocking" in capsys.readouterr().out


def test_compare_keeps_dimensions_separate(capsys):
    main(["compare","deployment-risk"]); output=capsys.readouterr().out
    assert "context-free" in output and "concise-decision-useful" in output
    assert "writing skill" not in output.lower()
