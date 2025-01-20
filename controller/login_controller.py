from services.logger import log_command
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import model.login_model as model


def isValidLogin(email: str, password: str) -> bool | None:
    try:
        ph = PasswordHasher()
        stored_hash = model.getUserHash(email)
        if stored_hash is None:
            return None

        if ph.verify(stored_hash, password):
            return True

    except VerifyMismatchError:
        log_command.error(f'Invalid credentials.')
        return False
    except Exception as e:
        log_command.error(f'Erro on validate login credentials: {e}')
        raise
