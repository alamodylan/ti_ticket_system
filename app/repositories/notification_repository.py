from app.extensions import db

from app.models.notification import (
    Notification
)


class NotificationRepository:

    # =========================
    # GET ALL
    # =========================
    @staticmethod
    def get_all():

        return Notification.query.order_by(
            Notification.created_at.desc()
        ).all()

    # =========================
    # GET BY ID
    # =========================
    @staticmethod
    def get_by_id(notification_id):

        return db.session.get(
            Notification,
            notification_id
        )

    # =========================
    # GET BY USER
    # =========================
    @staticmethod
    def get_by_user(user_id):

        return Notification.query.filter_by(
            user_id=user_id
        ).order_by(
            Notification.created_at.desc()
        ).all()

    # =========================
    # GET UNREAD BY USER
    # =========================
    @staticmethod
    def get_unread_by_user(user_id):

        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).order_by(
            Notification.created_at.desc()
        ).all()

    # =========================
    # CREATE NOTIFICATION
    # =========================
    @staticmethod
    def create(**kwargs):

        notification = Notification(
            **kwargs
        )

        db.session.add(notification)

        return notification

    # =========================
    # DELETE NOTIFICATION
    # =========================
    @staticmethod
    def delete(notification):

        db.session.delete(notification)

    # =========================
    # MARK ALL AS READ
    # =========================
    @staticmethod
    def mark_all_as_read(user_id):

        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).all()

        for notification in notifications:

            notification.is_read = True

        return notifications

    # =========================
    # COUNT UNREAD
    # =========================
    @staticmethod
    def count_unread(user_id):

        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()