from flask import (
    Blueprint,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from app.models.notification import Notification
from app.extensions import db

notification_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications"
)


# =========================
# GET NOTIFICATIONS
# =========================
@notification_bp.route("/")
@login_required
def get_notifications():

    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    data = []

    for notification in notifications:

        data.append({
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at": (
                notification.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        })

    return jsonify(data)


# =========================
# MARK AS READ
# =========================
@notification_bp.route(
    "/<int:notification_id>/read",
    methods=["POST"]
)
@login_required
def mark_as_read(notification_id):

    notification = Notification.query.get_or_404(
        notification_id
    )

    if notification.user_id != current_user.id:

        return jsonify({
            "success": False
        }), 403

    notification.is_read = True

    db.session.commit()

    return jsonify({
        "success": True
    })