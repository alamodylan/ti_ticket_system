from app.extensions import db

from app.models.audit_log import (
    AuditLog
)


class AuditRepository:

    # =========================
    # CREATE AUDIT LOG
    # =========================
    @staticmethod
    def create(**kwargs):

        audit_log = AuditLog(
            **kwargs
        )

        db.session.add(audit_log)

        return audit_log

    # =========================
    # GET ALL LOGS
    # =========================
    @staticmethod
    def get_all():

        return (
            AuditLog.query
            .order_by(
                AuditLog.created_at.desc()
            )
            .all()
        )

    # =========================
    # GET RECENT LOGS
    # =========================
    @staticmethod
    def get_recent(limit=50):

        return (
            AuditLog.query
            .order_by(
                AuditLog.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    # =========================
    # GET BY ID
    # =========================
    @staticmethod
    def get_by_id(log_id):

        return db.session.get(
            AuditLog,
            log_id
        )

    # =========================
    # GET BY USER
    # =========================
    @staticmethod
    def get_by_user(user_id):

        return (
            AuditLog.query
            .filter_by(
                user_id=user_id
            )
            .order_by(
                AuditLog.created_at.desc()
            )
            .all()
        )

    # =========================
    # GET BY ENTITY
    # =========================
    @staticmethod
    def get_by_entity(
        entity,
        entity_id
    ):

        return (
            AuditLog.query
            .filter_by(
                entity=entity,
                entity_id=entity_id
            )
            .order_by(
                AuditLog.created_at.desc()
            )
            .all()
        )

    # =========================
    # DELETE AUDIT LOG
    # =========================
    @staticmethod
    def delete(audit_log):

        db.session.delete(audit_log)