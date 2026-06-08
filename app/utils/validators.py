import re

from email_validator import (
    validate_email,
    EmailNotValidError
)


# =========================
# EMAIL VALIDATOR
# =========================
def is_valid_email(email):

    try:

        validate_email(email)

        return True

    except EmailNotValidError:

        return False


# =========================
# PASSWORD VALIDATOR
# =========================
def is_strong_password(password):

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True


# =========================
# ALLOWED FILES
# =========================
def allowed_file(filename):

    allowed_extensions = {
        "png",
        "jpg",
        "jpeg",
        "pdf",
        "doc",
        "docx",
        "xlsx",
        "txt"
    }

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in allowed_extensions
    )