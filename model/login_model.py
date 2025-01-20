from services.logger import log_command
import sqlite3


def getUserHash(email: str) -> str | None:
    try:
        with sqlite3.connect('login.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE `email` = ?;", (email,))
            user_query = cursor.fetchone()
            if user_query:
                return user_query[0]
            else:
                return None

    except Exception as e:
        log_command.error(f'Error on get user hash: {e}')
        raise
