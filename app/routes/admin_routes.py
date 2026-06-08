from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for
)

from flask_login import (
    current_user
)

from app.decorators.permission_decorator import (
    admin_required
)

from app.models.user import User
from app.models.role import Role
from app.models.department import Department
from app.models.category import Category
from app.models.ticket import Ticket


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# =========================
# ADMIN DASHBOARD
# =========================
@admin_bp.route("/")
@admin_required
def index():

    try:

        users = User.query.order_by(
            User.created_at.desc()
        ).all()

        roles = Role.query.order_by(
            Role.name.asc()
        ).all()

        departments = Department.query.order_by(
            Department.name.asc()
        ).all()

        categories = Category.query.order_by(
            Category.name.asc()
        ).all()

        tickets = Ticket.query.order_by(
            Ticket.created_at.desc()
        ).limit(10).all()

        stats = {

            "total_users": User.query.count(),

            "total_roles": Role.query.count(),

            "total_departments": (
                Department.query.count()
            ),

            "total_categories": (
                Category.query.count()
            ),

            "total_tickets": (
                Ticket.query.count()
            )
        }

        return render_template(
            "admin/index.html",
            users=users,
            roles=roles,
            departments=departments,
            categories=categories,
            tickets=tickets,
            stats=stats
        )

    except Exception:

        flash(
            "Error cargando panel administrativo.",
            "danger"
        )

        return redirect(
            url_for(
                "dashboard.index"
            )
        )