# Chapter 11 — Working With Managers

## Educational question

> How do you give a manager enough visibility to trust your work without requiring them to manage every detail?

## Learning objectives

The learner should be able to:

- distinguish autonomy from silence and visibility from permission-seeking;
- identify delegated decision boundaries and manager visibility thresholds;
- handle routine work independently while communicating material risk;
- consult before crossing shared decision boundaries and escalate true blockers;
- provide recommendations when seeking decisions;
- clarify vague management expectations and adapt to explicit changes;
- prepare useful manager conversations; and
- explain how repeated behavior can support professional trust and autonomy.

## Professional concept

> A manager should be able to trust two things at the same time: that you will handle ordinary work without unnecessary supervision, and that important problems will not remain hidden.

Professional autonomy means owning execution while making important state, risk, decisions, and dependencies visible. A manager should not have to discover material problems by accident. Keeping a manager informed does not mean asking permission for every routine decision.

> Independence is not measured by how rarely you talk to your manager. It is measured partly by whether you can distinguish what you should own, what they should know, and what requires a decision beyond your authority.

These distinctions matter:

- **Autonomy** is action within delegated ownership; **silence** is absence of visibility.
- **Visibility** supplies decision-relevant state; **permission-seeking** delegates a choice upward.
- **Delegation** establishes ownership; **escalation** surfaces a crossed risk or authority boundary.
- **Manager support** can remove a dependency or make a decision. It is not failure of autonomy.
- **Micromanagement** is not inferred from a person's character. The laboratory models observable approval latency, duplicate effort, and unclear ownership, then invites clarification of the agreement.

Alex may change a private helper without asking. A public API contract used by Jordan crosses a consultation boundary. Asking Morgan for help at that boundary is compatible with autonomy. Manager authority also does not require Alex to suppress evidence-based disagreement: Chapter 9's decision ownership and Chapter 10's serious-risk boundary still apply.

## The working agreement

At kickoff Morgan tells Alex:

> You own the implementation. I don't need every technical detail, but tell me early if the T8 delivery is at risk, if another team is blocking you, or if you need to change the API contract Jordan is integrating against.

The immutable `WorkingAgreement` records participants, responsibilities, contextual `ManagerExpectation` values, cadence, dependencies, and explicit agreement evidence. Its four thresholds are not universal rules:

| Event | Threshold | Expected judgment |
|---|---|---|
| Internal refactor | `ROUTINE` | Act independently |
| Safe vendor normalization | `ROUTINE` | Act independently |
| Material T8 risk | `INFORM` | Update Morgan; permission is not required |
| Jordan's API contract may change | `CONSULT` | Discuss before acting |
| Vendor outage prevents validation | `ESCALATE` | Promptly surface blocker and impact |

An agreement may be explicitly superseded. In the changing-autonomy scenario, daily updates become risk- and decision-based updates after a history of reliable work. Reliability can support expanded autonomy; this is not a claim that individual behavior is the only cause. Team, organizational, regulatory, and manager context also matter.

## Engineering concept: alerting thresholds

A system that alerts on every normal event creates noise. A system that never alerts until total failure creates dangerous silence. Useful observability distinguishes normal operation, warning, and intervention required. Similarly, useful manager visibility distinguishes routine action, information, consultation, and escalation. This is only an analogy: people and working agreements are not monitoring systems.

## Run the laboratory

```bash
python -m soft_skills_lab scenario project-autonomy
python -m soft_skills_lab evaluate project-autonomy permission-for-everything
python -m soft_skills_lab evaluate project-autonomy silent-autonomy
python -m soft_skills_lab evaluate project-autonomy status-flood
python -m soft_skills_lab evaluate project-autonomy late-escalation
python -m soft_skills_lab evaluate project-autonomy escalate-without-investigation
python -m soft_skills_lab evaluate project-autonomy managed-autonomy
python -m soft_skills_lab evaluate project-autonomy visibility-with-recommendation
python -m soft_skills_lab compare project-autonomy
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

## What to observe

1. **Permission for everything** shifts routine ownership to Morgan; asking useful questions is not the problem.
2. **Silent autonomy** hides risk, contract impact, and the blocker.
3. **Status flooding** is accurate but buries the signal Chapters 4–5 teach us to select.
4. **Late escalation** continues solo after the agreed blocker threshold. Trying first can be good; continuing after the threshold can be poor judgment.
5. **Premature escalation** calls the safe T3 normalization a blocker without inspecting it, contrary to Chapter 3.
6. **Managed autonomy** owns T2–T3, informs at T4, consults at T5, escalates at T6, continues possible work, and sets follow-up.
7. **Recommendation-based escalation** makes the same state visible and recommends preserving Jordan's contract. Escalation is not handing Morgan an empty problem.
8. **Ownership with recommendation** investigates facts and uncertainty, recommends action, preserves Morgan's production authority, and follows up. “Own this” does not grant every authority.
9. **Vague direction** becomes measurable only after evidence inspection and focused clarification.
10. **Changing expectations** are explicit rather than guessed.
11. **Approval ambiguity** is discussed rather than silently resisted; Morgan need not accept Alex's proposal.
12. **Manager unavailability** leaves decision boundaries intact: routine work continues, a shared decision waits, and a true blocker uses the named alternate path.
13. **One-on-one preparation** selects one risk, one manager decision, and one development question. A one-on-one is not merely status, but preparation makes limited shared time useful.

When Morgan says, “I need earlier visibility,” a strong verbal response is only a beginning. Later material-risk updates and completed follow-ups are better evidence. Trust history can support less routine supervision and confidence that important issues will surface. It does not score obedience, confidence, likability, or personality.

## Reflection

1. Which decisions did Morgan explicitly delegate to Alex?
2. At what point did the schedule issue become something Morgan needed to know?
3. Why does the T3 vendor behavior not require escalation?
4. Why does the API contract change require consultation?
5. What makes T6 a true blocker?
6. How can Alex escalate without simply asking Morgan to solve the problem?
7. What information should Alex omit from a manager update?
8. How could Alex clarify expectations if Morgan begins reviewing every small decision?
9. When should an employee continue independently while the manager is unavailable?
10. What repeated behaviors would make a manager comfortable granting more autonomy?

## Limits

The laboratory authors semantics explicitly and does not judge arbitrary prose, diagnose managers, build an HR system, or supply legal analysis. Thresholds belong to each scenario. Chapter 12 applies these boundaries horizontally between peers.
