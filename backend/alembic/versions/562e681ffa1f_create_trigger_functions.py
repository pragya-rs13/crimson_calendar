"""create trigger functions

Revision ID: 562e681ffa1f
Revises: 3e0de9eabde0
Create Date: 2025-05-01 00:43:49.525912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '562e681ffa1f'
down_revision: Union[str, None] = '3e0de9eabde0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )

    for table in [
        "users", "profiles", "periodhistories", "cycles", "cyclephaseinfos",
    ]:
        op.execute(
            f"""
            CREATE TRIGGER update_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
            """
        )



def downgrade() -> None:
    """Downgrade schema."""
    for table in [
        "users", "profiles", "periodhistories", "cycles", "cyclephaseinfos",
    ]:
        op.execute(f"DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};")

    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column;")
