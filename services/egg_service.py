from datetime import datetime, timedelta
from database.models import Egg, User
from sqlalchemy.orm import Session
from utils.helpers import calculate_hatching_time, determine_egg_rarity
from utils.constants import EGG_TYPES

class EggService:
    @staticmethod
    def create_egg(session: Session, user: User, egg_type: str):
        hatching_hours = calculate_hatching_time(egg_type)
        rarity = determine_egg_rarity(egg_type)
        
        egg = Egg(
            user_id=user.id,
            egg_type=egg_type,
            rarity=rarity,
            hatching_time=hatching_hours,
            started_hatching_at=datetime.utcnow(),
            hatches_at=datetime.utcnow() + timedelta(hours=hatching_hours)
        )
        
        session.add(egg)
        session.flush()
        return egg
    
    @staticmethod
    def get_user_eggs(session: Session, user: User, include_hatched: bool = False):
        query = session.query(Egg).filter_by(user_id=user.id)
        if not include_hatched:
            query = query.filter_by(is_hatched=False)
        return query.all()
    
    @staticmethod
    def get_egg_by_id(session: Session, egg_id: int, user_id: int):
        return session.query(Egg).filter_by(id=egg_id, user_id=user_id).first()
    
    @staticmethod
    def check_ready_eggs(session: Session, user: User):
        now = datetime.utcnow()
        eggs = session.query(Egg).filter_by(user_id=user.id, is_hatched=False).all()
        ready_eggs = [egg for egg in eggs if egg.hatches_at <= now and not egg.is_ready]
        
        for egg in ready_eggs:
            egg.is_ready = True
        
        session.flush()
        return ready_eggs
    
    @staticmethod
    def hatch_egg(session: Session, egg: Egg):
        if not egg.is_ready and egg.hatches_at > datetime.utcnow():
            return None
        
        egg.is_hatched = True
        egg.is_ready = True
        session.flush()
        return egg
    
    @staticmethod
    def can_purchase_egg(user: User, egg_type: str):
        egg_data = EGG_TYPES.get(egg_type)
        if not egg_data:
            return False, "Invalid egg type"
        
        cost_gold = egg_data['cost_gold']
        cost_crystals = egg_data['cost_crystals']
        
        if cost_gold > 0 and user.gold < cost_gold:
            return False, f"Not enough gold! Need {cost_gold} gold."
        
        if cost_crystals > 0 and user.crystals < cost_crystals:
            return False, f"Not enough crystals! Need {cost_crystals} crystals."
        
        return True, "OK"
