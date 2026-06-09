from app.extensions import db
from app.database import BaseModel


# =========================
# MANY TO MANY
# =========================
role_permissions = db.Table(
    "role_permissions",
    db.metadata,

    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("tickets_ti.roles.id"),
        primary_key=True
    ),

    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("tickets_ti.permissions.id"),
        primary_key=True
    ),

    db.Index(
        "ix_role_permissions_role_id",
        "role_id"
    ),

    db.Index(
        "ix_role_permissions_permission_id",
        "permission_id"
    ),

    schema="tickets_ti"
)


class Role(BaseModel):

    __tablename__ = "roles"

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text
    )

    permissions = db.relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
        lazy="dynamic"
    )

    users = db.relationship(
        "User",
        back_populates="role",
        lazy="dynamic"
    )

    def has_permission(
        self,
        permission_code
    ):

        return (
            self.permissions
            .filter_by(
                code=permission_code
            )
            .first()
            is not None
        )

    @property
    def users_count(self):

        try:
            return self.users.count()

        except Exception:
            return 0

    @property
    def permissions_count(self):

        try:
            return self.permissions.count()

        except Exception:
            return 0

    @property
    def is_admin_role(self):

        return (
            self.name.lower()
            == "administrador"
        )

    @property
    def display_name(self):

        return self.name

    def __repr__(self):

        return (
            f"<Role {self.name}>"
        )