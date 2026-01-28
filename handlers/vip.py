from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from database import get_session
from database.models import User
from services import UserService
from payment.stars_handler import send_stars_invoice
from localization import t
from datetime import datetime, timedelta
import config

async def vip_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show VIP status and options"""
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        
        # Check if VIP is active
        is_vip_active = user.vip_level > 0 and (
            user.vip_expiration is None or 
            user.vip_expiration > datetime.utcnow()
        )
        
        text = t(lang, 'vip_title')
        
        if is_vip_active:
            vip_info = config.VIP_BENEFITS[user.vip_level]
            text += f"{vip_info['emoji']} {vip_info['name']}\n"
            text += t(lang, 'vip_expiration', 
                      date=user.vip_expiration.strftime('%d.%m.%Y') if user.vip_expiration else '∞')
            text += "\n\n"
        else:
            text += t(lang, 'vip_not_active')
            user.vip_level = 0
        
        text += t(lang, 'vip_benefits_title')
        text += t(lang, 'vip_level_0')
        text += "\n\n"
        text += t(lang, 'vip_level_1')
        text += "\n\n"
        text += t(lang, 'vip_level_2')
        text += "\n\n"
        text += t(lang, 'vip_level_3')
        text += "\n\n"
        text += t(lang, 'vip_level_4')
    
    keyboard = [
        ["🥉 VIP Bronze 99⭐️"],
        ["🥈 VIP Silver 499⭐️"],
        ["🥇 VIP Gold 999⭐️"],
        ["💎 VIP Platinum 1999⭐️"],
        [t(lang, 'nav_back')]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if query:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def activate_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle VIP activation button"""
    message = update.message.text
    
    vip_map = {
        "🥉 VIP Bronze 99⭐️": 1,
        "🥈 VIP Silver 499⭐️": 2,
        "🥇 VIP Gold 999⭐️": 3,
        "💎 VIP Platinum 1999⭐️": 4
    }
    
    vip_level = vip_map.get(message)
    if vip_level:
        await send_stars_invoice(update, context, 'vip', vip_level, config.VIP_PRICES[vip_level])

def register_vip_handlers(application):
    """Register VIP handlers"""
    application.add_handler(CallbackQueryHandler(vip_menu, pattern="^vip_menu$"))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('VIP'), activate_vip))
