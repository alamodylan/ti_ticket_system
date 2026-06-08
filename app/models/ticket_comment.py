from app.extensions import db
from app.database import BaseModel


class TicketComment(BaseModel):

    __tablename__ = "ticket_comments"

    # =========================
    # COMMENT CONTENT
    # =========================
    comment = db.Column(
        db.Text,
        nullable=False
    )

    comment_type = db.Column(
        db.String(30),
        default="user",
        nullable=False,
        index=True
    )

    # =========================
    # FOREIGN KEYS
    # =========================
    ticket_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets.id"),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    ticket = db.relationship(
        "Ticket",
        back_populates="comments",
        lazy="joined"
    )

    user = db.relationship(
        "User",
        back_populates="comments",
        lazy="joined"
    )

    # =========================
    # HELPERS
    # =========================
    @property
    def author_name(self):

        if not self.user:
            return "Usuario eliminado"

        return self.user.full_name

    @property
    def type_label(self):

        labels = {
            "user": "Usuario",
            "technical": "Responsable TI",
            "internal": "Interno"
        }

        return labels.get(
            self.comment_type,
            "Usuario"
        )

    @property
    def type_badge_class(self):

        classes = {
            "user": "bg-primary",
            "technical": "bg-success",
            "internal": "bg-dark"
        }

        return classes.get(
            self.comment_type,
            "bg-secondary"
        )

    @property
    def is_internal(self):

        return (
            self.comment_type
            == "internal"
        )

    @property
    def short_comment(self):

        if len(self.comment) <= 100:
            return self.comment

        return (
            self.comment[:100] + "..."
        )

    # =========================
    # REPRESENTATION
    # =========================
    def __repr__(self):

        return (
            f"<TicketComment {self.id}>"
        )