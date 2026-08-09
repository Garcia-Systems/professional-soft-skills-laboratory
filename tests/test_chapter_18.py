"""Chapter 18 interview communication invariants."""
import pytest
from soft_skills_lab.domain.models import Outcome
from soft_skills_lab.evaluation.interviews import evaluate_interview_response, followup_consistent
from soft_skills_lab.scenarios import get_response, get_scenario
from soft_skills_lab.scenarios.interviews import get_answer, get_question, select_story
from soft_skills_lab.cli import main

def outcomes(sid,rid):
 s=get_scenario(sid); return {x.criterion.criterion_id:x.outcome for x in evaluate_interview_response(s,get_response(sid,rid))}

def test_question_representation_and_competencies():
 q=get_question("mistake"); assert "Responsibility" in q.competencies and len(q.follow_ups)==4

def test_experience_reuses_chapter_8_facts_and_supported_metric():
 e=get_scenario("interview-mistake").experience_evidence[0]
 assert "Required staging validation was skipped." in e.facts
 assert e.supported_metrics == ("Failure rate rose to about 18% during the incident.",)

def test_answer_represents_ownership_team_reasoning_outcome_and_learning():
 a=get_answer("mistake","evidence-based-mistake")
 assert a.ownership_accurate and a.team_contribution and a.reasoning and a.outcome and a.later_evidence

@pytest.mark.parametrize("rid,criterion,expected",[
 ("fake-non-mistake","answers-question-directly",Outcome.FAIL),
 ("blame-story","states-ownership-accurately",Outcome.FAIL),
 ("self-destruction","preserves-truth",Outcome.PARTIAL),
 ("technical-dump","keeps-relevant-scope",Outcome.FAIL),
 ("vague-learning","shows-learning-evidence",Outcome.PARTIAL),
 ("overclaim-learning","preserves-truth",Outcome.FAIL),
 ("evidence-based-mistake","shows-learning-evidence",Outcome.PASS),
 ("concise-evidence-based","uses-specific-evidence",Outcome.PASS),])
def test_primary_paths(rid,criterion,expected): assert outcomes("interview-mistake",rid)[criterion] is expected

def test_concision_is_not_vagueness_or_word_count():
 short=outcomes("interview-mistake","concise-evidence-based")
 assert short["uses-specific-evidence"] is Outcome.PASS and short["shows-outcome"] is Outcome.PASS

def test_specificity_is_not_technical_dump(): assert outcomes("interview-mistake","technical-dump")["keeps-relevant-scope"] is Outcome.FAIL

def test_clear_ownership_does_not_take_team_credit():
 a=get_answer("mistake","evidence-based-mistake"); assert "alone" in a.ownership_claim and a.team_contribution

def test_team_contribution_does_not_erase_personal_contribution(): assert get_answer("mistake","concise-evidence-based").responsibility.startswith("Skipped")

def test_confidence_does_not_require_exaggeration(): assert outcomes("interview-mistake","evidence-based-mistake")["preserves-truth"] is Outcome.PASS

def test_learning_claim_is_not_learning_evidence():
 assert outcomes("interview-mistake","vague-learning")["shows-learning-evidence"] is Outcome.PARTIAL

def test_unsupported_metric_is_not_evidence():
 a=get_answer("mistake","overclaim-learning"); assert a.unsupported_claims and outcomes("interview-mistake","overclaim-learning")["preserves-truth"] is Outcome.FAIL

@pytest.mark.parametrize("sid,rid",[("interview-disagreement","collaborative-decision"),("interview-conflict","de-escalate-and-resolve"),("interview-failure","responsible-failure"),("interview-weakness","evidence-based-weakness"),("interview-layoff","concise-forward"),("interview-resume-gap","bounded-gap"),("interview-technical-unknown","bounded-reasoning"),("interview-estimation","conditional-estimate"),("interview-imperfect-outcome","partial-success")])
def test_additional_strong_scenarios(sid,rid): assert outcomes(sid,rid)["answers-question-directly"] is Outcome.PASS

def test_failure_does_not_invent_personal_fault(): assert get_answer("failure","responsible-failure").ownership_accurate

def test_private_detail_not_required(): assert outcomes("interview-resume-gap","bounded-gap")["preserves-privacy"] is Outcome.PASS

def test_i_dont_know_is_not_failure(): assert outcomes("interview-technical-unknown","bounded-reasoning")["preserves-truth"] is Outcome.PASS

def test_imperfect_outcome_can_be_successful_answer(): assert get_answer("project-not-planned","partial-success").outcome.endswith("deferred.")

def test_followup_consistency_and_contradiction():
 a=get_answer("mistake","evidence-based-mistake"); assert followup_consistent(a)
 from dataclasses import replace
 assert not followup_consistent(replace(a,followup_ownership_claims=(("why-skip-validation","The team decided; Alex was not involved."),)))

def test_story_selection_prefers_influence_evidence(): assert select_story("influence").experience_id == "adapter-boundary-decision"

def test_behaviorally_equivalent_strong_answers():
 assert outcomes("interview-mistake","evidence-based-mistake") == outcomes("interview-mistake","concise-evidence-based")

@pytest.mark.parametrize("args,text",[
 (["interview-question","mistake"],"LIKELY EVALUATION AREAS"),
 (["interview-answer","mistake","evidence-based-mistake"],"OWNED ACTION"),
 (["interview-followup","mistake","why-skip-validation"],"CONSISTENT EVIDENCE"),
 (["story-selection","influence"],"adapter-boundary-decision"),
 (["compare","interview-mistake"],"concise-evidence-based"),])
def test_cli_deterministic(args,text,capsys):
 assert main(args)==0; assert text in capsys.readouterr().out
