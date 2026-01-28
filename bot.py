import logging
import sys
from telegram.ext import Application
from telegram import Update
import config
from database import init_db
from handlers import (
    register_start_handlers,
    register_dragon_handlers,
    register_egg_handlers,
    register_garden_handlers,
    register_profile_handlers
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        logger.error("Please create a .env file with your bot token.")
        logger.error("See .env.example for reference.")
        sys.exit(1)
    
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully!")
    
    logger.info("Creating bot application...")
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    logger.info("Registering handlers...")
    register_start_handlers(application)
    register_dragon_handlers(application)
    register_egg_handlers(application)
    register_garden_handlers(application)
    register_profile_handlers(application)
    logger.info("All handlers registered!")
    
    logger.info("Starting bot...")
    logger.info(f"Bot username: @{config.BOT_USERNAME}")
    logger.info("Dragon Garden bot is now running! Press Ctrl+C to stop.")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
