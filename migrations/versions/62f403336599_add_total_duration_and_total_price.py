"""Add total_duration and total_price

Revision ID: 62f403336599
Revises: 60e5bc2feb0e
Create Date: 2024-05-08 07:20:24.671585

"""
from typing import Sequence

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '62f403336599'
down_revision: str | None = '60e5bc2feb0e'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('total_duration', sa.Integer(), nullable=False))
    op.add_column('appointment', sa.Column('total_price', sa.DECIMAL(precision=10, scale=2), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('appointment', 'total_price')
    op.drop_column('appointment', 'total_duration')
    # ### end Alembic commands ###
