# Trabalho Prático — Testes de Componente em um Sistema de Locação de Veículos

## Objetivo

Neste trabalho, vocês receberão um pequeno sistema de locação de veículos já implementado, contendo:

- código-fonte do subsistema;
- testes de unidade prontos;
- estrutura básica do projeto.

O trabalho de vocês será criar os **testes de componente** do sistema, utilizando `pytest`.

Os testes de componente devem verificar a colaboração real entre as classes do subsistema, cobrindo fluxos de negócio relevantes. Não é permitido transformar o trabalho em testes unitários disfarçados, nem substituir as classes internas do subsistema por mocks.

## Sistema

O sistema representa um pequeno subsistema de locação de veículos.

As classes principais do projeto são:

- `VehicleRepository`
- `DriverRepository`
- `RentalRepository`
- `HoldRepository`
- `RentalService`

## Regras de negócio

### Locação
Um motorista pode alugar um veículo somente se:

- o motorista existir;
- o veículo existir;
- o motorista não estiver bloqueado;
- o motorista tiver habilitação válida;
- o veículo estiver disponível;
- o motorista tiver menos de 2 locações ativas;
- o veículo não estiver reservado para outro motorista.

Quando a locação é feita com sucesso:

- o veículo deixa de estar disponível;
- a locação ativa é registrada;
- se o motorista tinha uma reserva para esse veículo, ela deve ser removida.

### Devolução
Ao devolver um veículo:

- a locação ativa correspondente deve existir;
- a locação é encerrada;
- se não houver reserva pendente para o veículo, ele volta a ficar disponível;
- se houver reserva pendente, ele continua indisponível.

### Reserva
Um motorista pode reservar um veículo somente se:

- o motorista existir;
- o veículo existir;
- o motorista não estiver bloqueado;
- o motorista tiver habilitação válida;
- o veículo estiver indisponível;
- o motorista não tiver uma reserva duplicada para o mesmo veículo;
- o motorista não for quem já está com o veículo alugado.

A reserva deve respeitar a ordem de chegada.

## Tarefa

Criem os testes de componente em:

```text 
tests/components/
```

Sugestão de arquivo:

```text
tests/components/test_rental_component.py
```

## Quantidade esperada
Espera-se entre **10 e 12 testes de componente**.

## Cenários mínimos obrigatórios

1. locação com sucesso;
2. locação de veículo inexistente;
3. locação por motorista inexistente;
4. locação bloqueada por habilitação inválida;
5. locação bloqueada por motorista bloqueado;
6. locação bloqueada por limite de 2 locações ativas;
7. reserva com sucesso para veículo indisponível;
8. tentativa de reserva duplicada;
9. devolução simples sem reserva pendente;
10. devolução com reserva pendente, mantendo o veículo indisponível;
11. locação bem-sucedida por motorista que tinha reserva para o mesmo veículo, removendo a reserva;
12. sequência completa: locação → reserva por outro motorista → devolução → tentativa de nova locação.

## Requisitos de qualidade

Os testes devem:

- usar as classes reais do subsistema;
- refletir fluxos de negócio;
- ser legíveis e bem nomeados;
- evitar duplicação excessiva;
- ser determinísticos.

## Execução

Para executar os testes de unidade:

```bash
pytest tests/unit
```

Para executar todos os testes:

```bash
pytest
```
