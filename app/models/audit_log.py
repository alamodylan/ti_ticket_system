from app.extensions import db
from app.database import BaseModel


class AuditLog(BaseModel):

    __tablename__ = "audit_logs"

    action = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    entity = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    entity_id = db.Column(
        db.Integer,
        nullable=True,
        index=True
    )

    details = db.Column(
        db.Text,
        nullable=True
    )

    ip_address = db.Column(
        db.String(100),
        nullable=True
    )

    user_agent = db.Column(
        db.Text,
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    user = db.relationship(
        "User",
        backref="audit_logs",
        lazy="joined"
    )

    # =========================
    # HELPERS
    # =========================
    @property
    def actor_name(self):

        if not self.user:
            return "Sistema"

        return self.user.full_name

    @property
    def short_details(self):

        if not self.details:
            return "-"

        if len(self.details) <= 100:
            return self.details

        return self.details[:100] + "..."

    @property
    def action_label(self):

        labels = {
            "ticket_created": "Ticket Creado",
            "ticket_updated": "Ticket Actualizado",
            "ticket_status_updated": "Estado Actualizado",
            "ticket_priority_updated": "Prioridad Actualizada",
            "ticket_comment_created": "Comentario Agregado",
            "user_created": "Usuario Creado",
            "user_updated": "Usuario Actualizado",
            "user_deleted": "Usuario Eliminado"
        }

        return labels.get(
            self.action,
            self.action.replace("_", " ").title()
        )

    # =========================
    # REPRESENTATION
    # =========================
    def __repr__(self):

        return (
            f"<AuditLog {self.action}>"
        )