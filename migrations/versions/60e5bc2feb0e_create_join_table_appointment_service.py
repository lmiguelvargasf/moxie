"""Create join table appointment service

Revision ID: 60e5bc2feb0e
Revises: d0930134cb37
Create Date: 2024-05-07 16:33:36.941298

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "60e5bc2feb0e"
down_revision: str | None = "d0930134cb37"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "appointmentservicelink",
        sa.Column("appointment_id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["appointment_id"],
            ["appointment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["service.id"],
        ),
        sa.PrimaryKeyConstraint("appointment_id", "service_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("appointmentservicelink")
    # ### end Alembic commands ###
