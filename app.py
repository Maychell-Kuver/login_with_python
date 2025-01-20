from flask import Flask, jsonify, render_template, request, url_for, session, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from datetime import datetime
from flasgger import Swagger
from flask_session import Session
from services.logger import log_command
from dotenv import load_dotenv
from routes.login import login_bp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
import os


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = "eu_nao_sei"
jwt = JWTManager(app)
# Session(app)

# app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Status variables
api_version = '1.0.0'
api_start_time = datetime.now()
last_request_timestamp = ''

# Swagger configuration
app.config['SWAGGER'] = {
    'title': 'Controle Acesso Restaurante - API',
    'version': api_version,
    'description': 'API que auxilia na cobrança para cada acesso no restaurante.',
    'swagger_ui': True,
    'specs_route': '/docs'
}

swagger = Swagger(app)

app.register_blueprint(login_bp)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    try:
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        return render_template('home.html')
    except Exception as e:
        log_command.error(f'Error: {e}')
        # return jsonify({'error': "User not authorized", "redirect_url": url_for('home', _external=True)}), 401

        return redirect(url_for('login', _external=True))


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": type(e).__name__, "message": str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": "Resource not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
