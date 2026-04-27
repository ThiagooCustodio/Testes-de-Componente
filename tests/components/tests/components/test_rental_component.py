import pytest

from vehicle_repository import VehicleRepository
from driver_repository import DriverRepository
from rental_repository import RentalRepository
from hold_repository import HoldRepository
from rental_service import RentalService


@pytest.fixture
def setup_system():
    vehicle_repo = VehicleRepository()
    driver_repo = DriverRepository()
    rental_repo = RentalRepository()
    hold_repo = HoldRepository()

    service = RentalService(
        vehicle_repo,
        driver_repo,
        rental_repo,
        hold_repo
    )

    return service, vehicle_repo, driver_repo, rental_repo, hold_repo
 

# 1. locação com sucesso
def test_rent_vehicle_success(setup_system):
    service, vehicle_repo, *_ = setup_system

    result = service.rent_vehicle(10, 1)

    assert result is True
    assert vehicle_repo.is_available(1) is False
