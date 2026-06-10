from app.repositories.user_repository import (
    UserRepository
)

from app.services.audit_service import (
    AuditService
)


class AuthService:

    # =========================
    # AUTHENTICATE USER
    # =========================
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

        print(
            f"DEBUG AUTH HASH START: {user.password_hash[:10] if user.password_hash else 'NO_HASH'}"
        )

        password_ok = user.check_password(
            password
        )

        print(
            f"DEBUG AUTH PASSWORD OK: {password_ok}"
        )

        if not password_ok:

            raise ValueError(
                "Credenciales inválidas."
            )

        # =========================
        # VALIDATE ACTIVE USER
        # =========================
        if not user.is_active:

            raise ValueError(
                "Usuario inactivo."
            )

        # =========================
        # AUDIT LOGIN
        # =========================
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