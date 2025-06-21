from app.core.models.period_histories import PeriodHistories
from app.core.models.profiles import Profiles
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import List, Optional


class PeriodHistoriesRepository:
    def __init__(self, db: Session):
        self.db = db
        self.query = self.db.query(PeriodHistories)

    def get_paginated_by_user(self, user_id: int, page: int = 1, page_size: int = 20) -> List[PeriodHistories]:
        offset = (page - 1) * page_size
        return (
            self.query
            .filter(PeriodHistories.user_id == user_id)
            .order_by(PeriodHistories.start_date.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

    #  Create or update current prediction record
    def create_or_update_latest_period(self, user_id: int, new_start_date: date) -> PeriodHistories:
        latest_pred = (
            self.query
            .filter(PeriodHistories.user_id == user_id, PeriodHistories.is_prediction is True)
            .order_by(PeriodHistories.start_date.desc())
            .first()
        )

        profile = self.db.query(Profiles).filter(Profiles.user_id == user_id).first()
        duration = profile.avg_mens_duration if profile and profile.avg_mens_duration else 5
        end_date = new_start_date + timedelta(days=duration)

        if latest_pred:
            latest_pred.start_date = new_start_date
            latest_pred.end_date = end_date
            latest_pred.is_ongoing = True
            latest_pred.is_prediction = False
            self.db.commit()
            return latest_pred

        new = PeriodHistories(
            user_id=user_id,
            start_date=new_start_date,
            end_date=end_date,
            is_prediction=False,
            is_ongoing=True,
        )
        self.db.add(new)
        self.db.commit()
        self.db.refresh(new)
        return new

    #  Close current ongoing period
    def close_ongoing_period(self, user_id: int, actual_end_date: date) -> Optional[PeriodHistories]:
        ongoing = (
            self.query
            .filter(PeriodHistories.user_id == user_id, PeriodHistories.is_ongoing)
            .order_by(PeriodHistories.start_date.desc())
            .first()
        )
        if ongoing:
            ongoing.end_date = actual_end_date
            ongoing.is_ongoing = False
            self.db.commit()
            return ongoing
        return None

    #  update by entry id
    def update_period_entry(self, entry_id: int, start_date: Optional[date], end_date: Optional[date]) -> Optional[PeriodHistories]:
        entry = self.query.filter(PeriodHistories.id == entry_id).first()
        if not entry:
            return None
        if start_date:
            entry.start_date = start_date
        if end_date:
            entry.end_date = end_date
            if end_date < date.today():
                entry.is_ongoing = False
        self.db.commit()
        return entry

    # delete one
    def delete_by_id(self, entry_id: int) -> bool:
        entry = self.query.filter(PeriodHistories.id == entry_id).first()
        if entry:
            self.db.delete(entry)
            self.db.commit()
            return True
        return False

    # bulk delete
    def delete_many_by_ids(self, entry_ids: List[int]) -> int:
        deleted = self.query.filter(PeriodHistories.id.in_(entry_ids)).delete(synchronize_session=False)
        self.db.commit()
        return deleted

    # Bulk create
    def bulk_create(self, period_data: List[dict]) -> List[PeriodHistories]:
        new_rows = [PeriodHistories(**data) for data in period_data]
        self.db.add_all(new_rows)
        self.db.commit()
        return new_rows
    
    # get all histories (for ML model mostly)
    def get_all_by_user(self, user_id: int) -> List[PeriodHistories]:
        return (
            self.query
            .filter(PeriodHistories.user_id == user_id)
            .order_by(PeriodHistories.start_date.asc())
            .all()
        )
    
    # fun to create prediction period
    def create_prediction_period(
    self,
    user_id: int,
    predicted_start_date: date,
    predicted_duration: int
    ) -> PeriodHistories:
        
        # Update profile duration if needed
        profile = self.db.query(Profiles).filter(Profiles.user_id == user_id).first()
        if profile:
            if not profile.avg_mens_duration or profile.avg_mens_duration != predicted_duration:
                profile.avg_mens_duration = predicted_duration
                self.db.add(profile)

        predicted_end_date = predicted_start_date + timedelta(days=predicted_duration)

        new_prediction = PeriodHistories(
            user_id=user_id,
            start_date=predicted_start_date,
            end_date=predicted_end_date,
            is_prediction=True,
            is_ongoing=False,
        )

        self.db.add(new_prediction)
        self.db.commit()
        self.db.refresh(new_prediction)
        return new_prediction
