from sqlalchemy import or_

from app.models.ticket import Ticket
from app.models.user import User
from app.models.department import Department


class DashboardService:

    OPEN_STATUSES = [
        "Nuevo",
        "Asignado",
        "En Progreso",
        "Pendiente"
    ]

    RESOLVED_STATUSES = [
        "Resuelto",
        "Cerrado"
    ]

    @staticmethod
    def _user_tickets_query(user):

        return Ticket.query.filter(
            or_(
                Ticket.created_by_id == user.id,
                Ticket.assigned_to_id == user.id
            )
        )

    @staticmethod
    def _apply_site_filter(
        query,
        model,
        site_id=None
    ):

        if site_id:

            query = query.filter(
                model.site_id == site_id
            )

        return query

    @staticmethod
    def get_dashboard_stats(
        user,
        site_id=None
    ):

        if user.is_admin:

            tickets_query = DashboardService._apply_site_filter(
                Ticket.query,
                Ticket,
                site_id
            )

            users_query = DashboardService._apply_site_filter(
                User.query,
                User,
                site_id
            )

            return {
                "total_tickets": tickets_query.count(),
                "total_users": users_query.count(),
                "total_departments": Department.query.count(),
                "open_tickets": tickets_query.filter(
                    Ticket.status.in_(
                        DashboardService.OPEN_STATUSES
                    )
                ).count(),
                "closed_tickets": tickets_query.filter_by(
                    status="Cerrado"
                ).count(),
                "critical_tickets": tickets_query.filter_by(
                    priority="Crítica"
                ).count(),
                "my_total_tickets": 0,
                "my_pending_tickets": 0,
                "my_resolved_tickets": 0
            }

        user_tickets_query = DashboardService._user_tickets_query(
            user
        )

        return {
            "total_tickets": 0,
            "total_users": 0,
            "total_departments": 0,
            "open_tickets": 0,
            "closed_tickets": 0,
            "critical_tickets": 0,
            "my_total_tickets": user_tickets_query.count(),
            "my_pending_tickets": user_tickets_query.filter(
                Ticket.status.in_(
                    DashboardService.OPEN_STATUSES
                )
            ).count(),
            "my_resolved_tickets": user_tickets_query.filter(
                Ticket.status.in_(
                    DashboardService.RESOLVED_STATUSES
                )
            ).count()
        }

    @staticmethod
    def get_recent_tickets(
        user,
        limit=10,
        site_id=None
    ):

        query = Ticket.query

        if not user.is_admin:

            query = DashboardService._user_tickets_query(
                user
            )

        if user.is_admin and site_id:

            query = query.filter(
                Ticket.site_id == site_id
            )

        return (
            query
            .order_by(
                Ticket.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_user_assigned_tickets(
        user_id,
        limit=10,
        site_id=None
    ):

        query = Ticket.query.filter(
            Ticket.assigned_to_id == user_id
        )

        if site_id:

            query = query.filter(
                Ticket.site_id == site_id
            )

        return (
            query
            .order_by(
                Ticket.created_at.desc()
            )
            .limit(limit)
            .all()
        )