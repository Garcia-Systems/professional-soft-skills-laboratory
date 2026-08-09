# Chapter 21: Trust and Reputation

## Educational question

> What repeated evidence causes other people to change how much they rely on you?

## Learning objectives

The learner should be able to:

- distinguish trust from likability and reputation from one event;
- identify multiple dimensions of professional trust and trace each conclusion to evidence;
- distinguish competence from reliability;
- understand how risk visibility and handoff behavior affect trust;
- recognize trust degradation and rebuilding;
- understand why promises alone do not repair trust;
- understand how autonomy can change with relevant evidence;
- recognize observer-specific trust;
- keep private circumstances out of professionalism scoring; and
- understand why behavioral change may precede reputation change.

## Professional concept

> People learn whether they can rely on you from repeated experiences of what happens when work becomes uncertain, difficult, or dependent on you.

Professional trust is accumulated evidence. Reputation is not one event: it is the pattern people infer from repeated evidence. Neither is a judgment of a “trustworthy personality,” likability, confidence, charisma, popularity, familiarity, or personal chemistry. These may affect impressions, but they are not evidence that a commitment will close or a material risk will become visible.

Trust, reputation, likability, familiarity, competence, reliability, credibility, and autonomy are related but not equivalent. **Trust** is an evidence-supported expectation within a scope. **Reputation** is the pattern inferred from a history. **Competence** concerns capability; **reliability** concerns repeatable follow-through; **credibility** concerns whether bounded claims match later reality. **Autonomy** is an operating arrangement that evidence may support, not a personality prize. Alex can produce excellent fixes while Morgan still adds checkpoints because Alex's estimates and handoffs are weak.

> Trust does not mean believing that you will never make a mistake. It means having evidence about how you behave when commitments, risks, mistakes, and dependencies appear.

The laboratory therefore separates `COMMITMENT_RELIABILITY`, `RISK_VISIBILITY`, `HANDOFF_RELIABILITY`, `TECHNICAL_JUDGMENT`, `OWNERSHIP`, `FEEDBACK_RESPONSIVENESS`, `INCIDENT_COMMUNICATION`, and `DECISION_CREDIBILITY`. One missed handoff does not contaminate incident communication. Three hidden risks affect risk visibility, not every domain. Transparency can support risk visibility, but disclosure alone is not follow-through. Conversely, completed work does not excuse surprises caused by hidden risks.

Each `TrustEvidence` record has an event id, time, dimension, positive/negative/neutral polarity, observable behavior, provenance, linked scenario, and observers. Provenance is direct observation, shared artifact, or documented event—not gossip. The observer filter prevents Dana from inheriting Morgan's incident knowledge or Jordan's handoff experience. Private circumstances never enter this history. Communicating capacity impact, revising a commitment, and completing follow-up may enter because those are professional handling behaviors.

States are semantic rather than percentages: `INSUFFICIENT_EVIDENCE`, `DEVELOPING`, `ESTABLISHED`, `MIXED`, `DEGRADED`, and `REBUILDING`. One success remains insufficient history. One failure remains evidence, not a complete reputation. Earlier failure plus later repeated success can indicate rebuilding; the failure is not deleted. An apology or “I promise it will be different” is communication, not observed reliability repair.

> Reputation is lagging evidence.

Behavior can change today while coworkers reasonably wait for repeated relevant observations before changing expectations. This is not an exponential-decay formula or punishment. It is evidence accumulation. Recent repeated hidden risks can degrade previously strong risk visibility; later repeated early communication can begin rebuilding it. There is deliberately no universal number of events and no aggregate professionalism score.

The six-week history brings earlier chapters together: kept commitments, an early reforecast, a missed and corrected handoff, accurate incident communication and ownership, evidence-based disagreement, and proactive dependency communication. Its commitment and risk evidence are established; handoff evidence is rebuilding; ownership and incident communication are established; the single architecture and decision events are not yet established patterns.

Trust changes coordination. Morgan may replace daily updates with threshold-based updates after repeated routine ownership, risk visibility, and consultation at boundaries. That is a possible operational consequence, not an automatic reward. Jordan may begin frontend work with less contingency after repeated stable contracts, early change communication, and closed handoffs. Yet established individual-contributor reliability does not prove first-time cross-team leadership: trust in current scope is not proven trust in expanded scope. This boundary prepares later study without implementing Chapter 22.

## Engineering concept

Reliability history is a limited analogy. One successful request does not prove that a service is reliable; one failure does not prove it unusable. Operators inspect success, failure, recovery, observability, and repeated behavior. Professional trust likewise needs inspectable history rather than a personality label. People are not services, and this chapter does not turn judgment into statistical reliability engineering.

The deterministic flow is:

```text
Work event -> observable behavior -> evidence event
           -> dimension/provenance/time -> evidence history
           -> pattern interpretation -> trust state
           -> possible autonomy, dependency, or credibility consequence
```

Interpretations remain authored and inspectable. Older evidence stays present, domains remain separate, and there is no average.

## Run the laboratory

```bash
python -m soft_skills_lab scenario six-week-project
python -m soft_skills_lab trust-history six-week-project
python -m soft_skills_lab trust-explain six-week-project commitment-reliability
python -m soft_skills_lab trust-explain six-week-project handoff-reliability
python -m soft_skills_lab trust-view six-week-project --observer Morgan
python -m soft_skills_lab trust-view six-week-project --observer Jordan
python -m soft_skills_lab trust-view six-week-project --observer Dana
python -m soft_skills_lab scenario one-success
python -m soft_skills_lab trust-history one-success
python -m soft_skills_lab scenario one-mistake
python -m soft_skills_lab trust-history one-mistake
python -m soft_skills_lab scenario trust-degradation
python -m soft_skills_lab trust-history trust-degradation
python -m soft_skills_lab scenario trust-rebuilding
python -m soft_skills_lab trust-history trust-rebuilding
python -m soft_skills_lab scenario competence-coordination
python -m soft_skills_lab trust-history competence-coordination
python -m soft_skills_lab scenario domain-transfer
python -m soft_skills_lab trust-history domain-transfer
python -m soft_skills_lab scenario autonomy-expansion
python -m soft_skills_lab trust-history autonomy-expansion
python -m soft_skills_lab scenario capacity-handling
python -m soft_skills_lab trust-history capacity-handling
```

## What to observe

Inspect the multidimensional six-week history and its coexisting positive and negative handoff evidence. Compare Morgan, Jordan, and Dana: their states differ because their available evidence differs. One success does not establish a pattern; one handled mistake does not destroy unrelated history. Degradation preserves earlier positives, while rebuilding preserves the negative events and displays later behavior.

The autonomy scenario ties changed update cadence only to relevant evidence and retains consultation thresholds. Domain transfer leaves first-time expanded scope insufficient. Competence-coordination keeps technical judgment strong while handoff reliability is degraded and claim credibility remains separately inspectable. Capacity-handling records impact, revision, and follow-through but no private cause. Accurate bounded forecasts can build decision credibility; repeated unsupported certainty, inflated metrics, and false-green status would weaken claim/evidence consistency without inferring an “honest” or “dishonest” personality.

## Reflection

1. What evidence supports Morgan trusting Alex to surface risk?
2. Why is handoff reliability still mixed after Week 3?
3. Why should one missed handoff not destroy technical-judgment trust?
4. What evidence would justify increased autonomy?
5. Why does verbal reassurance not repair trust?
6. How many good events are enough to establish a pattern? Why should the model avoid pretending there is one universal number?
7. Why might Jordan and Morgan have different trust views?
8. How can someone be highly competent but difficult to coordinate with?
9. Why does reputation change more slowly than behavior?
10. How can handling a mistake well preserve or strengthen some trust dimensions?
11. Which personal details from Chapter 16 must never enter the trust history?
12. What evidence would convince you that degraded trust is rebuilding?
