from flask import (
    Blueprint,
    render_template,
    session
)

from flask_login import (
    login_required,
    current_user
)

from app.services.dashboard_service import (
    DashboardService
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


# =========================
# DASHBOARD
# =========================
@dashboard_bp.route("/")
@login_required
def index():

    selected_site_id = session.get(
        "selected_site_id"
    )

    if selected_site_id:

        try:

            selected_site_id = int(
                selected_site_id
            )

        except Exception:

            selected_site_id = None

    stats = DashboardService.get_dashboard_stats(
        user=current_user,
        site_id=selected_site_id
    )

    recent_tickets = DashboardService.get_recent_tickets(
        user=current_user,
        site_id=selected_site_id
    )

    my_tickets = DashboardService.get_user_assigned_tickets(
        user_id=current_user.id,
        site_id=selected_site_id
    )

    return render_template(
        "dashboard/index.html",
        is_admin=current_user.is_admin,
        total_tickets=stats.get(
            "total_tickets",
            0
        ),
        total_users=stats.get(
            "total_users",
            0
        ),
        total_departments=stats.get(
            "total_departments",
            0
        ),
        open_tickets=stats.get(
            "open_tickets",
            0
        ),
        closed_tickets=stats.get(
            "closed_tickets",
            0
        ),
        critical_tickets=stats.get(
            "critical_tickets",
            0
        ),
        my_total_tickets=stats.get(
            "my_total_tickets",
            0
        ),
        my_pending_tickets=stats.get(
            "my_pending_tickets",
            0
        ),
        my_resolved_tickets=stats.get(
            "my_resolved_tickets",
            0
        ),
        recent_tickets=recent_tickets,
        my_tickets=my_tickets
    )