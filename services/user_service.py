from datetime import datetime
from database.models import User, Garden
from sqlalchemy.orm import Session

class UserService:
    @staticmethod
    def get_or_create_user(session: Session, telegram_user):
        user = session.query(User).filter_by(telegram_id=telegram_user.id).first()
        
        if not user:
            user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name or 'Dragon Trainer',
                gold=1000,
                crystals=50
            )
            session.add(user)
            session.flush()
            
            garden = Garden(user_id=user.id)
            session.add(garden)
            session.flush()
        
        return user
    
    @staticmethod
    def add_gold(session: Session, user: User, amount: int):
        user.gold += amount
        user.updated_at = datetime.utcnow()
        session.flush()
        return user
    
    @staticmethod
    def remove_gold(session: Session, user: User, amount: int):
        if user.gold >= amount:
            user.gold -= amount
            user.updated_at = datetime.utcnow()
            session.flush()
            return True
        return False
    
    @staticmethod
    def add_crystals(session: Session, user: User, amount: int):
        user.crystals += amount
        user.updated_at = datetime.utcnow()
        session.flush()
        return user
    
    @staticmethod
    def remove_crystals(session: Session, user: User, amount: int):
        if user.crystals >= amount:
            user.crystals -= amount
            user.updated_at = datetime.utcnow()
            session.flush()
            return True
        return False
    
    @staticmethod
    def update_daily_egg_time(session: Session, user: User):
        user.last_daily_egg = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        session.flush()
        return user
