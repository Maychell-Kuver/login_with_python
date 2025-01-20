from flask import redirect, url_for, current_app, session, jsonify, make_response
import functools
from flask import Flask as App, request as _request
from services.logger import log_command


class loginRequired:
    def __call__(self):
        def wrapper(inner_function):
            @functools.wraps(inner_function)
            def decorated(*args, **kwargs):
                try:
                    log_command.debug("Vai verificar se tem LOGIN")
                    user = current_app.auth.get_user()
                    if user is None:
                        log_command.debug("USER IS NONE")
                        return redirect(url_for("login"))
                except Exception as e:
                    log_command.debug(f"USER Exception {e}")
                    return redirect(url_for("login"))

                log_command.debug(f'LOGIN VALIDADO COM SUCESSO')
                return inner_function(*args, **kwargs)
            return decorated
        return wrapper


class loginRequiredAPI:
    def __call__(self):
        def wrapper(inner_function):
            @functools.wraps(inner_function)
            def decorated(*args, **kwargs):
                try:
                    user = current_app.auth.get_user()
                    if user is None:
                        return jsonify({"error": "Usuário não autenticado"}), 401
                except:

                    return jsonify({"error": "Usuário não autenticado"}), 401

                return inner_function(*args, **kwargs)
            return decorated
        return wrapper
