from app.extensions import db
from app.database import BaseModel
from app.models.role import role_permissions


class Permission(BaseModel):

    __tablename__ = "permissions"

    # =========================
    # BASIC INFO
    # =========================
    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    code = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    roles = db.relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions",
        lazy="dynamic"
    )

    # =========================
    # HELPERS
    # =========================
    @property
    def roles_count(self):

        try:

            return self.roles.count()

        except Exception:

            return 0

    @property
    def display_name(self):

        return self.name

    # =========================
    # REPRESENTATION
    # =========================
    def __repr__(self):

        return (
            f"<Permission {self.code}>"
        )