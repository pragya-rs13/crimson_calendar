"""seed info in cycle info table

Revision ID: 4d52bfddcc68
Revises: 562e681ffa1f
Create Date: 2025-05-01 00:51:52.946412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d52bfddcc68'
down_revision: Union[str, None] = '562e681ffa1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()

    for phase in [
        {
            "name": "menstrual",
            "description": "Menstrual bleeding begins. Hormone levels are at their lowest.",
            "tips": "Rest, use heat packs, hydrate, and eat iron-rich foods.",
            "lh": 10, "fsh": 20, "estrogen": 15, "progesterone": 5, "androgen": 20,
            "insulin": 30, "prolactin": 10, "testosterone": 15, "cortisol": 25,
            "light_mode_colour": "#92374d", "dark_mode_colour": "#d78a76"
        },
        {
            "name": "follicular",
            "description": "Follicles mature, estrogen begins to rise.",
            "tips": "Focus on strength training, eat high-fiber carbs and proteins.",
            "lh": 20, "fsh": 25, "estrogen": 40, "progesterone": 5, "androgen": 25,
            "insulin": 35, "prolactin": 12, "testosterone": 20, "cortisol": 30,
            "light_mode_colour": "#4e6e58", "dark_mode_colour": "#7796cb"
        },
        {
            "name": "ovulation",
            "description": "LH surges, causing egg release. Estrogen peaks.",
            "tips": "You may feel more social and energized. Great time for cardio or networking.",
            "lh": 70, "fsh": 30, "estrogen": 80, "progesterone": 10, "androgen": 35,
            "insulin": 25, "prolactin": 14, "testosterone": 40, "cortisol": 28,
            "light_mode_colour": "#7796cb", "dark_mode_colour": "#420039"
        },
        {
            "name": "luteal",
            "description": "Progesterone dominates, body prepares for possible implantation.",
            "tips": "Lower caffeine, eat complex carbs to reduce PMS.",
            "lh": 15, "fsh": 15, "estrogen": 30, "progesterone": 70, "androgen": 25,
            "insulin": 40, "prolactin": 20, "testosterone": 18, "cortisol": 35,
            "light_mode_colour": "#22577a", "dark_mode_colour": "#ffb5c2"
        }
    ]:
        result = connection.execute(
            sa.text("SELECT 1 FROM cyclephaseinfos WHERE name = :name"),
            {"name": phase["name"]}
        ).fetchone()

        if not result:
            connection.execute(
                sa.text("""
                    INSERT INTO cyclephaseinfos (
                        name, description, tips, lh, fsh, estrogen, progesterone,
                        androgen, insulin, prolactin, testosterone, cortisol,
                        light_mode_colour, dark_mode_colour, created_at, updated_at
                    ) VALUES (
                        :name, :description, :tips, :lh, :fsh, :estrogen, :progesterone,
                        :androgen, :insulin, :prolactin, :testosterone, :cortisol,
                        :light_mode_colour, :dark_mode_colour, now(), now()
                    )
                """),
                phase
            )


def downgrade() -> None:
    """Downgrade schema."""
    pass
