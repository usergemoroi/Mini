from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from database import get_session
from database.models import CryptoTransaction, User
from services import UserService
from payment import CryptoBotAPI
from localization import t
import logging
import uuid

logger = logging.getLogger(__name__)

async def show_crypto_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show cryptocurrency payment options"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    text = t(lang, 'crypto_title')
    
    keyboard = [
        [t(lang, 'crypto_btc')],
        [t(lang, 'crypto_eth')],
        [t(lang, 'crypto_usdt')],
        [t(lang, 'crypto_ton')],
        [t(lang, 'nav_back')]
    ]
    
    from telegram import ReplyKeyboardMarkup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    if update.callback_query:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def handle_crypto_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle cryptocurrency selection"""
    message_text = update.message.text
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    # Map text to currency
    currency_map = {
        t(lang, 'crypto_btc'): 'BTC',
        t(lang, 'crypto_eth'): 'ETH',
        t(lang, 'crypto_usdt'): 'USDT',
        t(lang, 'crypto_ton'): 'TON'
    }
    
    currency = currency_map.get(message_text)
    if not currency:
        await update.message.reply_text(t(lang, 'error_invalid_input'))
        return
    
    # Default amounts per currency (in USD equivalent)
    amounts = {
        'BTC': 0.01,  # ~$10-100 depending on BTC price
        'ETH': 0.01,  # ~$20-40
        'USDT': 10.0,  # $10
        'TON': 5.0    # ~$5
    }
    
    # Create CryptoBot invoice
    cryptobot = CryptoBotAPI()
    invoice_id = str(uuid.uuid4())
    
    result = await cryptobot.create_invoice(
        amount=amounts[currency],
        currency=currency,
        description=f"Dragon Garden - {amounts[currency]} {currency}",
        payload=invoice_id
    )
    
    if not result['success']:
        logger.error(f"Failed to create CryptoBot invoice: {result.get('error')}")
        await update.message.reply_text(t(lang, 'error_general'))
        return
    
    # Save transaction
    tx = CryptoTransaction(
        user_id=user.id,
        invoice_id=result['invoice_id'],
        currency=currency,
        amount=amounts[currency],
        status='pending'
    )
    
    with get_session() as session:
        session.add(tx)
    
    # Send payment link
    text = t(lang, 'crypto_invoice_created',
             amount=amounts[currency],
             currency=currency,
             address=result.get('pay_url', 'See payment link')
    )
    
    keyboard = [
        [f"🔍 {t(lang, 'crypto_check_payment')}:{result['invoice_id']}"],
        [t(lang, 'nav_back')]
    ]
    
    from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Also send an inline button for direct payment
    inline_keyboard = [[InlineKeyboardButton("💳 Оплатить", url=result['pay_url'])]]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)
    
    await update.message.reply_text(text=text, reply_markup=reply_markup)
    await update.message.reply_text("👇 Или нажмите кнопку для оплаты:", reply_markup=inline_markup)

async def check_crypto_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check cryptocurrency payment status"""
    message_text = update.message.text
    
    # Extract invoice_id from message
    if not message_text.startswith("🔍"):
        return
    
    parts = message_text.split(':')
    if len(parts) < 2:
        return
    
    invoice_id = parts[-1].strip()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        
        # Get transaction
        tx = session.query(CryptoTransaction).filter_by(invoice_id=invoice_id).first()
        if not tx:
            await update.message.reply_text(t(lang, 'error_not_found'))
            return
        
        if tx.status == 'completed':
            await update.message.reply_text(
                t(lang, 'crypto_completed', crystals=100),
                parse_mode='Markdown'
            )
            return
        
        # Check with CryptoBot
        cryptobot = CryptoBotAPI()
        result = await cryptobot.get_invoice(invoice_id)
        
        if not result['success']:
            await update.message.reply_text(t(lang, 'error_general'))
            return
        
        status = result['status']
        
        if status == 'completed':
            # Payment successful
            from services import UserService
            tx.status = 'completed'
            tx.completed_at = __import__('datetime').datetime.utcnow()
            
            # Give crystals (simplified: 100 crystals per transaction)
            UserService.add_crystals(session, user, 100)
            
            await update.message.reply_text(
                t(lang, 'crypto_completed', crystals=100),
                parse_mode='Markdown'
            )
        
        elif status == 'failed':
            tx.status = 'failed'
            await update.message.reply_text(t(lang, 'crypto_failed'))
        
        else:
            await update.message.reply_text(t(lang, 'crypto_pending'))

def register_crypto_handlers(application):
    """Register crypto payment handlers"""
    # Register crypto payment handlers
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(
        filters.TEXT & (
            filters.Regex('₿') | 
            filters.Regex('⟠') | 
            filters.Regex('USDT') | 
            filters.Regex('TON')
        ),
        handle_crypto_selection
    ))
    
    # Register check payment handler
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('🔍'),
        check_crypto_payment
    ))
