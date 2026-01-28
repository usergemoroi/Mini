from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
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
    await query.answer()
    
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
        [t(lang, 'battlepass_buy_button')],
        [t(lang, 'nav_back')]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if query:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def buy_battlepass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buy Battlepass"""
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        
        if user.crystals < config.BATTLEPASS_PRICE:
            await update.message.reply_text(
                t(lang, 'shop_not_enough_crystals')
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
        
        await update.message.reply_text(
            "✅ Боевой пропуск активирован!\n\n"
            f"Действует до: {bp.expiration_date.strftime('%d.%m.%Y')}\n\n"
            "Заходите ежедневно для прогресса!"
        )

async def claim_battlepass_rewards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Claim Battlepass rewards"""
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        
        bp = session.query(Battlepass).filter_by(user_id=user.id).first()
        
        if not bp or not bp.is_active:
            await update.message.reply_text(
                t(lang, 'battlepass_not_active')
            )
            return
        
        # Simple reward logic: give rewards based on progress
        if bp.current_progress >= 7:  # Weekly reward
            UserService.add_gold(session, user, 300)
            await update.message.reply_text(
                f"🎁 Еженедельная награда получена!\n\n"
                f"💎 +300 Золота"
            )
        else:
            await update.message.reply_text(
                "⏰ Еженедельная награда доступна через 7 дней"
            )

def register_battlepass_handlers(application):
    """Register Battlepass handlers"""
    application.add_handler(CallbackQueryHandler(battlepass_menu, pattern="^battlepass_menu$"))
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('🎖️ Боевой пропуск|🎖️ Battlepass'),
        battlepass_menu
    ))
