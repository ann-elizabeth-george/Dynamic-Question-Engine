"""add age column to user_profiles

Revision ID: 6e4bd9144c83
Revises: 9b66be447756
Create Date: 2026-07-20 23:53:17.299096
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "6e4bd9144c83"
down_revision: Union[str, None] = "9b66be447756"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "user_profiles",
        sa.Column("age", sa.Integer(), nullable=True)
    )

    op.execute(
        "UPDATE user_profiles SET age = 0 WHERE age IS NULL"
    )

    op.alter_column(
        "user_profiles",
        "age",
        nullable=False
    )


def downgrade():
    op.drop_column(
        "user_profiles",
        "age"
    )