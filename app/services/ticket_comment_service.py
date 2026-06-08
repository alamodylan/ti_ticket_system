from app.extensions import db

from app.repositories.ticket_comment_repository import (
    TicketCommentRepository
)

from app.services.audit_service import (
    AuditService
)


class TicketCommentService:

    VALID_COMMENT_TYPES = [
        "user",
        "technical",
        "internal"
    ]

    @staticmethod
    def validate_comment(comment):

        if not comment:

            raise ValueError(
                "El comentario es requerido."
            )

        if len(comment.strip()) < 2:

            raise ValueError(
                "Comentario demasiado corto."
            )

    @staticmethod
    def validate_comment_type(comment_type):

        if comment_type not in TicketCommentService.VALID_COMMENT_TYPES:

            raise ValueError(
                "Tipo de comentario inválido."
            )

    @staticmethod
    def create_comment(
        ticket_id,
        user_id,
        comment,
        comment_type="user",
        user=None
    ):

        try:

            TicketCommentService.validate_comment(
                comment
            )

            TicketCommentService.validate_comment_type(
                comment_type
            )

            if comment_type in [
                "technical",
                "internal"
            ]:

                if not user or not user.is_admin:

                    raise ValueError(
                        "No tiene permisos para crear comentarios técnicos o internos."
                    )

            new_comment = TicketCommentRepository.create(
                ticket_id=ticket_id,
                user_id=user_id,
                comment=comment.strip(),
                comment_type=comment_type
            )

            db.session.flush()

            try:

                AuditService.log_action(
                    action="ticket_comment_created",
                    entity="ticket_comment",
                    entity_id=new_comment.id,
                    details=(
                        f"Comentario tipo {comment_type} "
                        f"agregado al ticket {ticket_id}"
                    ),
                    user_id=user_id
                )

            except Exception:
                pass

            db.session.commit()

            return {
                "success": True,
                "comment": new_comment
            }

        except Exception as e:

            db.session.rollback()

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def get_comments_by_ticket(
        ticket_id,
        user=None
    ):

        try:

            comments = TicketCommentRepository.get_by_ticket(
                ticket_id
            )

            if not user or not user.is_admin:

                comments = [
                    comment
                    for comment in comments
                    if not comment.is_internal
                ]

            return {
                "success": True,
                "comments": comments
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e),
                "comments": []
            }