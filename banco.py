
import sqlite3
from pathlib import Path

# Define o caminho do banco dentro da pasta do projeto
CAMINHO_BANCO = Path(__file__).resolve().parent / "petshop.db"


def conectar():
    # Abre a conexão com o banco
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabela():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_pet TEXT NOT NULL,
                    tutor TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    cep TEXT NOT NULL,
                    logradouro TEXT NOT NULL,
                    bairro TEXT NOT NULL,
                    cidade_uf TEXT NOT NULL,
                    numero TEXT NOT NULL,
                    servico TEXT NOT NULL,
                    data_horario TEXT NOT NULL
                )
            """)

        print("Banco de dados e tabela preparados com sucesso!")

    except sqlite3.Error as erro:
        print(f"Erro ao criar a tabela: {erro}")

    
def cadastrar_agendamento(
    nome_pet, tutor, telefone, cep,
    logradouro, bairro, cidade_uf,
    numero, servico, data_horario
):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO agendamentos (
                    nome_pet, tutor, telefone, cep,
                    logradouro, bairro, cidade_uf,
                    numero, servico, data_horario
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                nome_pet.strip(),
                tutor.strip(),
                telefone.strip(),
                cep.strip(),
                logradouro.strip(),
                bairro.strip(),
                cidade_uf.strip(),
                numero.strip(),
                servico.strip(),
                data_horario.strip()
            ))

            id_agendamento = cursor.lastrowid

        print("Agendamento cadastrado com sucesso!")
        return id_agendamento

    except sqlite3.Error as erro:
        print(f"Erro ao cadastrar agendamento: {erro}")
        return None
    

def listar_agendamentos():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT * FROM agendamentos
                ORDER BY id
            """)

            agendamentos = cursor.fetchall()

        return agendamentos

    except sqlite3.Error as erro:
        print(f"Erro ao listar agendamentos: {erro}")
        return []

    
def atualizar_agendamento(
    id_agendamento, nome_pet, tutor, telefone,
    cep, logradouro, bairro, cidade_uf,
    numero, servico, data_horario
):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE agendamentos
                SET nome_pet = ?,
                    tutor = ?,
                    telefone = ?,
                    cep = ?,
                    logradouro = ?,
                    bairro = ?,
                    cidade_uf = ?,
                    numero = ?,
                    servico = ?,
                    data_horario = ?
                WHERE id = ?
            """, (
                nome_pet.strip(),
                tutor.strip(),
                telefone.strip(),
                cep.strip(),
                logradouro.strip(),
                bairro.strip(),
                cidade_uf.strip(),
                numero.strip(),
                servico.strip(),
                data_horario.strip(),
                id_agendamento
            ))

            registros_alterados = cursor.rowcount

        if registros_alterados > 0:
            print("Agendamento atualizado com sucesso!")
            return True
        else:
            print("Agendamento não encontrado.")
            return False

    except sqlite3.Error as erro:
        print(f"Erro ao atualizar agendamento: {erro}")
        return False
    

    
def excluir_agendamento(id_agendamento):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                DELETE FROM agendamentos
                WHERE id = ?
            """, (id_agendamento,))

            registros_excluidos = cursor.rowcount

        if registros_excluidos > 0:
            print("Agendamento excluído com sucesso!")
            return True
        else:
            print("Agendamento não encontrado.")
            return False

    except sqlite3.Error as erro:
        print(f"Erro ao excluir agendamento: {erro}")
        return False



if __name__ == "__main__":
    criar_tabela()

    try:
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = 'agendamentos'
            """)

            resultado = cursor.fetchone()

            if resultado:
                print("Teste OK: tabela agendamentos encontrada!")
            else:
                print("Teste falhou: tabela não encontrada.")

    except sqlite3.Error as erro:
        print(f"Erro ao verificar tabela: {erro}")

