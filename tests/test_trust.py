from dataclasses import FrozenInstanceError

import pytest

from soft_skills_lab.trust import DEMO_EVENTS, ProfessionalTrust


def test_trust_accumulates_history_and_integer_balance() -> None:
    trust = ProfessionalTrust()
    states = []
    for event in DEMO_EVENTS:
        trust = trust.record(event)
        states.append(trust.balance)
    assert states == [2, 4, 5, 7, 4]
    assert trust.history == DEMO_EVENTS
    assert isinstance(trust.balance, int)


def test_record_returns_new_immutable_state() -> None:
    empty = ProfessionalTrust()
    updated = empty.record(DEMO_EVENTS[0])
    assert empty.history == ()
    assert len(updated.history) == 1
    with pytest.raises(FrozenInstanceError):
        updated.history = ()  # type: ignore[misc]
