from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters, CallbackQueryHandler
from database import get_session
from database.models import Purchase, User
from services import UserService
from localization import t
import logging

logger = logging.getLogger(__name__)

async def pre_checkout_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pre-checkout query to validate purchase"""
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful payment"""
    payment = update.message.successful_payment
    user_id = update.effective_user.id
    
    try:
        with get_session() as session:
            user = UserService.get_or_create_user(session, update.effective_user)
            
            # Parse invoice payload: "item_type:amount:details"
            payload = payment.invoice_payload
            parts = payload.split(':')
            item_type = parts[0]
            
            if item_type == 'crystals':
                amount = int(parts[1])
                UserService.add_crystals(session, user, amount)
                message = t(user.language, 'pay_success', crystals=amount)
            
            elif item_type == 'vip':
                vip_level = int(parts[1])
                # Activate VIP
                from datetime import datetime, timedelta
                user.vip_level = vip_level
                if user.vip_expiration and user.vip_expiration > datetime.utcnow():
                    # Extend existing VIP
                    user.vip_expiration = user.vip_expiration + timedelta(days=30)
                else:
                    # New VIP
                    user.vip_expiration = datetime.utcnow() + timedelta(days=30)
                message = f"✅ VIP {vip_level} активирован!\n\nДействует до: {user.vip_expiration.strftime('%d.%m.%Y')}"
            
            elif item_type == 'battlepass':
                from datetime import datetime, timedelta
                from database.models import Battlepass
                # Activate battlepass
                bp = session.query(Battlepass).filter_by(user_id=user.id).first()
                if not bp:
                    bp = Battlepass(
                        user_id=user.id,
                        is_active=True,
                        purchase_date=datetime.utcnow(),
                        expiration_date=datetime.utcnow() + timedelta(days=30),
                        season_number=1
                    )
                    session.add(bp)
                else:
                    bp.is_active = True
                    bp.purchase_date = datetime.utcnow()
                    bp.expiration_date = datetime.utcnow() + timedelta(days=30)
                    bp.current_progress = 0
                    bp.rewards_claimed = {}
                
                message = "✅ Боевой пропуск активирован!\n\nДействует 30 дней"
            
            else:
                message = "❌ Неизвестный тип покупки"
            
            # Record purchase
            purchase = Purchase(
                user_id=user.id,
                payment_type='stars',
                amount_stars=payment.total_amount,
                item_type=item_type,
                item_data={'payload': payload},
                status='completed',
                telegram_payment_charge_id=payment.telegram_payment_charge_id
            )
            session.add(purchase)
            
            await update.message.reply_text(message)
            
    except Exception as e:
        logger.error(f"Error processing payment: {e}")
        await update.message.reply_text(t(user.language, 'pay_failed'))

async def show_payment_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show payment options"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    text = t(lang, 'pay_title')
    
    keyboard = [
        [t(lang, 'pay_stars')],
        [t(lang, 'pay_crypto')],
        [t(lang, 'nav_back')]
    ]
    
    from telegram import ReplyKeyboardMarkup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def send_stars_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE, item_type: str, amount: int, price_stars: int):
    """Send a Stars payment invoice"""
    user_id = update.effective_user.id
    
    if item_type == 'crystals':
        title = f"{amount} Кристаллов"
        description = f"Пакет {amount} кристаллов для Dragon Garden"
        payload = f"crystals:{amount}"
    
    elif item_type == 'vip':
        title = f"VIP Level {amount}"
        description = f"VIP подписка уровня {amount} на 30 дней"
        payload = f"vip:{amount}"
    
    elif item_type == 'battlepass':
        title = "Боевой Пропуск"
        description = "30 дней эпических наград"
        payload = "battlepass:200"
    
    else:
        return
    
    prices = [LabeledPrice(title, price_stars * 100)]  # Stars are in cents
    
    await context.bot.send_invoice(
        chat_id=user_id,
        title=title,
        description=description,
        payload=payload,
        provider_token="",  # Empty for Telegram Stars
        currency="XTR",  # Telegram Stars
        prices=prices
    )

def register_stars_handlers(application):
    """Register Stars payment handlers"""
    application.add_handler(PreCheckoutQueryHandler(pre_checkout_query))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
