
from banco import (
    criar_tabela,
    cadastrar_agendamento,
    listar_agendamentos,
    excluir_agendamento
)

criar_tabela()

# Cria um agendamento apenas para teste
id_teste = cadastrar_agendamento(
    nome_pet="Bob",
    tutor="Maria Oliveira",
    telefone="85988887777",
    cep="60000000",
    logradouro="Rua Teste",
    bairro="Centro",
    cidade_uf="Fortaleza/CE",
    numero="50",
    servico="Banho e Tosa",
    data_horario="22/11/2026 09:00"
)

if id_teste is not None:
    print("\nAgendamento de teste criado. ID:", id_teste)

    # Exclui somente o registro recém-criado
    resultado = excluir_agendamento(id_teste)

    if resultado:
        print("\nVerificando se Bob foi removido...")

        agendamentos = listar_agendamentos()

        encontrado = any(
            agendamento[0] == id_teste
            for agendamento in agendamentos
        )

        if not encontrado:
            print("TESTE OK: Bob foi excluído do banco!")
        else:
            print("TESTE FALHOU: Bob ainda está cadastrado.")
else:
    print("Não foi possível criar o registro de teste.")
