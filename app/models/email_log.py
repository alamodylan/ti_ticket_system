from app.extensions import db
from app.database import BaseModel


class EmailLog(BaseModel):

    __tablename__ = "email_logs"

    subject = db.Column(
        db.String(255),
        nullable=False
    )

    recipients = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="sent",
        nullable=False,
        index=True
    )

    error_message = db.Column(
        db.Text
    )

    sent_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        index=True
    )

    def __repr__(self):

        return (
            f"<EmailLog {self.subject}>"
        )