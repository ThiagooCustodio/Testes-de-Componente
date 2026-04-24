import pytest
from unittest.mock import Mock
from src.rental_service import RentalService


def make_service():
    vehicle_repository = Mock()
    driver_repository = Mock()
    rental_repository = Mock()
    hold_repository = Mock()
    service = RentalService(
        vehicle_repository,
        driver_repository,
        rental_repository,
        hold_repository,
    )
    return service, vehicle_repository, driver_repository, rental_repository, hold_repository


def test_rent_vehicle_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Driver ID and vehicle ID are required"):
        service.rent_vehicle(None, 1)


def test_rent_vehicle_returns_false_when_driver_does_not_exist():
    service, _, driver_repository, _, _ = make_service()
    driver_repository.exists.return_value = False
    assert service.rent_vehicle(999, 1) is False


def test_rent_vehicle_creates_rental_when_all_rules_are_satisfied():
    service, vehicle_repository, driver_repository, rental_repository, hold_repository = make_service()

    driver_repository.exists.return_value = True
    vehicle_repository.exists.return_value = True
    driver_repository.is_blocked.return_value = False
    driver_repository.has_valid_license.return_value = True
    vehicle_repository.is_available.return_value = True
    rental_repository.count_active_rentals.return_value = 0
    hold_repository.next_driver.return_value = None
    hold_repository.has_hold.return_value = False

    result = service.rent_vehicle(10, 1)

    assert result is True
    vehicle_repository.mark_unavailable.assert_called_once_with(1)
    rental_repository.create_rental.assert_called_once_with(10, 1)


def test_return_vehicle_returns_false_when_rental_does_not_exist():
    service, _, _, rental_repository, _ = make_service()
    rental_repository.is_vehicle_with_driver.return_value = False
    assert service.return_vehicle(10, 1) is False


def test_hold_vehicle_adds_entry_when_rules_are_satisfied():
    service, vehicle_repository, driver_repository, rental_repository, hold_repository = make_service()

    driver_repository.exists.return_value = True
    vehicle_repository.exists.return_value = True
    driver_repository.is_blocked.return_value = False
    driver_repository.has_valid_license.return_value = True
    vehicle_repository.is_available.return_value = False
    hold_repository.has_hold.return_value = False
    rental_repository.is_vehicle_with_driver.return_value = False

    result = service.hold_vehicle(10, 1)

    assert result is True
    hold_repository.add_hold.assert_called_once_with(10, 1)


def test_hold_vehicle_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Driver ID and vehicle ID are required"):
        service.hold_vehicle(None, 1)
