import uuid

from datetime import datetime


# =========================
# GENERATE UUID
# =========================
def generate_uuid():

    return str(uuid.uuid4())


# =========================
# GENERATE TICKET NUMBER
# =========================
def generate_ticket_number(ticket_id):

    current_year = datetime.now().year

    return (
        f"TK-{current_year}-{ticket_id:04d}"
    )


# =========================
# FORMAT DATETIME
# =========================
def format_datetime(
    value,
    date_format="%Y-%m-%d %H:%M:%S"
):

    if not value:
        return ""

    return value.strftime(date_format)


# =========================
# FORMAT FILE SIZE
# =========================
def format_file_size(size):

    if size < 1024:
        return f"{size} B"

    elif size < 1024 * 1024:
        return f"{round(size / 1024, 2)} KB"

    else:
        return (
            f"{round(size / (1024 * 1024), 2)} MB"
        )