from datetime import datetime, timedelta
from database.models import Dragon, User
from sqlalchemy.orm import Session
from utils.helpers import get_random_dragon
from utils.constants import RARITIES

class DragonService:
    @staticmethod
    def create_dragon(session: Session, user: User, rarity: str, custom_name: str = None):
        dragon_data = get_random_dragon(rarity)
        base_stats = RARITIES[rarity]['base_stats']
        
        dragon_name = custom_name if custom_name else dragon_data['name']
        
        dragon = Dragon(
            user_id=user.id,
            dragon_type=dragon_data['name'],
            name=dragon_name,
            rarity=rarity,
            level=1,
            experience=0,
            hunger=100,
            happiness=100,
            strength=base_stats,
            agility=base_stats,
            intelligence=base_stats
        )
        
        session.add(dragon)
        session.flush()
        return dragon
    
    @staticmethod
    def feed_dragon(session: Session, dragon: Dragon):
        now = datetime.utcnow()
        
        if dragon.last_fed:
            time_since_fed = now - dragon.last_fed
            if time_since_fed.total_seconds() < 24 * 60 * 60:
                hours_remaining = 24 - (time_since_fed.total_seconds() / 3600)
                return False, hours_remaining
        
        dragon.hunger = min(100, dragon.hunger + 50)
        dragon.happiness = min(100, dragon.happiness + 20)
        dragon.experience += 10
        dragon.last_fed = now
        
        if dragon.experience >= dragon.level * 100:
            dragon.level += 1
            dragon.strength += 5
            dragon.agility += 5
            dragon.intelligence += 5
            session.flush()
            return True, "level_up"
        
        session.flush()
        return True, "fed"
    
    @staticmethod
    def get_user_dragons(session: Session, user: User):
        return session.query(Dragon).filter_by(user_id=user.id).all()
    
    @staticmethod
    def get_dragon_by_id(session: Session, dragon_id: int, user_id: int):
        return session.query(Dragon).filter_by(id=dragon_id, user_id=user_id).first()
    
    @staticmethod
    def rename_dragon(session: Session, dragon: Dragon, new_name: str):
        dragon.name = new_name
        session.flush()
        return dragon
    
    @staticmethod
    def decrease_dragon_hunger(session: Session):
        dragons = session.query(Dragon).all()
        for dragon in dragons:
            dragon.hunger = max(0, dragon.hunger - 10)
            dragon.happiness = max(0, dragon.happiness - 5)
        session.flush()
