from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    session,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from app.services.ticket_service import TicketService
from app.services.ticket_comment_service import TicketCommentService
from app.services.ticket_attachment_service import TicketAttachmentService
from app.services.audit_service import AuditService

from app.repositories.user_repository import UserRepository

from app.models.category import Category
from app.models.department import Department
from app.models.site import Site


ticket_bp = Blueprint(
    "tickets",
    __name__,
    url_prefix="/tickets"
)


@ticket_bp.route("/")
@login_required
def ticket_list():

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")

    selected_site_id = session.get("selected_site_id")

    sites = []

    if current_user.is_admin:
        sites = (
            Site.query
            .filter_by(is_active=True)
            .order_by(Site.name.asc())
            .all()
        )

    result = TicketService.get_filtered_tickets(
        user=current_user,
        search=search or None,
        status=status or None,
        priority=priority or None,
        site_id=selected_site_id
    )

    tickets = result.get("tickets", [])

    return render_template(
        "tickets/ticket_list.html",
        tickets=tickets,
        search=search,
        status=status,
        priority=priority,
        site_id=selected_site_id,
        sites=sites,
        valid_statuses=TicketService.VALID_STATUSES,
        valid_priorities=TicketService.VALID_PRIORITIES
    )


@ticket_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_ticket():

    categories = Category.query.all()
    departments = Department.query.all()

    if request.method == "POST":

        current_app.logger.warning("ROUTE CREATE TICKET EJECUTADA")

        data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "priority": request.form.get("priority"),
            "category_id": request.form.get("category_id"),
            "department_id": request.form.get("department_id"),
            "created_by_id": current_user.id,
            "assigned_to_id": request.form.get("assigned_to_id"),
            "site_id": current_user.site_id
        }

        result = TicketService.create_ticket(data)

        if result["success"]:
            flash("Ticket creado correctamente.", "success")
            return redirect(url_for("tickets.ticket_list"))

        flash(result["message"], "danger")

    return render_template(
        "tickets/create_ticket.html",
        categories=categories,
        departments=departments
    )


@ticket_bp.route("/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def ticket_detail(ticket_id):

    ticket = TicketService.get_ticket_by_id(
        ticket_id=ticket_id,
        user=current_user
    )

    if not ticket:
        flash("Ticket no encontrado o sin permisos.", "danger")
        return redirect(url_for("tickets.ticket_list"))

    if request.method == "POST":

        action = request.form.get("action")

        current_app.logger.warning("====================================")
        current_app.logger.warning("POST TICKET DETAIL EJECUTADO")
        current_app.logger.warning(f"Ticket ID: {ticket.id}")
        current_app.logger.warning(f"Ticket Number: {ticket.ticket_number}")
        current_app.logger.warning(f"Acción recibida: {action}")
        current_app.logger.warning(f"Usuario actual: {current_user.full_name}")
        current_app.logger.warning(f"Es admin: {current_user.is_admin}")
        current_app.logger.warning("====================================")

        flash(f"DEBUG: acción recibida -> {action}", "info")

        if action == "comment":

            result = TicketCommentService.create_comment(
                ticket_id=ticket.id,
                user_id=current_user.id,
                comment=request.form.get("comment"),
                comment_type=request.form.get("comment_type", "user"),
                user=current_user
            )

            flash(
                "Comentario agregado." if result["success"] else result["message"],
                "success" if result["success"] else "danger"
            )

        elif action == "attachment":

            result = TicketAttachmentService.save_attachment(
                ticket_id=ticket.id,
                user_id=current_user.id,
                file=request.files.get("attachment")
            )

            flash(
                "Archivo adjuntado correctamente." if result["success"] else result["message"],
                "success" if result["success"] else "danger"
            )

        elif action == "take_ticket":

            current_app.logger.warning("ROUTE TAKE TICKET EJECUTADA")

            result = TicketService.take_ticket(
                ticket=ticket,
                user=current_user
            )

            current_app.logger.warning(f"RESULTADO TAKE TICKET: {result}")

            flash(
                "Ticket tomado correctamente." if result["success"] else result["message"],
                "success" if result["success"] else "danger"
            )

        elif action == "assign_ticket":

            current_app.logger.warning("ROUTE ASSIGN TICKET EJECUTADA")

            result = TicketService.assign_ticket(
                ticket=ticket,
                assigned_to_id=request.form.get("assigned_to_id"),
                user=current_user
            )

            current_app.logger.warning(f"RESULTADO ASSIGN TICKET: {result}")

            flash(
                "Ticket asignado correctamente." if result["success"] else result["message"],
                "success" if result["success"] else "danger"
            )

        elif action == "mark_in_progress":

            current_app.logger.warning("ROUTE MARK IN PROGRESS EJECUTADA")

            result = TicketService.mark_in_progress(
                ticket=ticket,
                user=current_user
            )

            current_app.logger.warning(f"RESULTADO MARK IN PROGRESS: {result}")

            flash(
                "Ticket marcado como En Progreso." if result["success"] else result["message"],
                "success" if result["success"] else "danger"
            )

        elif action == "mark_pending":

            current_app.logger.warning("ROUTE MARK PENDING EJECUTADA")

            result = TicketService.mark_pending(
                ticket=ticket,
                user=current_user
            )

            current_app.logger.warning(f"RESULTADO MARK PENDING: {result}")

            flash(
                "Ticket marcado como Pendiente." if result["success"] else result["message"],
                "success" if result["success"] else "danger"
            )

        elif action == "resolve_ticket":

            current_app.logger.warning("ROUTE RESOLVE TICKET EJECUTADA")

            result = TicketService.resolve_ticket(
                ticket=ticket,
                user=current_user
            )

            current_app.logger.warning(f"RESULTADO RESOLVE TICKET: {result}")

            flash(
                "Ticket marcado como Resuelto." if result["success"] else result["message"],
                "success" if result["success"] else "danger"
            )

        elif action == "close_ticket":

            current_app.logger.warning("ROUTE CLOSE TICKET EJECUTADA")

            result = TicketService.close_ticket(
                ticket=ticket,
                user=current_user
            )

            current_app.logger.warning(f"RESULTADO CLOSE TICKET: {result}")

            flash(
                "Ticket cerrado correctamente." if result["success"] else result["message"],
                "success" if result["success"] else "danger"
            )

        else:

            current_app.logger.warning(f"ACCIÓN NO VÁLIDA RECIBIDA: {action}")
            flash("Acción no válida.", "warning")

        return redirect(
            url_for(
                "tickets.ticket_detail",
                ticket_id=ticket.id
            )
        )

    comments_result = TicketCommentService.get_comments_by_ticket(
        ticket_id=ticket.id,
        user=current_user
    )

    attachments_result = TicketAttachmentService.get_attachments_by_ticket(
        ticket.id
    )

    audit_logs = AuditService.get_ticket_history(
        ticket.id
    )

    admin_users = []

    if current_user.is_admin:
        admin_users = UserRepository.get_admin_users(
            site_id=ticket.site_id
        )

    return render_template(
        "tickets/ticket_detail.html",
        ticket=ticket,
        comments=comments_result.get("comments", []),
        attachments=attachments_result.get("attachments", []),
        audit_logs=audit_logs,
        admin_users=admin_users,
        valid_statuses=TicketService.VALID_STATUSES,
        valid_priorities=TicketService.VALID_PRIORITIES
    )


@ticket_bp.route("/<int:ticket_id>/edit", methods=["GET", "POST"])
@login_required
def edit_ticket(ticket_id):

    if not current_user.is_admin:
        flash("No tiene permisos para editar tickets.", "danger")
        return redirect(url_for("dashboard.index"))

    ticket = TicketService.get_ticket_by_id(
        ticket_id=ticket_id,
        user=current_user
    )

    if not ticket:
        flash("Ticket no encontrado.", "danger")
        return redirect(url_for("tickets.ticket_list"))

    if ticket.status == "Cerrado":
        flash("No se puede editar un ticket cerrado.", "warning")
        return redirect(
            url_for(
                "tickets.ticket_detail",
                ticket_id=ticket.id
            )
        )

    if request.method == "POST":

        current_app.logger.warning("ROUTE EDIT TICKET EJECUTADA")

        info_result = TicketService.update_ticket_info(
            ticket=ticket,
            title=request.form.get("title"),
            description=request.form.get("description"),
            user=current_user
        )

        if not info_result["success"]:
            flash(info_result["message"], "danger")
            return redirect(
                url_for(
                    "tickets.edit_ticket",
                    ticket_id=ticket.id
                )
            )

        status_result = TicketService.update_status(
            ticket=ticket,
            status=request.form.get("status"),
            user=current_user
        )

        if not status_result["success"]:
            flash(status_result["message"], "danger")
            return redirect(
                url_for(
                    "tickets.edit_ticket",
                    ticket_id=ticket.id
                )
            )

        priority_result = TicketService.change_priority(
            ticket=ticket,
            priority=request.form.get("priority"),
            user=current_user
        )

        if not priority_result["success"]:
            flash(priority_result["message"], "danger")
            return redirect(
                url_for(
                    "tickets.edit_ticket",
                    ticket_id=ticket.id
                )
            )

        flash("Ticket actualizado correctamente.", "success")

        return redirect(
            url_for(
                "tickets.ticket_detail",
                ticket_id=ticket.id
            )
        )

    return render_template(
        "tickets/edit_ticket.html",
        ticket=ticket,
        valid_statuses=TicketService.VALID_STATUSES,
        valid_priorities=TicketService.VALID_PRIORITIES
    )