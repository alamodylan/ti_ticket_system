from app import create_app
from app.extensions import db

from app.models.user import User
from app.models.role import Role

app = create_app()

with app.app_context():

    # =========================
    # ROLE
    # =========================
    role = Role.query.filter_by(
        name="Administrador"
    ).first()

    if not role:

        role = Role(
            name="Administrador",
            description="Super usuario"
        )

        db.session.add(role)
        db.session.commit()

        print("ROL CREADO")

    # =========================
    # USER
    # =========================
    user = User.query.filter_by(
        email="soporte@alamoterminales.com"
    ).first()

    if not user:

        user = User(
            first_name="Soporte",
            last_name="TI",
            username="soporte",
            email="soporte@alamoterminales.com",
            role_id=role.id
        )

        db.session.add(user)

    # =========================
    # FORCE PASSWORD RESET
    # =========================
    user.set_password("atm0808")

    db.session.commit()

    print("USUARIO ADMIN ACTUALIZADO")