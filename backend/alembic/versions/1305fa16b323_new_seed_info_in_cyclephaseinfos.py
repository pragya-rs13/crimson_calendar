"""new seed info in  cyclephaseinfos

Revision ID: 1305fa16b323
Revises: d0fbd5f1554e
Create Date: 2025-05-02 10:28:18.181968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1305fa16b323'
down_revision: Union[str, None] = 'd0fbd5f1554e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Update values
    connection = op.get_bind()
    updates = {
        "menstrual": {
            "recommended_foods": "Iron-rich foods (spinach, red meat), citrus fruits, omega-3s (chia, flax), dark chocolate, magnesium-rich foods (pumpkin seeds)",
            "exercise_notes": "Gentle yoga, stretching, or walking. Focus on rest and recovery.",
            "calorie_guidance": "Consume at or slightly above maintenance. Minimum 1600 kcal recommended.",
        },
        "follicular": {
            "recommended_foods": "High-fiber carbs (oats, quinoa), broccoli, kale, tofu, chicken, berries, nuts",
            "exercise_notes": "Best phase for strength training, trying new routines, and pushing intensity.",
            "calorie_guidance": "Slight calorie deficit allowed (1500–1700 kcal). Energy and mood improve.",
        },
        "ovulation": {
            "recommended_foods": "Avocados, salmon, flaxseed, pumpkin seeds, eggs, bananas, blueberries",
            "exercise_notes": "Ideal time for high-intensity cardio, group workouts, and social activities.",
            "calorie_guidance": "Avoid aggressive dieting during ovulation. Stay at maintenance calories",
        },
        "luteal": {
            "recommended_foods": "Complex carbs like Sweet potatoes, lentils, leafy greens, almonds, turkey, eggs",
            "exercise_notes": "Focus on lighter resistance, pilates, or walking. Fatigue may increase.",
            "calorie_guidance": "Avoid strict deficit. Stay at maintenance. Cravings may rise.",
        },
    }

    for phase, values in updates.items():
        connection.execute(
            sa.text("""
                UPDATE cyclephaseinfos
                SET recommended_foods = :foods,
                    exercise_notes = :exercise,
                    calorie_tips = :calories
                WHERE name = :phase
            """),
            {
                "foods": values["recommended_foods"],
                "exercise": values["exercise_notes"],
                "calories": values["calorie_guidance"],
                "phase": phase,
            }
        )


def downgrade() -> None:
    """Downgrade schema."""
    pass
