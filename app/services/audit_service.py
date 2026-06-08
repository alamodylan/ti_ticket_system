from flask import (
    request,
    has_request_context
)

from app.repositories.audit_repository import (
    AuditRepository
)


class AuditService:

    # =========================
    # LOG ACTION
    # =========================
    @staticmethod
    def log_action(
        action,
        entity,
        entity_id=None,
        details=None,
        user_id=None
    ):

        if not action:

            raise ValueError(
                "La acción es requerida."
            )

        if not entity:

            raise ValueError(
                "La entidad es requerida."
            )

        ip_address = None
        user_agent = None

        if has_request_context():

            ip_address = request.remote_addr

            user_agent = (
                request.user_agent.string
            )

        return AuditRepository.create(
            action=action,
            entity=entity,
            entity_id=entity_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            user_id=user_id
        )

    # =========================
    # GET TICKET HISTORY
    # =========================
    @staticmethod
    def get_ticket_history(ticket_id):

        try:

            return AuditRepository.get_by_entity(
                entity="ticket",
                entity_id=ticket_id
            )

        except Exception:

            return []

    # =========================
    # GET USER HISTORY
    # =========================
    @staticmethod
    def get_user_history(user_id):

        try:

            return AuditRepository.get_by_user(
                user_id
            )

        except Exception:

            return []

    # =========================
    # GET RECENT LOGS
    # =========================
    @staticmethod
    def get_recent_logs(limit=50):

        try:

            return AuditRepository.get_recent(
                limit=limit
            )

        except Exception:

            return []