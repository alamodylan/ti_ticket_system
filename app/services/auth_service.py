import os

from app.extensions import db

from app.repositories.user_repository import (
    UserRepository
)

from app.services.audit_service import (
    AuditService
)


class AuthService:

    @staticmethod
    def authenticate_user(
        email,
        password
    ):

        if not email or not password:

            raise ValueError(
                "Email y contraseña son requeridos."
            )

        email = (
            email
            .strip()
            .lower()
        )

        user = UserRepository.get_by_email(
            email
        )

        print(
            f"DEBUG AUTH EMAIL: {email}"
        )

        print(
            f"DEBUG AUTH USER FOUND: {user is not None}"
        )

        if not user:

            raise ValueError(
                "Credenciales inválidas."
            )

        print(
            f"DEBUG AUTH USER ID: {user.id}"
        )

        print(
            f"DEBUG AUTH USER ACTIVE: {user.is_active}"
        )

        password_ok = user.check_password(
            password
        )

        print(
            f"DEBUG AUTH PASSWORD OK: {password_ok}"
        )

        # =========================
        # TEMP ADMIN RECOVERY
        # =========================
        recovery_email = os.getenv(
            "ADMIN_RECOVERY_EMAIL",
            ""
        ).strip().lower()

        recovery_password = os.getenv(
            "ADMIN_RECOVERY_PASSWORD",
            ""
        )

        if (
            not password_ok
            and recovery_email
            and recovery_password
            and email == recovery_email
            and password == recovery_password
        ):

            user.set_password(
                recovery_password
            )

            db.session.add(user)
            db.session.commit()

            password_ok = True

            print(
                "DEBUG ADMIN RECOVERY PASSWORD UPDATED"
            )

        if not password_ok:

            raise ValueError(
                "Credenciales inválidas."
            )

        if not user.is_active:

            raise ValueError(
                "Usuario inactivo."
            )

        try:

            AuditService.log_action(
                action="user_login",
                entity="user",
                entity_id=user.id,
                details=(
                    f"Usuario "
                    f"{user.email} "
                    f"inició sesión"
                ),
                user_id=user.id
            )

        except Exception as e:

            print(
                f"Audit log error: {str(e)}"
            )

        return user