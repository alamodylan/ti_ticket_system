from app.extensions import db
from app.database import BaseModel


class Ticket(BaseModel):

    __tablename__ = "tickets"

    # =========================
    # BASIC INFO
    # =========================
    ticket_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    # =========================
    # REQUESTER INFO
    # =========================
    requester_name = db.Column(
        db.String(150)
    )

    requester_email = db.Column(
        db.String(150),
        index=True
    )

    requester_phone = db.Column(
        db.String(50)
    )

    source = db.Column(
        db.String(50),
        default="manual",
        nullable=False,
        index=True
    )

    email_message_id = db.Column(
        db.String(255),
        unique=True,
        index=True
    )

    email_subject = db.Column(
        db.String(255)
    )

    # =========================
    # STATUS & PRIORITY
    # =========================
    status = db.Column(
        db.String(50),
        default="Nuevo",
        nullable=False,
        index=True
    )

    priority = db.Column(
        db.String(50),
        default="Media",
        nullable=False,
        index=True
    )

    # =========================
    # FOREIGN KEYS
    # =========================
    created_by_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets_ti.users.id"),
        nullable=False,
        index=True
    )

    assigned_to_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets_ti.users.id"),
        index=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets_ti.categories.id"),
        index=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets_ti.departments.id"),
        index=True
    )

    site_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets_ti.sites.id"),
        index=True
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    created_by = db.relationship(
        "User",
        foreign_keys=[created_by_id],
        back_populates="created_tickets",
        lazy="joined"
    )

    assigned_to = db.relationship(
        "User",
        foreign_keys=[assigned_to_id],
        back_populates="assigned_tickets",
        lazy="joined"
    )

    category = db.relationship(
        "Category",
        back_populates="tickets",
        lazy="joined"
    )

    department = db.relationship(
        "Department",
        back_populates="tickets",
        lazy="joined"
    )

    site = db.relationship(
        "Site",
        back_populates="tickets",
        lazy="joined"
    )

    comments = db.relationship(
        "TicketComment",
        back_populates="ticket",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    attachments = db.relationship(
        "TicketAttachment",
        back_populates="ticket",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    # =========================
    # HELPERS
    # =========================
    @property
    def site_name(self):

        if not self.site:
            return "Sin sede"

        return self.site.name

    @property
    def requester_display_name(self):

        if self.requester_name:
            return self.requester_name

        if self.created_by:
            return self.created_by.full_name

        return "Solicitante no disponible"

    @property
    def requester_display_email(self):

        if self.requester_email:
            return self.requester_email

        if self.created_by:
            return self.created_by.email

        return "Sin correo"

    @property
    def source_label(self):

        labels = {
            "manual": "Manual",
            "email": "Correo electrónico",
            "system": "Sistema"
        }

        return labels.get(
            self.source,
            self.source
        )

    @property
    def status_badge_class(self):

        classes = {
            "Nuevo": "bg-primary",
            "Asignado": "bg-info",
            "En Progreso": "bg-warning text-dark",
            "Pendiente": "bg-secondary",
            "Resuelto": "bg-success",
            "Cerrado": "bg-dark"
        }

        return classes.get(
            self.status,
            "bg-secondary"
        )

    @property
    def priority_badge_class(self):

        classes = {
            "Baja": "bg-success",
            "Media": "bg-primary",
            "Alta": "bg-warning text-dark",
            "Crítica": "bg-danger"
        }

        return classes.get(
            self.priority,
            "bg-secondary"
        )

    @property
    def comments_count(self):

        try:
            return self.comments.count()

        except Exception:
            return 0

    @property
    def attachments_count(self):

        try:
            return self.attachments.count()

        except Exception:
            return 0

    def __repr__(self):

        return (
            f"<Ticket {self.ticket_number}>"
        )