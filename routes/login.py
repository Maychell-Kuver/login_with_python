from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from flasgger.utils import swag_from
from services import security as sec
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
        cookies = request.cookies
        session = cookies.get("session", None)
        if session is None:
            return jsonify({"error": "Error. Please contact suport."}), 500

        access_token = sec.createAccessToken(session, email)
        sec.saveToken(session, access_token)
        return jsonify({
            "message": "Logged in successfully",
            "redirect_url": url_for('home', _external=True),
        }), 200

    return jsonify({'error': "User not authorized"}), 401
