from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
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
    is_callback = query is not None
    
    if is_callback:
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
        [InlineKeyboardButton("🥉 VIP Bronze 99⭐️", callback_data="buy_vip_1")],
        [InlineKeyboardButton("🥈 VIP Silver 499⭐️", callback_data="buy_vip_2")],
        [InlineKeyboardButton("🥇 VIP Gold 999⭐️", callback_data="buy_vip_3")],
        [InlineKeyboardButton("💎 VIP Platinum 1999⭐️", callback_data="buy_vip_4")],
        [InlineKeyboardButton(t(lang, 'nav_back'), callback_data="start_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def buy_vip_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle VIP purchase via callback"""
    query = update.callback_query
    await query.answer()
    
    vip_level = int(query.data.split('_')[-1])
    
    # Don't send invoice for callback queries, use a different approach
    # For now, show a message with instructions
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    await query.edit_message_text(
        text=t(lang, 'vip_payment_message', level=vip_level),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, 'nav_back'), callback_data="vip_menu")]])
    )

def register_vip_handlers(application):
    """Register VIP handlers"""
    application.add_handler(CallbackQueryHandler(vip_menu, pattern="^vip_menu$"))
    application.add_handler(CallbackQueryHandler(buy_vip_callback, pattern="^buy_vip_"))
