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

An installed `soft-skills-lab` entry point provides the same commands. The scenario catalog contains immutable domain values. Responses record structured behavioral evidence, and the evaluator applies explicit predicates to those fields rather than searching message text. This is intentionally a teaching model, not a natural-language judge.

## Volume I: Professional Reliability and Communication

0. **The Executable Professional** (implemented)
1. Professionalism as Observable Behavior
2. Listening Before Responding
3. Asking Good Questions
4. Explaining Technical Ideas Simply
5. Giving Status Updates
6. Saying “I Don’t Know” Professionally
7. Receiving Feedback Without Defensiveness
8. Taking Responsibility
9. Disagreeing Professionally
10. Conflict and De-escalation
11. Working With Managers
12. Working With Teammates
13. Working With Business Stakeholders
14. Handling Ambiguous Requirements
15. Handling Mistakes and Incidents
16. When Personal Problems Affect Work
17. Performance Feedback and PIPs
18. Interview Communication
19. Meetings and Presence
20. Written Professional Communication
21. Trust and Reputation
22. Leadership Without Authority
23. Professional Judgment
24. End-to-End Workplace Simulation

Later chapters are a roadmap, not yet implemented.

## Limits and responsible use

This laboratory is **not a psychological assessment**, does not diagnose personality, and does not evaluate personal worth. It does not claim there is one universally correct response to every workplace situation. Culture, power, urgency, safety, law, and missing context can change an appropriate response. The exercises deliberately model simplified, deterministic situations for practice and evaluate only stated professional behaviors. They are prompts for judgment and reflection, not replacements for organizational policy, expert help, or human context.
