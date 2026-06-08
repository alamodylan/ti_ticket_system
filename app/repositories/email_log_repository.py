# app/repositories/email_log_repository.py

from app.extensions import db

from app.models.email_log import (
    EmailLog
)


class EmailLogRepository:

    # =========================
    # CREATE EMAIL LOG
    # =========================
    @staticmethod
    def create(**kwargs):

        log = EmailLog(
            **kwargs
        )

        db.session.add(log)

        return log

    # =========================
    # GET ALL LOGS
    # =========================
    @staticmethod
    def get_all():

        return EmailLog.query.order_by(
            EmailLog.created_at.desc()
        ).all()

    # =========================
    # GET BY ID
    # =========================
    @staticmethod
    def get_by_id(log_id):

        return db.session.get(
            EmailLog,
            log_id
        )

    # =========================
    # GET SENT EMAILS
    # =========================
    @staticmethod
    def get_sent():

        return EmailLog.query.filter_by(
            status="sent"
        ).order_by(
            EmailLog.created_at.desc()
        ).all()

    # =========================
    # GET FAILED EMAILS
    # =========================
    @staticmethod
    def get_failed():

        return EmailLog.query.filter_by(
            status="failed"
        ).order_by(
            EmailLog.created_at.desc()
        ).all()

    # =========================
    # DELETE LOG
    # =========================
    @staticmethod
    def delete(log):

        db.session.delete(log)