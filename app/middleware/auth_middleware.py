from flask import (
    request,
    jsonify
)

from flask_login import (
    current_user
)


# =========================
# AUTHENTICATION MIDDLEWARE
# =========================
def register_auth_middleware(app):

    @app.before_request
    def check_authentication():

        public_routes = [
            "auth.login",
            "static"
        ]

        if request.endpoint is None:
            return

        if request.endpoint in public_routes:
            return

        # Skip API auth for now
        if request.path.startswith("/api/"):
            return

        # Skip static files
        if request.path.startswith("/static/"):
            return

        # User not authenticated
        if not current_user.is_authenticated:

            return jsonify({
                "success": False,
                "message": "Authentication required."
            }), 401