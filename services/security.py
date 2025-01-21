import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from services.logger import log_command
import os

# Chave secreta usada para assinar o JWT
SECRET_KEY = "sua_chave_secreta"

SESSION_FOLDER = "sessions"


def createAccessToken(session: str, email: str, expiration_minutes: int = 30):
    global SECRET_KEY
    # Define o payload do token
    payload = {
        "sub": session,  # Identificação do usuário
        "email": email,
        "iat": datetime.now(tz=timezone.utc),  # Hora em que o token foi emitido
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=expiration_minutes)  # Expiração
    }

    # Gera o token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token


def validateToken(token: str):
    global SECRET_KEY
    try:
        # Decodifica e valida o token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Token é válido
        return decoded_token

    except ExpiredSignatureError:
        log_command.debug("Expired token")
        raise
    except InvalidTokenError:
        log_command.error("Invalid token")
        raise
    except Exception as e:
        log_command.error(f"Error validanting token: {e}")
        raise


def saveToken(session: str, token: str) -> None:
    global SESSION_FOLDER
    try:
        with open(f"{SESSION_FOLDER}/{session}", "w") as file:
            file.write(token)
    except Exception as e:
        log_command.error(f'Erro to save token: {e}')
        raise


def getToken(session: str) -> str:
    global SESSION_FOLDER
    try:
        with open(f"{SESSION_FOLDER}/{session}", "r") as file:
            token = file.read()
        return token
    except Exception as e:
        log_command.error(f'Erro to save token: {e}')
        raise


def deleteToken(session: str) -> None:
    global SESSION_FOLDER
    try:
        file_path = f"{SESSION_FOLDER}/{session}"
        os.remove(file_path)
        log_command.info(f"Arquivo {file_path} removido com sucesso!")
    except FileNotFoundError:
        log_command.debug(f"O arquivo {file_path} não foi encontrado.")
        raise
    except PermissionError:
        log_command.error(f"Permissão negada para excluir o arquivo {file_path}.")
        raise

    except Exception as e:
        log_command.error(f'Erro to save token: {e}')
        raise
