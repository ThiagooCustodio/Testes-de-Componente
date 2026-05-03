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
def test_veiculo_reservado_para_outro_motorista():
    service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()

    # motorista 40 faz reserva
    hold_repo.add_hold(40, 1)

    # motorista 10 tenta alugar o mesmo veículo
    resultado = service.rent_vehicle(10, 1)

    assert resultado is False

#8. Teste tentativa de reserva duplicada
def test_reservas_duplicadas():
    service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()

    hold_repo.add_hold(10, 1)
    hold_repo.add_hold(40, 1)

    # continua existindo reserva para o veículo
    assert hold_repo.has_any_hold(1) is True

    # ambos estão na lista (duplicado permitido)
    assert hold_repo.has_hold(10, 1) is True
    assert hold_repo.has_hold(40, 1) is True 

""" def test_reserva_duplicada_deve_falhar():
     service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()
     
     hold_repo.add_hold(10, 1)
     with pytest.raises(ValueError):
          hold_repo.add_hold(40, 1)   """

#9. Teste devolução simples sem reserva pendente;
def test_devolucao_sem_reserva():
    service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()

    # faz a locação
    resultado_locacao = service.rent_vehicle(10, 1)
    assert resultado_locacao is True

    # devolve o veículo
    resultado_devolucao = service.return_vehicle(10, 1)
    assert resultado_devolucao is True

    # veículo volta a ficar disponível
    assert vehicle_repo.is_available(1) is True

    # locação deve ser removida
    assert rental_repo.is_vehicle_with_driver(10, 1) is False

#10. devolução com reserva pendente, mantendo o veículo indisponível;
def test_devolucao_com_reserva_pendente():
    service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()

    # motorista 10 aluga o veículo
    assert service.rent_vehicle(10, 1) is True

    # motorista 40 faz reserva para o mesmo veículo
    hold_repo.add_hold(40, 1)

    # motorista 10 devolve o veículo
    resultado = service.return_vehicle(10, 1)

    assert resultado is True

    # veículo NÃO deve ficar disponível
    assert vehicle_repo.is_available(1) is False

    # locação deve ter sido encerrada
    assert rental_repo.is_vehicle_with_driver(10, 1) is False    

#11. Teste locação bem-sucedida por motorista que tinha reserva para o mesmo veículo, removendo a reserva;
def test_locacao_com_reserva_do_mesmo_motorista_removendo_reserva():
    service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()

    # motorista 10 faz reserva
    hold_repo.add_hold(10, 1)

    # garante que o hold existe
    assert hold_repo.has_hold(10, 1) is True

    # motorista 10 realiza a locação
    resultado = service.rent_vehicle(10, 1)

    assert resultado is True

    # veículo fica indisponível
    assert vehicle_repo.is_available(1) is False

    # locação foi registrada
    assert rental_repo.is_vehicle_with_driver(10, 1) is True

    # hold deve ser removido
    assert hold_repo.has_hold(10, 1) is False


#12. Teste sequência completa: locação → reserva por outro motorista → devolução → tentativa de nova locação.
def test_fluxo_completo():
    service, vehicle_repo, driver_repo, rental_repo, hold_repo = criar_locacao()

    # 1. Motorista 10 aluga
    assert service.rent_vehicle(10, 1) is True

    # 2. Motorista 40 faz reserva
    hold_repo.add_hold(40, 1)
    assert hold_repo.has_hold(40, 1) is True

    # 3. Motorista 10 devolve
    assert service.return_vehicle(10, 1) is True

    # veículo ainda não deve estar disponível (há reserva)
    assert vehicle_repo.is_available(1) is False

    # 4. Motorista 40 realiza a locação
    resultado = service.rent_vehicle(40, 1)

    assert resultado is True

    # veículo continua indisponível (agora alugado novamente)
    assert vehicle_repo.is_available(1) is False

    # locação registrada para o novo motorista
    assert rental_repo.is_vehicle_with_driver(40, 1) is True

    # hold deve ter sido removido
    assert hold_repo.has_hold(40, 1) is False
    
    
