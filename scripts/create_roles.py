import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app import create_app
from app.extensions import db

from app.models.role import Role


app = create_app()

with app.app_context():

    admin_role = Role.query.filter_by(
        name="Administrador"
    ).first()

    if not admin_role:

        admin_role = Role(
            name="Administrador",
            description="Acceso total al sistema"
        )

        db.session.add(admin_role)

        print("ROL ADMINISTRADOR CREADO")

    user_role = Role.query.filter_by(
        name="Usuario"
    ).first()

    if not user_role:

        user_role = Role(
            name="Usuario",
            description="Usuario normal del sistema"
        )

        db.session.add(user_role)

        print("ROL USUARIO CREADO")

    db.session.commit()

    print("ROLES VERIFICADOS")