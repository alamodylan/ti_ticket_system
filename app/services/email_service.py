# app/services/email_service.py

from flask import current_app
from flask_mail import Message

from app.extensions import db, mail

from app.repositories.email_log_repository import EmailLogRepository


class EmailService:

    # =========================
    # GET DEFAULT SENDER
    # =========================
    @staticmethod
    def _get_sender():

        sender_email = current_app.config.get(
            "MAIL_DEFAULT_SENDER"
        )

        if not sender_email:
            sender_email = current_app.config.get(
                "MAIL_USERNAME"
            )

        return sender_email

    # =========================
    # SEND EMAIL
    # =========================
    @staticmethod
    def send_email(subject, recipients, body=None, html=None):

        if not recipients:
            print("\n====================")
            print("EMAIL NO ENVIADO")
            print("Motivo: lista recipients vacía")
            print(f"Asunto: {subject}")
            print("====================\n")
            return False

        recipients = [
            email.strip()
            for email in recipients
            if email and email.strip()
        ]

        if not recipients:
            print("\n====================")
            print("EMAIL NO ENVIADO")
            print("Motivo: recipients quedó vacío después del filtro")
            print(f"Asunto: {subject}")
            print("====================\n")
            return False

        try:
            sender = EmailService._get_sender()

            print("\n====================")
            print("EMAIL SERVICE EJECUTADO")
            print(f"Asunto: {subject}")
            print(f"Para: {', '.join(recipients)}")
            print(f"Remitente: {sender}")
            print("====================\n")

            msg = Message(
                subject=subject,
                recipients=recipients,
                body=body,
                html=html,
                sender=sender
            )

            mail.send(msg)

            EmailLogRepository.create(
                subject=subject,
                recipients=",".join(recipients),
                status="sent"
            )

            db.session.commit()

            print("\n====================")
            print("EMAIL ENVIADO")
            print(f"Asunto: {subject}")
            print(f"Para: {', '.join(recipients)}")
            print(f"Remitente: {sender}")
            print("====================\n")

            return True

        except Exception as error:
            db.session.rollback()

            print("\n====================")
            print("ERROR SMTP / EMAIL SERVICE")
            print(str(error))
            print("====================\n")

            try:
                EmailLogRepository.create(
                    subject=subject,
                    recipients=",".join(recipients),
                    status="failed",
                    error_message=str(error)
                )

                db.session.commit()

            except Exception as log_error:
                db.session.rollback()

                print("\n====================")
                print("ERROR GUARDANDO EMAIL LOG")
                print(str(log_error))
                print("====================\n")

            return False

    # =========================
    # BASE TICKET EMAIL TEMPLATE
    # =========================
    @staticmethod
    def _ticket_email_html(title, message, ticket):

        department_name = (
            ticket.department.name
            if ticket.department
            else "Sin departamento"
        )

        created_by_name = (
            ticket.created_by.full_name
            if ticket.created_by
            else "Sistema"
        )

        assigned_to_name = (
            ticket.assigned_to.full_name
            if ticket.assigned_to
            else "Sin asignar"
        )

        site_name = (
            ticket.site.name
            if hasattr(ticket, "site") and ticket.site
            else "Sin sede"
        )

        requester_name = (
            ticket.requester_display_name
            if hasattr(ticket, "requester_display_name")
            else created_by_name
        )

        requester_email = (
            ticket.requester_display_email
            if hasattr(ticket, "requester_display_email")
            else "Sin correo"
        )

        return f"""
        <div style="font-family: Arial, sans-serif; color: #222;">

            <h2>{title}</h2>

            <p>{message}</p>

            <hr>

            <p>
                <strong>Número de ticket:</strong><br>
                {ticket.ticket_number}
            </p>

            <p>
                <strong>Título:</strong><br>
                {ticket.title}
            </p>

            <p>
                <strong>Estado:</strong><br>
                {ticket.status}
            </p>

            <p>
                <strong>Prioridad:</strong><br>
                {ticket.priority}
            </p>

            <p>
                <strong>Sede:</strong><br>
                {site_name}
            </p>

            <p>
                <strong>Departamento:</strong><br>
                {department_name}
            </p>

            <p>
                <strong>Solicitante:</strong><br>
                {requester_name}
            </p>

            <p>
                <strong>Correo solicitante:</strong><br>
                {requester_email}
            </p>

            <p>
                <strong>Asignado a:</strong><br>
                {assigned_to_name}
            </p>

            <hr>

            <p style="font-size: 12px; color: #666;">
                Este correo fue generado automáticamente por el Sistema Tickets TI - ALAMO.
            </p>

        </div>
        """

    # =========================
    # GET CREATOR / REQUESTER RECIPIENT
    # =========================
    @staticmethod
    def _creator_recipient(ticket):

        if hasattr(ticket, "requester_email") and ticket.requester_email:
            return [ticket.requester_email]

        if ticket.created_by and ticket.created_by.email:
            return [ticket.created_by.email]

        return []

    # =========================
    # GET ASSIGNED RECIPIENT
    # =========================
    @staticmethod
    def _assigned_recipient(ticket):

        if ticket.assigned_to and ticket.assigned_to.email:
            return [ticket.assigned_to.email]

        return []

    # =========================
    # SEND TICKET CREATED EMAIL
    # =========================
    @staticmethod
    def send_ticket_created_email(ticket):

        recipients = EmailService._creator_recipient(ticket)

        html = EmailService._ticket_email_html(
            title="Ticket creado correctamente",
            message=(
                "Su solicitud fue registrada correctamente. "
                "El equipo de TI dará seguimiento al caso."
            ),
            ticket=ticket
        )

        return EmailService.send_email(
            subject=f"Ticket {ticket.ticket_number} creado correctamente",
            recipients=recipients,
            html=html
        )

    # =========================
    # SEND TICKET ASSIGNED EMAIL
    # =========================
    @staticmethod
    def send_ticket_assigned_email(ticket):

        recipients = EmailService._creator_recipient(ticket)

        html = EmailService._ticket_email_html(
            title="Ticket asignado",
            message="Su ticket fue asignado a un responsable de TI.",
            ticket=ticket
        )

        return EmailService.send_email(
            subject=f"Ticket {ticket.ticket_number} asignado",
            recipients=recipients,
            html=html
        )

    # =========================
    # SEND TICKET TAKEN EMAIL
    # =========================
    @staticmethod
    def send_ticket_taken_email(ticket):

        recipients = EmailService._creator_recipient(ticket)

        html = EmailService._ticket_email_html(
            title="Ticket en atención",
            message=(
                "Su ticket fue tomado por un responsable de TI "
                "y será atendido próximamente."
            ),
            ticket=ticket
        )

        return EmailService.send_email(
            subject=f"Ticket {ticket.ticket_number} en atención",
            recipients=recipients,
            html=html
        )

    # =========================
    # SEND TICKET IN PROGRESS EMAIL
    # =========================
    @staticmethod
    def send_ticket_in_progress_email(ticket):

        recipients = EmailService._creator_recipient(ticket)

        html = EmailService._ticket_email_html(
            title="Ticket en progreso",
            message="Su ticket cambió de estado a En Progreso.",
            ticket=ticket
        )

        return EmailService.send_email(
            subject=f"Ticket {ticket.ticket_number} en progreso",
            recipients=recipients,
            html=html
        )

    # =========================
    # SEND TICKET PENDING EMAIL
    # =========================
    @staticmethod
    def send_ticket_pending_email(ticket):

        recipients = EmailService._creator_recipient(ticket)

        html = EmailService._ticket_email_html(
            title="Ticket pendiente",
            message=(
                "Su ticket fue marcado como Pendiente. "
                "Esto puede significar que se requiere información adicional, "
                "aprobación o seguimiento externo."
            ),
            ticket=ticket
        )

        return EmailService.send_email(
            subject=f"Ticket {ticket.ticket_number} pendiente",
            recipients=recipients,
            html=html
        )

    # =========================
    # SEND TICKET RESOLVED EMAIL
    # =========================
    @staticmethod
    def send_ticket_resolved_email(ticket):

        recipients = EmailService._creator_recipient(ticket)

        html = EmailService._ticket_email_html(
            title="Ticket resuelto",
            message="Su ticket fue marcado como Resuelto por el equipo de TI.",
            ticket=ticket
        )

        return EmailService.send_email(
            subject=f"Ticket {ticket.ticket_number} resuelto",
            recipients=recipients,
            html=html
        )

    # =========================
    # SEND TICKET CLOSED EMAIL
    # =========================
    @staticmethod
    def send_ticket_closed_email(ticket):

        recipients = EmailService._creator_recipient(ticket)

        html = EmailService._ticket_email_html(
            title="Ticket cerrado",
            message=(
                "Su ticket fue cerrado. "
                "Gracias por utilizar el Sistema Tickets TI - ALAMO."
            ),
            ticket=ticket
        )

        return EmailService.send_email(
            subject=f"Ticket {ticket.ticket_number} cerrado",
            recipients=recipients,
            html=html
        )

    # =========================
    # NOTIFY ASSIGNED RESPONSIBLE
    # =========================
    @staticmethod
    def notify_assigned_responsible(ticket):

        recipients = EmailService._assigned_recipient(ticket)

        html = EmailService._ticket_email_html(
            title="Nuevo ticket asignado",
            message="Se le asignó un ticket para su atención.",
            ticket=ticket
        )

        return EmailService.send_email(
            subject=f"Ticket {ticket.ticket_number} asignado a usted",
            recipients=recipients,
            html=html
        )