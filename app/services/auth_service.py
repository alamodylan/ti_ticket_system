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

        user = UserRepository.get_by_email(
            email
        )

        if not user:

            raise ValueError(
                "Credenciales inválidas."
            )

        if not user.check_password(
            password
        ):

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