from flask import redirect, url_for, current_app, session, jsonify, request
import functools
from services.logger import log_command
from services.security import validateToken, getToken


class loginRequired:
    def __call__(self):
        def wrapper(inner_function):
            @functools.wraps(inner_function)
            def decorated(*args, **kwargs):
                try:
                    session = cookies = request.cookies
                    session = cookies.get("session", None)
                    if session is not None:
                        token = getToken(session)
                        validateToken(token)
                    else:
                        log_command.debug("SESSION IS NONE")
                        return redirect(url_for('login', _external=True))
                except Exception as e:
                    log_command.debug(f"USER Exception {e}")
                    return redirect(url_for('login', _external=True))

                log_command.debug(f'LOGIN VALIDADO COM SUCESSO')
                return inner_function(*args, **kwargs)
            return decorated
        return wrapper
