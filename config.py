import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///dragon_garden.db')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'dragon_garden_bot')
ADMIN_USER_IDS = [int(id.strip()) for id in os.getenv('ADMIN_USER_IDS', '').split(',') if id.strip()]

# CryptoBot Settings
CRYPTOBOT_API_TOKEN = os.getenv('CRYPTOBOT_API_TOKEN')
CRYPTOBOT_API_URL = os.getenv('CRYPTOBOT_API_URL', 'https://pay.crypt.bot/api')

# Game Settings
DAILY_FREE_EGG_COOLDOWN = 24 * 60 * 60
DRAGON_FEED_COOLDOWN = 24 * 60 * 60
PLANT_GROWTH_TIME = 60 * 60

# VIP Settings
VIP_BENEFITS = {
    0: {
        'name': 'Free',
        'emoji': '⚪️',
        'gold_bonus': 0,
        'max_dragons': 1,
        'premium_seeds_per_week': 0,
        'daily_gold_bonus': 0,
        'egg_discount': 0
    },
    1: {
        'name': 'VIP Bronze',
        'emoji': '🥉',
        'gold_bonus': 0.20,
        'max_dragons': 2,
        'premium_seeds_per_week': 1,
        'daily_gold_bonus': 0,
        'egg_discount': 0
    },
    2: {
        'name': 'VIP Silver',
        'emoji': '🥈',
        'gold_bonus': 0.40,
        'max_dragons': 3,
        'premium_seeds_per_week': 3,
        'daily_gold_bonus': 100,
        'egg_discount': 0
    },
    3: {
        'name': 'VIP Gold',
        'emoji': '🥇',
        'gold_bonus': 0.60,
        'max_dragons': 5,
        'premium_seeds_per_week': 7,
        'daily_gold_bonus': 300,
        'egg_discount': 0
    },
    4: {
        'name': 'VIP Platinum',
        'emoji': '💎',
        'gold_bonus': 1.0,
        'max_dragons': 10,
        'premium_seeds_per_week': 15,
        'daily_gold_bonus': 500,
        'egg_discount': 0.5
    }
}

# VIP Pricing (in Telegram Stars)
VIP_PRICES = {
    1: 99,
    2: 499,
    3: 999,
    4: 1999
}

# Crystal Pricing (in Telegram Stars)
CRYSTAL_PACKAGES = {
    100: 99,
    500: 499,
    1200: 999,
    2700: 1999
}

# Battlepass Settings
BATTLEPASS_PRICE = 200  # Crystals
BATTLEPASS_DURATION_DAYS = 30
BATTLEPASS_MAX_DAYS = 50
