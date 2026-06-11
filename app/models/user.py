from flask_login import UserMixin

from app.extensions import (
    db,
    bcrypt,
    login_manager
)

from app.database import BaseModel


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


class User(BaseModel, UserMixin):

    __tablename__ = "users"

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    phone = db.Column(
        db.String(30)
    )

    profile_image = db.Column(
        db.String(255)
    )

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets_ti.roles.id"),
        nullable=False,
        index=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets_ti.departments.id"),
        index=True
    )

    site_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets_ti.sites.id"),
        index=True
    )

    role = db.relationship(
        "Role",
        back_populates="users"
    )

    department = db.relationship(
        "Department",
        back_populates="users"
    )

    site = db.relationship(
        "Site",
        back_populates="users"
    )

    created_tickets = db.relationship(
        "Ticket",
        foreign_keys="Ticket.created_by_id",
        back_populates="created_by"
    )

    assigned_tickets = db.relationship(
        "Ticket",
        foreign_keys="Ticket.assigned_to_id",
        back_populates="assigned_to"
    )

    comments = db.relationship(
        "TicketComment",
        back_populates="user"
    )

    notifications = db.relationship(
        "Notification",
        back_populates="user"
    )

    def set_password(self, password):

        self.password_hash = (
            bcrypt.generate_password_hash(
                password
            ).decode("utf-8")
        )

    def check_password(self, password):

        return bcrypt.check_password_hash(
            self.password_hash,
            password
        )

    @property
    def full_name(self):

        return (
            f"{self.first_name} "
            f"{self.last_name}"
        )

    @property
    def role_name(self):

        if not self.role:
            return "Sin rol"

        return self.role.name

    @property
    def department_name(self):

        if not self.department:
            return "Sin departamento"

        return self.department.name

    @property
    def site_name(self):

        if not self.site:
            return "Sin sede"

        return self.site.name

    @property
    def created_tickets_count(self):

        return len(
            self.created_tickets
        )

    @property
    def assigned_tickets_count(self):

        return len(
            self.assigned_tickets
        )

    @property
    def open_tickets_count(self):

        return len([
            ticket
            for ticket in self.created_tickets
            if ticket.status not in [
                "Resuelto",
                "Cerrado"
            ]
        ])

    def has_permission(
        self,
        permission_code
    ):

        if not self.role:
            return False

        permissions = self.role.permissions

        if hasattr(permissions, "filter_by"):

            return (
                permissions
                .filter_by(
                    code=permission_code
                )
                .first()
                is not None
            )

        return any(
            permission.code == permission_code
            for permission in permissions
        )

    @property
    def is_admin(self):

        if not self.role:
            return False

        return (
            self.role.name.lower()
            == "administrador"
        )

    def __repr__(self):

        return (
            f"<User {self.email}>"
        )