"""Add moderation status fields

Revision ID: 049e464f5755
Revises: fd71f71ebb0f
Create Date: 2024-11-15 00:06:14.377359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '049e464f5755'
down_revision: Union[str, None] = 'fd71f71ebb0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promotions', sa.Column('image', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('promotions', 'image')
    # ### end Alembic commands ###
