from sqlalchemy import or_

from app.extensions import db
from app.models.ticket import Ticket


class TicketRepository:

    # =========================
    # NORMALIZE SITE ID
    # =========================
    @staticmethod
    def _normalize_site_id(site_id):

        if site_id in [None, "", "None"]:
            return None

        try:
            return int(site_id)
        except Exception:
            return None

    # =========================
    # CREATE TICKET
    # =========================
    @staticmethod
    def create(**kwargs):

        ticket = Ticket(**kwargs)

        db.session.add(ticket)

        return ticket

    # =========================
    # SAVE TICKET
    # =========================
    @staticmethod
    def save(ticket):

        db.session.add(ticket)

        return ticket

    # =========================
    # GET ALL TICKETS
    # =========================
    @staticmethod
    def get_all(user=None):

        query = Ticket.query

        if user and not user.is_admin:
            query = query.filter(
                or_(
                    Ticket.created_by_id == user.id,
                    Ticket.assigned_to_id == user.id
                )
            )

        return (
            query
            .order_by(Ticket.created_at.desc())
            .all()
        )

    # =========================
    # GET TICKET BY ID
    # =========================
    @staticmethod
    def get_by_id(ticket_id, user=None):

        ticket = db.session.get(
            Ticket,
            ticket_id
        )

        if not ticket:
            return None

        if user and user.is_admin:
            return ticket

        if user:
            if (
                ticket.created_by_id == user.id
                or ticket.assigned_to_id == user.id
            ):
                return ticket
            return None

        return ticket

    # =========================
    # GET BY TICKET NUMBER
    # =========================
    @staticmethod
    def get_by_ticket_number(ticket_number):

        return (
            Ticket.query
            .filter_by(ticket_number=ticket_number)
            .first()
        )

    # =========================
    # GET BY EMAIL MESSAGE ID
    # =========================
    @staticmethod
    def get_by_email_message_id(email_message_id):

        if not email_message_id:
            return None

        return (
            Ticket.query
            .filter_by(email_message_id=email_message_id)
            .first()
        )

    # =========================
    # EMAIL TICKET EXISTS
    # =========================
    @staticmethod
    def email_ticket_exists(email_message_id):

        if not email_message_id:
            return False

        ticket = TicketRepository.get_by_email_message_id(
            email_message_id
        )

        return ticket is not None

    # =========================
    # DELETE TICKET
    # =========================
    @staticmethod
    def delete(ticket):

        db.session.delete(ticket)

    # =========================
    # FILTER TICKETS
    # =========================
    @staticmethod
    def filter_tickets(
        user,
        search=None,
        status=None,
        priority=None,
        site_id=None
    ):

        site_id = TicketRepository._normalize_site_id(
            site_id
        )

        query = Ticket.query

        if not user.is_admin:
            query = query.filter(
                or_(
                    Ticket.created_by_id == user.id,
                    Ticket.assigned_to_id == user.id
                )
            )

        if user.is_admin and site_id is not None:
            query = query.filter(
                Ticket.site_id == site_id
            )

        if search:
            query = query.filter(
                or_(
                    Ticket.ticket_number.ilike(f"%{search}%"),
                    Ticket.title.ilike(f"%{search}%"),
                    Ticket.description.ilike(f"%{search}%"),
                    Ticket.requester_name.ilike(f"%{search}%"),
                    Ticket.requester_email.ilike(f"%{search}%")
                )
            )

        if status:
            query = query.filter(
                Ticket.status == status
            )

        if priority:
            query = query.filter(
                Ticket.priority == priority
            )

        return (
            query
            .order_by(Ticket.created_at.desc())
            .all()
        )

    # =========================
    # GET RECENT TICKETS
    # =========================
    @staticmethod
    def get_recent(
        user,
        limit=10,
        site_id=None
    ):

        site_id = TicketRepository._normalize_site_id(
            site_id
        )

        query = Ticket.query

        if not user.is_admin:
            query = query.filter(
                or_(
                    Ticket.created_by_id == user.id,
                    Ticket.assigned_to_id == user.id
                )
            )

        if user.is_admin and site_id is not None:
            query = query.filter(
                Ticket.site_id == site_id
            )

        return (
            query
            .order_by(Ticket.created_at.desc())
            .limit(limit)
            .all()
        )

    # =========================
    # GET USER TICKETS
    # =========================
    @staticmethod
    def get_user_tickets(user_id):

        return (
            Ticket.query
            .filter(
                or_(
                    Ticket.created_by_id == user_id,
                    Ticket.assigned_to_id == user_id
                )
            )
            .order_by(Ticket.created_at.desc())
            .all()
        )