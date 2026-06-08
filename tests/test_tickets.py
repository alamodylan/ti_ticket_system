import pytest

from app import create_app
from app.extensions import db

from app.models.user import User
from app.models.ticket import Ticket


@pytest.fixture
def app():

    app = create_app("testing")

    with app.app_context():

        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):

    return app.test_client()


def test_ticket_creation(app):

    with app.app_context():

        user = User(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john@test.com"
        )

        user.set_password("Password123")

        db.session.add(user)
        db.session.commit()

        ticket = Ticket(
            title="Problema VPN",
            description="No conecta VPN",
            created_by_id=user.id
        )

        db.session.add(ticket)
        db.session.commit()

        saved_ticket = Ticket.query.first()

        assert saved_ticket is not None
        assert saved_ticket.title == "Problema VPN"


def test_ticket_list_page(client):

    response = client.get("/tickets")

    assert response.status_code in [200, 302]