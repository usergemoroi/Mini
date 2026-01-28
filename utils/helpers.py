import random
from datetime import datetime, timedelta
from utils.constants import RARITIES, DRAGONS, EGG_TYPES

def format_time_remaining(target_time):
    now = datetime.utcnow()
    if target_time <= now:
        return "Ready!"
    
    delta = target_time - now
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 24:
        days = hours // 24
        hours = hours % 24
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m {seconds}s"

def calculate_hatching_time(egg_type):
    egg_data = EGG_TYPES.get(egg_type)
    if not egg_data:
        return 48
    return egg_data['hatching_hours']

def determine_egg_rarity(egg_type):
    egg_data = EGG_TYPES.get(egg_type)
    if not egg_data:
        return 'Common'
    
    rarities = egg_data['rarities']
    rand = random.randint(1, 100)
    cumulative = 0
    
    for rarity, chance in rarities.items():
        cumulative += chance
        if rand <= cumulative:
            return rarity
    
    return 'Common'

def get_random_dragon(rarity):
    dragons = DRAGONS.get(rarity, DRAGONS['Common'])
    return random.choice(dragons)

def format_dragon_stats(dragon):
    rarity_emoji = RARITIES[dragon.rarity]['emoji']
    return (
        f"{rarity_emoji} **{dragon.name}** {rarity_emoji}\n"
        f"🎭 Type: {dragon.dragon_type}\n"
        f"⭐ Level: {dragon.level}\n"
        f"💪 Strength: {dragon.strength}\n"
        f"⚡ Agility: {dragon.agility}\n"
        f"🧠 Intelligence: {dragon.intelligence}\n"
        f"❤️ Hunger: {dragon.hunger}%\n"
        f"😊 Happiness: {dragon.happiness}%"
    )

def format_user_profile(user):
    return (
        f"👤 **{user.first_name}**\n"
        f"💰 Gold: {user.gold}\n"
        f"💎 Crystals: {user.crystals}\n"
        f"👑 VIP: {user.vip_level}\n"
        f"🐉 Dragons: {len(user.dragons)}\n"
        f"🥚 Eggs: {len([e for e in user.eggs if not e.is_hatched])}\n"
        f"🌱 Plants: {len([p for p in user.plants if not p.is_harvested])}"
    )

def can_claim_daily_egg(user):
    if not user.last_daily_egg:
        return True
    
    now = datetime.utcnow()
    time_since_last = now - user.last_daily_egg
    return time_since_last.total_seconds() >= 24 * 60 * 60

def format_gold(amount):
    return f"💰 {amount:,}"

def format_crystals(amount):
    return f"💎 {amount:,}"
