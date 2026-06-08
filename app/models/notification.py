from app.extensions import db
from app.database import BaseModel


class Notification(BaseModel):

    __tablename__ = "notifications"

    title = db.Column(
        db.String(255),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    user = db.relationship(
        "User",
        back_populates="notifications"
    )

    def __repr__(self):

        return (
            f"<Notification {self.id}>"
        )