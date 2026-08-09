# Professional Soft Skills Laboratory

An executable textbook for practicing professional reliability and communication. Its central question is: **how can a person communicate, collaborate, handle conflict, receive feedback, take responsibility, and build trust in difficult workplace situations?**

The laboratory treats soft skills as observable decisions and behaviors—not personality traits. A chapter combines an explanation with a deterministic scenario that can be inspected and evaluated. Results name each criterion, pass or fail it, and show the relevant evidence; they do not hide judgment inside a charisma or confidence score.

## Project philosophy

- Separate known facts from assumptions before drawing conclusions.
- Evaluate ownership, timely risk communication, next actions, follow-through, appropriate escalation, blame avoidance, and boundaries explicitly.
- Preserve the evidence behind professional trust rather than treating trust as likability.
- Make each simplified model small enough to read, question, change, and retry.
- Treat professional disagreement as compatible with responsibility and respect. Professionalism is not submissiveness.

## Install and run

Python 3.13 or newer is required. The runtime uses only the standard library; pytest is a development dependency.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest
```

Inspect and evaluate Chapter 0:

```bash
python -m soft_skills_lab scenario production-incident
python -m soft_skills_lab evaluate production-incident defensive
python -m soft_skills_lab evaluate production-incident blame-shifting
python -m soft_skills_lab evaluate production-incident over-accepting
python -m soft_skills_lab evaluate production-incident professional
python -m soft_skills_lab trust-demo
```

Explore Chapter 1's commitment paths:

```bash
python -m soft_skills_lab scenario commitment-at-risk
python -m soft_skills_lab evaluate commitment-at-risk silent
python -m soft_skills_lab evaluate commitment-at-risk vague-warning
python -m soft_skills_lab evaluate commitment-at-risk premature-promise
python -m soft_skills_lab evaluate commitment-at-risk professional-update
python -m soft_skills_lab compare commitment-at-risk
```

Practice Chapter 2's deterministic listening scenarios:

```bash
python -m soft_skills_lab scenario demo-stability
python -m soft_skills_lab evaluate demo-stability premature-solution
python -m soft_skills_lab evaluate demo-stability defensive-interpretation
python -m soft_skills_lab evaluate demo-stability passive-acknowledgment
python -m soft_skills_lab evaluate demo-stability listen-then-clarify
python -m soft_skills_lab compare demo-stability
python -m soft_skills_lab interpret demo-stability
python -m soft_skills_lab scenario teammate-contract
python -m soft_skills_lab scenario stakeholder-search
```

Explore Chapter 3's decision-relevant questions and deterministic answers:

```bash
python -m soft_skills_lab scenario report-export
python -m soft_skills_lab unknowns report-export
python -m soft_skills_lab evaluate report-export no-questions
python -m soft_skills_lab evaluate report-export question-dump
python -m soft_skills_lab evaluate report-export ask-before-looking
python -m soft_skills_lab evaluate report-export leading-question
python -m soft_skills_lab evaluate report-export focused-questions
python -m soft_skills_lab compare report-export
python -m soft_skills_lab answer report-export
python -m soft_skills_lab scenario deployment-failure
python -m soft_skills_lab evaluate deployment-failure professional-question
python -m soft_skills_lab evaluate authorization-risk immediate-escalation
```

Explore Chapter 4's truthful, decision-relevant explanations:

```bash
python -m soft_skills_lab scenario payment-timeout
python -m soft_skills_lab evaluate payment-timeout jargon-dump
python -m soft_skills_lab evaluate payment-timeout decision-oriented
python -m soft_skills_lab compare payment-timeout
python -m soft_skills_lab explain payment-timeout --audience engineer
python -m soft_skills_lab explain payment-timeout --audience product-manager
python -m soft_skills_lab explain payment-timeout --audience business-operations
python -m soft_skills_lab layers payment-timeout
python -m soft_skills_lab scenario database-migration
python -m soft_skills_lab evaluate database-migration decision-oriented
```

Practice Chapter 5's decision-useful status updates:

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
python -m soft_skills_lab status integration-delivery decision-useful --audience jordan
python -m soft_skills_lab status integration-delivery decision-useful --audience morgan
python -m soft_skills_lab status integration-delivery decision-useful --audience business
python -m soft_skills_lab scenario credential-blocker
python -m soft_skills_lab evaluate credential-blocker actionable-escalation
python -m soft_skills_lab status credential-blocker actionable-escalation
python -m soft_skills_lab evaluate verification-completion closed-loop
```

Practice Chapter 6's explicit, bounded uncertainty:

```bash
python -m soft_skills_lab scenario profile-update-failure
python -m soft_skills_lab evaluate profile-update-failure bluff
python -m soft_skills_lab evaluate profile-update-failure defensive-certainty
python -m soft_skills_lab evaluate profile-update-failure empty-unknown
python -m soft_skills_lab evaluate profile-update-failure speculative-answer
python -m soft_skills_lab evaluate profile-update-failure investigation-dump
python -m soft_skills_lab evaluate profile-update-failure bounded-uncertainty
python -m soft_skills_lab compare profile-update-failure
python -m soft_skills_lab evidence profile-update-failure
python -m soft_skills_lab uncertainty profile-update-failure
python -m soft_skills_lab evaluate profile-fix-estimate learning-point
python -m soft_skills_lab evaluate judgment-under-pressure bounded-judgment
python -m soft_skills_lab evaluate migration-safety-unknown inspect-first
python -m soft_skills_lab evaluate customer-payment-verification customer-safe
```

Practice Chapter 7's evidence-based feedback reception:

```bash
python -m soft_skills_lab scenario project-visibility
python -m soft_skills_lab evaluate project-visibility immediate-defense
python -m soft_skills_lab evaluate project-visibility blame-shift
python -m soft_skills_lab evaluate project-visibility automatic-agreement
python -m soft_skills_lab evaluate project-visibility explanation-as-defense
python -m soft_skills_lab evaluate project-visibility silent-compliance
python -m soft_skills_lab evaluate project-visibility understand-and-respond
python -m soft_skills_lab compare project-visibility
python -m soft_skills_lab feedback project-visibility
python -m soft_skills_lab feedback vague-manager-feedback
python -m soft_skills_lab evaluate vague-manager-feedback clarify-without-capitulating
python -m soft_skills_lab evaluate adapter-review evidence-based-disagreement
python -m soft_skills_lab evaluate feedback-follow-up demonstrated-change
python -m soft_skills_lab improvement feedback-follow-up
```

Practice Chapter 8's evidence-based responsibility boundaries and follow-through:

```bash
python -m soft_skills_lab scenario skipped-validation
python -m soft_skills_lab evaluate skipped-validation deny
python -m soft_skills_lab evaluate skipped-validation blame-process
python -m soft_skills_lab evaluate skipped-validation excuse-pressure
python -m soft_skills_lab evaluate skipped-validation over-own
python -m soft_skills_lab evaluate skipped-validation empty-apology
python -m soft_skills_lab evaluate skipped-validation explanation-without-ownership
python -m soft_skills_lab evaluate skipped-validation accurate-ownership
python -m soft_skills_lab compare skipped-validation
python -m soft_skills_lab responsibility skipped-validation
python -m soft_skills_lab evaluate missed-handoff own-and-recover
python -m soft_skills_lab evaluate shared-responsibility bounded-ownership
python -m soft_skills_lab evaluate unavoidable-outcome evidence-bounded
python -m soft_skills_lab learning responsibility-follow-up
```

Practice Chapter 9's evidence-based disagreement and decision ownership:

```bash
python -m soft_skills_lab scenario adapter-boundary
python -m soft_skills_lab evaluate adapter-boundary evidence-based-disagreement
python -m soft_skills_lab evaluate adapter-boundary disagree-and-commit
python -m soft_skills_lab compare adapter-boundary
python -m soft_skills_lab decision adapter-boundary
python -m soft_skills_lab evaluate reporting-deadline scope-reduction
python -m soft_skills_lab evaluate code-review-preference name-preference
python -m soft_skills_lab evaluate manager-correct update-position
python -m soft_skills_lab evaluate cache-strategy prototype
python -m soft_skills_lab evaluate sensitive-logging escalate
python -m soft_skills_lab disagreement-trust
```

Practice Chapter 10's observable conflict de-escalation and repair:

```bash
python -m soft_skills_lab scenario release-validation
python -m soft_skills_lab evaluate release-validation counterattack
python -m soft_skills_lab evaluate release-validation motive-attack
python -m soft_skills_lab evaluate release-validation sarcasm
python -m soft_skills_lab evaluate release-validation capitulation
python -m soft_skills_lab evaluate release-validation repeat-louder
python -m soft_skills_lab evaluate release-validation de-escalate-and-refocus
python -m soft_skills_lab evaluate release-validation pause-and-resume
python -m soft_skills_lab compare release-validation
python -m soft_skills_lab conflict release-validation
python -m soft_skills_lab evaluate code-review-conflict restore-technical-question
python -m soft_skills_lab evaluate release-validation avoid-indefinitely
python -m soft_skills_lab evaluate manager-tradeoff-conflict confirm-and-proceed
python -m soft_skills_lab evaluate manager-material-risk document-and-escalate
python -m soft_skills_lab evaluate public-deadline-conflict change-venue
```

Practice Chapter 11's managed autonomy and contextual visibility thresholds:

```bash
python -m soft_skills_lab scenario project-autonomy
python -m soft_skills_lab compare project-autonomy
python -m soft_skills_lab evaluate project-autonomy managed-autonomy
python -m soft_skills_lab evaluate project-autonomy visibility-with-recommendation
python -m soft_skills_lab manager-agreement project-autonomy
python -m soft_skills_lab visibility project-autonomy
python -m soft_skills_lab evaluate deployment-ownership professional-ownership
python -m soft_skills_lab evaluate vague-manager-direction clarify-outcome
python -m soft_skills_lab evaluate changing-autonomy expanded-autonomy
python -m soft_skills_lab evaluate micromanagement-clarification clarify-boundaries
python -m soft_skills_lab evaluate manager-unavailable use-boundaries
python -m soft_skills_lab evaluate manager-one-on-one prepared-topics
python -m soft_skills_lab manager-trust
```

Practice Chapter 12's explicit peer ownership, handoffs, review, and bounded help:

```bash
python -m soft_skills_lab scenario verification-integration
python -m soft_skills_lab evaluate verification-integration silent-handoff
python -m soft_skills_lab evaluate verification-integration throw-over-wall
python -m soft_skills_lab evaluate verification-integration over-help
python -m soft_skills_lab evaluate verification-integration wait-for-them-to-ask
python -m soft_skills_lab evaluate verification-integration dependency-blame
python -m soft_skills_lab evaluate verification-integration coordinated-handoff
python -m soft_skills_lab evaluate verification-integration coordinated-help
python -m soft_skills_lab compare verification-integration
python -m soft_skills_lab handoff verification-integration
python -m soft_skills_lab ownership verification-integration
python -m soft_skills_lab evaluate peer-code-review useful-review
python -m soft_skills_lab evaluate teammate-context targeted-context
python -m soft_skills_lab evaluate bounded-peer-help bounded-help
python -m soft_skills_lab evaluate shared-peer-task assign-owner
python -m soft_skills_lab evaluate missed-peer-commitment peer-check
python -m soft_skills_lab evaluate team-contribution accurate-credit
python -m soft_skills_lab collaboration-trust
```

Practice Chapter 13's outcome clarification, stakeholder tradeoffs, scope decisions, and recommendations:

```bash
python -m soft_skills_lab scenario reporting-export
python -m soft_skills_lab stakeholder-request reporting-export
python -m soft_skills_lab tradeoffs reporting-export
python -m soft_skills_lab evaluate reporting-export literal-yes
python -m soft_skills_lab evaluate reporting-export technical-no
python -m soft_skills_lab evaluate reporting-export jargon-rejection
python -m soft_skills_lab evaluate reporting-export requirement-interrogation
python -m soft_skills_lab evaluate reporting-export silent-scope-reduction
python -m soft_skills_lab evaluate reporting-export outcome-first-tradeoff
python -m soft_skills_lab evaluate reporting-export recommendation-with-decision
python -m soft_skills_lab compare reporting-export
python -m soft_skills_lab evaluate stakeholder-search-performance clarify-experience
python -m soft_skills_lab evaluate urgent-bulk-upload controlled-option
python -m soft_skills_lab scope-change export-scope-change
python -m soft_skills_lab evaluate export-security-constraint safe-alternative
python -m soft_skills_lab evaluate xlsx-required update-recommendation
python -m soft_skills_lab evaluate impossible-export-constraints surface-conflict
python -m soft_skills_lab stakeholder-trust
```

Practice Chapter 14's focused ambiguity reduction and explicit acceptance contracts:

```bash
python -m soft_skills_lab scenario transaction-export
python -m soft_skills_lab evaluate transaction-export assume-everything
python -m soft_skills_lab evaluate transaction-export block-on-everything
python -m soft_skills_lab evaluate transaction-export resolve-decision-relevant-ambiguity
python -m soft_skills_lab evaluate transaction-export progressive-clarification
python -m soft_skills_lab compare transaction-export
python -m soft_skills_lab ambiguities transaction-export
python -m soft_skills_lab contradictions transaction-export
python -m soft_skills_lab acceptance transaction-export
python -m soft_skills_lab requirement-history transaction-export
python -m soft_skills_lab ambiguities verification-notification
python -m soft_skills_lab scenario contradictory-export-stakeholders
python -m soft_skills_lab scenario verification-retry
python -m soft_skills_lab scenario download-button-default
python -m soft_skills_lab scenario pending-requirement-change
```


Practice Chapter 15's accurate, coordinated incident response:

```bash
python -m soft_skills_lab scenario payment-authorization
python -m soft_skills_lab compare payment-authorization
python -m soft_skills_lab incident payment-authorization
python -m soft_skills_lab recovery payment-authorization
python -m soft_skills_lab incident-audience payment-authorization --audience customer-support
python -m soft_skills_lab incident-review payment-authorization
python -m soft_skills_lab incident data-exposure-risk
python -m soft_skills_lab incident payment-alert-false-alarm
python -m soft_skills_lab incident-trust
```

Practice Chapter 16's privacy-preserving work-impact communication:

```bash
python -m soft_skills_lab scenario personal-capacity
python -m soft_skills_lab evaluate personal-capacity bounded-professional-disclosure
python -m soft_skills_lab compare personal-capacity
python -m soft_skills_lab boundary personal-capacity
python -m soft_skills_lab work-impact personal-capacity
python -m soft_skills_lab evaluate one-day-availability proactive-reschedule
python -m soft_skills_lab evaluate high-risk-capacity reassign-safely
python -m soft_skills_lab evaluate urgent-personal-absence minimal-handoff
python -m soft_skills_lab evaluate recurring-capacity-impact durable-plan
python -m soft_skills_lab personal-capacity-trust
```

Practice Chapter 17's evidence-based performance planning:

```bash
python -m soft_skills_lab scenario communication-visibility
python -m soft_skills_lab compare communication-visibility
python -m soft_skills_lab evaluate communication-visibility clarify-and-plan
python -m soft_skills_lab evaluate communication-visibility execute-and-demonstrate
python -m soft_skills_lab performance-plan communication-visibility
python -m soft_skills_lab performance-evidence communication-visibility
python -m soft_skills_lab checkpoint communication-visibility --day 14
python -m soft_skills_lab evaluate vague-performance-plan clarify-observable-plan
python -m soft_skills_lab evaluate performance-factual-error correct-and-engage
python -m soft_skills_lab evaluate impossible-performance-expectation propose-controllable-measures
python -m soft_skills_lab evaluate changing-performance-scope clarify-new-scope
```

Practice Chapter 18's evidence-based interview communication:

```bash
python -m soft_skills_lab scenario interview-mistake
python -m soft_skills_lab compare interview-mistake
python -m soft_skills_lab evaluate interview-mistake evidence-based-mistake
python -m soft_skills_lab evaluate interview-mistake concise-evidence-based
python -m soft_skills_lab interview-question mistake
python -m soft_skills_lab interview-answer mistake evidence-based-mistake
python -m soft_skills_lab interview-followup mistake why-skip-validation
python -m soft_skills_lab evaluate interview-disagreement collaborative-decision
python -m soft_skills_lab evaluate interview-conflict de-escalate-and-resolve
python -m soft_skills_lab evaluate interview-failure responsible-failure
python -m soft_skills_lab evaluate interview-weakness evidence-based-weakness
python -m soft_skills_lab evaluate interview-layoff concise-forward
python -m soft_skills_lab evaluate interview-resume-gap bounded-gap
python -m soft_skills_lab evaluate interview-technical-unknown bounded-reasoning
python -m soft_skills_lab evaluate interview-estimation conditional-estimate
python -m soft_skills_lab evaluate interview-imperfect-outcome partial-success
python -m soft_skills_lab story-selection influence
```

Practice Chapter 19's purpose-driven meeting presence:

```bash
python -m soft_skills_lab scenario release-readiness
python -m soft_skills_lab compare release-readiness
python -m soft_skills_lab evaluate release-readiness useful-contribution
python -m soft_skills_lab evaluate release-readiness useful-question
python -m soft_skills_lab evaluate release-readiness summarize-and-close
python -m soft_skills_lab meeting release-readiness
python -m soft_skills_lab meeting-flow release-readiness
python -m soft_skills_lab meeting-outcome release-readiness
python -m soft_skills_lab evaluate daily-standup useful-standup
python -m soft_skills_lab evaluate design-review purposeful-detail
python -m soft_skills_lab evaluate meeting-interruption clarify-after-listening
python -m soft_skills_lab evaluate deployment-success-update use-async
```

Practice Chapter 20's durable, decision-useful professional writing:

```bash
python -m soft_skills_lab scenario deployment-risk
python -m soft_skills_lab evaluate deployment-risk context-free
python -m soft_skills_lab evaluate deployment-risk activity-only
python -m soft_skills_lab evaluate deployment-risk alarm-without-evidence
python -m soft_skills_lab evaluate deployment-risk false-reassurance
python -m soft_skills_lab evaluate deployment-risk wall-of-text
python -m soft_skills_lab evaluate deployment-risk ambiguous-request
python -m soft_skills_lab evaluate deployment-risk decision-useful
python -m soft_skills_lab evaluate deployment-risk concise-decision-useful
python -m soft_skills_lab compare deployment-risk
python -m soft_skills_lab written-message deployment-risk decision-useful
python -m soft_skills_lab written-artifact release-readiness-recap
python -m soft_skills_lab written-artifact verification-pr-review
python -m soft_skills_lab written-artifact verification-ticket
python -m soft_skills_lab written-artifact api-handoff
python -m soft_skills_lab written-artifact adapter-disagreement
python -m soft_skills_lab written-artifact security-escalation
python -m soft_skills_lab written-artifact material-correction
```

Practice Chapter 21's domain-specific evidence histories:

```bash
python -m soft_skills_lab scenario six-week-project
python -m soft_skills_lab trust-history six-week-project
python -m soft_skills_lab trust-explain six-week-project commitment-reliability
python -m soft_skills_lab trust-explain six-week-project handoff-reliability
python -m soft_skills_lab trust-view six-week-project --observer Morgan
python -m soft_skills_lab trust-view six-week-project --observer Jordan
python -m soft_skills_lab trust-view six-week-project --observer Dana
python -m soft_skills_lab scenario trust-degradation
python -m soft_skills_lab scenario trust-rebuilding
```

Practice Chapter 22's coordination without authority:

```bash
python -m soft_skills_lab scenario verification-launch
python -m soft_skills_lab compare verification-launch
python -m soft_skills_lab leadership verification-launch
python -m soft_skills_lab coordination-map verification-launch
python -m soft_skills_lab evaluate verification-launch coordinate-without-authority
python -m soft_skills_lab evaluate verification-launch facilitate-and-recommend
python -m soft_skills_lab evaluate cross-team-api negotiate-checkpoint
python -m soft_skills_lab evaluate leader-wrong update-recommendation
```

An installed `soft-skills-lab` entry point provides the same commands. The scenario catalog contains immutable domain values. Responses record structured behavioral evidence, and the evaluator applies explicit predicates to those fields rather than searching message text. This is intentionally a teaching model, not a natural-language judge.

## Volume I: Professional Reliability and Communication

0. **The Executable Professional** (implemented)
1. **Professionalism as Observable Behavior** (implemented)
2. **Listening Before Responding** (implemented)
3. **Asking Good Questions** (implemented)
4. **Explaining Technical Ideas Simply** (implemented)
5. **Giving Status Updates** (implemented)
6. **Saying “I Don’t Know” Professionally** (implemented)
7. **Receiving Feedback Without Defensiveness** (implemented)
8. **Taking Responsibility** (implemented)
9. **Disagreeing Professionally** (implemented)
10. **Conflict and De-escalation** (implemented)
11. **Working With Managers** (implemented)
12. **Working With Teammates** (implemented)
13. **Working With Business Stakeholders** (implemented)
14. **Handling Ambiguous Requirements** (implemented)
15. **Handling Mistakes and Incidents** (implemented)
16. **When Personal Problems Affect Work** (implemented)
17. **Performance Feedback and PIPs** (implemented)
18. **Interview Communication** (implemented)
19. **Meetings and Presence** (implemented)
20. **Written Professional Communication** (implemented)
21. **Trust and Reputation** (implemented)
22. **Leadership Without Authority** (implemented)
23. Professional Judgment
24. End-to-End Workplace Simulation

Later chapters are a roadmap, not yet implemented.

## Limits and responsible use

This laboratory is **not a psychological assessment**, does not diagnose personality, and does not evaluate personal worth. It does not claim there is one universally correct response to every workplace situation. Culture, power, urgency, safety, law, and missing context can change an appropriate response. The exercises deliberately model simplified, deterministic situations for practice and evaluate only stated professional behaviors. They are prompts for judgment and reflection, not replacements for organizational policy, expert help, or human context.
