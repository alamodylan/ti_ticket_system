from app.extensions import db

from app.models.ticket_attachment import (
    TicketAttachment
)


class TicketAttachmentRepository:

    @staticmethod
    def create(**kwargs):

        attachment = TicketAttachment(
            **kwargs
        )

        db.session.add(attachment)

        return attachment

    @staticmethod
    def get_by_id(attachment_id):

        return db.session.get(
            TicketAttachment,
            attachment_id
        )

    @staticmethod
    def get_by_ticket(ticket_id):

        return (
            TicketAttachment.query
            .filter_by(
                ticket_id=ticket_id
            )
            .order_by(
                TicketAttachment.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def delete(attachment):

        db.session.delete(attachment)