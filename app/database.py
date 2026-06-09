from app.extensions import db


# =========================
# BASE MODEL
# =========================
class BaseModel(db.Model):

    __abstract__ = True

    __table_args__ = {
        "schema": "tickets_ti"
    }

    # =========================
    # PRIMARY KEY
    # =========================
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =========================
    # TIMESTAMPS
    # =========================
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )

    # =========================
    # STATUS
    # =========================
    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # =========================
    # SAVE INSTANCE
    # =========================
    def save(self):

        db.session.add(self)

    # =========================
    # DELETE INSTANCE
    # =========================
    def delete(self):

        db.session.delete(self)

    # =========================
    # COMMIT SESSION
    # =========================
    @staticmethod
    def commit():

        db.session.commit()

    # =========================
    # ROLLBACK SESSION
    # =========================
    @staticmethod
    def rollback():

        db.session.rollback()

    # =========================
    # SERIALIZATION
    # =========================
    def to_dict(self):

        return {
            column.name: getattr(
                self,
                column.name
            )
            for column in self.__table__.columns
        }