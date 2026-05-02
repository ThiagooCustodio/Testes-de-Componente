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
   #retira a disponibilidade do veículo 1
   assert vehicle_repo.is_available(1) is False
   #inclui a reserva do veículo 1
   assert rental_repo.has_active_rental(1) is True


#2. Teste locação de veículo inexistente
def test_existencia_veiculo():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       veiculo = service.rent_vehicle(10, 10)
       
       assert veiculo is False

#3. Teste locação por motorista inexistente
def test_existencia_motorista():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       motorista = service.rent_vehicle(1, 1)
       
       assert motorista is False

#4. Teste locação bloqueada por habilitação inválida
def test_motorista_habilitacao_invalida():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       motorista_habilit_invalida1 = service.rent_vehicle(30, 1)
       motorista_habilit_invalida2 = service.rent_vehicle(10, 1)
       
       assert motorista_habilit_invalida1 is False
       assert motorista_habilit_invalida2 is True

#5. Teste locação bloqueada por motorista bloqueado
def test_motorista_bloqueado():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       motorista_bloqueado1 = service.rent_vehicle(20, 1)
       motorista_bloqueado2 = service.rent_vehicle(10, 1)
       
       assert motorista_bloqueado1 is False
       assert motorista_bloqueado2 is True


#6. Teste locação bloqueada por limite de 2 locações ativas
def test_limite_locacoes_ativas():
    service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()

    locacao1 = service.rent_vehicle(10, 1)
    locacao2 = service.rent_vehicle(10, 2)

    # Cria mais um veículo 
    vehicle_repo._vehicles[4] = {"model": "Pickup", "available": True}

    locacao3 = service.rent_vehicle(10, 4)

    assert locacao1 is True
    assert locacao2 is True
    assert locacao3 is False
    #Aqui verificado que o sistema permite a locação de 2 veículos para cada motorista
    #if self.rental_repository.count_active_rentals(driver_id) >= 2:
            #return False

#7. Teste reserva com sucesso para veículo indisponível
def test_veiculo_disponivel():
       service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
       veiculo_disp1 = service.rent_vehicle(10, 1)
       veiculo_disp2 = service.rent_vehicle(10, 2)
       veiculo_disp3 = service.rent_vehicle(10, 3)
       
       assert veiculo_disp1 is True
       assert veiculo_disp2 is True
       assert veiculo_disp3 is False



#1111. Teste se o veículo já esta reservado para um motorista
def test_veiculo_ja_reservado():
    service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()

    # motorista 10 reserva o veículo 1
    hold_repo.add_hold(10, 1)
    # motorista 40 tenta alugar o mesmo veículo
    resultado = service.rent_vehicle(40, 1)

    assert resultado is False
