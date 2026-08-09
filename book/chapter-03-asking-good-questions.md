# Chapter 3: Asking Good Questions

## Educational question

> How do you ask for information without outsourcing your thinking to someone else?

## Learning objectives

The learner should be able to:

- identify decision-relevant unknowns;
- distinguish blocking from non-blocking questions;
- investigate available evidence before asking;
- provide useful context and ask specific, answerable questions;
- avoid assumptions disguised as questions and avoid question dumps;
- sequence questions from problem to solution;
- recognize when immediate escalation is appropriate; and
- update understanding after receiving an answer.

## Professional concept

> A good professional question reduces decision-relevant uncertainty.

Not every unknown deserves a question. Good questions demonstrate thinking rather than replace thinking. “What should I do?” can be weak when cheap, safe investigation has not occurred. “I found X, checked Y, and still don't understand Z. My current interpretation is A. Am I missing something?” exposes both the investigation and the remaining uncertainty.

That wording is not a rigid template. “I don't understand this yet. Can you help me?” can be entirely appropriate. Context determines how much investigation is reasonable. Asking questions is not helplessness; asking someone else to perform investigation one could reasonably perform can become helplessness. Conversely, investigating alone is not always better:

> Investigate before asking when investigation is cheap and safe. Ask early when delay itself creates risk.

High risk, limited authority, or increasing harm can make immediate escalation the professional choice.

## Engineering concept

A useful debugging question narrows the search space. A useful professional question similarly reduces uncertainty that affects a decision. The analogy stops there: people, product authority, urgency, and safety cannot be reduced to a debugging procedure.

Question order matters. When told “search must be faster,” questions about the affected workflow, observed response time, acceptable response time, and conditions should precede Redis, Elasticsearch, or a rewrite. Ask about the problem before asking which solution to implement. This extends Chapter 2's warning about premature solutions.

## Run the laboratory

```bash
python -m soft_skills_lab scenario report-export
python -m soft_skills_lab evaluate report-export no-questions
python -m soft_skills_lab evaluate report-export question-dump
python -m soft_skills_lab evaluate report-export ask-before-looking
python -m soft_skills_lab evaluate report-export leading-question
python -m soft_skills_lab evaluate report-export focused-questions
python -m soft_skills_lab compare report-export
python -m soft_skills_lab unknowns report-export
python -m soft_skills_lab answer report-export

python -m soft_skills_lab scenario deployment-failure
python -m soft_skills_lab evaluate deployment-failure helpless-escalation
python -m soft_skills_lab evaluate deployment-failure endless-solo-investigation
python -m soft_skills_lab evaluate deployment-failure professional-question
python -m soft_skills_lab scenario authorization-risk
python -m soft_skills_lab evaluate authorization-risk immediate-escalation
```

The answer command demonstrates the deterministic lifecycle: unknown → question → answer → known fact → decision. Priya confirms CSV, current filters, member-visible fields, and a 90-day maximum.

## What to observe

1. **No questions:** correct guesses would still leave unnecessary requirement risk because Alex has not confirmed the contract.
2. **Question dump:** quantity shifts prioritization and cognitive work to Priya; low-value icon and filename details obscure blocking decisions.
3. **Ask before looking:** repository evidence already establishes the generic download component and streamed browser behavior. It cannot decide product-specific format or fields.
4. **Leading question:** one confirmation hides separate assumptions about CSV, filters, and visible columns, making superficial agreement easy.
5. **Focused questions:** Alex supplies investigation context, removes resolved infrastructure questions, and asks about format, row scope, field authorization, and size.

The deployment example separates helpless escalation, harmful silence, and a professional request that includes evidence, uncertainty, and a proposed rollback. The authorization example shows why hours of solo experimentation would be worse than immediate escalation.

## Reflection

1. Which unknowns actually blocked Alex?
2. Which questions could Alex answer independently?
3. Why is a question dump difficult for Priya to answer?
4. What assumptions are hidden inside the leading question?
5. How does context make a question easier to answer?
6. When does investigation become excessive?
7. When should risk cause you to ask or escalate immediately?
8. How can asking a question demonstrate competence rather than uncertainty alone?

The model evaluates authored, observable semantics rather than arbitrary prose. It does not assign a numeric question-quality score and does not claim one universal wording is professional.
