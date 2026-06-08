class PermissionService:

    # =========================
    # CHECK PERMISSION
    # =========================
    @staticmethod
    def has_permission(
        user,
        permission_code
    ):

        if not user:
            return False

        return user.has_permission(
            permission_code
        )

    # =========================
    # CHECK ROLE
    # =========================
    @staticmethod
    def has_role(
        user,
        role_name
    ):

        if not user:
            return False

        if not user.role:
            return False

        return (
            user.role.name.lower()
            == role_name.lower()
        )

    # =========================
    # CHECK ADMIN
    # =========================
    @staticmethod
    def is_admin(user):

        if not user:
            return False

        if not user.role:
            return False

        admin_roles = [
            "admin",
            "super admin"
        ]

        return (
            user.role.name.lower()
            in admin_roles
        )

    # =========================
    # CHECK IT STAFF
    # =========================
    @staticmethod
    def is_it_staff(user):

        if not user:
            return False

        if not user.department:
            return False

        return (
            user.department.name.lower()
            in [
                "ti",
                "tecnologia",
                "informatica",
                "it"
            ]
        )