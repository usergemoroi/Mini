RARITIES = {
    'Common': {'emoji': '⚪️', 'chance': 50, 'base_stats': 10},
    'Rare': {'emoji': '🔵', 'chance': 30, 'base_stats': 15},
    'Epic': {'emoji': '🟣', 'chance': 15, 'base_stats': 25},
    'Legendary': {'emoji': '🟡', 'chance': 4, 'base_stats': 40},
    'Mythic': {'emoji': '🔴', 'chance': 1, 'base_stats': 60},
}

DRAGONS = {
    'Common': [
        {'name': 'Spark Dragon', 'emoji': '⚡', 'color': 'Yellow', 'element': 'Electric', 'ability': 'Lightning Strike'},
        {'name': 'Aqua Dragon', 'emoji': '💧', 'color': 'Blue', 'element': 'Water', 'ability': 'Tidal Wave'},
        {'name': 'Leaf Dragon', 'emoji': '🍃', 'color': 'Green', 'element': 'Nature', 'ability': 'Vine Whip'},
        {'name': 'Ember Dragon', 'emoji': '🔥', 'color': 'Red', 'element': 'Fire', 'ability': 'Flame Burst'},
        {'name': 'Stone Dragon', 'emoji': '🪨', 'color': 'Gray', 'element': 'Earth', 'ability': 'Rock Throw'},
        {'name': 'Breeze Dragon', 'emoji': '💨', 'color': 'White', 'element': 'Air', 'ability': 'Gust'},
        {'name': 'Cloud Dragon', 'emoji': '☁️', 'color': 'White', 'element': 'Air', 'ability': 'Cloud Cover'},
        {'name': 'Puddle Dragon', 'emoji': '🌊', 'color': 'Light Blue', 'element': 'Water', 'ability': 'Splash'},
        {'name': 'Pebble Dragon', 'emoji': '⚪', 'color': 'Brown', 'element': 'Earth', 'ability': 'Stone Shield'},
        {'name': 'Seedling Dragon', 'emoji': '🌱', 'color': 'Light Green', 'element': 'Nature', 'ability': 'Growth'},
        {'name': 'Ash Dragon', 'emoji': '🌫️', 'color': 'Gray', 'element': 'Fire', 'ability': 'Smoke Screen'},
        {'name': 'Static Dragon', 'emoji': '⚡', 'color': 'Pale Yellow', 'element': 'Electric', 'ability': 'Shock'},
    ],
    'Rare': [
        {'name': 'Frost Dragon', 'emoji': '❄️', 'color': 'Ice Blue', 'element': 'Ice', 'ability': 'Frost Breath'},
        {'name': 'Blaze Dragon', 'emoji': '🔥', 'color': 'Orange', 'element': 'Fire', 'ability': 'Inferno'},
        {'name': 'Thunder Dragon', 'emoji': '⚡', 'color': 'Gold', 'element': 'Electric', 'ability': 'Thunder Bolt'},
        {'name': 'Forest Dragon', 'emoji': '🌲', 'color': 'Dark Green', 'element': 'Nature', 'ability': 'Forest Guardian'},
        {'name': 'Ocean Dragon', 'emoji': '🌊', 'color': 'Deep Blue', 'element': 'Water', 'ability': 'Tsunami'},
        {'name': 'Mountain Dragon', 'emoji': '⛰️', 'color': 'Brown', 'element': 'Earth', 'ability': 'Earthquake'},
        {'name': 'Storm Dragon', 'emoji': '⛈️', 'color': 'Dark Gray', 'element': 'Air', 'ability': 'Storm Call'},
        {'name': 'Crystal Dragon', 'emoji': '💎', 'color': 'Rainbow', 'element': 'Crystal', 'ability': 'Crystal Shard'},
        {'name': 'Coral Dragon', 'emoji': '🪸', 'color': 'Pink', 'element': 'Water', 'ability': 'Coral Barrier'},
        {'name': 'Blossom Dragon', 'emoji': '🌸', 'color': 'Pink', 'element': 'Nature', 'ability': 'Petal Dance'},
        {'name': 'Desert Dragon', 'emoji': '🏜️', 'color': 'Sand', 'element': 'Earth', 'ability': 'Sand Storm'},
        {'name': 'Magma Dragon', 'emoji': '🌋', 'color': 'Red-Orange', 'element': 'Fire', 'ability': 'Lava Flow'},
    ],
    'Epic': [
        {'name': 'Shadow Dragon', 'emoji': '🌑', 'color': 'Black', 'element': 'Dark', 'ability': 'Shadow Strike'},
        {'name': 'Light Dragon', 'emoji': '✨', 'color': 'Pure White', 'element': 'Light', 'ability': 'Holy Beam'},
        {'name': 'Phoenix Dragon', 'emoji': '🔥', 'color': 'Crimson', 'element': 'Fire', 'ability': 'Rebirth Flame'},
        {'name': 'Glacier Dragon', 'emoji': '🧊', 'color': 'Ice White', 'element': 'Ice', 'ability': 'Absolute Zero'},
        {'name': 'Plasma Dragon', 'emoji': '⚡', 'color': 'Neon Blue', 'element': 'Electric', 'ability': 'Plasma Burst'},
        {'name': 'Jungle Dragon', 'emoji': '🦎', 'color': 'Emerald', 'element': 'Nature', 'ability': 'Overgrowth'},
        {'name': 'Abyssal Dragon', 'emoji': '🌀', 'color': 'Deep Purple', 'element': 'Water', 'ability': 'Whirlpool'},
        {'name': 'Sky Dragon', 'emoji': '☁️', 'color': 'Sky Blue', 'element': 'Air', 'ability': 'Sky Dominion'},
        {'name': 'Obsidian Dragon', 'emoji': '⬛', 'color': 'Obsidian', 'element': 'Earth', 'ability': 'Obsidian Armor'},
        {'name': 'Aurora Dragon', 'emoji': '🌈', 'color': 'Aurora', 'element': 'Light', 'ability': 'Aurora Veil'},
        {'name': 'Nebula Dragon', 'emoji': '🌌', 'color': 'Space Purple', 'element': 'Cosmic', 'ability': 'Star Fall'},
        {'name': 'Lunar Dragon', 'emoji': '🌙', 'color': 'Silver', 'element': 'Moon', 'ability': 'Moon Beam'},
    ],
    'Legendary': [
        {'name': 'Celestial Dragon', 'emoji': '⭐', 'color': 'Golden', 'element': 'Celestial', 'ability': 'Stellar Nova'},
        {'name': 'Inferno Dragon', 'emoji': '🔥', 'color': 'Dark Red', 'element': 'Fire', 'ability': 'Hell Fire'},
        {'name': 'Void Dragon', 'emoji': '🕳️', 'color': 'Void Black', 'element': 'Void', 'ability': 'Void Collapse'},
        {'name': 'Solar Dragon', 'emoji': '☀️', 'color': 'Bright Yellow', 'element': 'Sun', 'ability': 'Solar Flare'},
        {'name': 'Eternal Dragon', 'emoji': '♾️', 'color': 'Platinum', 'element': 'Time', 'ability': 'Time Freeze'},
        {'name': 'Titan Dragon', 'emoji': '🗿', 'color': 'Stone Gray', 'element': 'Earth', 'ability': 'Titan Slam'},
        {'name': 'Tempest Dragon', 'emoji': '🌪️', 'color': 'Storm Blue', 'element': 'Air', 'ability': 'Mega Tornado'},
        {'name': 'Leviathan Dragon', 'emoji': '🐉', 'color': 'Ocean Blue', 'element': 'Water', 'ability': 'Tidal Destruction'},
        {'name': 'Ancient Dragon', 'emoji': '🦴', 'color': 'Bone White', 'element': 'Ancient', 'ability': 'Ancient Power'},
        {'name': 'Divine Dragon', 'emoji': '👑', 'color': 'Holy Gold', 'element': 'Divine', 'ability': 'Divine Judgment'},
        {'name': 'Chaos Dragon', 'emoji': '💥', 'color': 'Chaotic', 'element': 'Chaos', 'ability': 'Chaos Rift'},
        {'name': 'Prism Dragon', 'emoji': '🔷', 'color': 'Prismatic', 'element': 'Light', 'ability': 'Prism Break'},
    ],
    'Mythic': [
        {'name': 'Origin Dragon', 'emoji': '🌟', 'color': 'Primordial', 'element': 'Creation', 'ability': 'Genesis Wave'},
        {'name': 'Apocalypse Dragon', 'emoji': '💀', 'color': 'Death Black', 'element': 'Destruction', 'ability': 'End Times'},
        {'name': 'Cosmic Dragon', 'emoji': '🌌', 'color': 'Universe', 'element': 'Cosmic', 'ability': 'Big Bang'},
        {'name': 'Omega Dragon', 'emoji': '🔱', 'color': 'Final', 'element': 'Omega', 'ability': 'Omega Blast'},
        {'name': 'Eternal Phoenix', 'emoji': '🔥', 'color': 'Eternal Flame', 'element': 'Immortal Fire', 'ability': 'Eternal Rebirth'},
        {'name': 'Galactic Dragon', 'emoji': '🪐', 'color': 'Galaxy', 'element': 'Space', 'ability': 'Black Hole'},
        {'name': 'Quantum Dragon', 'emoji': '⚛️', 'color': 'Quantum', 'element': 'Reality', 'ability': 'Reality Warp'},
        {'name': 'Mythril Dragon', 'emoji': '💠', 'color': 'Mythril', 'element': 'Mythical', 'ability': 'Mythic Force'},
        {'name': 'Chronos Dragon', 'emoji': '⏰', 'color': 'Time', 'element': 'Temporal', 'ability': 'Time Manipulation'},
        {'name': 'Primordial Dragon', 'emoji': '🐲', 'color': 'First', 'element': 'Primordial', 'ability': 'Primal Rage'},
        {'name': 'Sovereign Dragon', 'emoji': '👑', 'color': 'Royal', 'element': 'Supreme', 'ability': 'Supreme Authority'},
        {'name': 'Infinity Dragon', 'emoji': '♾️', 'color': 'Infinite', 'element': 'Infinite', 'ability': 'Infinite Power'},
    ]
}

EGG_TYPES = {
    'Daily Free': {
        'cost_gold': 0,
        'cost_crystals': 0,
        'hatching_hours': 48,
        'emoji': '🥚',
        'rarities': {'Common': 70, 'Rare': 25, 'Epic': 5, 'Legendary': 0, 'Mythic': 0}
    },
    'Regular': {
        'cost_gold': 500,
        'cost_crystals': 0,
        'hatching_hours': 48,
        'emoji': '🥚',
        'rarities': {'Common': 60, 'Rare': 30, 'Epic': 9, 'Legendary': 1, 'Mythic': 0}
    },
    'Rare': {
        'cost_gold': 2000,
        'cost_crystals': 0,
        'hatching_hours': 72,
        'emoji': '🔵',
        'rarities': {'Common': 30, 'Rare': 45, 'Epic': 20, 'Legendary': 5, 'Mythic': 0}
    },
    'Premium': {
        'cost_gold': 0,
        'cost_crystals': 200,
        'hatching_hours': 96,
        'emoji': '💎',
        'rarities': {'Common': 10, 'Rare': 35, 'Epic': 35, 'Legendary': 18, 'Mythic': 2}
    },
    'Legendary': {
        'cost_gold': 0,
        'cost_crystals': 500,
        'hatching_hours': 168,
        'emoji': '🌟',
        'rarities': {'Common': 0, 'Rare': 15, 'Epic': 45, 'Legendary': 35, 'Mythic': 5}
    }
}

PLANTS = {
    'Sunflower': {
        'emoji': '🌻',
        'growth_hours': 1,
        'cost_gold': 50,
        'reward_gold': 150,
        'description': 'A bright magical sunflower'
    },
    'Rose': {
        'emoji': '🌹',
        'growth_hours': 2,
        'cost_gold': 100,
        'reward_gold': 350,
        'description': 'Enchanted roses that bloom eternally'
    },
    'Tulip': {
        'emoji': '🌷',
        'growth_hours': 1.5,
        'cost_gold': 75,
        'reward_gold': 225,
        'description': 'Colorful magical tulips'
    },
    'Lotus': {
        'emoji': '🪷',
        'growth_hours': 3,
        'cost_gold': 200,
        'reward_gold': 700,
        'description': 'Sacred lotus from dragon waters'
    },
    'Cherry Blossom': {
        'emoji': '🌸',
        'growth_hours': 2.5,
        'cost_gold': 150,
        'reward_gold': 500,
        'description': 'Delicate blossoms of spring'
    },
    'Hibiscus': {
        'emoji': '🌺',
        'growth_hours': 2,
        'cost_gold': 100,
        'reward_gold': 320,
        'description': 'Tropical dragon hibiscus'
    },
    'Lavender': {
        'emoji': '💜',
        'growth_hours': 1.5,
        'cost_gold': 80,
        'reward_gold': 250,
        'description': 'Calming lavender fields'
    },
    'Mushroom': {
        'emoji': '🍄',
        'growth_hours': 0.5,
        'cost_gold': 30,
        'reward_gold': 80,
        'description': 'Magical mushrooms grow fast'
    }
}

DECORATIONS = [
    {'name': 'Dragon Statue', 'emoji': '🗿', 'cost_gold': 1000},
    {'name': 'Fountain', 'emoji': '⛲', 'cost_gold': 1500},
    {'name': 'Bench', 'emoji': '🪑', 'cost_gold': 300},
    {'name': 'Lamp Post', 'emoji': '💡', 'cost_gold': 500},
    {'name': 'Tree', 'emoji': '🌳', 'cost_gold': 400},
    {'name': 'Bush', 'emoji': '🌿', 'cost_gold': 200},
    {'name': 'Pond', 'emoji': '🌊', 'cost_gold': 800},
    {'name': 'Rock', 'emoji': '🪨', 'cost_gold': 150},
    {'name': 'Fence', 'emoji': '🚧', 'cost_gold': 250},
    {'name': 'Gate', 'emoji': '⛩️', 'cost_gold': 1200},
]
