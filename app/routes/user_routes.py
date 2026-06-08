from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session
)

from flask_login import (
    login_required,
    current_user
)

from app.services.user_service import (
    UserService
)

from app.models.role import Role
from app.models.site import Site
from app.models.department import Department


users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users"
)


def admin_required():

    if not current_user.is_admin:

        flash(
            "Acceso restringido.",
            "danger"
        )

        return False

    return True


def get_user_form_data():

    roles = (
        Role.query
        .order_by(
            Role.name.asc()
        )
        .all()
    )

    sites = (
        Site.query
        .order_by(
            Site.name.asc()
        )
        .all()
    )

    departments = (
        Department.query
        .order_by(
            Department.name.asc()
        )
        .all()
    )

    return roles, sites, departments


@users_bp.route("/")
@login_required
def user_list():

    if not admin_required():

        return redirect(
            url_for("dashboard.index")
        )

    selected_site_id = session.get(
        "selected_site_id"
    )

    users = UserService.get_all_users(
        site_id=selected_site_id
    )

    return render_template(
        "users/list.html",
        users=users
    )


@users_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
def create_user():

    if not admin_required():

        return redirect(
            url_for("dashboard.index")
        )

    roles, sites, departments = get_user_form_data()

    if request.method == "POST":

        data = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "role_id": request.form.get("role_id"),
            "site_id": request.form.get("site_id"),
            "department_id": request.form.get("department_id"),
            "phone": request.form.get("phone")
        }

        result = UserService.create_user(
            data=data,
            created_by=current_user
        )

        if result["success"]:

            flash(
                "Usuario creado correctamente.",
                "success"
            )

            return redirect(
                url_for("users.user_list")
            )

        flash(
            result["message"],
            "danger"
        )

    return render_template(
        "users/create.html",
        roles=roles,
        sites=sites,
        departments=departments
    )


@users_bp.route(
    "/<int:user_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_user(user_id):

    if not admin_required():

        return redirect(
            url_for("dashboard.index")
        )

    user = UserService.get_user_by_id(
        user_id
    )

    if not user:

        flash(
            "Usuario no encontrado.",
            "danger"
        )

        return redirect(
            url_for("users.user_list")
        )

    roles, sites, departments = get_user_form_data()

    if request.method == "POST":

        data = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "role_id": request.form.get("role_id"),
            "site_id": request.form.get("site_id"),
            "department_id": request.form.get("department_id"),
            "phone": request.form.get("phone")
        }

        result = UserService.update_user(
            user_id=user.id,
            data=data,
            updated_by=current_user
        )

        if result["success"]:

            flash(
                "Usuario actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("users.user_list")
            )

        flash(
            result["message"],
            "danger"
        )

    return render_template(
        "users/edit.html",
        user=user,
        roles=roles,
        sites=sites,
        departments=departments
    )


@users_bp.route(
    "/<int:user_id>/deactivate",
    methods=["POST"]
)
@login_required
def deactivate_user(user_id):

    if not admin_required():

        return redirect(
            url_for("dashboard.index")
        )

    if user_id == current_user.id:

        flash(
            "No puedes desactivar tu propio usuario.",
            "danger"
        )

        return redirect(
            url_for("users.user_list")
        )

    result = UserService.deactivate_user(
        user_id=user_id,
        deactivated_by=current_user
    )

    if result["success"]:

        flash(
            "Usuario desactivado correctamente.",
            "success"
        )

    else:

        flash(
            result["message"],
            "danger"
        )

    return redirect(
        url_for("users.user_list")
    )