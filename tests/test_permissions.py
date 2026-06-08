import pytest

from app import create_app
from app.extensions import db

from app.models.role import Role
from app.models.permission import Permission


@pytest.fixture
def app():

    app = create_app("testing")

    with app.app_context():

        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


def test_create_permission(app):

    with app.app_context():

        permission = Permission(
            name="Crear Ticket",
            code="ticket.create",
            description="Permite crear tickets"
        )

        db.session.add(permission)
        db.session.commit()

        saved_permission = Permission.query.filter_by(
            code="ticket.create"
        ).first()

        assert saved_permission is not None


def test_create_role(app):

    with app.app_context():

        role = Role(
            name="Administrador",
            description="Acceso total"
        )

        db.session.add(role)
        db.session.commit()

        saved_role = Role.query.filter_by(
            name="Administrador"
        ).first()

        assert saved_role is not None