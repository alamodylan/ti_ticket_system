import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from flask import current_app

from app.extensions import db
from app.repositories.email_log_repository import EmailLogRepository


class EmailService:

    # =========================
    # GET DEFAULT SENDER
    # =========================
    @staticmethod
    def _get_sender_email():

        return (
            current_app.config.get("MAIL_DEFAULT_SENDER")
            or current_app.config.get("MAIL_USERNAME")
        )

    # =========================
    # SEND EMAIL
    # =========================
    @staticmethod
    def send_email(subject, recipients, body=None, html=None):

        recipients = [
            email.strip()
            for email in recipients or []
            if email and email.strip()
        ]

        if not recipients:

            print("\n====================")
            print("EMAIL NO ENVIADO")
            print("Motivo: recipients vacío")
            print(f"Asunto: {subject}")
            print("====================\n")

            return False

        mail_server = current_app.config.get("MAIL_SERVER")
        mail_port = int(current_app.config.get("MAIL_PORT", 587))
        mail_use_tls = current_app.config.get("MAIL_USE_TLS", True)
        mail_use_ssl = current_app.config.get("MAIL_USE_SSL", False)
        mail_username = current_app.config.get("MAIL_USERNAME")
        mail_password = current_app.config.get("MAIL_PASSWORD")
        mail_suppress_send = current_app.config.get("MAIL_SUPPRESS_SEND", False)
        mail_timeout = int(current_app.config.get("MAIL_TIMEOUT", 10))

        sender_email = EmailService._get_sender_email()

        print("\n====================")
        print("EMAIL SERVICE EJECUTADO")
        print(f"MAIL_SERVER: {mail_server}")
        print(f"MAIL_PORT: {mail_port}")
        print(f"MAIL_USE_TLS: {mail_use_tls}")
        print(f"MAIL_USE_SSL: {mail_use_ssl}")
        print(f"MAIL_USERNAME: {mail_username}")
        print(f"MAIL_DEFAULT_SENDER: {sender_email}")
        print(f"MAIL_SUPPRESS_SEND: {mail_suppress_send}")
        print(f"MAIL_TIMEOUT: {mail_timeout}")
        print(f"Asunto: {subject}")
        print(f"Para: {', '.join(recipients)}")
        print("====================\n")

        if mail_suppress_send:

            print("\n====================")
            print("EMAIL SUPRIMIDO")
            print("Motivo: MAIL_SUPPRESS_SEND=True")
            print(f"Asunto: {subject}")
            print(f"Para: {', '.join(recipients)}")
            print("====================\n")

            try:

                EmailLogRepository.create(
                    subject=subject,
                    recipients=",".join(recipients),
                    status="suppressed",
                    error_message="MAIL_SUPPRESS_SEND=True"
                )

                db.session.commit()

            except Exception as log_error:

                db.session.rollback()

                print("\n====================")
                print("ERROR GUARDANDO EMAIL LOG SUPPRESSED")
                print(str(log_error))
                print("====================\n")

            return False

        if not mail_server or not sender_email:

            error_message = (
                "Configuración SMTP incompleta: "
                "MAIL_SERVER o MAIL_DEFAULT_SENDER/MAIL_USERNAME vacío."
            )

            print("\n====================")
            print("ERROR SMTP / EMAIL SERVICE")
            print(error_message)
            print("====================\n")

            try:

                EmailLogRepository.create(
                    subject=subject,
                    recipients=",".join(recipients),
                    status="failed",
                    error_message=error_message
                )

                db.session.commit()

            except Exception:

                db.session.rollback()

            return False

        try:

            message = MIMEMultipart("alternative")

            message["Subject"] = subject
            message["From"] = formataddr(
                (
                    "Sistema Tickets TI - ALAMO",
                    sender_email
                )
            )
            message["To"] = ", ".join(recipients)

            if body:

                message.attach(
                    MIMEText(
                        body,
                        "plain",
                        "utf-8"
                    )
                )

            if html:

                message.attach(
                    MIMEText(
                        html,
                        "html",
                        "utf-8"
                    )
                )

            if not body and not html:

                message.attach(
                    MIMEText(
                        "",
                        "plain",
                        "utf-8"
                    )
                )

            if mail_use_ssl:

                context = ssl.create_default_context()

                smtp = smtplib.SMTP_SSL(
                    mail_server,
                    mail_port,
                    timeout=mail_timeout,
                    context=context
                )

            else:

                smtp = smtplib.SMTP(
                    mail_server,
                    mail_port,
                    timeout=mail_timeout
                )

            with smtp:

                smtp.ehlo()

                if mail_use_tls and not mail_use_ssl:

                    context = ssl.create_default_context()

                    smtp.starttls(
                        context=context
                    )

                    smtp.ehlo()

                if mail_username and mail_password:

                    smtp.login(
                        mail_username,
                        mail_password
                    )

                smtp.sendmail(
                    sender_email,
                    recipients,
                    message.as_string()
                )

            EmailLogRepository.create(
                subject=subject,
                recipients=",".join(recipients),
                status="sent"
            )

            db.session.commit()

            print("\n====================")
            print("EMAIL ENVIADO CORRECTAMENTE")
            print(f"Asunto: {subject}")
            print(f"Para: {', '.join(recipients)}")
            print("====================\n")

            return True

        except Exception as error:

            db.session.rollback()

            print("\n====================")
            print("ERROR SMTP / EMAIL SERVICE")
            print(f"Tipo: {type(error).__name__}")
            print(f"Detalle: {str(error)}")
            print("====================\n")

            try:

                EmailLogRepository.create(
                    subject=subject,
                    recipients=",".join(recipients),
                    status="failed",
                    error_message=(
                        f"{type(error).__name__}: {str(error)}"
                    )
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