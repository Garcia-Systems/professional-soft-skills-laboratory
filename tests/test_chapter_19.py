from soft_skills_lab.domain.models import ContributionType
from soft_skills_lab.evaluation.meetings import evaluate_meeting_response
from soft_skills_lab.scenarios import get_response, get_scenario, list_responses
from soft_skills_lab.cli import main
from soft_skills_lab.trust.model import MEETING_EVENTS

def results(sid,rid):
    return {x.criterion.criterion_id:x.outcome.value for x in evaluate_meeting_response(get_scenario(sid),get_response(sid,rid))}

def test_release_context_preparation_agenda_and_owner():
    m=get_scenario("release-readiness").meeting_context
    assert m.purpose == "Decide whether Friday release is acceptable."
    assert len(m.agenda_items)==4 and dict(m.decision_owners)["Morgan"]=="engineering release approval"
    assert "Remaining test failure." in dict(m.role_preparation)["Alex"]
    assert "Full backend architecture walkthrough." in dict(m.not_required_preparation)["Alex"]

def test_contribution_semantics_not_airtime():
    useful=get_response("release-readiness","useful-question").meeting_contribution
    dominant=get_response("release-readiness","dominate-meeting").meeting_contribution
    assert useful.contribution_type is ContributionType.QUESTION and useful.decision_relevant
    assert not dominant.within_scope
    assert results("release-readiness","useful-question")["contributes-decision-relevant-information"]=="PASS"
    assert results("release-readiness","dominate-meeting")["matches-meeting-purpose"]=="FAIL"

def test_primary_paths_and_invariants():
    assert len(list_responses("release-readiness"))==8
    assert results("release-readiness","unprepared-silence")["prepares-for-role"]=="FAIL"
    assert results("release-readiness","silent-relevant-risk")["surfaces-relevant-risk"]=="FAIL"
    assert results("release-readiness","repeat-existing-point")["avoids-redundant-airtime"]=="FAIL"
    assert results("release-readiness","summarize-and-close")["closes-meeting-loop"]=="PASS"

def test_decision_action_and_notes_preserve_state_change():
    out=get_scenario("release-readiness").meeting_context.outcome
    assert out.decisions[0].owner=="Morgan" and out.actions[0].owner=="Alex" and out.actions[0].due_point=="T4"
    assert get_response("scope-without-owner","route-recommendation").respects_decision_ownership
    assert not get_response("scope-without-owner","pretend-consensus").decision_captured

def test_purpose_changes_appropriate_detail_and_silence_can_be_useful():
    assert results("daily-standup","deep-debugging")["matches-meeting-purpose"]=="FAIL"
    assert results("design-review","purposeful-detail")["matches-meeting-purpose"]=="PASS"
    assert results("operations-support","low-airtime-useful")["matches-meeting-purpose"]=="PASS"

def test_uncertainty_interruption_disagreement_and_conflict():
    assert get_response("meeting-uncertainty","bounded-follow-up").preserves_uncertainty
    assert not get_response("meeting-interruption","interrupt").captures_explicit_concern
    assert get_response("meeting-interrupted-risk","protect-relevant-point").relevant_point_protected
    assert get_response("meeting-group-disagreement","evidence-once").respects_decision_ownership
    assert get_response("meeting-conflict","refocus").creates_decision_path

def test_attention_async_and_trust_do_not_penalize_quietness():
    assert get_response("remote-decision","missed-question").attention_failure
    assert get_response("deployment-success-update","use-async").async_recommended
    assert all("quiet" not in event.kind.label.lower() for event in MEETING_EVENTS)

def test_cli_inspection_is_deterministic(capsys):
    for command in (("meeting","release-readiness"),("meeting-outcome","release-readiness"),("meeting-flow","release-readiness"),("compare","release-readiness")):
        assert main(list(command))==0
    output=capsys.readouterr().out
    assert "ALEX SHOULD PREPARE" in output and "Alex: Fix and validate" in output
    assert "no presence, airtime, or personality score" in output
