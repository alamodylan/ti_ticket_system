import os

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

PROJECT_DIR = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        ".."
    )
)


def get_database_url():

    database_url = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(PROJECT_DIR, 'tickets.db')}"
    )

    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql+pg8000://",
            1
        )

    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+pg8000://",
            1
        )

    return database_url


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    APP_NAME = os.getenv(
        "APP_NAME",
        "Sistema de Tickets TI"
    )

    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = get_database_url()

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        SECRET_KEY
    )

    # =========================
    # MAIL CONFIG (SALIDA)
    # =========================
    MAIL_SERVER = os.getenv("MAIL_SERVER")

    MAIL_PORT = int(
        os.getenv("MAIL_PORT", 587)
    )

    MAIL_USE_TLS = (
        os.getenv("MAIL_USE_TLS", "True") == "True"
    )

    MAIL_USE_SSL = (
        os.getenv("MAIL_USE_SSL", "False") == "True"
    )

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER"
    )

    MAIL_SUPPRESS_SEND = (
        os.getenv("MAIL_SUPPRESS_SEND", "False") == "True"
    )

    MAIL_TIMEOUT = int(
        os.getenv("MAIL_TIMEOUT", 10)
    )

    # =========================
    # EMAIL API PROVIDER
    # =========================
    EMAIL_PROVIDER = os.getenv(
        "EMAIL_PROVIDER",
        "smtp"
    )

    RESEND_API_KEY = os.getenv(
        "RESEND_API_KEY"
    )

    RESEND_FROM = os.getenv(
        "RESEND_FROM",
        "Soporte Álamo <onboarding@resend.dev>"
    )

    # =========================
    # EMAIL INBOX POP3 (ENTRADA)
    # =========================
    INBOX_POP_SERVER = os.getenv(
        "INBOX_POP_SERVER"
    )

    INBOX_POP_PORT = int(
        os.getenv(
            "INBOX_POP_PORT",
            110
        )
    )

    INBOX_POP_USE_SSL = (
        os.getenv(
            "INBOX_POP_USE_SSL",
            "False"
        ) == "True"
    )

    INBOX_EMAIL = os.getenv(
        "INBOX_EMAIL"
    )

    INBOX_PASSWORD = os.getenv(
        "INBOX_PASSWORD"
    )

    SYSTEM_TICKET_USER_ID = int(
        os.getenv(
            "SYSTEM_TICKET_USER_ID",
            1
        )
    )

    PROCESS_INBOX_TOKEN = os.getenv(
        "PROCESS_INBOX_TOKEN"
    )

    # =========================
    # INTERNAL SCHEDULER
    # =========================
    ENABLE_INBOX_SCHEDULER = (
        os.getenv(
            "ENABLE_INBOX_SCHEDULER",
            "False"
        ) == "True"
    )

    INBOX_SCHEDULER_INTERVAL_SECONDS = int(
        os.getenv(
            "INBOX_SCHEDULER_INTERVAL_SECONDS",
            120
        )
    )

    # =========================
    # FILES
    # =========================
    MAX_CONTENT_LENGTH = (
        16 * 1024 * 1024
    )

    UPLOAD_FOLDER = os.path.join(
        PROJECT_DIR,
        "app",
        "static",
        "uploads"
    )

    TICKETS_UPLOAD_FOLDER = os.path.join(
        PROJECT_DIR,
        "app",
        "static",
        "uploads",
        "tickets"
    )

    # =========================
    # SECURITY
    # =========================
    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = False

    REMEMBER_COOKIE_HTTPONLY = True

    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):

    DEBUG = True


class ProductionConfig(Config):

    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"
    )

    WTF_CSRF_ENABLED = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}