"""first migration

Revision ID: 64d057ccb562
Revises: 
Create Date: 2023-05-16 13:55:39.308511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "64d057ccb562"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("username_lower", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("joined_on", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("about", sa.String(length=280), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_users_email"), ["email"], unique=True)
        batch_op.create_index(
            batch_op.f("ix_users_username"), ["username"], unique=True
        )
        batch_op.create_index(
            batch_op.f("ix_users_username_lower"), ["username_lower"], unique=True
        )

    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("uq_article_slug", sa.String(), nullable=True),
        sa.Column("is_draft", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("articles", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_articles_uq_article_slug"), ["uq_article_slug"], unique=True
        )

    op.create_table(
        "user_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("settings", sa.LargeBinary(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "articledata",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=64), nullable=False),
        sa.Column("value", sa.String(length=256), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["articles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "article_data_association_table",
        sa.Column("articledata_id", sa.Integer(), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["articledata.id"],
        ),
        sa.ForeignKeyConstraint(
            ["articledata_id"],
            ["articles.id"],
        ),
        sa.PrimaryKeyConstraint("articledata_id", "article_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("article_data_association_table")
    op.drop_table("articledata")
    op.drop_table("user_settings")
    with op.batch_alter_table("articles", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_articles_uq_article_slug"))

    op.drop_table("articles")
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_username_lower"))
        batch_op.drop_index(batch_op.f("ix_users_username"))
        batch_op.drop_index(batch_op.f("ix_users_email"))

    op.drop_table("users")
    # ### end Alembic commands ###
