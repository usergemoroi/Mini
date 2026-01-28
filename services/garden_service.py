from datetime import datetime, timedelta
from database.models import Plant, User, Garden
from sqlalchemy.orm import Session
from utils.constants import PLANTS

class GardenService:
    @staticmethod
    def plant_crop(session: Session, user: User, plant_type: str):
        plant_data = PLANTS.get(plant_type)
        if not plant_data:
            return None, "Invalid plant type"
        
        cost = plant_data['cost_gold']
        if user.gold < cost:
            return None, f"Not enough gold! Need {cost} gold."
        
        user.gold -= cost
        
        growth_hours = plant_data['growth_hours']
        plant = Plant(
            user_id=user.id,
            plant_type=plant_type,
            planted_at=datetime.utcnow(),
            ready_at=datetime.utcnow() + timedelta(hours=growth_hours)
        )
        
        session.add(plant)
        session.flush()
        return plant, "OK"
    
    @staticmethod
    def get_user_plants(session: Session, user: User, include_harvested: bool = False):
        query = session.query(Plant).filter_by(user_id=user.id)
        if not include_harvested:
            query = query.filter_by(is_harvested=False)
        return query.all()
    
    @staticmethod
    def get_plant_by_id(session: Session, plant_id: int, user_id: int):
        return session.query(Plant).filter_by(id=plant_id, user_id=user_id).first()
    
    @staticmethod
    def check_ready_plants(session: Session, user: User):
        now = datetime.utcnow()
        plants = session.query(Plant).filter_by(user_id=user.id, is_harvested=False).all()
        ready_plants = [plant for plant in plants if plant.ready_at <= now and not plant.is_ready]
        
        for plant in ready_plants:
            plant.is_ready = True
        
        session.flush()
        return ready_plants
    
    @staticmethod
    def harvest_plant(session: Session, user: User, plant: Plant):
        if not plant.is_ready and plant.ready_at > datetime.utcnow():
            return None
        
        plant_data = PLANTS.get(plant.plant_type)
        if not plant_data:
            return None
        
        reward = plant_data['reward_gold']
        user.gold += reward
        plant.is_harvested = True
        plant.is_ready = True
        
        session.flush()
        return reward
    
    @staticmethod
    def get_user_garden(session: Session, user: User):
        return session.query(Garden).filter_by(user_id=user.id).first()
    
    @staticmethod
    def update_garden(session: Session, garden: Garden, name: str = None, description: str = None, theme: str = None):
        if name:
            garden.name = name
        if description:
            garden.description = description
        if theme:
            garden.theme = theme
        
        session.flush()
        return garden
