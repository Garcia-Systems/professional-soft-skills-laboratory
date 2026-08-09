# Chapter 23 — Professional Judgment

## Educational question

> How do you decide what professional behavior fits when asking, acting, waiting, escalating, complying, or refusing could all be reasonable in different circumstances?

## Learning objectives

The learner should be able to:

- identify relevant facts and unknowns;
- assess potential impact and reversibility;
- identify decision ownership and distinguish delegated authority from escalation boundaries;
- evaluate the cost of waiting and whether investigation is worth the delay;
- act under uncertainty when risk requires it;
- use safe reversible defaults while avoiding irreversible action under material ambiguity;
- escalate proportionally;
- distinguish disagreement from refusal and refuse explicit safety, security, or integrity violations;
- recognize multiple defensible choices;
- evaluate decisions from what was known at the time; and
- distinguish outcome quality from judgment quality.

## Professional concept

> Professional judgment is not memorizing the “right” behavior. It is recognizing which responsibility matters most in the situation you actually have.

Good professional behavior is contextual. **Act**, **ask**, **inform**, **consult**, **escalate**, **wait**, **defer**, **refuse**, **say no**, **pause**, and **commit** are modes, not moral categories. Asking can be needless upward delegation. Independent action can cross an authority or safety boundary. Waiting can preserve safety or silently accept growing harm. Refusal can preserve an explicit boundary or improperly replace ordinary disagree-and-commit.

Judgment asks: What is known? What is at risk? Who owns the decision? What may I decide? How reversible is the action? What happens if I wait or act? Who needs to know? What evidence would change the choice?

> The more irreversible and harmful a decision could be, the more evidence and authority matter.

> The more costly delay becomes, the less attractive waiting for certainty may be.

> Good judgment often means choosing which risk you are willing to accept—not finding an option with no risk.

The laboratory represents those factors explicitly. It calculates no judgment score and does not pretend every context has one correct answer.

## Production timeout: the same action in different contexts

At T2, Alex finds a payment timeout of 30 seconds where documentation says 10. The value may be an undocumented incident change. There is no current incident, a change could affect in-flight requests, and a one-hour investigation is cheap. Alex may make routine corrections, but production changes require communication. **Investigate and inform** is strongest: inspect configuration/deployment history and incident notes, update Morgan concisely, and set a follow-up. Immediate change assumes that undocumented means wrong; emergency paging is disproportionate; ignoring hides state; waiting only for Morgan wastes available evidence.

At T3, worker saturation, rising queue depth, and payment degradation establish impact. Returning to 10 seconds is now a known reversible containment action. Alex should contain within authority, immediately inform/escalate through the incident path, monitor, and continue diagnosis. The same configuration action is weak at T2 and appropriate at T3 because evidence, risk, urgency, and delay cost changed.

## Competing principles in the other scenarios

- **Ask versus act:** a clear, local, reversible test fix in Alex's owned code should be fixed without asking Morgan. Asking is not always safer.
- **Ask versus escalate:** possible exposure of internal risk metadata has high potential harm. Contain and escalate before complete diagnosis; high risk lowers the certainty needed for escalation.
- **Help versus commitment:** give Jordan the likely-useful 15 minutes, return ownership, and protect Alex's high-priority commitment. Collaboration does not require takeover.
- **Manager authority:** ship Morgan's cosmetic tradeoff after raising evidence once. Do not ship a defect that violates the scenario's explicit unauthorized-data policy; state the risk, refuse, and route appropriately. Decision ownership operates inside higher-order constraints.
- **Low-value ambiguity:** choose visible, reversible label and filename defaults when behavior and security are explicit. Authorization ambiguity is material and must be resolved. A safe default is not a hidden material assumption.
- **Privacy and capacity:** report inability to deploy safely, protect the private cause, and request reassignment while continuing documentation.
- **Waiting under uncertainty:** before T5, make the reversible release choice, record assumptions, monitor, and define rollback. Inaction is a decision with consequences.
- **Experiment versus debate:** time-box safe prototypes and define deciding evidence rather than escalating an endless architecture discussion.
- **Irreversible deletion:** ambiguous requirements and uncertain backups require pause and verification.
- **Deadline versus validation:** preserve required validation, surface schedule risk, and request a scope/timing decision. Commitment is not an obligation to take an unsafe shortcut.
- **Professional no:** “Not in today's scope; preserve today's delivery, or add scheduling and move the date” exposes the decision rather than merely rejecting the stakeholder.
- **Refusal:** never claim required validation ran when it did not. This explicit integrity boundary differs from ordinary disagreement.
- **Proportional escalation:** executives are not the resolution path for a naming preference.
- **Missing authority:** identify and route to a legitimate owner rather than assuming authority.
- **Multiple valid answers:** for a reversible, low-impact implementation detail, acting by established convention and informing later or asking a quick clarification may both be defensible.

## Records, outcomes, hindsight, and trust

A `JudgmentRecord` preserves facts, uncertainty, choice, rationale, owner, expected consequence, review point, and later outcome. Review uses evidence available at decision time. A responsible reversible choice can lead to a bad outcome without proving bad judgment. A shortcut can succeed without becoming good judgment. Thus `bad outcome != proof of bad judgment`, and `good outcome != proof of good judgment`.

Observable trust evidence can include acting within authority, escalating material risk, using a reversible experiment, refusing a boundary violation, surfacing a tradeoff, changing a decision after new evidence, and documenting rationale. Negative evidence can include unnecessary escalation, ignored material risk, irreversible action under ambiguity, an unauthorized commitment, unsafe shortcut, or falsified validation. These are evidence events, not an aggregate judgment score.

This chapter composes earlier investigation, status/risk, uncertainty, decision ownership, manager thresholds, stakeholder tradeoffs, requirement ambiguity, incident containment, work-impact privacy, commitments, teamwork, writing, reputation, and leadership concepts. It does not create a separate opaque engine.

## Engineering concept: limited safety analogy

A reversible feature-flag or configuration change with observability and rollback may justify action under less certainty than permanent data deletion. Reversibility, blast radius, observability, rollback path, and authority alter the decision threshold. Transaction and deployment safety are useful limited analogies; people and professional responsibility are not software transactions.

## Run the laboratory

```bash
python -m soft_skills_lab scenario production-timeout
python -m soft_skills_lab evaluate production-timeout act-immediately
python -m soft_skills_lab evaluate production-timeout escalate-emergency
python -m soft_skills_lab evaluate production-timeout ignore
python -m soft_skills_lab evaluate production-timeout wait-indefinitely
python -m soft_skills_lab evaluate production-timeout investigate-and-inform
python -m soft_skills_lab compare production-timeout --at T2
python -m soft_skills_lab compare production-timeout --at T3
python -m soft_skills_lab judgment production-timeout --at T2
python -m soft_skills_lab judgment production-timeout --at T3
python -m soft_skills_lab judgment-options production-timeout --at T2
python -m soft_skills_lab judgment-record production-timeout
python -m soft_skills_lab evaluate owned-unit-test professional
python -m soft_skills_lab evaluate risk-metadata-exposure professional
python -m soft_skills_lab evaluate bounded-teammate-help professional
python -m soft_skills_lab evaluate manager-cosmetic-ship professional
python -m soft_skills_lab evaluate manager-unsafe-ship professional
python -m soft_skills_lab evaluate safe-default-requirement professional
python -m soft_skills_lab evaluate privacy-capacity-judgment professional
python -m soft_skills_lab evaluate release-window-uncertainty professional
```

```bash
python -m soft_skills_lab evaluate architecture-experiment professional
python -m soft_skills_lab evaluate historical-data-cleanup professional
python -m soft_skills_lab evaluate deadline-validation professional
python -m soft_skills_lab evaluate scheduled-export-scope professional
python -m soft_skills_lab evaluate falsify-validation professional
python -m soft_skills_lab evaluate naming-escalation professional
python -m soft_skills_lab evaluate unknown-decision-owner professional
python -m soft_skills_lab evaluate defensible-implementation professional
python -m soft_skills_lab evaluate reasonable-bad-outcome professional
python -m soft_skills_lab evaluate reckless-good-outcome professional
```

## What to observe

Observe acting too soon, over-escalation, invisible unresolved state, waiting too long, cheap investigation, changed judgment after changed risk, high-risk containment, bounded help, security refusal, ordinary disagree-and-commit, reversible experiment, irreversible action, safe defaults, scope tradeoffs, multiple passing responses, and hindsight bias. Criteria stay separate and deterministic.

## Reflection

1. Why is changing the timeout immediately weak judgment at T2?
2. What changes at T3?
3. Why is escalating at T2 different from escalating at T3?
4. How does reversibility affect the choice?
5. When is asking a manager unnecessary?
6. When is waiting itself risky?
7. Why should unauthorized-data exposure change the escalation threshold?
8. When should Alex comply with a manager's release decision?
9. When should Alex refuse?
10. How does a safe default differ from a hidden material assumption?
11. Why can two different choices both be professionally defensible?
12. How should a decision be evaluated when the outcome later turns out badly?
13. What evidence would justify changing the original decision?
14. Which earlier chapters contribute most directly to professional judgment?

## Boundary of this chapter

The model is deterministic and scenario-authored. It does not infer legal duties, diagnose people, parse arbitrary prose, calculate risk probabilities, or provide a universal taxonomy. It does not implement Chapter 24's end-to-end capstone.
