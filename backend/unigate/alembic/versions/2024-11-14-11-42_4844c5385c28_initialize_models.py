"""initialize models

Revision ID: 4844c5385c28
Revises:
Create Date: 2024-11-14 11:42:10.167346

"""

from collections.abc import Sequence

import sqlalchemy as sa

# see https://stackoverflow.com/a/69063829 for sqlmodel
import sqlmodel
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4844c5385c28"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "students",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column(
            "email", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False
        ),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column(
            "surname", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_students_email"), "students", ["email"], unique=True)
    op.create_index(op.f("ix_students_number"), "students", ["number"], unique=True)
    op.create_table(
        "groups",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "category", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column(
            "type", sa.Enum("PUBLIC", "PRIVATE", name="group_type"), nullable=True
        ),
        sa.Column("creator_id", sa.Uuid(), nullable=False),
        sa.Column("members_count", sa.Integer(), nullable=False, default=0),
        sa.ForeignKeyConstraint(["creator_id"], ["students.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "joins",
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("group_id", sa.Uuid(), nullable=False),
        sa.Column("date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("student_id", "group_id"),
    )
    op.create_table(
        "requests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("PENDING", "APPROVED", "REJECTED", name="request_status"),
            nullable=True,
        ),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("group_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "super_students",
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("group_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("student_id", "group_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
