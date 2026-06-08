# app/services/notification_service.py

from app.repositories.notification_repository import (
    NotificationRepository
)


class NotificationService:

    # =========================
    # CREATE NOTIFICATION
    # =========================
    @staticmethod
    def create_notification(
        user_id,
        title,
        message
    ):

        if not user_id:

            raise ValueError(
                "El user_id es requerido."
            )

        if not title:

            raise ValueError(
                "El título es requerido."
            )

        if not message:

            raise ValueError(
                "El mensaje es requerido."
            )

        return NotificationRepository.create(
            user_id=user_id,
            title=title,
            message=message
        )

    # =========================
    # MARK AS READ
    # =========================
    @staticmethod
    def mark_as_read(notification):

        notification.is_read = True

        return notification

    # =========================
    # GET USER NOTIFICATIONS
    # =========================
    @staticmethod
    def get_user_notifications(user_id):

        return NotificationRepository.get_by_user(
            user_id
        )

    # =========================
    # GET UNREAD NOTIFICATIONS
    # =========================
    @staticmethod
    def get_unread_notifications(user_id):

        return (
            NotificationRepository.get_unread_by_user(
                user_id
            )
        )