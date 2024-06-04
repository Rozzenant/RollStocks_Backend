"""initial migration

Revision ID: 4d9bc5af5917
Revises: 
Create Date: 2024-06-04 06:31:38.629973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d9bc5af5917'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rolls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('length', sa.Float(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.Column('date_removed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rolls')
    # ### end Alembic commands ###