
from datetime import datetime
from pathlib import Path

# Arquivo de log na pasta do projeto
CAMINHO_LOG = (
    Path(__file__).resolve().parent
    / "log_agendamentos.txt"
)


def registrar_log(operacao, descricao):
    try:
        # Data e hora atuais
        data_hora = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        # Monta a mensagem do log
        mensagem = (
            f"[{data_hora}] "
            f"{operacao} - {descricao}\n"
        )

        # Abre o arquivo em modo de adição
        with open(
            CAMINHO_LOG,
            "a",
            encoding="utf-8"
        ) as arquivo:
            arquivo.write(mensagem)

    except OSError as erro:
        print(f"Erro ao gravar log: {erro}")
