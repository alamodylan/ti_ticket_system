import click

from app.extensions import db
from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User


# =========================
# REGISTER COMMANDS
# =========================
def register_commands(app):

    app.cli.add_command(seed_permissions)
    app.cli.add_command(seed_roles)
    app.cli.add_command(seed_admin)


# =========================
# SEED PERMISSIONS
# =========================
@click.command("seed-permissions")
def seed_permissions():

    permissions = [

        # =========================
        # TICKETS
        # =========================
        {
            "name": "Ver Tickets",
            "code": "ticket.view"
        },

        {
            "name": "Crear Tickets",
            "code": "ticket.create"
        },

        {
            "name": "Editar Tickets",
            "code": "ticket.edit"
        },

        {
            "name": "Eliminar Tickets",
            "code": "ticket.delete"
        },

        {
            "name": "Asignar Tickets",
            "code": "ticket.assign"
        },

        # =========================
        # USERS
        # =========================
        {
            "name": "Ver Usuarios",
            "code": "user.view"
        },

        {
            "name": "Crear Usuarios",
            "code": "user.create"
        },

        {
            "name": "Editar Usuarios",
            "code": "user.edit"
        },

        {
            "name": "Eliminar Usuarios",
            "code": "user.delete"
        },

        # =========================
        # DASHBOARD
        # =========================
        {
            "name": "Ver Dashboard",
            "code": "dashboard.view"
        }
    ]

    created = 0

    for data in permissions:

        exists = Permission.query.filter_by(
            code=data["code"]
        ).first()

        if exists:
            continue

        permission = Permission(
            name=data["name"],
            code=data["code"]
        )

        db.session.add(permission)

        created += 1

    db.session.commit()

    click.echo(
        f"{created} permisos creados."
    )


# =========================
# SEED ROLES
# =========================
@click.command("seed-roles")
def seed_roles():

    roles = [

        {
            "name": "Admin",
            "description": "Administrador del sistema"
        },

        {
            "name": "Tecnico",
            "description": "Soporte TI"
        },

        {
            "name": "Empleado",
            "description": "Usuario normal"
        }
    ]

    created = 0

    for data in roles:

        exists = Role.query.filter_by(
            name=data["name"]
        ).first()

        if exists:
            continue

        role = Role(
            name=data["name"],
            description=data["description"]
        )

        db.session.add(role)

        created += 1

    db.session.commit()

    click.echo(
        f"{created} roles creados."
    )


# =========================
# SEED ADMIN
# =========================
@click.command("seed-admin")
def seed_admin():

    admin = User.query.filter_by(
        email="admin@empresa.com"
    ).first()

    if admin:

        click.echo(
            "Admin ya existe."
        )

        return

    role = Role.query.filter_by(
        name="Admin"
    ).first()

    if not role:

        click.echo(
            "Primero ejecute seed-roles"
        )

        return

    user = User(
        first_name="System",
        last_name="Admin",
        email="admin@empresa.com",
        username="admin",
        role_id=role.id
    )

    user.set_password(
        "Admin123*"
    )

    db.session.add(user)

    db.session.commit()

    click.echo(
        "Usuario admin creado."
    )