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


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# =========================
# REGISTER DISABLED
# =========================
@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    flash(
        "El registro público está deshabilitado. Solo el administrador puede acceder al sistema.",
        "warning"
    )

    return redirect(
        url_for("auth.login")
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

            if not user:

                flash(
                    "Correo o contraseña incorrectos.",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
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

    flash(
        "La recuperación de contraseña todavía no está habilitada.",
        "warning"
    )

    return redirect(
        url_for("auth.login")
    )


# =========================
# RESET PASSWORD
# =========================
@auth_bp.route(
    "/reset-password/<token>",
    methods=["GET", "POST"]
)
def reset_password(token):

    flash(
        "La recuperación de contraseña todavía no está habilitada.",
        "warning"
    )

    return redirect(
        url_for("auth.login")
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