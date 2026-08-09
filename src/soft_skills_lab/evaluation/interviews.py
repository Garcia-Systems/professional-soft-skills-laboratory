"""Explicit Chapter 18 answer-quality evaluation."""
from soft_skills_lab.domain.models import EvaluationCriterion, EvaluationResult, Outcome
CRITERIA=(
 EvaluationCriterion("answers-question-directly","Addresses the evaluation need."),
 EvaluationCriterion("uses-specific-evidence","Provides concrete authored evidence."),
 EvaluationCriterion("states-ownership-accurately","Preserves personal and team boundaries."),
 EvaluationCriterion("preserves-truth","Avoids unsupported claims and metrics."),
 EvaluationCriterion("keeps-relevant-scope","Avoids irrelevant detail without deleting evidence."),
 EvaluationCriterion("explains-reasoning","Explains reasoning when useful."),
 EvaluationCriterion("shows-outcome","States what happened."),
 EvaluationCriterion("shows-learning-evidence","Supports claimed learning with changed behavior or later evidence."),
 EvaluationCriterion("preserves-privacy","Does not require private detail."),
 EvaluationCriterion("handles-follow-up-consistently","Follow-up ownership does not contradict the initial claim."),)
def followup_consistent(answer):
    return not answer.ownership_claim or all(claim == answer.ownership_claim for _,claim in answer.followup_ownership_claims)
def evaluate_interview_response(scenario,response):
    a=response.interview_answer
    if a is None: raise ValueError("response has no interview metadata")
    values=(a.answers_directly,bool(a.evidence),a.ownership_accurate,not a.unsupported_claims,
        not a.irrelevant_detail,bool(a.reasoning) or a.question_id in {"gap","leaving","weakness"},bool(a.outcome) or a.question_id in {"technical-unknown","estimate","weakness"},
        bool(a.later_evidence) or bool(a.learning_action) or a.question_id not in {"mistake","weakness","failure","project-not-planned"},a.privacy_preserved,followup_consistent(a))
    partial={"blame-story":{1,3},"self-destruction":{1,3},"technical-dump":{0,2},"vague-learning":{7},"overclaim-learning":{7}}
    results=[]
    for i,(criterion,value) in enumerate(zip(CRITERIA,values)):
        outcome=Outcome.PARTIAL if i in partial.get(response.response_id,set()) else Outcome.PASS if value else Outcome.FAIL
        results.append(EvaluationResult(criterion,outcome,"Authored semantic metadata makes this behavior inspectable.",(response.message,)))
    return tuple(results)
