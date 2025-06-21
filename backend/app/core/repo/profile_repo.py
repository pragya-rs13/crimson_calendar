from fastapi import Depends
from sqlmodel import Session
from app.core.models.profile_schema import Profiles
from app.db.base_repository import BaseRepository
from datetime import date
from typing import Optional

from app.db.session import get_session

class ProfileRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)
        self.profile_query = self.db.query(Profiles)
        
    @classmethod
    def with_session(cls, db: Session = Depends(get_session)):
        return cls(db)

    def get_by_user(self, user_id: int) -> Profiles | None:
        return self.profile_query.filter(Profiles.user_id == user_id).first()

    def partial_update_profile(
        self, 
        profile: Profiles, 
        current_weight: int = None, 
        current_height: int = None, 
        date_of_birth: str = None,
        avg_mens_duration: int = None,
        avg_cycle_duration: int = None
        ) -> Profiles:
        if current_weight is not None:
            profile.current_weight = current_weight
        if current_height is not None:
            profile.current_height = current_height
        if date_of_birth is not None:
            profile.date_of_birth = date_of_birth
        if avg_mens_duration is not None:
            profile.avg_mens_duration = avg_mens_duration
        if avg_cycle_duration is not None:
            profile.avg_cycle_duration = avg_cycle_duration

        self.db.add(profile)
        self.db.commit()
        return profile

    def create_profile_for_user(
        self, 
        user_id: int, 
        current_weight: int = None, 
        current_height: int = None, 
        date_of_birth: str = None
        ) -> Profiles:
        existing = self.get_by_user(user_id)
        if existing:
            return existing
        
        profile = Profiles(
            user_id=user_id,
            current_weight=current_weight,
            current_height=current_height,
            date_of_birth=date_of_birth
        )
        
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile
    
    def create_or_update(
        self,
        user_id: int,
        current_weight: Optional[int] = None,
        current_height: Optional[int] = None,
        date_of_birth: Optional[date] = None,
        ongoing_mens: Optional[bool] = None,
        avg_mens_duration: int = None,
        avg_cycle_duration: int = None
    ) -> Profiles:
        profile = self.get_by_user_id(user_id)
        if not profile:
            profile = Profiles(user_id=user_id)

        if current_weight is not None:
            profile.current_weight = current_weight
        if current_height is not None:
            profile.current_height = current_height
        if date_of_birth is not None:
            profile.date_of_birth = date_of_birth
        if ongoing_mens is not None:
            profile.ongoing_mens = ongoing_mens
        if avg_mens_duration is not None:
            profile.avg_mens_duration = avg_mens_duration
        if avg_cycle_duration is not None:
            profile.average_cycle_duration = avg_cycle_duration

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_all_profiles(self) -> list[Profiles]:
        return self.profile_query.all()

    def delete_by_user_id(self, user_id: int) -> bool:
        profile = self.get_by_user_id(user_id)
        if profile:
            self.db.delete(profile)
            self.db.commit()
            return True
        return False
    
    def update_ongoing_mens_if_period_started(self, user_id: int, today: date) -> bool:
        from app.cycles.models.period_history import PeriodHistories

        period = self.db.query(PeriodHistories).filter(
            PeriodHistories.user_id == user_id,
            PeriodHistories.start_date <= today,
            PeriodHistories.is_ongoing
        ).order_by(PeriodHistories.start_date.desc()).first()

        if period:
            profile = self.get_by_user_id(user_id)
            if profile:
                profile.ongoing_mens = True
                self.db.commit()
                return True
        return False