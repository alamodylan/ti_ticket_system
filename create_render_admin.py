from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.role import Role


app = create_app()


with app.app_context():

    admin_role = (
        Role.query
        .filter_by(
            name="Administrador"
        )
        .first()
    )

    if not admin_role:
        raise Exception(
            "No existe el rol Administrador"
        )

    user = (
        User.query
        .filter_by(
            email="soporte@alamoterminales.com"
        )
        .first()
    )

    if not user:

        user = User(
            first_name="Wells",
            last_name="Treminio",
            email="soporte@alamoterminales.com",
            username="WTreminio",
            role_id=admin_role.id,
            is_active=True
        )

        db.session.add(user)

    user.username = "WTreminio"
    user.role_id = admin_role.id
    user.is_active = True

    user.set_password(
        "Admin12345"
    )

    db.session.commit()

    print(
        "Administrador creado/actualizado correctamente."
    )