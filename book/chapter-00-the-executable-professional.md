# Chapter 0: The Executable Professional

> **Thesis:** Professional soft skills can be treated as observable decisions and behaviors that can be modeled, rehearsed, evaluated, and improved.

## From labels to actions

Advice like “communicate better,” “be professional,” “be confident,” “be a team player,” or “don’t be defensive” names a desired impression, not an action someone can practice. Two observers may interpret the same person differently, and a learner receives no testable next step.

Compare “communicate better” with these questions:

- Did the person clarify what happened before responding?
- Did they distinguish facts from assumptions?
- Did they acknowledge the responsibility they actually own?
- Did they communicate risk early?
- Did they name a next action, its owner, and a follow-up point?
- Did they avoid unsupported blame and escalate through a useful channel?
- Did they maintain appropriate professional boundaries?

These questions concern visible evidence. They can be rehearsed, evaluated, and discussed without turning a professional situation into a verdict about personality or worth.

## The laboratory method

1. **Observe the situation.** Notice participants, commitments, impact, risk, and available evidence.
2. **Separate facts from assumptions.** State what is known and mark what still requires evidence.
3. **Identify professional responsibilities.** Distinguish owned work from unknown cause and from responsibilities held by others.
4. **Choose a response.** Communicate and act; do not optimize only for a polished sentence.
5. **Observe consequences.** Look for operational and relationship effects that follow.
6. **Evaluate behavior against explicit criteria.** Explain every pass or failure with evidence.
7. **Reflect and retry.** Change a decision, rerun the model, and compare the result.

The loop is illustrated in [`diagrams/laboratory-method.md`](../diagrams/laboratory-method.md). Determinism makes a retry comparable; it does not suggest real workplaces are fully predictable.

## Scenario: the incident after a release

A developer delivers a feature. A production incident occurs after deployment. The manager says the feature caused the incident. The developer believes that explanation is incomplete.

Known facts include the deployment timing, the incident, and the manager's statement. The causal mechanism, possible contributions from other changes, and the complete event sequence remain uncertain. Timing is evidence worth investigating, but timing alone does not establish causation.

### Reference responses

**Defensive denial**

> “My code did not cause this. It worked in testing.”

This rejects a cause before reviewing production evidence. Passing tests matters, but does not prove innocence. It also offers no investigation, ownership, or follow-up.

**Premature acceptance of all blame**

> “This is entirely my fault. I caused the incident.”

Acknowledging impact and taking responsibility can be useful; declaring an unknown cause is not. Over-acceptance can corrupt the investigation just as denial can. Responsibility for investigating owned changes is different from accepting every causal claim.

**Blame shifting**

> “Operations must have configured it incorrectly; ask them.”

This replaces one unsupported conclusion with another and abandons shared incident work. Asking operations for configuration evidence could be appropriate; assigning fault first is not.

**Investigation-oriented response**

> “I see the incident followed our release. I own reviewing my change now. Let's avoid settling the cause until we compare logs and deployment changes. I will report initial findings at the 15:00 incident update.”

This response acknowledges the incident, states what is known, leaves causation open, accepts a clearly owned part of the response, names an investigation action, and establishes a follow-up. It is a reference, not a script. Different language—and different actions suited to local incident practice—can demonstrate the same behaviors.

## Disagreement is not defiance

Professionalism is not submissiveness, automatic agreement, or absorbing blame to protect authority. A professional may appropriately disagree with a manager's conclusion, correct an inaccurate account, ask that evidence be preserved, or escalate a safety or integrity concern. The relevant questions are whether the disagreement distinguishes evidence from inference, addresses the work rather than attacking a person, accepts real responsibility, and advances a useful next action.

Conversely, a courteous tone does not repair hidden risk, missing ownership, or a knowingly unsupported claim. The laboratory evaluates modeled behavior, not deference or style.

## Run the exercise

```console
$ python -m soft_skills_lab scenario production-incident
$ python -m soft_skills_lab evaluate production-incident defensive
$ python -m soft_skills_lab evaluate production-incident blame-shifting
$ python -m soft_skills_lab evaluate production-incident over-accepting
$ python -m soft_skills_lab evaluate production-incident professional
```

Each evaluation reports `PASS` or `FAIL` for six explicit criteria: acknowledging impact, avoiding unsupported claims, accepting owned responsibility, avoiding blame, establishing a next action, and establishing a follow-up. It follows each outcome with an explanation and evidence. There is no opaque total score and no claim that only one sentence could pass.

## Trust as accumulated evidence

Professional trust is not a personality property or a synonym for likability. It is a defeasible history: commitments kept, risks raised early, mistakes acknowledged, and follow-ups completed support reliance; hidden risks and unwarned missed commitments count against it.

```console
$ python -m soft_skills_lab trust-demo
```

The fixed demonstration records five events and prints each event's small integer weight plus the resulting balance. The balance is only a compact state; the history is the explanation. Context still matters—a missed commitment during an emergency is not fully understood by an integer—and the model deliberately does not infer motive.

> **Professional trust is accumulated evidence.**

## Reflection

Try constructing another `ProfessionalResponse` with entirely different wording but equivalent acknowledged facts, owned responsibility, investigation action, and follow-up. It should satisfy the same criteria. Then remove the follow-up behavior while leaving “professional” words in the message. It should fail that criterion. This boundary is essential: the executable professional is a model of choices and evidence, not a phrase-matching chatbot.
