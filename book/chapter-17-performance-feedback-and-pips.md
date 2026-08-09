# Chapter 17: Performance Feedback and PIPs

## Educational question

> How do you turn “your performance needs to improve” into a concrete plan that both you and your manager can actually evaluate?

This chapter is about observable professional behavior when feedback is formal or consequential. It gives no legal advice, predicts no termination, and does not assume that every plan is fair or every manager claim correct. Fear, anxiety, and embarrassment are not scored. A formal plan is neither proof of an inevitable outcome nor agreement with every allegation.

## Learning objectives

The learner should be able to:

- separate performance claims from evidence;
- identify supported and unsupported generalizations;
- correct material factual inaccuracies without rejecting valid concerns;
- translate vague expectations into observable behavior;
- define useful measurements and establish checkpoints;
- focus improvement on behaviors reasonably within professional control;
- create concrete improvement actions and track evidence across time;
- distinguish effort from demonstrated improvement;
- recognize patterns rather than overreacting to one event;
- preserve plan scope when expectations change; and
- respond professionally when disagreement remains.

## Professional concept

> A performance concern becomes more actionable when everyone can answer: “What would I observe if this improved?”

A **performance concern** is a claim about a gap. **Performance evidence** is an example in the record. A **generalization** extends beyond those examples. An **expectation** describes wanted behavior. A **measurement** explains how relevant evidence will be inspected. An **improvement action** is what an owner will do under a trigger. A **checkpoint** reviews evidence accumulated during a stated interval. An **outcome** says whether the defined criteria were satisfied. A **formal plan** connects those concepts; it is not interchangeable with any one of them.

> “Communicate better” is a concern. “Surface material delivery risk before dependent plans are surprised” is an observable expectation.

When performance is questioned, the useful first move is to convert broad concern into specific evidence, expectations, measurements, actions, and checkpoints. A plan is actionable only if both sides can explain successful improvement. The goal should be clarity about behavior, evidence, and progress—not guessing what the manager means each week. Real plans do not always meet that ideal.

The primary scenario combines earlier models. Risk visibility uses status, commitments, and manager thresholds; handoff closure uses `DELIVERED` and `ACKNOWLEDGED`; status quality uses state, risk, next action, and follow-up; factual disagreement uses evidence without refusing the process; personal capacity uses work impact and revised commitments.

Measurement should increase clarity, not create fake precision. “Send five status messages per day” is a pure activity measure that may reward noise. “Show more confidence” is a personality judgment outside this evaluator. “Never miss a deadline” is outcome-only and ignores uncontrollable conditions. “Surface known delivery risk before dependent plans are surprised” is observable behavior within reasonable professional control. Not every workplace behavior can be measured perfectly.

Effort may be real without demonstrating improvement. Likewise, feelings of improvement are not evidence by themselves. At Day 7, useful updates and an acknowledged handoff are positive evidence, but no material risk occurred: absence of failure is not proof that risk behavior changed. At Day 14, early communication during a real risk event is stronger evidence. One good event does not establish a pattern; one later mistake does not erase the preceding history. Patterns matter.

Correcting “Alex missed T8” matters because the record says delivery occurred at T8. It does not eliminate the supported concern that risk was surfaced late. Accepting the process does not require accepting the inaccurate statement. Similarly, successful technical delivery does not prove that every communication expectation was met.

New feedback can be legitimate coaching. If it becomes a formal expectation, its relationship to the written plan should be explicit. Formal expectations should not become silently moving targets. If Morgan and Alex disagree at a checkpoint, Alex can ask which criterion is unmet, review examples rather than effort alone, document the unresolved disagreement, and continue professional behavior.

## Engineering concept: observable acceptance conditions

An automated test saying “Make the system better” cannot meaningfully pass or fail. A test saying “When a retryable vendor timeout occurs, the API returns `retryable=true`” establishes an observable contract. Professional expectations also become easier to act on when acceptance conditions are visible. Humans are not software; this limited analogy concerns clarity, not mechanistic treatment of people.

## Run the laboratory

```bash
python -m soft_skills_lab scenario communication-visibility
python -m soft_skills_lab evaluate communication-visibility panic-resignation
python -m soft_skills_lab evaluate communication-visibility total-denial
python -m soft_skills_lab evaluate communication-visibility automatic-confession
python -m soft_skills_lab evaluate communication-visibility argue-every-example
python -m soft_skills_lab evaluate communication-visibility vague-promise
python -m soft_skills_lab evaluate communication-visibility passive-signoff
python -m soft_skills_lab evaluate communication-visibility clarify-and-plan
python -m soft_skills_lab evaluate communication-visibility execute-and-demonstrate
python -m soft_skills_lab compare communication-visibility
python -m soft_skills_lab performance-plan communication-visibility
python -m soft_skills_lab performance-evidence communication-visibility
python -m soft_skills_lab checkpoint communication-visibility --day 7
python -m soft_skills_lab checkpoint communication-visibility --day 14
python -m soft_skills_lab checkpoint communication-visibility --day 30
python -m soft_skills_lab evaluate vague-performance-plan clarify-observable-plan
python -m soft_skills_lab evaluate performance-factual-error correct-and-engage
python -m soft_skills_lab evaluate impossible-performance-expectation propose-controllable-measures
python -m soft_skills_lab evaluate changing-performance-scope clarify-new-scope
python -m soft_skills_lab evaluate performance-plan-capacity update-impact-and-plan
python -m soft_skills_lab evaluate performance-rating-disagreement review-criteria-and-continue
```

## What to observe

- Panic assumes an outcome the scenario does not establish and abandons clarification; it is not a character judgment.
- Denial incorrectly treats technical output as eliminating communication expectations.
- Automatic confession overgeneralizes and turns evidence into an identity statement.
- Debating every historical detail can prevent forward clarity, though material corrections still matter.
- Vague promises, passive acceptance, and message-count activity do not define success.
- Clarification separates supported examples from broad claims and defines behavior, measurement, actions, checkpoints, and completion.
- Execution records early risk communication, explicit handoff closure, feedback application, and the full evidence pattern.
- Vague, inaccurate, impossible, capacity-intersection, rating-disagreement, and moving-scope cases preserve the same evidence-based architecture.

Written clarity helps both parties reason about the same expectations. The plan history is deliberately small: concerns, clarified expectations, agreed actions, evidence, checkpoints, corrections, explicit updates, and outcome. It is not an HR information system or legal-document workflow. Outcomes (`COMPLETED`, `EXTENDED`, `UNSATISFACTORY`, `SUPERSEDED`) describe only satisfaction of authored behavioral criteria, never employment consequences.

## Reflection

1. Which concerns are directly supported by the scenario evidence?
2. Which statements would be overgeneralizations?
3. Why doesn't meeting the T8 delivery eliminate Morgan's visibility concern?
4. What does “communicate better” need to become before Alex can act on it?
5. Which behaviors can the plan measure using earlier models?
6. Why would “send five updates per day” be a weak metric?
7. What should Alex do if the plan contains a factual error?
8. What does a useful checkpoint examine?
9. Why isn't one quiet week evidence that risk communication improved?
10. Why shouldn't one missed handoff erase three weeks of improvement?
11. How should Alex handle a new concern introduced mid-plan?
12. What evidence would support successful completion of the plan?

## Limits

The laboratory authors scenarios rather than parsing arbitrary conversations. It does not evaluate personality, confidence, likability, emotion, motive, legality, organizational policy, plan fairness, or future employment decisions. It does not implement Chapter 18.
