import poplib
import email
from email.header import decode_header
from email.utils import parseaddr
from bs4 import BeautifulSoup

from flask import current_app

from app.services.ticket_service import TicketService
from app.services.email_service import EmailService


class EmailPopInboxService:

    REQUIRED_SUBJECT_KEYWORD = "soporte"

    @staticmethod
    def _decode_value(value):

        if not value:
            return ""

        decoded_parts = decode_header(value)
        result = ""

        for part, encoding in decoded_parts:

            if isinstance(part, bytes):
                result += part.decode(
                    encoding or "utf-8",
                    errors="ignore"
                )
            else:
                result += part

        return result.strip()

    @staticmethod
    def _extract_addresses(raw_value):

        if not raw_value:
            return []

        addresses = email.utils.getaddresses(
            [raw_value]
        )

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

                disposition = str(
                    part.get("Content-Disposition") or ""
                )

                if "attachment" in disposition:
                    continue

                payload = part.get_payload(
                    decode=True
                )

                if not payload:
                    continue

                charset = (
                    part.get_content_charset()
                    or "utf-8"
                )

                try:
                    content = payload.decode(
                        charset,
                        errors="ignore"
                    )
                except Exception:
                    content = payload.decode(
                        "utf-8",
                        errors="ignore"
                    )

                if content_type == "text/plain":
                    return content.strip()

                if content_type == "text/html" and not body:

                    soup = BeautifulSoup(
                        content,
                        "html.parser"
                    )

                    body = soup.get_text(
                        separator="\n"
                    ).strip()

        else:

            payload = message.get_payload(
                decode=True
            )

            if payload:

                charset = (
                    message.get_content_charset()
                    or "utf-8"
                )

                body = payload.decode(
                    charset,
                    errors="ignore"
                )

        return body.strip()

    @staticmethod
    def _subject_has_required_keyword(subject):

        if not subject:
            return False

        return (
            EmailPopInboxService.REQUIRED_SUBJECT_KEYWORD
            in subject.lower()
        )

    @staticmethod
    def _clean_ticket_title(subject):

        if not subject or not subject.strip():
            return "Solicitud de soporte"

        original_subject = subject.strip()
        title = original_subject

        prefixes = [
            "SOPORTE -",
            "SOPORTE-",
            "SOPORTE:",
            "SOPORTE"
        ]

        for prefix in prefixes:

            if title.upper().startswith(prefix):

                cleaned_title = title[len(prefix):].strip()

                if cleaned_title:
                    return cleaned_title[:255]

                return original_subject[:255]

        if title.strip():
            return title[:255]

        return "Solicitud de soporte"

    @staticmethod
    def _should_process_email(message, support_email):

        from_email = parseaddr(
            message.get("From")
        )[1].lower().strip()

        to_addresses = EmailPopInboxService._extract_addresses(
            message.get("To")
        )

        support_email = support_email.lower().strip()

        subject = EmailPopInboxService._decode_value(
            message.get("Subject")
        )

        if from_email == support_email:
            return False, "Ignorado: correo enviado por soporte."

        if support_email not in to_addresses:
            return False, "Ignorado: soporte no está en TO."

        if not EmailPopInboxService._subject_has_required_keyword(
            subject
        ):
            return False, "Ignorado: asunto no contiene SOPORTE."

        return True, "Procesar correo."

    @staticmethod
    def process_latest_emails(limit=10):

        pop_server = current_app.config.get(
            "INBOX_POP_SERVER"
        )

        pop_port = int(
            current_app.config.get(
                "INBOX_POP_PORT",
                110
            )
        )

        use_ssl = current_app.config.get(
            "INBOX_POP_USE_SSL",
            False
        )

        inbox_email = current_app.config.get(
            "INBOX_EMAIL"
        )

        inbox_password = current_app.config.get(
            "INBOX_PASSWORD"
        )

        system_user_id = current_app.config.get(
            "SYSTEM_TICKET_USER_ID"
        )

        if not pop_server or not inbox_email or not inbox_password:

            return {
                "success": False,
                "message": "Configuración POP incompleta.",
                "created": 0,
                "ignored": 0,
                "errors": []
            }

        if not system_user_id:

            return {
                "success": False,
                "message": "SYSTEM_TICKET_USER_ID no configurado.",
                "created": 0,
                "ignored": 0,
                "errors": []
            }

        created_count = 0
        ignored_count = 0
        errors = []

        try:

            if use_ssl:
                mailbox = poplib.POP3_SSL(
                    pop_server,
                    pop_port,
                    timeout=30
                )
            else:
                mailbox = poplib.POP3(
                    pop_server,
                    pop_port,
                    timeout=30
                )

            mailbox.user(
                inbox_email
            )

            mailbox.pass_(
                inbox_password
            )

            total_messages = len(
                mailbox.list()[1]
            )

            start_index = max(
                1,
                total_messages - limit + 1
            )

            for message_index in range(
                total_messages,
                start_index - 1,
                -1
            ):

                try:

                    response, lines, octets = mailbox.retr(
                        message_index
                    )

                    raw_message = b"\n".join(
                        lines
                    )

                    message = email.message_from_bytes(
                        raw_message
                    )

                    should_process, reason = EmailPopInboxService._should_process_email(
                        message=message,
                        support_email=inbox_email
                    )

                    if not should_process:
                        ignored_count += 1
                        print(reason)
                        continue

                    message_id = message.get(
                        "Message-ID"
                    )

                    subject = EmailPopInboxService._decode_value(
                        message.get("Subject")
                    )

                    from_name, from_email = parseaddr(
                        message.get("From")
                    )

                    from_name = EmailPopInboxService._decode_value(
                        from_name
                    )

                    body = EmailPopInboxService._extract_body(
                        message
                    )

                    if not body:
                        body = "Correo recibido sin contenido."

                    ticket_title = EmailPopInboxService._clean_ticket_title(
                        subject
                    )

                    result = TicketService.create_ticket(
                        {
                            "title": ticket_title,
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

                        if result.get("message") == "El correo ya fue procesado previamente.":
                            ignored_count += 1
                            print(
                                f"Ignorado: correo ya procesado para {ticket.ticket_number}."
                            )
                            continue

                        print("================================")
                        print("INTENTANDO ENVIAR CORREO AUTOMATICO")
                        print(f"DESTINO: {from_email}")
                        print(f"TICKET: {ticket.ticket_number}")
                        print("================================")

                        email_result = EmailService.send_email(
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

                        print("================================")
                        print(f"RESULTADO ENVIO EMAIL: {email_result}")
                        print("================================")

                        created_count += 1

                    else:

                        errors.append(
                            result.get("message")
                        )

                except Exception as error:

                    errors.append(
                        str(error)
                    )

            mailbox.quit()

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