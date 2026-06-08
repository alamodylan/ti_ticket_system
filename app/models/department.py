from app.extensions import db
from app.database import BaseModel


class Department(BaseModel):

    __tablename__ = "departments"

    # =========================
    # BASIC INFO
    # =========================
    name = db.Column(
        db.String(150),
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
    users = db.relationship(
        "User",
        back_populates="department",
        lazy="dynamic"
    )

    tickets = db.relationship(
        "Ticket",
        back_populates="department",
        lazy="dynamic"
    )

    # =========================
    # HELPERS
    # =========================
    @property
    def users_count(self):

        try:

            return self.users.count()

        except Exception:

            return 0

    @property
    def tickets_count(self):

        try:

            return self.tickets.count()

        except Exception:

            return 0

    @property
    def active_users_count(self):

        try:

            return self.users.filter_by(
                is_active=True
            ).count()

        except Exception:

            return 0

    # =========================
    # REPRESENTATION
    # =========================
    def __repr__(self):

        return (
            f"<Department {self.name}>"
        )