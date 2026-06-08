from flask import (
    Blueprint,
    redirect,
    request,
    session,
    url_for
)

from flask_login import (
    login_required,
    current_user
)


site_bp = Blueprint(
    "sites",
    __name__,
    url_prefix="/sites"
)


@site_bp.route("/select", methods=["POST"])
@login_required
def select_site():

    if not current_user.is_admin:

        return redirect(
            url_for("dashboard.index")
        )

    site_id = request.form.get("site_id")

    if site_id:

        session["selected_site_id"] = site_id

    else:

        session.pop(
            "selected_site_id",
            None
        )

    next_url = request.form.get(
        "next"
    ) or url_for("dashboard.index")

    return redirect(next_url)