import pytest

from app import create_app
from app.extensions import db
from app.models.user import User


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


def test_login_page(client):

    response = client.get("/auth/login")

    assert response.status_code == 200


def test_register_page(client):

    response = client.get("/auth/register")

    assert response.status_code == 200


def test_create_user(app):

    with app.app_context():

        user = User(
            first_name="Admin",
            last_name="System",
            username="admin",
            email="admin@test.com"
        )

        user.set_password("Password123")

        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(
            email="admin@test.com"
        ).first()

        assert saved_user is not None
        assert saved_user.username == "admin"