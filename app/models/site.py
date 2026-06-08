from app.extensions import db
from app.database import BaseModel


class Site(BaseModel):

    __tablename__ = "sites"

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
        db.String(50),
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
        back_populates="site",
        lazy="dynamic"
    )

    tickets = db.relationship(
        "Ticket",
        back_populates="site",
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
    def active_users_count(self):

        try:

            return self.users.filter_by(
                is_active=True
            ).count()

        except Exception:

            return 0

    @property
    def tickets_count(self):

        try:

            return self.tickets.count()

        except Exception:

            return 0

    @property
    def display_name(self):

        return (
            f"{self.code} - {self.name}"
        )

    # =========================
    # REPRESENTATION
    # =========================
    def __repr__(self):

        return (
            f"<Site {self.code}>"
        )