from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import Battlepass, User
import config

class BattlepassService:
    @staticmethod
    def get_or_create_battlepass(session: Session, user: User) -> Battlepass:
        """Get or create battlepass for user"""
        bp = session.query(Battlepass).filter_by(user_id=user.id).first()
        
        if not bp:
            bp = Battlepass(
                user_id=user.id,
                season_number=1,
                is_active=False,
                current_progress=0,
                rewards_claimed={}
            )
            session.add(bp)
            session.flush()
        
        return bp
    
    @staticmethod
    def is_battlepass_active(user: User) -> bool:
        """Check if battlepass is currently active"""
        if not hasattr(user, 'battlepass') or not user.battlepass:
            return False
        
        bp = user.battlepass
        
        if not bp.is_active:
            return False
        
        if bp.expiration_date and bp.expiration_date < datetime.utcnow():
            # Battlepass expired
            bp.is_active = False
            return False
        
        return True
    
    @staticmethod
    def activate_battlepass(session: Session, user: User, days: int = None) -> Battlepass:
        """Activate battlepass"""
        days = days or config.BATTLEPASS_DURATION_DAYS
        
        bp = BattlepassService.get_or_create_battlepass(session, user)
        
        bp.is_active = True
        bp.purchase_date = datetime.utcnow()
        bp.expiration_date = datetime.utcnow() + timedelta(days=days)
        bp.current_progress = 0
        bp.rewards_claimed = {}
        
        session.flush()
        return bp
    
    @staticmethod
    def check_daily_login(session: Session, user: User) -> bool:
        """Record daily login and increase progress"""
        bp = BattlepassService.get_or_create_battlepass(session, user)
        
        if not BattlepassService.is_battlepass_active(user):
            return False
        
        # Check if already logged in today
        # In production, track last login date separately
        # For now, just increment progress
        if bp.current_progress < config.BATTLEPASS_MAX_DAYS:
            bp.current_progress += 1
        
        return True
    
    @staticmethod
    def can_claim_reward(bp: Battlepass, day: int) -> bool:
        """Check if reward can be claimed for specific day"""
        if not bp.is_active:
            return False
        
        if bp.current_progress < day:
            return False  # Haven't reached this day yet
        
        if str(day) in bp.rewards_claimed:
            return False  # Already claimed
        
        return True
    
    @staticmethod
    def claim_reward(session: Session, bp: Battlepass, day: int) -> tuple[bool, str, dict]:
        """Claim reward for specific day"""
        if not BattlepassService.can_claim_reward(bp, day):
            return False, "Награда недоступна", {}
        
        # Mark as claimed
        bp.rewards_claimed[str(day)] = datetime.utcnow().isoformat()
        
        # Give rewards based on day
        rewards = BattlepassService.get_rewards_for_day(day)
        
        # Apply rewards
        from services import UserService
        user = bp.user
        
        if 'gold' in rewards:
            UserService.add_gold(session, user, rewards['gold'])
        
        if 'crystals' in rewards:
            UserService.add_crystals(session, user, rewards['crystals'])
        
        # Other rewards would be handled here (eggs, decorations, etc.)
        
        return True, f"Награда дня {day} получена!", rewards
    
    @staticmethod
    def get_rewards_for_day(day: int) -> dict:
        """Get rewards for specific day"""
        # Simplified reward system
        rewards = {}
        
        # Weekly rewards
        if day == 7:
            rewards['gold'] = 300
        elif day == 14:
            rewards['gold'] = 500
            rewards['crystals'] = 50
        elif day == 21:
            rewards['gold'] = 700
        elif day == 30:
            rewards['gold'] = 1000
            rewards['crystals'] = 100
            rewards['egg'] = 'Epic'
        elif day == 50:
            rewards['gold'] = 2000
            rewards['crystals'] = 200
            rewards['egg'] = 'Legendary'
        
        return rewards
    
    @staticmethod
    def get_claimable_days(bp: Battlepass) -> list:
        """Get list of days that can be claimed"""
        claimable = []
        
        for day in range(1, config.BATTLEPASS_MAX_DAYS + 1):
            if BattlepassService.can_claim_reward(bp, day):
                claimable.append(day)
        
        return claimable
    
    @staticmethod
    def get_progress(bp: Battlepass) -> tuple[int, int]:
        """Get battlepass progress (current, max)"""
        return bp.current_progress, config.BATTLEPASS_MAX_DAYS
