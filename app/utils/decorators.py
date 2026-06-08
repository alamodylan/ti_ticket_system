from functools import wraps

from flask import (
    abort
)

from flask_login import (
    current_user
)


# =========================
# PERMISSION REQUIRED
# =========================
def permission_required(permission_code):

    def decorator(function):

        @wraps(function)
        def decorated_function(*args, **kwargs):

            if not current_user.is_authenticated:
                abort(401)

            if not current_user.has_permission(
                permission_code
            ):
                abort(403)

            return function(
                *args,
                **kwargs
            )

        return decorated_function

    return decorator


# =========================
# ADMIN REQUIRED
# =========================
def admin_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            abort(401)

        if current_user.role.name.lower() not in [
            "admin",
            "super admin"
        ]:
            abort(403)

        return function(
            *args,
            **kwargs
        )

    return decorated_function