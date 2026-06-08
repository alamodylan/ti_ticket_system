from flask import (
    Blueprint,
    jsonify,
    request
)

from app.extensions import db

from app.models.ticket import Ticket

ticket_api_bp = Blueprint(
    "ticket_api",
    __name__,
    url_prefix="/api/tickets"
)


# =========================
# GET ALL TICKETS
# =========================
@ticket_api_bp.route(
    "/",
    methods=["GET"]
)
def get_tickets():

    tickets = Ticket.query.order_by(
        Ticket.created_at.desc()
    ).all()

    data = []

    for ticket in tickets:

        data.append({
            "id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "title": ticket.title,
            "status": ticket.status,
            "priority": ticket.priority,
            "created_by": (
                ticket.created_by.full_name
                if ticket.created_by
                else None
            ),
            "assigned_to": (
                ticket.assigned_to.full_name
                if ticket.assigned_to
                else None
            ),
            "created_at": (
                ticket.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        })

    return jsonify(data)


# =========================
# GET SINGLE TICKET
# =========================
@ticket_api_bp.route(
    "/<int:ticket_id>",
    methods=["GET"]
)
def get_ticket(ticket_id):

    ticket = Ticket.query.get_or_404(
        ticket_id
    )

    return jsonify({
        "id": ticket.id,
        "ticket_number": ticket.ticket_number,
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "created_by": (
            ticket.created_by.full_name
            if ticket.created_by
            else None
        ),
        "assigned_to": (
            ticket.assigned_to.full_name
            if ticket.assigned_to
            else None
        ),
        "category": (
            ticket.category.name
            if ticket.category
            else None
        ),
        "department": (
            ticket.department.name
            if ticket.department
            else None
        )
    })


# =========================
# CREATE TICKET
# =========================
@ticket_api_bp.route(
    "/create",
    methods=["POST"]
)
def create_ticket():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No data provided."
        }), 400

    ticket = Ticket(
        ticket_number="TEMP",
        title=data.get("title"),
        description=data.get("description"),
        priority=data.get("priority", "Media"),
        status="Nuevo",
        created_by_id=data.get("created_by_id"),
        category_id=data.get("category_id"),
        department_id=data.get("department_id")
    )

    db.session.add(ticket)
    db.session.commit()

    ticket.ticket_number = (
        f"TK-2026-{ticket.id:04d}"
    )

    db.session.commit()

    return jsonify({
        "success": True,
        "ticket_id": ticket.id,
        "ticket_number": ticket.ticket_number
    }), 201