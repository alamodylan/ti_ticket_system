import os
import uuid

from werkzeug.utils import secure_filename

from app.extensions import db

from app.repositories.ticket_attachment_repository import (
    TicketAttachmentRepository
)

from app.services.audit_service import (
    AuditService
)


class TicketAttachmentService:

    UPLOAD_FOLDER = "app/static/uploads/tickets"

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "txt"
    }

    MAX_FILE_SIZE = 5 * 1024 * 1024

    @staticmethod
    def _allowed_file(filename):

        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in TicketAttachmentService.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def save_attachment(
        ticket_id,
        user_id,
        file
    ):

        try:

            if not file:
                raise ValueError(
                    "No se recibió ningún archivo."
                )

            if not file.filename:
                raise ValueError(
                    "El archivo no tiene nombre."
                )

            if not TicketAttachmentService._allowed_file(
                file.filename
            ):
                raise ValueError(
                    "Tipo de archivo no permitido."
                )

            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > TicketAttachmentService.MAX_FILE_SIZE:
                raise ValueError(
                    "El archivo supera el tamaño máximo permitido de 5 MB."
                )

            os.makedirs(
                TicketAttachmentService.UPLOAD_FOLDER,
                exist_ok=True
            )

            original_name = secure_filename(
                file.filename
            )

            extension = original_name.rsplit(
                ".",
                1
            )[1].lower()

            file_name = (
                f"{uuid.uuid4().hex}.{extension}"
            )

            file_path = os.path.join(
                TicketAttachmentService.UPLOAD_FOLDER,
                file_name
            )

            file.save(file_path)

            attachment = TicketAttachmentRepository.create(
                file_name=file_name,
                original_name=original_name,
                file_path=file_path,
                file_size=file_size,
                mime_type=file.mimetype,
                ticket_id=ticket_id,
                uploaded_by_id=user_id
            )

            db.session.flush()

            try:

                AuditService.log_action(
                    action="ticket_attachment_uploaded",
                    entity="ticket",
                    entity_id=ticket_id,
                    details=(
                        f"Adjunto agregado: {original_name}"
                    ),
                    user_id=user_id
                )

            except Exception:
                pass

            db.session.commit()

            return {
                "success": True,
                "attachment": attachment
            }

        except Exception as e:

            db.session.rollback()

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def get_attachments_by_ticket(ticket_id):

        try:

            attachments = (
                TicketAttachmentRepository.get_by_ticket(
                    ticket_id
                )
            )

            return {
                "success": True,
                "attachments": attachments
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e),
                "attachments": []
            }