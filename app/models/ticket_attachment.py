from app.extensions import db
from app.database import BaseModel


class TicketAttachment(BaseModel):

    __tablename__ = "ticket_attachments"

    # =========================
    # FILE INFO
    # =========================
    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    original_name = db.Column(
        db.String(255),
        nullable=False
    )

    file_path = db.Column(
        db.String(500),
        nullable=False
    )

    file_size = db.Column(
        db.Integer
    )

    mime_type = db.Column(
        db.String(100)
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

    uploaded_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        index=True
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    ticket = db.relationship(
        "Ticket",
        back_populates="attachments",
        lazy="joined"
    )

    uploaded_by = db.relationship(
        "User",
        lazy="joined"
    )

    # =========================
    # HELPERS
    # =========================
    @property
    def uploader_name(self):

        if not self.uploaded_by:
            return "Sistema"

        return self.uploaded_by.full_name

    @property
    def size_label(self):

        if not self.file_size:
            return "N/A"

        size = self.file_size

        if size < 1024:
            return f"{size} B"

        if size < 1024 * 1024:
            return f"{round(size / 1024, 2)} KB"

        return f"{round(size / (1024 * 1024), 2)} MB"

    @property
    def is_image(self):

        if not self.mime_type:
            return False

        return self.mime_type.startswith(
            "image/"
        )

    @property
    def extension(self):

        if "." not in self.original_name:
            return ""

        return self.original_name.rsplit(
            ".",
            1
        )[1].lower()

    # =========================
    # REPRESENTATION
    # =========================
    def __repr__(self):

        return (
            f"<TicketAttachment {self.file_name}>"
        )