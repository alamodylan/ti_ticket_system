from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager


db = SQLAlchemy(
    session_options={
        "expire_on_commit": False
    }
)

migrate = Migrate()

login_manager = LoginManager()
login_manager.session_protection = "strong"

bcrypt = Bcrypt()

mail = Mail()

jwt = JWTManager()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        "200 per day",
        "50 per hour"
    ]
)