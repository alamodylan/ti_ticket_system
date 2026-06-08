from app.extensions import db
from app.database import BaseModel


class Category(BaseModel):

    __tablename__ = "categories"

    name = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text
    )

    tickets = db.relationship(
        "Ticket",
        back_populates="category",
        lazy="dynamic"
    )

    @property
    def tickets_count(self):

        try:
            return self.tickets.count()

        except Exception:
            return 0

    @property
    def open_tickets_count(self):

        try:
            from app.models.ticket import Ticket

            return self.tickets.filter(
                Ticket.status.notin_([
                    "Resuelto",
                    "Cerrado"
                ])
            ).count()

        except Exception:
            return 0

    def __repr__(self):

        return (
            f"<Category {self.name}>"
        )