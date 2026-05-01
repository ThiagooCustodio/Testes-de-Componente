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
 

#1. Teste locação com sucesso
def test_rent_veiculo_sucesso():
   service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
   test = service.rent_vehicle(10, 1)

   assert test is True
   assert vehicle_repo.is_available(1) is False

#2. Teste se o motorista existir
def test_existencia_motorista():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       motorista = service.rent_vehicle(1, 1)
       
       assert motorista is False

#3. Teste se o veículo existir
def test_existencia_veiculo():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       veiculo = service.rent_vehicle(10, 10)
       
       assert veiculo is False

#4. Teste motorista bloqueado
def test_motorista_bloqueado():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       motorista_bloqueado = service.rent_vehicle(20, 1)
       
       assert motorista_bloqueado is False

#5. Teste motorista com habilitação válida
def test_motorista_habilitacao_invalida():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       motorista_habilit_invalida = service.rent_vehicle(30, 1)
       
       assert motorista_habilit_invalida is False

#6. Teste veículo disponível
def test_veiculo_disponivel():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       veiculo_disp1 = service.rent_vehicle(10, 1)
       veiculo_disp2 = service.rent_vehicle(10, 2)
       veiculo_disp3 = service.rent_vehicle(10, 3)
       
       assert veiculo_disp1 is True
       assert veiculo_disp2 is True
       assert veiculo_disp3 is False

