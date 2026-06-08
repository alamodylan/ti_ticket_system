import secrets

from werkzeug.utils import secure_filename


# =========================
# GENERATE SECURE TOKEN
# =========================
def generate_secure_token(length=32):

    return secrets.token_hex(length)


# =========================
# GENERATE RANDOM PASSWORD
# =========================
def generate_random_password(length=12):

    alphabet = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
    )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


# =========================
# SECURE FILE NAME
# =========================
def secure_file_name(filename):

    return secure_filename(filename)