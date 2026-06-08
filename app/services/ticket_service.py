from app.repositories.ticket_repository import TicketRepository
from app.repositories.user_repository import UserRepository

from app.services.notification_service import NotificationService
from app.services.email_service import EmailService
from app.services.audit_service import AuditService

from app.extensions import db


class TicketService:

    VALID_STATUSES = [
        "Nuevo",
        "Asignado",
        "En Progreso",
        "Pendiente",
        "Resuelto",
        "Cerrado"
    ]

    VALID_PRIORITIES = [
        "Baja",
        "Media",
        "Alta",
        "Crítica"
    ]

    @staticmethod
    def generate_ticket_number(ticket_id):
        return f"TK-{ticket_id:03d}"

    @staticmethod
    def _validate_required_fields(data):

        required = [
            "title",
            "description",
            "created_by_id"
        ]

        for field in required:
            if not data.get(field):
                raise ValueError(f"{field} es requerido.")

    @staticmethod
    def _validate_priority(priority):

        if priority not in TicketService.VALID_PRIORITIES:
            raise ValueError("Prioridad inválida.")

    @staticmethod
    def _validate_status(status):

        if status not in TicketService.VALID_STATUSES:
            raise ValueError("Estado inválido.")

    @staticmethod
    def _validate_admin(user):

        if not user or not user.is_admin:
            raise ValueError("No tiene permisos para gestionar tickets.")

    @staticmethod
    def _validate_ticket_open(ticket):

        if ticket.status == "Cerrado":
            raise ValueError("No se puede modificar un ticket cerrado.")

    @staticmethod
    def create_ticket(data):

        try:

            TicketService._validate_required_fields(data)

            priority = data.get("priority") or "Media"
            status = data.get("status") or "Nuevo"
            source = data.get("source") or "manual"
            email_message_id = data.get("email_message_id")

            TicketService._validate_priority(priority)
            TicketService._validate_status(status)

            if source == "email" and email_message_id:

                existing_ticket = TicketRepository.get_by_email_message_id(
                    email_message_id
                )

                if existing_ticket:

                    return {
                        "success": True,
                        "ticket": existing_ticket,
                        "message": "El correo ya fue procesado previamente."
                    }

            ticket = TicketRepository.create(
                ticket_number="TEMP",
                title=data["title"],
                description=data["description"],
                priority=priority,
                status=status,
                created_by_id=data["created_by_id"],
                assigned_to_id=data.get("assigned_to_id"),
                category_id=data.get("category_id"),
                department_id=data.get("department_id"),
                site_id=data.get("site_id"),
                requester_name=data.get("requester_name"),
                requester_email=data.get("requester_email"),
                requester_phone=data.get("requester_phone"),
                source=source,
                email_message_id=email_message_id,
                email_subject=data.get("email_subject")
            )

            db.session.flush()

            ticket.ticket_number = TicketService.generate_ticket_number(
                ticket.id
            )

            TicketRepository.save(ticket)

            db.session.commit()

            try:

                AuditService.log_action(
                    action="ticket_created",
                    entity="ticket",
                    entity_id=ticket.id,
                    details=(
                        f"Ticket {ticket.ticket_number} creado "
                        f"desde {ticket.source_label}"
                    ),
                    user_id=ticket.created_by_id
                )

            except Exception as error:

                print("\n====================")
                print("ERROR AUDITORIA CREATE TICKET")
                print(str(error))
                print("====================\n")

            if ticket.assigned_to_id:

                try:

                    NotificationService.create_notification(
                        user_id=ticket.assigned_to_id,
                        title="Nuevo ticket asignado",
                        message=f"Se le asignó el ticket {ticket.ticket_number}"
                    )

                except Exception as error:

                    print("\n====================")
                    print("ERROR NOTIFICACION CREATE TICKET")
                    print(str(error))
                    print("====================\n")

            return {
                "success": True,
                "ticket": ticket
            }

        except Exception as e:

            db.session.rollback()

            print("\n====================")
            print("ERROR CREATE TICKET")
            print(str(e))
            print("====================\n")

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def update_status(ticket, status, user=None):

        try:

            TicketService._validate_status(status)
            TicketService._validate_ticket_open(ticket)

            old_status = ticket.status
            ticket.status = status

            TicketRepository.save(ticket)

            db.session.commit()

            try:

                AuditService.log_action(
                    action="ticket_status_updated",
                    entity="ticket",
                    entity_id=ticket.id,
                    details=f"Estado cambiado de {old_status} a {status}",
                    user_id=user.id if user else None
                )

            except Exception as error:

                print("\n====================")
                print("ERROR AUDITORIA UPDATE STATUS")
                print(str(error))
                print("====================\n")

            return {
                "success": True
            }

        except Exception as e:

            db.session.rollback()

            print("\n====================")
            print("ERROR UPDATE STATUS")
            print(str(e))
            print("====================\n")

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def change_priority(ticket, priority, user=None):

        try:

            TicketService._validate_priority(priority)
            TicketService._validate_ticket_open(ticket)

            old_priority = ticket.priority
            ticket.priority = priority

            TicketRepository.save(ticket)

            db.session.commit()

            try:

                AuditService.log_action(
                    action="ticket_priority_updated",
                    entity="ticket",
                    entity_id=ticket.id,
                    details=f"Prioridad cambiada de {old_priority} a {priority}",
                    user_id=user.id if user else None
                )

            except Exception as error:

                print("\n====================")
                print("ERROR AUDITORIA CHANGE PRIORITY")
                print(str(error))
                print("====================\n")

            return {
                "success": True
            }

        except Exception as e:

            db.session.rollback()

            print("\n====================")
            print("ERROR CHANGE PRIORITY")
            print(str(e))
            print("====================\n")

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def update_ticket_info(ticket, title, description, user=None):

        try:

            TicketService._validate_ticket_open(ticket)

            if not title:
                raise ValueError("El título es requerido.")

            if not description:
                raise ValueError("La descripción es requerida.")

            ticket.title = title
            ticket.description = description

            TicketRepository.save(ticket)

            db.session.commit()

            try:

                AuditService.log_action(
                    action="ticket_updated",
                    entity="ticket",
                    entity_id=ticket.id,
                    details="Información del ticket actualizada",
                    user_id=user.id if user else None
                )

            except Exception as error:

                print("\n====================")
                print("ERROR AUDITORIA UPDATE TICKET INFO")
                print(str(error))
                print("====================\n")

            return {
                "success": True
            }

        except Exception as e:

            db.session.rollback()

            print("\n====================")
            print("ERROR UPDATE TICKET INFO")
            print(str(e))
            print("====================\n")

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def take_ticket(ticket, user):

        try:

            TicketService._validate_admin(user)
            TicketService._validate_ticket_open(ticket)

            ticket.assigned_to_id = user.id
            ticket.status = "Asignado"

            TicketRepository.save(ticket)

            db.session.commit()

            try:

                AuditService.log_action(
                    action="ticket_taken",
                    entity="ticket",
                    entity_id=ticket.id,
                    details=f"Ticket tomado por {user.full_name}",
                    user_id=user.id
                )

            except Exception as error:

                print("\n====================")
                print("ERROR AUDITORIA TAKE TICKET")
                print(str(error))
                print("====================\n")

            EmailService.send_ticket_taken_email(ticket)

            return {
                "success": True
            }

        except Exception as e:

            db.session.rollback()

            print("\n====================")
            print("ERROR TAKE TICKET")
            print(str(e))
            print("====================\n")

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def assign_ticket(ticket, assigned_to_id, user):

        try:

            TicketService._validate_admin(user)
            TicketService._validate_ticket_open(ticket)

            assigned_user = UserRepository.get_by_id(
                int(assigned_to_id)
            )

            if not assigned_user:
                raise ValueError("Usuario asignado no encontrado.")

            if not assigned_user.is_admin:
                raise ValueError("Solo se puede asignar a un responsable TI.")

            old_assigned = (
                ticket.assigned_to.full_name
                if ticket.assigned_to
                else "Sin asignar"
            )

            ticket.assigned_to_id = assigned_user.id
            ticket.status = "Asignado"

            TicketRepository.save(ticket)

            db.session.commit()

            try:

                AuditService.log_action(
                    action="ticket_assigned",
                    entity="ticket",
                    entity_id=ticket.id,
                    details=(
                        f"Asignado de {old_assigned} "
                        f"a {assigned_user.full_name}"
                    ),
                    user_id=user.id
                )

            except Exception as error:

                print("\n====================")
                print("ERROR AUDITORIA ASSIGN TICKET")
                print(str(error))
                print("====================\n")

            try:

                NotificationService.create_notification(
                    user_id=assigned_user.id,
                    title="Ticket asignado",
                    message=f"Se le asignó el ticket {ticket.ticket_number}"
                )

            except Exception as error:

                print("\n====================")
                print("ERROR NOTIFICACION ASSIGN TICKET")
                print(str(error))
                print("====================\n")

            return {
                "success": True
            }

        except Exception as e:

            db.session.rollback()

            print("\n====================")
            print("ERROR ASSIGN TICKET")
            print(str(e))
            print("====================\n")

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def mark_in_progress(ticket, user):

        return TicketService.update_status(
            ticket=ticket,
            status="En Progreso",
            user=user
        )

    @staticmethod
    def mark_pending(ticket, user):

        return TicketService.update_status(
            ticket=ticket,
            status="Pendiente",
            user=user
        )

    @staticmethod
    def resolve_ticket(ticket, user):

        return TicketService.update_status(
            ticket=ticket,
            status="Resuelto",
            user=user
        )

    @staticmethod
    def close_ticket(ticket, user):

        try:

            TicketService._validate_admin(user)

            if ticket.status == "Cerrado":
                raise ValueError("El ticket ya está cerrado.")

            old_status = ticket.status
            ticket.status = "Cerrado"

            TicketRepository.save(ticket)

            db.session.commit()

            try:

                AuditService.log_action(
                    action="ticket_closed",
                    entity="ticket",
                    entity_id=ticket.id,
                    details=f"Ticket cerrado. Estado anterior: {old_status}",
                    user_id=user.id
                )

            except Exception as error:

                print("\n====================")
                print("ERROR AUDITORIA CLOSE TICKET")
                print(str(error))
                print("====================\n")

            EmailService.send_ticket_closed_email(ticket)

            return {
                "success": True
            }

        except Exception as e:

            db.session.rollback()

            print("\n====================")
            print("ERROR CLOSE TICKET")
            print(str(e))
            print("====================\n")

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def get_filtered_tickets(
        user,
        search=None,
        status=None,
        priority=None,
        site_id=None
    ):

        try:

            tickets = TicketRepository.filter_tickets(
                user=user,
                search=search,
                status=status,
                priority=priority,
                site_id=site_id
            )

            return {
                "success": True,
                "tickets": tickets
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e),
                "tickets": []
            }

    @staticmethod
    def get_all_tickets(user):

        try:

            return TicketRepository.get_all(user=user)

        except Exception:

            return []

    @staticmethod
    def get_ticket_by_id(ticket_id, user):

        try:

            return TicketRepository.get_by_id(
                ticket_id=ticket_id,
                user=user
            )

        except Exception:

            return None