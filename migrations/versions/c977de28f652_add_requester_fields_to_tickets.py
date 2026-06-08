"""add requester fields to tickets

Revision ID: c977de28f652
Revises: 3b06d9fdae0f
Create Date: 2026-06-04

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c977de28f652"
down_revision = "3b06d9fdae0f"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("tickets", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "requester_name",
                sa.String(length=150),
                nullable=True
            )
        )

        batch_op.add_column(
            sa.Column(
                "requester_email",
                sa.String(length=150),
                nullable=True
            )
        )

        batch_op.add_column(
            sa.Column(
                "requester_phone",
                sa.String(length=50),
                nullable=True
            )
        )

        batch_op.add_column(
            sa.Column(
                "source",
                sa.String(length=50),
                nullable=True,
                server_default="manual"
            )
        )

        batch_op.add_column(
            sa.Column(
                "email_message_id",
                sa.String(length=255),
                nullable=True
            )
        )

        batch_op.add_column(
            sa.Column(
                "email_subject",
                sa.String(length=255),
                nullable=True
            )
        )

        batch_op.create_index(
            "ix_tickets_requester_email",
            ["requester_email"],
            unique=False
        )

        batch_op.create_index(
            "ix_tickets_source",
            ["source"],
            unique=False
        )

        batch_op.create_index(
            "ix_tickets_email_message_id",
            ["email_message_id"],
            unique=True
        )


def downgrade():

    with op.batch_alter_table("tickets", schema=None) as batch_op:

        batch_op.drop_index("ix_tickets_email_message_id")
        batch_op.drop_index("ix_tickets_source")
        batch_op.drop_index("ix_tickets_requester_email")

        batch_op.drop_column("email_subject")
        batch_op.drop_column("email_message_id")
        batch_op.drop_column("source")
        batch_op.drop_column("requester_phone")
        batch_op.drop_column("requester_email")
        batch_op.drop_column("requester_name")