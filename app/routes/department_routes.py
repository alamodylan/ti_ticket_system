from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_required,
    current_user
)

from app.services.department_service import (
    DepartmentService
)


department_bp = Blueprint(
    "departments",
    __name__,
    url_prefix="/departments"
)


def admin_required():

    if not current_user.is_admin:

        flash(
            "Acceso restringido.",
            "danger"
        )

        return False

    return True


@department_bp.route("/")
@login_required
def department_list():

    if not admin_required():

        return redirect(
            url_for("dashboard.index")
        )

    departments = DepartmentService.get_all_departments()

    return render_template(
        "departments/list.html",
        departments=departments
    )


@department_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
def create_department():

    if not admin_required():

        return redirect(
            url_for("dashboard.index")
        )

    if request.method == "POST":

        data = {
            "name": request.form.get("name"),
            "description": request.form.get("description")
        }

        result = DepartmentService.create_department(
            data=data,
            created_by=current_user
        )

        if result["success"]:

            flash(
                "Departamento creado correctamente.",
                "success"
            )

            return redirect(
                url_for("departments.department_list")
            )

        flash(
            result["message"],
            "danger"
        )

    return render_template(
        "departments/create.html"
    )


@department_bp.route(
    "/<int:department_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_department(department_id):

    if not admin_required():

        return redirect(
            url_for("dashboard.index")
        )

    department = DepartmentService.get_department_by_id(
        department_id
    )

    if not department:

        flash(
            "Departamento no encontrado.",
            "danger"
        )

        return redirect(
            url_for("departments.department_list")
        )

    if request.method == "POST":

        data = {
            "name": request.form.get("name"),
            "description": request.form.get("description")
        }

        result = DepartmentService.update_department(
            department_id=department.id,
            data=data,
            updated_by=current_user
        )

        if result["success"]:

            flash(
                "Departamento actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("departments.department_list")
            )

        flash(
            result["message"],
            "danger"
        )

    return render_template(
        "departments/edit.html",
        department=department
    )


@department_bp.route(
    "/<int:department_id>/deactivate",
    methods=["POST"]
)
@login_required
def deactivate_department(department_id):

    if not admin_required():

        return redirect(
            url_for("dashboard.index")
        )

    result = DepartmentService.deactivate_department(
        department_id=department_id,
        deactivated_by=current_user
    )

    if result["success"]:

        flash(
            "Departamento desactivado correctamente.",
            "success"
        )

    else:

        flash(
            result["message"],
            "danger"
        )

    return redirect(
        url_for("departments.department_list")
    )