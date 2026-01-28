from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import User
import config

class VIPService:
    @staticmethod
    def get_vip_level(user: User) -> int:
        """Get current VIP level (0-4)"""
        # Check if VIP is expired
        if user.vip_level > 0 and user.vip_expiration:
            if user.vip_expiration < datetime.utcnow():
                # VIP expired
                user.vip_level = 0
                user.vip_expiration = None
                return 0
        
        return user.vip_level
    
    @staticmethod
    def is_vip_active(user: User) -> bool:
        """Check if VIP is currently active"""
        if user.vip_level == 0:
            return False
        
        if user.vip_expiration is None:
            return True  # Permanent VIP
        
        return user.vip_expiration > datetime.utcnow()
    
    @staticmethod
    def get_vip_benefits(user: User) -> dict:
        """Get VIP benefits for current level"""
        level = VIPService.get_vip_level(user)
        return config.VIP_BENEFITS.get(level, config.VIP_BENEFITS[0])
    
    @staticmethod
    def get_gold_bonus(user: User) -> float:
        """Get gold bonus multiplier (e.g., 0.2 for 20% bonus)"""
        benefits = VIPService.get_vip_benefits(user)
        return benefits.get('gold_bonus', 0)
    
    @staticmethod
    def get_max_dragons(user: User) -> int:
        """Get maximum number of dragons user can have"""
        benefits = VIPService.get_vip_benefits(user)
        return benefits.get('max_dragons', 1)
    
    @staticmethod
    def can_have_more_dragons(user: User, current_count: int) -> bool:
        """Check if user can have more dragons"""
        max_dragons = VIPService.get_max_dragons(user)
        return current_count < max_dragons
    
    @staticmethod
    def get_daily_gold_bonus(user: User) -> int:
        """Get daily gold bonus from VIP"""
        benefits = VIPService.get_vip_benefits(user)
        return benefits.get('daily_gold_bonus', 0)
    
    @staticmethod
    def claim_daily_gold(session: Session, user: User) -> tuple[bool, str]:
        """Claim daily VIP gold bonus"""
        if not VIPService.is_vip_active(user):
            return False, "VIP неактивен"
        
        bonus = VIPService.get_daily_gold_bonus(user)
        if bonus == 0:
            return False, "Ежедневный бонус недоступен для вашего уровня"
        
        # Check cooldown (once per day)
        if user.last_daily_gold_claim:
            hours_since_claim = (datetime.utcnow() - user.last_daily_gold_claim).total_seconds() / 3600
            if hours_since_claim < 24:
                hours_left = 24 - hours_since_claim
                return False, f"Можно получить через {hours_left:.1f} часов"
        
        # Give bonus
        from services import UserService
        UserService.add_gold(session, user, bonus)
        user.last_daily_gold_claim = datetime.utcnow()
        
        return True, f"Получено {bonus} золота!"
    
    @staticmethod
    def get_egg_discount(user: User) -> float:
        """Get egg discount (0-0.5 for 50% off)"""
        benefits = VIPService.get_vip_benefits(user)
        return benefits.get('egg_discount', 0)
    
    @staticmethod
    def activate_vip(session: Session, user: User, level: int, days: int = 30) -> User:
        """Activate VIP subscription"""
        user.vip_level = level
        
        if user.vip_expiration and user.vip_expiration > datetime.utcnow():
            # Extend existing VIP
            user.vip_expiration = user.vip_expiration + timedelta(days=days)
        else:
            # New VIP
            user.vip_expiration = datetime.utcnow() + timedelta(days=days)
        
        session.flush()
        return user
    
    @staticmethod
    def get_premium_seeds_remaining(user: User) -> int:
        """Get remaining premium seeds for this week"""
        # This is a simplified version - in production, track weekly resets
        benefits = VIPService.get_vip_benefits(user)
        return benefits.get('premium_seeds_per_week', 0)
