from datetime import datetime, timedelta

import jwt

from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from app.models.user import User

auth_api_bp = Blueprint(
    "auth_api",
    __name__,
    url_prefix="/api/auth"
)


# =========================
# GENERATE JWT TOKEN
# =========================
def generate_token(user):

    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return token


# =========================
# API LOGIN
# =========================
@auth_api_bp.route(
    "/login",
    methods=["POST"]
)
def api_login():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No data provided."
        }), 400

    email = data.get("email")

    password = data.get("password")

    user = User.query.filter_by(
        email=email
    ).first()

    if not user or not user.check_password(password):

        return jsonify({
            "success": False,
            "message": "Invalid credentials."
        }), 401

    token = generate_token(user)

    return jsonify({
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role.name
        }
    })