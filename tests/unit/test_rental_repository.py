import pytest
from src.rental_repository import RentalRepository


def test_create_rental_registers_active_rental():
    repo = RentalRepository()
    repo.create_rental(10, 1)
    assert repo.has_active_rental(1) is True


def test_count_active_rentals_counts_only_driver_rentals():
    repo = RentalRepository()
    repo.create_rental(10, 1)
    repo.create_rental(10, 2)
    repo.create_rental(40, 3)
    assert repo.count_active_rentals(10) == 2


def test_is_vehicle_with_driver_returns_true_for_matching_rental():
    repo = RentalRepository()
    repo.create_rental(10, 1)
    assert repo.is_vehicle_with_driver(10, 1) is True


def test_close_rental_removes_active_rental():
    repo = RentalRepository()
    repo.create_rental(10, 1)
    repo.close_rental(10, 1)
    assert repo.has_active_rental(1) is False


def test_close_rental_raises_for_unknown_rental():
    repo = RentalRepository()
    with pytest.raises(ValueError, match="Active rental not found"):
        repo.close_rental(10, 1)
