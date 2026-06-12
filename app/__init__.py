from flask import (
    Flask,
    session,
    redirect,
    url_for
)

from sqlalchemy import event

from app.config.config import Config

# =========================
# EXTENSIONS
# =========================
from app.extensions import (
    db,
    migrate,
    login_manager,
    bcrypt,
    mail,
    jwt,
    limiter
)

# =========================
# BLUEPRINTS
# =========================
from app.routes.auth_routes import auth_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.ticket_routes import ticket_bp
from app.routes.user_routes import users_bp
from app.routes.department_routes import department_bp
from app.routes.site_routes import site_bp
from app.routes.task_routes import task_bp

# =========================
# MODELS
# =========================
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.department import Department
from app.models.category import Category
from app.models.ticket import Ticket
from app.models.ticket_comment import TicketComment
from app.models.ticket_attachment import TicketAttachment
from app.models.notification import Notification
from app.models.site import Site
from app.models.audit_log import AuditLog
from app.models.email_log import EmailLog


def create_app():

    app = Flask(__name__)

    # =========================
    # LOAD CONFIG
    # =========================
    app.config.from_object(
        Config
    )

    # =========================
    # MAIL DEBUG
    # =========================
    print("\n====================")
    print("MAIL CONFIG")
    print("SERVER:", app.config.get("MAIL_SERVER"))
    print("PORT:", app.config.get("MAIL_PORT"))
    print("TLS:", app.config.get("MAIL_USE_TLS"))
    print("SSL:", app.config.get("MAIL_USE_SSL"))
    print("USER:", app.config.get("MAIL_USERNAME"))
    print("SENDER:", app.config.get("MAIL_DEFAULT_SENDER"))
    print("SUPPRESS:", app.config.get("MAIL_SUPPRESS_SEND"))
    print("====================\n")

    # =========================
    # INIT EXTENSIONS
    # =========================
    db.init_app(app)

    # =========================
    # POSTGRESQL SCHEMA
    # =========================
    database_uri = app.config.get(
        "SQLALCHEMY_DATABASE_URI",
        ""
    )

    if "postgresql" in database_uri:

        with app.app_context():

            @event.listens_for(
                db.engine,
                "connect"
            )
            def set_search_path(
                dbapi_connection,
                connection_record
            ):

                cursor = dbapi_connection.cursor()

                cursor.execute(
                    "SET search_path TO tickets_ti"
                )

                cursor.close()

    migrate.init_app(
        app,
        db
    )

    login_manager.init_app(
        app
    )

    bcrypt.init_app(
        app
    )

    mail.init_app(
        app
    )

    jwt.init_app(
        app
    )

    limiter.init_app(
        app
    )

    # =========================
    # LOGIN CONFIG
    # =========================
    login_manager.login_view = (
        "auth.login"
    )

    login_manager.login_message = (
        "Debes iniciar sesión."
    )

    login_manager.login_message_category = (
        "warning"
    )

    # =========================
    # GLOBAL TEMPLATE CONTEXT
    # =========================
    @app.context_processor
    def inject_global_context():

        admin_sites = []
        selected_site = None

        try:

            admin_sites = (
                Site.query
                .filter_by(
                    is_active=True
                )
                .order_by(
                    Site.name.asc()
                )
                .all()
            )

            selected_site_id = session.get(
                "selected_site_id"
            )

            if selected_site_id:

                selected_site = db.session.get(
                    Site,
                    int(selected_site_id)
                )

        except Exception:

            admin_sites = []
            selected_site = None

        return {
            "admin_sites": admin_sites,
            "selected_site": selected_site
        }

    # =========================
    # REGISTER BLUEPRINTS
    # =========================
    app.register_blueprint(
        auth_bp
    )

    app.register_blueprint(
        dashboard_bp
    )

    app.register_blueprint(
        ticket_bp
    )

    app.register_blueprint(
        users_bp
    )

    app.register_blueprint(
        department_bp
    )

    app.register_blueprint(
        site_bp
    )

    app.register_blueprint(
        task_bp
    )

    # =========================
    # ROOT REDIRECT
    # =========================
    @app.route("/")
    def index():

        return redirect(
            url_for("auth.login")
        )

    # =========================
    # INTERNAL INBOX SCHEDULER
    # =========================
    if app.config.get("ENABLE_INBOX_SCHEDULER"):

        try:

            from app.tasks.inbox_scheduler import start_inbox_scheduler

            start_inbox_scheduler(
                app
            )

        except Exception as error:

            print("\n====================")
            print("ERROR STARTING INBOX SCHEDULER")
            print(str(error))
            print("====================\n")

    return app