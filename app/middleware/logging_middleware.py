import time

from flask import (
    request,
    g
)


# =========================
# LOGGING MIDDLEWARE
# =========================
def register_logging_middleware(app):

    @app.before_request
    def start_timer():

        g.start_time = time.time()

    @app.after_request
    def log_request(response):

        if not hasattr(g, "start_time"):
            return response

        duration = round(
            time.time() - g.start_time,
            4
        )

        app.logger.info(
            (
                f"{request.method} "
                f"{request.path} "
                f"{response.status_code} "
                f"{duration}s"
            )
        )

        return response