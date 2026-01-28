from .start import register_start_handlers
from .dragon import register_dragon_handlers
from .egg import register_egg_handlers
from .garden import register_garden_handlers
from .profile import register_profile_handlers

__all__ = [
    'register_start_handlers',
    'register_dragon_handlers',
    'register_egg_handlers',
    'register_garden_handlers',
    'register_profile_handlers'
]
