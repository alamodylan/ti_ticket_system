from app.extensions import db
from app.models.user import User


class UserRepository:

    # =========================
    # GET ALL USERS
    # =========================
    @staticmethod
    def get_all():

        return (
            User.query
            .order_by(
                User.first_name.asc()
            )
            .all()
        )

    # =========================
    # GET USER BY ID
    # =========================
    @staticmethod
    def get_by_id(user_id):

        return db.session.get(
            User,
            user_id
        )

    # =========================
    # GET USER BY EMAIL
    # =========================
    @staticmethod
    def get_by_email(email):

        return (
            User.query
            .filter_by(
                email=email
            )
            .first()
        )

    # =========================
    # GET USER BY USERNAME
    # =========================
    @staticmethod
    def get_by_username(username):

        return (
            User.query
            .filter_by(
                username=username
            )
            .first()
        )

    # =========================
    # CREATE USER
    # =========================
    @staticmethod
    def create(user):

        db.session.add(user)

        return user

    # =========================
    # SAVE USER
    # =========================
    @staticmethod
    def save(user):

        db.session.add(user)

        return user

    # =========================
    # DELETE USER
    # =========================
    @staticmethod
    def delete(user):

        db.session.delete(user)

    # =========================
    # SEARCH USERS
    # =========================
    @staticmethod
    def search(search_term):

        return (
            User.query
            .filter(
                User.first_name.ilike(
                    f"%{search_term}%"
                )
                |
                User.last_name.ilike(
                    f"%{search_term}%"
                )
                |
                User.email.ilike(
                    f"%{search_term}%"
                )
                |
                User.username.ilike(
                    f"%{search_term}%"
                )
            )
            .order_by(
                User.first_name.asc()
            )
            .all()
        )

    # =========================
    # GET ACTIVE USERS
    # =========================
    @staticmethod
    def get_active_users():

        return (
            User.query
            .filter_by(
                is_active=True
            )
            .order_by(
                User.first_name.asc()
            )
            .all()
        )

    # =========================
    # GET ADMIN USERS
    # =========================
    @staticmethod
    def get_admin_users(site_id=None):

        query = (
            User.query
            .join(User.role)
            .filter(
                User.is_active == True
            )
            .filter(
                User.role.has(
                    name="Administrador"
                )
            )
        )

        if site_id:

            query = query.filter(
                User.site_id == site_id
            )

        return (
            query
            .order_by(
                User.first_name.asc()
            )
            .all()
        )