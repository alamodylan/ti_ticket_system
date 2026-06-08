from app.extensions import db

from app.models.department import Department

from app.repositories.department_repository import (
    DepartmentRepository
)

from app.services.audit_service import (
    AuditService
)


class DepartmentService:

    @staticmethod
    def _validate_required_fields(data):

        if not data.get("name"):

            raise ValueError(
                "El nombre del departamento es requerido."
            )

    @staticmethod
    def _validate_unique_name(
        name,
        department_id=None
    ):

        existing = DepartmentRepository.get_by_name(
            name
        )

        if existing and existing.id != department_id:

            raise ValueError(
                "Ya existe un departamento con ese nombre."
            )

    @staticmethod
    def get_all_departments():

        try:

            return DepartmentRepository.get_all()

        except Exception:

            return []

    @staticmethod
    def get_department_by_id(department_id):

        try:

            return DepartmentRepository.get_by_id(
                department_id
            )

        except Exception:

            return None

    @staticmethod
    def create_department(
        data,
        created_by=None
    ):

        try:

            DepartmentService._validate_required_fields(
                data
            )

            name = data.get("name").strip()

            DepartmentService._validate_unique_name(
                name
            )

            department = Department(
                name=name,
                description=data.get("description")
            )

            DepartmentRepository.create(
                department
            )

            db.session.flush()

            try:

                AuditService.log_action(
                    action="department_created",
                    entity="department",
                    entity_id=department.id,
                    details=(
                        f"Departamento creado: {department.name}"
                    ),
                    user_id=created_by.id if created_by else None
                )

            except Exception:
                pass

            db.session.commit()

            return {
                "success": True,
                "department": department
            }

        except Exception as e:

            db.session.rollback()

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def update_department(
        department_id,
        data,
        updated_by=None
    ):

        try:

            department = DepartmentRepository.get_by_id(
                department_id
            )

            if not department:

                raise ValueError(
                    "Departamento no encontrado."
                )

            DepartmentService._validate_required_fields(
                data
            )

            name = data.get("name").strip()

            DepartmentService._validate_unique_name(
                name,
                department_id=department.id
            )

            department.name = name
            department.description = data.get("description")

            DepartmentRepository.save(
                department
            )

            db.session.flush()

            try:

                AuditService.log_action(
                    action="department_updated",
                    entity="department",
                    entity_id=department.id,
                    details=(
                        f"Departamento actualizado: {department.name}"
                    ),
                    user_id=updated_by.id if updated_by else None
                )

            except Exception:
                pass

            db.session.commit()

            return {
                "success": True,
                "department": department
            }

        except Exception as e:

            db.session.rollback()

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def deactivate_department(
        department_id,
        deactivated_by=None
    ):

        try:

            department = DepartmentRepository.get_by_id(
                department_id
            )

            if not department:

                raise ValueError(
                    "Departamento no encontrado."
                )

            department.is_active = False

            DepartmentRepository.save(
                department
            )

            db.session.flush()

            try:

                AuditService.log_action(
                    action="department_deactivated",
                    entity="department",
                    entity_id=department.id,
                    details=(
                        f"Departamento desactivado: {department.name}"
                    ),
                    user_id=deactivated_by.id if deactivated_by else None
                )

            except Exception:
                pass

            db.session.commit()

            return {
                "success": True
            }

        except Exception as e:

            db.session.rollback()

            return {
                "success": False,
                "message": str(e)
            }