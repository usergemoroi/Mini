from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database import get_session
from database.models import User, Battlepass
from services import UserService
from payment.stars_handler import send_stars_invoice
from localization import t
from datetime import datetime, timedelta
import config

async def battlepass_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Battlepass status"""
    query = update.callback_query
    is_callback = query is not None
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        
        text = t(lang, 'battlepass_title')
        
        # Get or create battlepass
        bp = session.query(Battlepass).filter_by(user_id=user.id).first()
        
        if bp and bp.is_active and bp.expiration_date and bp.expiration_date > datetime.utcnow():
            text += t(lang, 'battlepass_active',
                     date=bp.expiration_date.strftime('%d.%m.%Y'))
            text += t(lang, 'battlepass_progress', progress=bp.current_progress)
        else:
            text += t(lang, 'battlepass_not_active')
        
        text += t(lang, 'battlepass_price')
        text += t(lang, 'battlepass_rewards')
        
        # Check if can buy
        can_buy = user.crystals >= config.BATTLEPASS_PRICE
        if not can_buy:
            text += f"\n\n❌ Нужно {config.BATTLEPASS_PRICE} 💎 для покупки"
    
    keyboard = [
        [InlineKeyboardButton(t(lang, 'battlepass_buy_button'), callback_data="buy_battlepass")],
        [InlineKeyboardButton(t(lang, 'nav_back'), callback_data="start_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def buy_battlepass_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buy Battlepass via callback"""
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        
        if user.crystals < config.BATTLEPASS_PRICE:
            await query.edit_message_text(
                text=t(lang, 'shop_not_enough_crystals'),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, 'nav_back'), callback_data="battlepass_menu")]])
            )
            return
        
        # Purchase with crystals
        UserService.remove_crystals(session, user, config.BATTLEPASS_PRICE)
        
        # Create/activate battlepass
        bp = session.query(Battlepass).filter_by(user_id=user.id).first()
        if not bp:
            bp = Battlepass(
                user_id=user.id,
                is_active=True,
                purchase_date=datetime.utcnow(),
                expiration_date=datetime.utcnow() + timedelta(days=config.BATTLEPASS_DURATION_DAYS),
                season_number=1,
                current_progress=0
            )
            session.add(bp)
        else:
            bp.is_active = True
            bp.purchase_date = datetime.utcnow()
            bp.expiration_date = datetime.utcnow() + timedelta(days=config.BATTLEPASS_DURATION_DAYS)
            bp.current_progress = 0
            bp.rewards_claimed = {}
        
        await query.edit_message_text(
            text=f"✅ Боевой пропуск активирован!\n\nДействует до: {bp.expiration_date.strftime('%d.%m.%Y')}\n\nЗаходите ежедневно для прогресса!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, 'nav_back'), callback_data="start_menu")]])
        )

def register_battlepass_handlers(application):
    """Register Battlepass handlers"""
    application.add_handler(CallbackQueryHandler(battlepass_menu, pattern="^battlepass_menu$"))
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('🎖️ Боевой пропуск|🎖️ Battlepass'),
        battlepass_menu
    ))
