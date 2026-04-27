import pytest
from src.hold_repository import HoldRepository


def test_add_hold_registers_entry():
    repo = HoldRepository()
    repo.add_hold(10, 1)
    assert repo.has_hold(10, 1) is True


def test_has_any_hold_returns_true_when_vehicle_has_hold():
    repo = HoldRepository()
    repo.add_hold(10, 1)
    assert repo.has_any_hold(1) is True


def test_next_driver_returns_first_driver_in_queue():
    repo = HoldRepository()
    repo.add_hold(10, 1)
    repo.add_hold(40, 1)
    assert repo.next_driver(1) == 10


def test_remove_hold_removes_entry():
    repo = HoldRepository()
    repo.add_hold(10, 1)
    repo.remove_hold(10, 1)
    assert repo.has_hold(10, 1) is False


def test_remove_hold_raises_for_unknown_entry():
    repo = HoldRepository()
    with pytest.raises(ValueError, match="Hold entry not found"):
        repo.remove_hold(10, 1)
