from functools import wraps

from flask import (
    flash,
    redirect,
    url_for
)

from flask_login import (
    current_user,
    login_required
)

from app.services.permission_service import (
    PermissionService
)


# =========================
# PERMISSION REQUIRED
# =========================
def permission_required(
    permission_code
):

    def decorator(func):

        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):

            has_permission = (
                PermissionService.has_permission(
                    current_user,
                    permission_code
                )
            )

            if not has_permission:

                flash(
                    "No tiene permisos para acceder.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "dashboard.index"
                    )
                )

            return func(
                *args,
                **kwargs
            )

        return wrapper

    return decorator


# =========================
# ADMIN REQUIRED
# =========================
def admin_required(func):

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if not PermissionService.is_admin(
            current_user
        ):

            flash(
                "Acceso restringido.",
                "danger"
            )

            return redirect(
                url_for(
                    "dashboard.index"
                )
            )

        return func(
            *args,
            **kwargs
        )

    return wrapper


# =========================
# IT STAFF REQUIRED
# =========================
def it_staff_required(func):

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if not PermissionService.is_it_staff(
            current_user
        ):

            flash(
                "Acceso solo para TI.",
                "danger"
            )

            return redirect(
                url_for(
                    "dashboard.index"
                )
            )

        return func(
            *args,
            **kwargs
        )

    return wrapper