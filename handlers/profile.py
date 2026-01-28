from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from database import get_session
from database.models import User, Battlepass
from services import UserService
from utils.helpers import format_user_profile
from utils.constants import RARITIES
from localization import t
from datetime import datetime
import config

async def profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        
        text = t(lang, 'profile_title')
        text += t(lang, 'profile_name', name=user.first_name)
        text += t(lang, 'profile_id', id=user.telegram_id)
        text += t(lang, 'profile_resources', 
                  gold=user.gold, 
                  crystals=user.crystals)
        text += t(lang, 'profile_stats',
                  dragons=len(user.dragons),
                  eggs=len([e for e in user.eggs if not e.is_hatched]),
                  plants=len([p for p in user.plants if not p.is_harvested]),
                  created=user.created_at.strftime('%Y-%m-%d'))
        
        # VIP Status
        is_vip_active = user.vip_level > 0 and (
            user.vip_expiration is None or 
            user.vip_expiration > datetime.utcnow()
        )
        
        if is_vip_active:
            vip_info = config.VIP_BENEFITS[user.vip_level]
            text += f"\n👑 **VIP: {vip_info['name']}**\n"
            if user.vip_expiration:
                days_left = (user.vip_expiration - datetime.utcnow()).days
                text += f"⏰ Осталось: {days_left} дней\n"
        else:
            text += "\n👑 VIP: Неактивен\n"
        
        # Battlepass Status
        bp = session.query(Battlepass).filter_by(user_id=user.id).first()
        if bp and bp.is_active and bp.expiration_date and bp.expiration_date > datetime.utcnow():
            text += f"\n🎖️ Боевой пропуск: Активен\n"
            text += f"📊 Прогресс: {bp.current_progress}/{config.BATTLEPASS_MAX_DAYS} дней\n"
        else:
            text += "\n🎖️ Боевой пропуск: Неактивен\n"
        
        rarity_counts = {}
        for dragon in user.dragons:
            rarity_counts[dragon.rarity] = rarity_counts.get(dragon.rarity, 0) + 1
        
        if rarity_counts:
            text += "\n\n🐉 **Коллекция драконов:**\n"
            for rarity in ['Common', 'Rare', 'Epic', 'Legendary', 'Mythic']:
                count = rarity_counts.get(rarity, 0)
                if count > 0:
                    text += f"{RARITIES[rarity]['emoji']} {rarity}: {count}\n"
    
    keyboard = [[InlineKeyboardButton(t(lang, 'nav_back'), callback_data="start_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await profile_menu(update, context)

def register_profile_handlers(application):
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CallbackQueryHandler(profile_menu, pattern="^profile_menu$"
