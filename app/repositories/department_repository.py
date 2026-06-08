from app.extensions import db
from app.models.department import Department


class DepartmentRepository:

    @staticmethod
    def get_all():

        return (
            Department.query
            .order_by(
                Department.name.asc()
            )
            .all()
        )

    @staticmethod
    def get_by_id(department_id):

        return db.session.get(
            Department,
            department_id
        )

    @staticmethod
    def get_by_name(name):

        return (
            Department.query
            .filter_by(
                name=name
            )
            .first()
        )

    @staticmethod
    def create(department):

        db.session.add(department)

        return department

    @staticmethod
    def save(department):

        db.session.add(department)

        return department

    @staticmethod
    def delete(department):

        db.session.delete(department)