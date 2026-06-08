from flask_mail import Message

from app.extensions import mail


# =========================
# SEND EMAIL
# =========================
def send_email(
    subject,
    recipients,
    body=None,
    html=None,
    cc=None,
    bcc=None
):
    """
    Generic email sender.
    """

    try:

        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html,
            cc=cc,
            bcc=bcc
        )

        mail.send(msg)

        return True

    except Exception as error:

        print(f"[MAIL ERROR]: {error}")

        return False


# =========================
# SEND TICKET CREATED EMAIL
# =========================
def send_ticket_created_email(
    recipients,
    ticket
):

    subject = f"[{ticket.ticket_number}] Nuevo Ticket Creado"

    html = f"""
    <h2>Nuevo Ticket Registrado</h2>

    <p>
        <strong>Número:</strong> {ticket.ticket_number}
    </p>

    <p>
        <strong>Título:</strong> {ticket.title}
    </p>

    <p>
        <strong>Prioridad:</strong> {ticket.priority}
    </p>

    <p>
        <strong>Estado:</strong> {ticket.status}
    </p>

    <hr>

    <p>
        Sistema de Tickets TI
    </p>
    """

    return send_email(
        subject=subject,
        recipients=recipients,
        html=html
    )


# =========================
# SEND PASSWORD RESET EMAIL
# =========================
def send_password_reset_email(
    recipients,
    reset_url
):

    subject = "Restablecimiento de contraseña"

    html = f"""
    <h2>Restablecer Contraseña</h2>

    <p>
        Se solicitó un cambio de contraseña.
    </p>

    <p>
        Haga clic en el siguiente enlace:
    </p>

    <p>
        <a href="{reset_url}">
            Restablecer Contraseña
        </a>
    </p>

    <hr>

    <p>
        Sistema de Tickets TI
    </p>
    """

    return send_email(
        subject=subject,
        recipients=recipients,
        html=html
    )