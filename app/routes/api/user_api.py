from flask import (
    Blueprint,
    jsonify
)

from app.models.user import User

user_api_bp = Blueprint(
    "user_api",
    __name__,
    url_prefix="/api/users"
)


# =========================
# GET USERS
# =========================
@user_api_bp.route(
    "/",
    methods=["GET"]
)
def get_users():

    users = User.query.order_by(
        User.first_name.asc()
    ).all()

    data = []

    for user in users:

        data.append({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "username": user.username,
            "role": (
                user.role.name
                if user.role
                else None
            ),
            "department": (
                user.department.name
                if user.department
                else None
            ),
            "is_active": user.is_active
        })

    return jsonify(data)


# =========================
# GET USER DETAIL
# =========================
@user_api_bp.route(
    "/<int:user_id>",
    methods=["GET"]
)
def get_user(user_id):

    user = User.query.get_or_404(
        user_id
    )

    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name,
        "email": user.email,
        "username": user.username,
        "phone": user.phone,
        "role": (
            user.role.name
            if user.role
            else None
        ),
        "department": (
            user.department.name
            if user.department
            else None
        ),
        "created_at": (
            user.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    })