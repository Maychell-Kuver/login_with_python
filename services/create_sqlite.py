import sqlite3
from argon2 import PasswordHasher


def create_database():

    try:
        # Conectar ao banco de dados (ou criar um novo arquivo SQLite)
        ph = PasswordHasher()
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()

        # Criar tabela 'person_types'
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email VARCHAR(50) NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
        ''')

        cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", ("teste123@gmail.com", ph.hash("123")))
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Ocorreu um erro ao criar a base de dados: {e}")
        return False


if __name__ == '__main__':
    create_database()
    print("Banco de dados e tabelas criados com sucesso!")
