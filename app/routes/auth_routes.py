from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.services.auth_service import AuthService
from app.models.role import Role
from app.models.user import User
from app.extensions import db


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# =========================
# REGISTER
# =========================
@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard.index")
        )

    if request.method == "POST":

        try:

            first_name = request.form.get(
                "first_name"
            )

            last_name = request.form.get(
                "last_name"
            )

            username = request.form.get(
                "username"
            )

            email = request.form.get(
                "email"
            )

            password = request.form.get(
                "password"
            )

            confirm_password = request.form.get(
                "confirm_password"
            )

            # =========================
            # VALIDATIONS
            # =========================
            if password != confirm_password:

                flash(
                    "Las contraseñas no coinciden.",
                    "danger"
                )

                return redirect(
                    url_for("auth.register")
                )

            existing_user = User.query.filter(
                (
                    User.email == email
                ) |
                (
                    User.username == username
                )
            ).first()

            if existing_user:

                flash(
                    "El usuario o correo ya existe.",
                    "danger"
                )

                return redirect(
                    url_for("auth.register")
                )

            # =========================
            # DEFAULT ROLE
            # =========================
            role = Role.query.filter_by(
                name="Técnico"
            ).first()

            if not role:

                role = Role.query.first()

            if not role:

                flash(
                    "No existen roles creados.",
                    "danger"
                )

                return redirect(
                    url_for("auth.register")
                )

            # =========================
            # CREATE USER
            # =========================
            user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                role_id=role.id
            )

            user.set_password(password)

            db.session.add(user)

            db.session.commit()

            flash(
                "Cuenta creada correctamente.",
                "success"
            )

            return redirect(
                url_for("auth.login")
            )

        except Exception as e:

            db.session.rollback()

            flash(
                str(e),
                "danger"
            )

    return render_template(
        "auth/register.html"
    )


# =========================
# LOGIN
# =========================
@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard.index")
        )

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        try:

            user = AuthService.authenticate_user(
                email=email,
                password=password
            )

            login_user(user)

            flash(
                "Inicio de sesión exitoso.",
                "success"
            )

            return redirect(
                url_for("dashboard.index")
            )

        except ValueError as e:

            flash(
                str(e),
                "danger"
            )

        except Exception:

            flash(
                "Error inesperado al iniciar sesión.",
                "danger"
            )

    return render_template(
        "auth/login.html"
    )


# =========================
# FORGOT PASSWORD
# =========================
@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    return render_template(
        "auth/forgot_password.html"
    )


# =========================
# RESET PASSWORD
# =========================
@auth_bp.route(
    "/reset-password/<token>",
    methods=["GET", "POST"]
)
def reset_password(token):

    return render_template(
        "auth/reset_password.html",
        token=token
    )


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "info"
    )

    return redirect(
        url_for("auth.login")
    )