import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
from bs4 import BeautifulSoup

from flask import current_app

from app.services.ticket_service import TicketService
from app.services.email_service import EmailService


class EmailInboxService:

    @staticmethod
    def _decode_value(value):

        if not value:
            return ""

        decoded_parts = decode_header(value)
        result = ""

        for part, encoding in decoded_parts:

            if isinstance(part, bytes):
                result += part.decode(encoding or "utf-8", errors="ignore")
            else:
                result += part

        return result.strip()

    @staticmethod
    def _extract_addresses(raw_value):

        if not raw_value:
            return []

        addresses = email.utils.getaddresses([raw_value])

        return [
            address.lower().strip()
            for _, address in addresses
            if address
        ]

    @staticmethod
    def _extract_body(message):

        body = ""

        if message.is_multipart():

            for part in message.walk():

                content_type = part.get_content_type()
                disposition = str(part.get("Content-Disposition") or "")

                if "attachment" in disposition:
                    continue

                payload = part.get_payload(decode=True)

                if not payload:
                    continue

                charset = part.get_content_charset() or "utf-8"

                try:
                    content = payload.decode(charset, errors="ignore")
                except Exception:
                    content = payload.decode("utf-8", errors="ignore")

                if content_type == "text/plain":
                    return content.strip()

                if content_type == "text/html" and not body:
                    soup = BeautifulSoup(content, "html.parser")
                    body = soup.get_text(separator="\n").strip()

        else:

            payload = message.get_payload(decode=True)

            if payload:
                charset = message.get_content_charset() or "utf-8"
                body = payload.decode(charset, errors="ignore")

        return body.strip()

    @staticmethod
    def _should_process_email(message, support_email):

        from_email = parseaddr(message.get("From"))[1].lower().strip()

        to_addresses = EmailInboxService._extract_addresses(
            message.get("To")
        )

        support_email = support_email.lower().strip()

        if from_email == support_email:
            return False, "Ignorado: correo enviado por soporte."

        if support_email not in to_addresses:
            return False, "Ignorado: soporte no está en TO."

        return True, "Procesar correo."

    @staticmethod
    def process_unread_emails():

        imap_server = current_app.config.get("INBOX_IMAP_SERVER")
        imap_port = int(current_app.config.get("INBOX_IMAP_PORT", 993))
        inbox_email = current_app.config.get("INBOX_EMAIL")
        inbox_password = current_app.config.get("INBOX_PASSWORD")
        system_user_id = current_app.config.get("SYSTEM_TICKET_USER_ID")

        if not imap_server or not inbox_email or not inbox_password:
            return {
                "success": False,
                "message": "Configuración IMAP incompleta.",
                "created": 0
            }

        if not system_user_id:
            return {
                "success": False,
                "message": "SYSTEM_TICKET_USER_ID no configurado.",
                "created": 0
            }

        created_count = 0
        ignored_count = 0
        errors = []

        try:
            mail = imaplib.IMAP4_SSL(
                imap_server,
                imap_port
            )

            mail.login(
                inbox_email,
                inbox_password
            )

            mail.select("INBOX")

            status, messages = mail.search(
                None,
                "UNSEEN"
            )

            if status != "OK":
                return {
                    "success": False,
                    "message": "No se pudo buscar correos no leídos.",
                    "created": 0
                }

            email_ids = messages[0].split()

            for email_id in email_ids:

                try:
                    status, msg_data = mail.fetch(
                        email_id,
                        "(RFC822)"
                    )

                    if status != "OK":
                        ignored_count += 1
                        continue

                    raw_email = msg_data[0][1]
                    message = email.message_from_bytes(raw_email)

                    should_process, reason = EmailInboxService._should_process_email(
                        message=message,
                        support_email=inbox_email
                    )

                    if not should_process:
                        ignored_count += 1
                        print(reason)
                        continue

                    message_id = message.get("Message-ID")
                    subject = EmailInboxService._decode_value(
                        message.get("Subject")
                    )

                    from_name, from_email = parseaddr(
                        message.get("From")
                    )

                    from_name = EmailInboxService._decode_value(
                        from_name
                    )

                    body = EmailInboxService._extract_body(
                        message
                    )

                    if not subject:
                        subject = "Solicitud de soporte sin asunto"

                    if not body:
                        body = "Correo recibido sin contenido."

                    result = TicketService.create_ticket(
                        {
                            "title": subject[:255],
                            "description": body,
                            "priority": "Media",
                            "status": "Nuevo",
                            "created_by_id": int(system_user_id),
                            "requester_name": from_name,
                            "requester_email": from_email,
                            "source": "email",
                            "email_message_id": message_id,
                            "email_subject": subject
                        }
                    )

                    if result["success"]:

                        ticket = result["ticket"]

                        if result.get("message") != "El correo ya fue procesado previamente.":

                            EmailService.send_email(
                                subject=f"Solicitud registrada - {ticket.ticket_number}",
                                recipients=[from_email],
                                html=f"""
                                <div style="font-family: Arial, sans-serif; color: #222;">
                                    <h2>Solicitud registrada correctamente</h2>

                                    <p>
                                        Hemos recibido su solicitud de soporte.
                                    </p>

                                    <p>
                                        <strong>Número de ticket:</strong><br>
                                        {ticket.ticket_number}
                                    </p>

                                    <p>
                                        <strong>Asunto:</strong><br>
                                        {ticket.title}
                                    </p>

                                    <hr>

                                    <p style="font-size: 12px; color: #666;">
                                        Este correo fue generado automáticamente por el Sistema Tickets TI - ALAMO.
                                    </p>
                                </div>
                                """
                            )

                            created_count += 1

                        mail.store(
                            email_id,
                            "+FLAGS",
                            "\\Seen"
                        )

                    else:

                        errors.append(
                            result.get("message")
                        )

                except Exception as error:
                    errors.append(str(error))

            mail.logout()

            return {
                "success": True,
                "created": created_count,
                "ignored": ignored_count,
                "errors": errors
            }

        except Exception as error:

            return {
                "success": False,
                "message": str(error),
                "created": created_count,
                "ignored": ignored_count,
                "errors": errors
            }