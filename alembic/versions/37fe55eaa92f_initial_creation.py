"""initial creation

Revision ID: 37fe55eaa92f
Revises: 
Create Date: 2021-10-24 14:31:12.335449

"""
from sqlalchemy.sql.functions import now
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "37fe55eaa92f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # creating all quotes table
    op.create_table(
        "all_quotes",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column("quote", sa.String(2048), nullable=False),
        sa.Column("context", sa.String(2048), nullable=False),
        sa.Column("date_created", sa.DateTime, server_default=sa.func.now()),
    )

    # creating quotes up for release table
    op.create_table(
        "quotes_up_for_release",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column("incoming_quote", sa.String(2048), nullable=False),
        sa.Column("incoming_context", sa.String(2048), nullable=False),
        sa.Column("date_updated", sa.DateTime, server_default=sa.func.now()),
    )

    # creating used quotes with timestamp
    op.create_table(
        "used_quotes",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column("used_quote", sa.String(2048), nullable=False),
        sa.Column("used_context", sa.String(2048), nullable=False),
        sa.Column(
            "date_used", sa.DateTime, nullable=False, server_default=sa.func.now()
        ),
    )

    # creating table for all images
    op.create_table(
        "all_images",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column("image_link", sa.String(2048), nullable=False),
        sa.Column(
            "date_created", sa.DateTime, nullable=False, server_default=sa.func.now()
        ),
    )


def downgrade():
    # dropping all tables
    op.drop_table("all_quotes")
    op.drop_table("quotes_up_for_release")
    op.drop_table("used_quotes")
    op.drop_table("all_images")
