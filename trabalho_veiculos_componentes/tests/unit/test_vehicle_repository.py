import pytest
from src.vehicle_repository import VehicleRepository


def test_exists_returns_true_for_existing_vehicle():
    repo = VehicleRepository()
    assert repo.exists(1) is True


def test_is_available_returns_true_for_available_vehicle():
    repo = VehicleRepository()
    assert repo.is_available(1) is True


def test_is_available_returns_false_for_unavailable_vehicle():
    repo = VehicleRepository()
    assert repo.is_available(3) is False


def test_mark_unavailable_changes_vehicle_state():
    repo = VehicleRepository()
    repo.mark_unavailable(1)
    assert repo.is_available(1) is False


def test_mark_available_changes_vehicle_state():
    repo = VehicleRepository()
    repo.mark_available(3)
    assert repo.is_available(3) is True


def test_mark_unavailable_raises_for_unknown_vehicle():
    repo = VehicleRepository()
    with pytest.raises(ValueError, match="Vehicle not found"):
        repo.mark_unavailable(999)
