from app.extensions import db

from app.models.ticket_comment import (
    TicketComment
)


class TicketCommentRepository:

    # =========================
    # CREATE COMMENT
    # =========================
    @staticmethod
    def create(**kwargs):

        comment = TicketComment(
            **kwargs
        )

        db.session.add(comment)

        return comment

    # =========================
    # GET COMMENT BY ID
    # =========================
    @staticmethod
    def get_by_id(comment_id):

        return db.session.get(
            TicketComment,
            comment_id
        )

    # =========================
    # GET COMMENTS BY TICKET
    # =========================
    @staticmethod
    def get_by_ticket(ticket_id):

        return (
            TicketComment.query
            .filter_by(
                ticket_id=ticket_id
            )
            .order_by(
                TicketComment.created_at.asc()
            )
            .all()
        )

    # =========================
    # COUNT COMMENTS
    # =========================
    @staticmethod
    def count_by_ticket(ticket_id):

        return (
            TicketComment.query
            .filter_by(
                ticket_id=ticket_id
            )
            .count()
        )

    # =========================
    # DELETE COMMENT
    # =========================
    @staticmethod
    def delete(comment):

        db.session.delete(comment)