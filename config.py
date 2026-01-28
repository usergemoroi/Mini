import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///dragon_garden.db')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'dragon_garden_bot')
ADMIN_USER_IDS = [int(id.strip()) for id in os.getenv('ADMIN_USER_IDS', '').split(',') if id.strip()]

DAILY_FREE_EGG_COOLDOWN = 24 * 60 * 60
DRAGON_FEED_COOLDOWN = 24 * 60 * 60
PLANT_GROWTH_TIME = 60 * 60
