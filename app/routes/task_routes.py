from flask import (
    Blueprint,
    current_app,
    jsonify,
    request
)

from app.services.email_pop_inbox_service import (
    EmailPopInboxService
)


task_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks"
)


@task_bp.route(
    "/process-inbox",
    methods=["GET", "POST"]
)
def process_inbox():

    token = request.args.get(
        "token"
    )

    expected_token = current_app.config.get(
        "PROCESS_INBOX_TOKEN"
    )

    if not expected_token or token != expected_token:

        return jsonify({
            "success": False,
            "message": "Token inválido."
        }), 403

    result = EmailPopInboxService.process_latest_emails(
        limit=20
    )

    return jsonify(result), 200