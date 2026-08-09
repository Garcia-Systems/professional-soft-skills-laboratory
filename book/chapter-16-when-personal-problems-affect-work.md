# Chapter 16: When Personal Problems Affect Work

## Educational question

> How do you protect your privacy while still managing the professional effects of a difficult personal situation?

Personal difficulty is not itself professional failure. Failing to manage a known effect on professional responsibilities can become a professional problem. This laboratory evaluates only observable professional decisions after work impact exists. It does not judge whether a circumstance is serious, deserved, or legitimate; diagnose anything; or inspect private morality, health, family, or substance use.

## Learning objectives

The learner should be able to:

- distinguish private circumstance from professional impact;
- recognize when work impact crosses a visibility threshold;
- communicate impact without unnecessary disclosure;
- answer legitimate availability and capacity questions;
- request specific support and revise commitments explicitly;
- update dependencies and follow up when a revised plan changes;
- recognize when present capacity makes a high-risk task inappropriate;
- communicate urgent absence proportionally and maintain coworker boundaries;
- recognize recurring impact that needs a durable work plan; and
- recognize when a request may need a formal organizational process.

## Professional concept

> Your coworkers usually do not need the full story. They need the information necessary to manage work that depends on you.

A **personal circumstance** is the deliberately abstract cause. A **professional impact** is an observable effect on work. A **private detail** is an exact argument, diagnosis, family event, or history. **Relevant work information** describes capacity, availability, risk, remaining work, and dependencies. A **support request** asks for a concrete decision. An **accommodation request** may invoke a designated organizational process; it is not interchangeable with an ordinary schedule request. A **commitment revision** preserves the original expectation in history and proposes a new one. **Absence** describes availability. **Performance risk** describes threatened work. These concepts must not be collapsed.

> Privacy protects personal information. It does not erase professional dependencies.

> A useful disclosure describes the work effect and the needed decision more clearly than the private cause.

“I'm struggling” communicates a condition. “Can we move the review to T9?” communicates a decision request. Asking for help can be part of taking responsibility when it makes a commitment more realistic or prevents avoidable harm. A manager need not grant every request; the professional skill is making it decidable.

The model uses actor-declared or authored capacity states—not medical assessments: `FULL`, `REDUCED`, `UNAVAILABLE`, and `UNSAFE_FOR_HIGH_RISK_TASK`. A boundary may classify information as `PRIVATE`, `OPTIONAL_CONTEXT`, `WORK_RELEVANT`, or `REQUIRED_FOR_REQUEST`. The final category means only information needed to evaluate this authored request, never a legal rule.

Different requests need proportionate information. Leaving two hours early while covering a review may need very little context. Longer leave or a formal accommodation may require HR, a leave process, or another designated channel. Company policy and local law can affect those procedures. This laboratory models only the professional communication boundary and offers no employment-law conclusion.

## Engineering concept: a limited fault-isolation analogy

A system boundary can expose the state another component needs without exposing every internal implementation detail. Similarly, a professional boundary can expose availability, capacity, risk, a revised commitment, and required support without exposing the private circumstance. People are not components; the analogy is limited to information boundaries.

## Primary scenario

Alex owns verification integration at T8; Morgan manages the work and Jordan depends on the handoff. Work is on track at T0. An unspecified personal situation begins at T3. At T4 concentration is reduced and an internal checkpoint is missed. At T5 failure handling remains incomplete, T8 lacks strong supporting evidence, Jordan's dependency is exposed, and Morgan has not been told. The cause remains private; the professional threshold has nevertheless been crossed.

The laboratory compares hiding everything, unnecessary disclosure, a vague personal statement, explanation without plan, unsupported reassurance, disappearance, bounded professional disclosure, and an early smaller support request. It also demonstrates one-day availability, risky deployment reassignment, recurring impact, urgent absence, an intrusive peer question, a legitimate manager question, a formal-support boundary, and a revised commitment that changes again.

Explanation is not a recovery plan. Privacy is not invisibility. Professional transparency is not complete disclosure. Good early communication is good behavior but does not guarantee delivery. Repeated explanations do not replace a workable plan.

## Run the laboratory

```bash
python -m soft_skills_lab scenario personal-capacity
python -m soft_skills_lab evaluate personal-capacity hide-everything
python -m soft_skills_lab evaluate personal-capacity overshare
python -m soft_skills_lab evaluate personal-capacity vague-personal-problem
python -m soft_skills_lab evaluate personal-capacity explanation-without-plan
python -m soft_skills_lab evaluate personal-capacity unsupported-reassurance
python -m soft_skills_lab evaluate personal-capacity disappear
python -m soft_skills_lab evaluate personal-capacity bounded-professional-disclosure
python -m soft_skills_lab evaluate personal-capacity early-support-request
python -m soft_skills_lab compare personal-capacity
python -m soft_skills_lab boundary personal-capacity
python -m soft_skills_lab work-impact personal-capacity
python -m soft_skills_lab evaluate one-day-availability proactive-reschedule
python -m soft_skills_lab evaluate high-risk-capacity reassign-safely
python -m soft_skills_lab evaluate urgent-personal-absence minimal-handoff
python -m soft_skills_lab evaluate intrusive-peer-question maintain-boundary
python -m soft_skills_lab evaluate manager-capacity-question answer-operationally
python -m soft_skills_lab evaluate recurring-capacity-impact durable-plan
python -m soft_skills_lab evaluate revised-commitment-missed update-again
python -m soft_skills_lab evaluate formal-capacity-support use-formal-path
python -m soft_skills_lab personal-capacity-trust
```

## What to observe

- Hiding preserves details but hides material risk.
- Oversharing is not immoral; unnecessary details can obscure a request and create avoidable disclosure.
- “Personal problems” supplies context but no operational state.
- A true explanation still needs state, action, request, revision, and follow-up.
- “Definitely T8” contradicts the evidence and honest uncertainty.
- Disappearance is evaluated by availability and abandoned dependencies, not by judging its cause.
- Bounded disclosure names capacity, remaining work, risk, a concrete request, dependencies, and T6.
- Earlier small adjustments can sometimes prevent larger failure, but do not prove resolution.
- Urgent absence requires only what is reasonably feasible: brief notice, immediate risk, a feasible handoff, and later update.
- Current reduced capacity can justify stopping before a specified high-risk task.
- “It's personal” can answer an intrusive peer while still updating their handoff.
- That boundary cannot avoid Morgan's legitimate operational capacity question.
- Recurring effects call for a sustainable plan rather than repeated one-off explanations.
- If T9 later becomes unsafe, Alex must update again; revising a commitment does not guarantee its outcome.

Sometimes excellent boundary management is very simple: “I need to be unavailable tomorrow afternoon for a personal matter. Can we move the review to T4 morning? The API contract is already posted.”

## Reflection

1. At what point does Morgan need to know something is wrong?
2. Which details are professionally relevant at T5?
3. Which details can remain private?
4. Why is “I'm having personal problems” incomplete as a status update?
5. What makes a support request actionable?
6. Why can “I'll definitely finish” be harmful without supporting evidence?
7. What should Alex tell Jordan?
8. When should Alex stop performing a risky task?
9. How can Alex answer intrusive questions without becoming uncooperative?
10. What changes when impact becomes recurring rather than temporary?
11. Why does early communication not guarantee that the revised plan succeeds?
12. What should happen if requested support exceeds Morgan's authority?

The durable principle is: a personal difficulty and a professional responsibility are different things, but they can interact. You are allowed to keep private matters private. You remain responsible for making material work effects visible and manageable.
