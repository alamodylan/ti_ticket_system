from app import create_app
from app.extensions import db

from app.models.user import User
from app.models.role import Role
from app.models.site import Site
from app.models.department import Department
from app.models.category import Category


app = create_app()


def get_or_create(model, defaults=None, **kwargs):

    instance = model.query.filter_by(
        **kwargs
    ).first()

    if instance:
        return instance

    params = dict(kwargs)

    if defaults:
        params.update(defaults)

    instance = model(**params)

    db.session.add(instance)

    return instance


with app.app_context():

    sites = [
        {"name": "COYOL", "code": "CRSJO33"},
        {"name": "CALDERA", "code": "CRCAL33"},
        {"name": "LIMON", "code": "CRLIO34"}
    ]

    for site_data in sites:

        get_or_create(
            Site,
            name=site_data["name"],
            code=site_data["code"]
        )

    db.session.commit()

    print("SITIOS VERIFICADOS")

    roles = [
        {
            "name": "Administrador",
            "description": "Administrador general del sistema"
        },
        {
            "name": "Usuario",
            "description": "Usuario estándar del sistema"
        }
    ]

    for role_data in roles:

        get_or_create(
            Role,
            defaults={
                "description": role_data["description"]
            },
            name=role_data["name"]
        )

    db.session.commit()

    print("ROLES VERIFICADOS")

    departments = [
        "TI",
        "Administración",
        "Operaciones",
        "Control Equipo",
        "Inspección",
        "Seguridad",
        "Mantenimiento",
        "Auditoría",
        "Tracking",
        "Bodega",
        "Facturación",
        "Contabilidad",
        "Trámites",
        "Crédito y Cobro",
        "Supervisión",
        "RRHH",
        "Control Interno",
        "Vapores",
        "Proveeduría",
        "Pago Choferes",
        "Despacho",
        "Tráfico"
    ]

    for department_name in departments:

        get_or_create(
            Department,
            defaults={
                "description": f"Departamento de {department_name}"
            },
            name=department_name
        )

    db.session.commit()

    print("DEPARTAMENTOS VERIFICADOS")

    categories = [
        {
            "name": "Soporte Técnico",
            "description": "Incidentes técnicos generales"
        },
        {
            "name": "Redes",
            "description": "Problemas de red o conectividad"
        },
        {
            "name": "Hardware",
            "description": "Problemas relacionados con equipos físicos"
        },
        {
            "name": "Software",
            "description": "Problemas relacionados con aplicaciones"
        },
        {
            "name": "Accesos",
            "description": "Solicitudes de usuarios, claves o permisos"
        }
    ]

    for category_data in categories:

        get_or_create(
            Category,
            defaults={
                "description": category_data["description"]
            },
            name=category_data["name"]
        )

    db.session.commit()

    print("CATEGORÍAS VERIFICADAS")

    admin_role = Role.query.filter_by(
        name="Administrador"
    ).first()

    default_site = Site.query.filter_by(
        code="CRSJO33"
    ).first()

    default_department = Department.query.filter_by(
        name="TI"
    ).first()

    admin_user = User.query.filter_by(
        email="soporte@alamoterminales.com"
    ).first()

    if not admin_user:

        admin_user = User(
            first_name="Soporte",
            last_name="TI",
            username="admin",
            email="soporte@alamoterminales.com",
            role_id=admin_role.id,
            site_id=default_site.id,
            department_id=default_department.id,
            is_active=True
        )

        admin_user.set_password(
            "atm0808"
        )

        db.session.add(admin_user)

        db.session.commit()

        print("ADMIN CREADO")

    else:

        print("ADMIN YA EXISTE")

    print("SEED FINALIZADO CORRECTAMENTE")