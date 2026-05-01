import pytest

from src.vehicle_repository import VehicleRepository
from src.driver_repository import DriverRepository
from src.rental_repository import RentalRepository
from src.hold_repository import HoldRepository
from src.rental_service import RentalService


def criar_locacao():
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
def test_rent_veiculo_sucesso():
   service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
   test = service.rent_vehicle(10, 1)

   assert test is True
   assert vehicle_repo.is_available(1) is False

#2 teste se o motorista existir
def test_existencia_motorista():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       motorista = service.rent_vehicle(1, 1)
       
       assert motorista is False