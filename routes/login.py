from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flasgger.utils import swag_from
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from controller import login_controller as lc


login_bp = Blueprint('person', __name__)


@login_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Empty email or password"}), 400
    isValidLogin = lc.isValidLogin(email, password)

    if isValidLogin is None:
        return jsonify({'message': "User not registered"}), 404
    elif isValidLogin:
        access_token = create_access_token(identity={"email": email})
        return jsonify({
            "message": "Logged in successfully",
            "redirect_url": url_for('home', _external=True),
            "access_token": access_token
        }), 200

    return jsonify({'error': "User not authorized"}), 401
