from flask import (
    request,
    g
)

from datetime import datetime


# =========================
# REQUEST MIDDLEWARE
# =========================
def register_request_middleware(app):

    @app.before_request
    def attach_request_metadata():

        g.request_time = datetime.utcnow()

        g.client_ip = (
            request.headers.get(
                "X-Forwarded-For",
                request.remote_addr
            )
        )

        g.user_agent = request.user_agent.string

    @app.after_request
    def add_security_headers(response):

        # =========================
        # SECURITY HEADERS
        # =========================
        response.headers[
            "X-Frame-Options"
        ] = "SAMEORIGIN"

        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"

        response.headers[
            "Referrer-Policy"
        ] = "strict-origin-when-cross-origin"

        response.headers[
            "Permissions-Policy"
        ] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=()"
        )

        response.headers[
            "X-XSS-Protection"
        ] = "1; mode=block"

        return response