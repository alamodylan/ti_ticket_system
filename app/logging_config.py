import logging
import os

from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter


# =========================
# CREATE LOG DIRECTORY
# =========================
if not os.path.exists("logs"):
    os.mkdir("logs")


# =========================
# LOG FORMATTERS
# =========================
console_formatter = ColoredFormatter(
    "%(log_color)s"
    "[%(asctime)s] "
    "[%(levelname)s] "
    "%(name)s: "
    "%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True
)

file_formatter = logging.Formatter(
    "[%(asctime)s] "
    "[%(levelname)s] "
    "%(name)s: "
    "%(message)s"
)


# =========================
# CONSOLE HANDLER
# =========================
console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)

console_handler.setFormatter(console_formatter)


# =========================
# FILE HANDLER
# =========================
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=10
)

file_handler.setLevel(logging.INFO)

file_handler.setFormatter(file_formatter)


# =========================
# ROOT LOGGER
# =========================
def configure_logging(app):

    app.logger.setLevel(logging.INFO)

    app.logger.addHandler(console_handler)

    app.logger.addHandler(file_handler)

    app.logger.info(
        "Logging system initialized."
    )