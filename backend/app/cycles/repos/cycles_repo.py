from app.cycles.models.cycles import Cycles
from app.cycles.models.period_history import PeriodHistories
from app.core.models.profile_schema import Profiles
from sqlalchemy.orm import Session
from datetime import timedelta, date
from typing import Optional, List


class CyclesRepository:
    def __init__(self, db: Session):
        self.db = db
        self.query = db.query(Cycles)

    #  Create a prediction cycle
    def create_prediction_cycle(self, user_id: int, period: PeriodHistories) -> Cycles:
        profile = self.db.query(Profiles).filter(Profiles.user_id == user_id).first()
        cycle_length = profile.average_cycle_duration if profile else 27

        predicted_start = period.start_date
        predicted_end = predicted_start + timedelta(days=cycle_length)

        cycle = Cycles(
            user_id=user_id,
            period_id=period.id,
            cycle_start_date=predicted_start,
            cycle_end_date=predicted_end,
            cycle_length=cycle_length,
            is_prediction=True,
        )
        self.db.add(cycle)
        self.db.commit()
        self.db.refresh(cycle)
        return cycle

    #  Update cycle based on actual period entry
    def update_actual_cycle_for_period(self, user_id: int, current_period: PeriodHistories) -> Optional[Cycles]:
        if current_period.is_prediction:
            return None

        #  Fetch previous actual period
        previous_period = (
            self.db.query(PeriodHistories)
            .filter(PeriodHistories.user_id == user_id, PeriodHistories.is_prediction is False,
                    PeriodHistories.start_date < current_period.start_date)
            .order_by(PeriodHistories.start_date.desc())
            .first()
        )

        if not previous_period:
            return None  # not enough data to calculate cycle

        cycle_start = previous_period.start_date
        cycle_end = current_period.start_date
        cycle_length = (cycle_end - cycle_start).days

        # Update average cycle duration in profile
        profile = self.db.query(Profiles).filter(Profiles.user_id == user_id).first()
        if profile:
            # Update average with running mean (basic for now)
            existing_cycles = self.query.filter(Cycles.user_id == user_id, Cycles.is_prediction is False).count()
            if existing_cycles:
                new_avg = int((profile.average_cycle_duration * existing_cycles + cycle_length) / (existing_cycles + 1))
                profile.average_cycle_duration = new_avg
            else:
                profile.average_cycle_duration = cycle_length
            self.db.add(profile)


        menstrual_start = current_period.start_date
        menstrual_end = menstrual_start + timedelta(days=profile.avg_mens_duration or 5)
        follicular_end = current_period.start_date
        follicular_start = cycle_start + timedelta(days=5)
        ovulation_start = cycle_start + timedelta(days=int(cycle_length * 0.5) - 1)
        ovulation_end = ovulation_start + timedelta(days=1)
        luteal_start = ovulation_end
        luteal_end = cycle_end

        cycle = Cycles(
            user_id=user_id,
            period_id=current_period.id,
            cycle_start_date=cycle_start,
            cycle_end_date=cycle_end,
            cycle_length=cycle_length,
            menstrual_start=menstrual_start,
            menstrual_end=menstrual_end,
            follicular_start=follicular_start,
            follicular_end=follicular_end,
            ovulation_start=ovulation_start,
            ovulation_end=ovulation_end,
            luteal_start=luteal_start,
            luteal_end=luteal_end,
            is_prediction=False
        )

        self.db.add(cycle)
        self.db.commit()
        self.db.refresh(cycle)
        return cycle

    # Fetch all cycles for a user
    def get_cycles_by_user(self, user_id: int) -> List[Cycles]:
        return self.query.filter(Cycles.user_id == user_id).order_by(Cycles.cycle_start_date.desc()).all()
