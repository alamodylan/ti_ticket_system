from app.extensions import db

from app.models.user import User

from app.repositories.user_repository import (
    UserRepository
)

from app.services.audit_service import (
    AuditService
)


class UserService:

    # =========================
    # VALIDATIONS
    # =========================
    @staticmethod
    def _validate_required_fields(
        data,
        require_password=True
    ):

        required = [
            "first_name",
            "last_name",
            "username",
            "email",
            "role_id",
            "site_id"
        ]

        if require_password:

            required.append(
                "password"
            )

        for field in required:

            if not data.get(field):

                raise ValueError(
                    f"{field} es requerido."
                )

    @staticmethod
    def _validate_unique_user(
        email,
        username,
        user_id=None
    ):

        existing_email = UserRepository.get_by_email(
            email
        )

        if (
            existing_email
            and existing_email.id != user_id
        ):

            raise ValueError(
                "El correo ya existe."
            )

        existing_username = UserRepository.get_by_username(
            username
        )

        if (
            existing_username
            and existing_username.id != user_id
        ):

            raise ValueError(
                "El username ya existe."
            )

    # =========================
    # GET ALL USERS
    # =========================
    @staticmethod
    def get_all_users(
        site_id=None
    ):

        try:

            users = UserRepository.get_all()

            if site_id:

                users = [
                    user
                    for user in users
                    if str(user.site_id) == str(site_id)
                ]

            return users

        except Exception:

            return []

    # =========================
    # GET USER BY ID
    # =========================
    @staticmethod
    def get_user_by_id(user_id):

        try:

            return UserRepository.get_by_id(
                user_id
            )

        except Exception:

            return None

    # =========================
    # CREATE USER
    # =========================
    @staticmethod
    def create_user(
        data,
        created_by=None
    ):

        try:

            UserService._validate_required_fields(
                data,
                require_password=True
            )

            UserService._validate_unique_user(
                email=data.get("email"),
                username=data.get("username")
            )

            user = User(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                username=data.get("username"),
                email=data.get("email"),
                role_id=data.get("role_id"),
                site_id=data.get("site_id"),
                department_id=data.get("department_id") or None,
                phone=data.get("phone"),
                is_active=True
            )

            user.set_password(
                data.get("password")
            )

            UserRepository.create(
                user
            )

            db.session.flush()

            try:

                AuditService.log_action(
                    action="user_created",
                    entity="user",
                    entity_id=user.id,
                    details=(
                        f"Usuario creado: {user.full_name}"
                    ),
                    user_id=created_by.id if created_by else None
                )

            except Exception:
                pass

            db.session.commit()

            return {
                "success": True,
                "user": user
            }

        except Exception as e:

            db.session.rollback()

            return {
                "success": False,
                "message": str(e)
            }

    # =========================
    # UPDATE USER
    # =========================
    @staticmethod
    def update_user(
        user_id,
        data,
        updated_by=None
    ):

        try:

            user = UserRepository.get_by_id(
                user_id
            )

            if not user:

                raise ValueError(
                    "Usuario no encontrado."
                )

            UserService._validate_required_fields(
                data,
                require_password=False
            )

            UserService._validate_unique_user(
                email=data.get("email"),
                username=data.get("username"),
                user_id=user.id
            )

            user.first_name = data.get(
                "first_name"
            )

            user.last_name = data.get(
                "last_name"
            )

            user.username = data.get(
                "username"
            )

            user.email = data.get(
                "email"
            )

            user.role_id = data.get(
                "role_id"
            )

            user.site_id = data.get(
                "site_id"
            )

            user.department_id = (
                data.get("department_id") or None
            )

            user.phone = data.get(
                "phone"
            )

            if data.get("password"):

                user.set_password(
                    data.get("password")
                )

            UserRepository.save(
                user
            )

            db.session.flush()

            try:

                AuditService.log_action(
                    action="user_updated",
                    entity="user",
                    entity_id=user.id,
                    details=(
                        f"Usuario actualizado: {user.full_name}"
                    ),
                    user_id=updated_by.id if updated_by else None
                )

            except Exception:
                pass

            db.session.commit()

            return {
                "success": True,
                "user": user
            }

        except Exception as e:

            db.session.rollback()

            return {
                "success": False,
                "message": str(e)
            }

    # =========================
    # DEACTIVATE USER
    # =========================
    @staticmethod
    def deactivate_user(
        user_id,
        deactivated_by=None
    ):

        try:

            user = UserRepository.get_by_id(
                user_id
            )

            if not user:

                raise ValueError(
                    "Usuario no encontrado."
                )

            user.is_active = False

            UserRepository.save(
                user
            )

            db.session.flush()

            try:

                AuditService.log_action(
                    action="user_deactivated",
                    entity="user",
                    entity_id=user.id,
                    details=(
                        f"Usuario desactivado: {user.full_name}"
                    ),
                    user_id=deactivated_by.id if deactivated_by else None
                )

            except Exception:
                pass

            db.session.commit()

            return {
                "success": True
            }

        except Exception as e:

            db.session.rollback()

            return {
                "success": False,
                "message": str(e)
            }