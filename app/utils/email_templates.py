# =========================
# NEW TICKET EMAIL
# =========================
def new_ticket_template(ticket):

    return f"""
    <h2>Nuevo Ticket Registrado</h2>

    <p>
        <strong>Número:</strong>
        {ticket.ticket_number}
    </p>

    <p>
        <strong>Título:</strong>
        {ticket.title}
    </p>

    <p>
        <strong>Prioridad:</strong>
        {ticket.priority}
    </p>

    <p>
        <strong>Estado:</strong>
        {ticket.status}
    </p>

    <hr>

    <p>
        Sistema de Tickets TI
    </p>
    """


# =========================
# TICKET ASSIGNED EMAIL
# =========================
def ticket_assigned_template(ticket):

    return f"""
    <h2>Ticket Asignado</h2>

    <p>
        Se le asignó el ticket:
    </p>

    <p>
        <strong>{ticket.ticket_number}</strong>
    </p>

    <p>
        <strong>Título:</strong>
        {ticket.title}
    </p>

    <hr>

    <p>
        Sistema de Tickets TI
    </p>
    """


# =========================
# PASSWORD RESET EMAIL
# =========================
def password_reset_template(reset_url):

    return f"""
    <h2>Restablecimiento de Contraseña</h2>

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