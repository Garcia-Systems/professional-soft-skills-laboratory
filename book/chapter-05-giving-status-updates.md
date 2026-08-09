# Chapter 5: Giving Status Updates

## Educational question

> How do you communicate the state of work so that other people do not have to discover it themselves?

A useful status update reduces uncertainty about progress, risk, ownership, and what happens next. It is not a diary of everything you did.

## Learning objectives

By the end of this chapter, you should be able to:

- distinguish activity from progress and status;
- identify **on track**, **at risk**, **blocked**, and **completed** states;
- communicate risk before failure;
- communicate dependency impact;
- distinguish forecasts from promises;
- identify true blockers;
- request action when a dependency needs escalation;
- tailor status detail to the audience;
- close communication loops; and
- establish useful follow-up expectations.

## Professional concept: let another person update their plan

> A strong status update allows another person to update their plan.

If the recipient finishes reading and still has to ask, “So are we still on schedule?”, the update probably failed at its primary purpose. The recipient generally needs enough information to understand where work stands, what materially changed, whether the commitment remains realistic, what is blocked or unknown, who needs to act, what happens next, and when confidence will improve.

> Surprises are sometimes unavoidable. Silent surprises often are not.

This does not mean every unforeseen event was predictable. The professional expectation begins when material information becomes known: make it visible while another person can still adapt.

### Activity, progress, and status

These three ideas are related but not interchangeable:

- **Activity** describes effort or events: “I checked logs, refactored the client, updated tests, and met Jordan.” It can be useful supporting detail.
- **Progress** describes a meaningful change in the work: “The request path works, but error handling is incomplete.”
- **Status** connects state to a commitment and a recipient's plan: “The request path works, but error handling is incomplete. Jordan cannot integrate yet. T6 is at risk; I am adding a fallback and will update at T5.”

Activity does not answer “Is it ready?” Progress may still omit impact and next action. Status supplies the information needed for a decision. More detail is not automatically more useful.

## Semantic states

The laboratory uses names rather than undefined colors:

- **ON_TRACK** — current evidence supports the commitment.
- **AT_RISK** — material uncertainty could affect the commitment, although useful work can continue.
- **BLOCKED** — progress on the relevant work cannot continue without an external action, decision, permission, or dependency.
- **COMPLETED** — the stated commitment is satisfied.

A problem is something difficult. A risk may affect a commitment. A blocker stops progress on the relevant work. Undocumented vendor behavior can be a problem and a risk while Alex continues implementing a fallback; it is not therefore a blocker. A missing credential that prevents validation can be a blocker even if Alex can perform unrelated documentation work.

## The integration-delivery scenario

Alex, a backend developer, expects to provide a usable member-verification endpoint by T6. Jordan, a frontend developer, plans integration at T6. Morgan is the engineering manager.

- **T0:** work begins.
- **T2:** request flow and success response work.
- **T3:** undocumented provider error structures appear. Success works, failure normalization is incomplete, and Alex can keep coding. T6 is now **at risk**, not blocked.
- **T4:** two of three observed errors are normalized; one remains unexplained.
- **T5:** vendor support remains unavailable. The team must choose known-case delivery, a safe unknown-error fallback, or waiting.

The six authored paths separate important behaviors:

1. **no-update** — silence because T6 has not passed hides early risk and leaves Jordan planning from stale assumptions.
2. **activity-dump** — accurate effort is reported without readiness or commitment state.
3. **false-green** — “Everything is on track” contradicts material evidence and turns optimism into unsupported certainty.
4. **vague-risk** — “Might affect the deadline” is better than silence, but omits state, impact, next action, and follow-up. The evaluator treats this as partial risk communication.
5. **over-detailed** — payloads, stack traces, fixtures, and test internals obscure the state and decision, connecting to Chapter 4's audience principle.
6. **decision-useful** — completed and remaining state, T6 risk, Jordan's dependency, continued fallback work, conditional forecast, T5 update, and possible decision are explicit.

The wording is illustrative. Evaluation uses authored structured semantics and never tries to infer behavior by parsing arbitrary prose.

## Forecast versus promise

> An estimate is a forecast based on current evidence, not a guarantee.

“Based on the success path and two known error forms, T6 still looks achievable **if** the fallback safely handles the third form; I will know more at T5” names a target, basis, condition, and revision point. “It will definitely be done at T6” is a promise that the available evidence cannot support. The model uses no artificial confidence percentage. A forecast should be revised when its basis or material conditions change.

## Audience and one source of truth

The underlying work state does not change by recipient. The selection and level of detail do:

- **Jordan, dependent teammate:** integration readiness, stable contract, possible change, whether T6 remains safe, parallel work, and next update.
- **Morgan, engineering manager:** commitment state, completed scope, appropriately summarized cause and risk, dependency impact, decision needed, and next update.
- **Business stakeholder:** schedule, user-facing scope, decision required, and when confidence will improve.

The laboratory's audience views share the same structured `StatusUpdate` and fact identifiers. This prevents tailored explanations from becoming inconsistent facts.

## Blocker updates and escalation

In the smaller credential scenario, Alex requested a production-like test credential from security at T1. At T3 it has not arrived, and validation cannot continue. Compare:

- **silent-blocking:** Alex waits; nobody can manage the dependency.
- **passive-status:** “Still waiting on credentials” exposes a symptom but not impact, ownership, or requested action.
- **actionable-escalation:** validation is explicitly blocked; the T1 request and security ownership are visible; T5 confidence is affected; Morgan is asked to escalate; documentation can continue, but validation cannot.

> A blocker update should make ownership and impact visible.

Escalation is not blame. It routes a dependency to someone able to act. Hiding a true blocker and calling continuing work “blocked” are both misleading.

## Completion and loop closure

Completion changes another person's plan only when they learn about it. If Alex finishes but never tells Jordan, the technical result exists while the professional loop remains open. A proportionate completion update may be one line:

> Verification endpoint is ready for integration. The contract is unchanged, tests pass, and the unknown-error fallback is included.

This reuses Chapter 1's loop-closure evidence. Not every update needs a large template: “Done — deployed successfully and tests passed” can be sufficient when risk and dependency complexity are low.

## A flexible anatomy

For higher-risk work, consider:

```text
State
Risk
Impact
Next action
Needed action
Next update
```

This is a checklist for judgment, not a rigid form. Add completed and remaining scope, unknowns, a forecast basis, or a decision point when they help the recipient plan. Remove details that do not.

## Engineering concept: observability

Thousands of log events do not automatically provide useful operational status. Operators need meaningful state, relevant alerts, dependency health, impact, and an action. Raw event volume without synthesis can make diagnosis harder.

Professional communication has the same practical constraint. A list of commits, meetings, tests, and debugging steps resembles a large log stream. Those events can support a status update, but they do not replace the current state, commitment risk, dependency impact, and next action. The analogy is about selecting actionable signals, not treating people as machines.

## Run the laboratory

From the repository root after installation (or with `PYTHONPATH=src` in a source checkout), run:

```bash
python -m soft_skills_lab scenario integration-delivery
python -m soft_skills_lab evaluate integration-delivery no-update
python -m soft_skills_lab evaluate integration-delivery activity-dump
python -m soft_skills_lab evaluate integration-delivery false-green
python -m soft_skills_lab evaluate integration-delivery vague-risk
python -m soft_skills_lab evaluate integration-delivery over-detailed
python -m soft_skills_lab evaluate integration-delivery decision-useful
python -m soft_skills_lab compare integration-delivery
python -m soft_skills_lab status integration-delivery decision-useful
```

Inspect audience views sourced from the same facts:

```bash
python -m soft_skills_lab status integration-delivery decision-useful --audience jordan
python -m soft_skills_lab status integration-delivery decision-useful --audience morgan
python -m soft_skills_lab status integration-delivery decision-useful --audience business
```

Exercise a true blocker and completion loop closure:

```bash
python -m soft_skills_lab scenario credential-blocker
python -m soft_skills_lab evaluate credential-blocker silent-blocking
python -m soft_skills_lab evaluate credential-blocker passive-status
python -m soft_skills_lab evaluate credential-blocker actionable-escalation
python -m soft_skills_lab status credential-blocker actionable-escalation
python -m soft_skills_lab scenario verification-completion
python -m soft_skills_lab evaluate verification-completion silent-completion
python -m soft_skills_lab evaluate verification-completion closed-loop
python -m soft_skills_lab status verification-completion closed-loop
```

## What to observe

- Silence can fail risk visibility before a deadline is missed.
- Activity can be accurate without establishing work state.
- Unsupported optimism can be less trustworthy than a conditional forecast.
- Vague risk is useful evidence but may still force recipients to chase details.
- Excessive technical detail can hide the answer, as Chapter 4 predicts.
- Decision-useful status lets Jordan and Morgan update their plans.
- Teammates and managers need different views of the same facts.
- A true blocker names stopped work, external owner, impact, and action.
- Completed dependent work still needs explicit loop closure.

The evaluator keeps these dimensions separate rather than producing a personality or professionalism score. Existing criteria for risk visibility, dependency acknowledgement, uncertainty, audience relevance, decision support, follow-up, and loop closure inform the chapter; the status evaluator adds explicit state, material progress, dependency impact, blocker accuracy, forecast basis, and needed action.

## Reflection

1. When did Alex first have evidence that T6 was at risk?
2. Why was the work not yet blocked at T3?
3. What does Jordan need that Morgan may not?
4. Why is “everything is on track” professionally dangerous without supporting evidence?
5. What is missing from “might be late”?
6. When does a forecast need revision?
7. When should a blocker be escalated?
8. What information allows another person to update their own plan?
9. When is a one-line status update sufficient?
10. Why does completion sometimes require explicit communication?

## Scope and limits

This chapter uses small deterministic scenarios, explicit metadata, and simulated time. It does not parse free-form messages, predict delivery probability, connect to project-management systems, or prescribe one universal update format. It does not implement Chapter 6's treatment of saying “I don't know” professionally; unknowns here are reused only as status inputs.
