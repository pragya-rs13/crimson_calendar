"""add columns to cyclephaseinfos

Revision ID: d0fbd5f1554e
Revises: 5894ecc4c15e
Create Date: 2025-05-02 10:27:34.408126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd0fbd5f1554e'
down_revision: Union[str, None] = '5894ecc4c15e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cyclephaseinfos', sa.Column('recommended_foods', sqlmodel.sql.sqltypes.AutoString(length=3000), nullable=True))
    op.add_column('cyclephaseinfos', sa.Column('exercise_notes', sqlmodel.sql.sqltypes.AutoString(length=3000), nullable=True))
    op.add_column('cyclephaseinfos', sa.Column('calorie_tips', sqlmodel.sql.sqltypes.AutoString(length=3000), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cyclephaseinfos', 'calorie_tips')
    op.drop_column('cyclephaseinfos', 'exercise_notes')
    op.drop_column('cyclephaseinfos', 'recommended_foods')
    # ### end Alembic commands ###
