from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from database import get_session
from database.models import User
from services import UserService
from payment.stars_handler import send_stars_invoice
from localization import t
import config

async def shop_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main shop menu"""
    query = update.callback_query
    is_callback = query is not None
    
    if is_callback:
        await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    text = t(lang, 'shop_main_title')
    text += t(lang, 'shop_eggs_category')
    text += t(lang, 'shop_crystals_category')
    text += t(lang, 'shop_vip_category')
    text += t(lang, 'shop_battlepass_category')
    text += t(lang, 'shop_crypto_category')
    
    keyboard = [
        [t(lang, 'shop_eggs_category')],
        [t(lang, 'shop_crystals_category')],
        [t(lang, 'shop_vip_category')],
        [t(lang, 'shop_battlepass_category')],
        [t(lang, 'nav_back')]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if is_callback:
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def show_eggs_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show eggs shop"""
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    text = t(lang, 'shop_eggs_title')
    text += t(lang, 'shop_eggs_regular', gold=500)
    text += "\n\n"
    text += t(lang, 'shop_eggs_rare', gold=2000)
    text += "\n\n"
    text += t(lang, 'shop_eggs_premium', crystals=200)
    text += "\n\n"
    text += t(lang, 'shop_eggs_legendary', crystals=500)
    
    keyboard = [
        ["🥚 500 💰"],
        ["🔵 2000 💰"],
        ["💎 200 💎"],
        ["🌟 500 💎"],
        [t(lang, 'nav_back')]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def show_crystals_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show crystals shop"""
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    text = t(lang, 'shop_crystals_title')
    text += t(lang, 'shop_100_crystals')
    text += "\n\n"
    text += t(lang, 'shop_500_crystals')
    text += "\n\n"
    text += t(lang, 'shop_1200_crystals')
    text += "\n\n"
    text += t(lang, 'shop_2700_crystals')
    
    keyboard = [
        ["💎 100 ⭐️"],
        ["💎 500 ⭐️"],
        ["💎 1200 ⭐️"],
        ["💎 2700 ⭐️"],
        [t(lang, 'nav_back')]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def show_vip_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show VIP subscriptions"""
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    text = t(lang, 'vip_title')
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
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def handle_shop_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle shop purchase button clicks"""
    message = update.message.text
    
    # Eggs
    if message == "🥚 500 💰":
        await buy_egg(update, context, 'Regular', 500, 0)
    elif message == "🔵 2000 💰":
        await buy_egg(update, context, 'Rare', 2000, 0)
    elif message == "💎 200 💎":
        await buy_egg(update, context, 'Premium', 0, 200)
    elif message == "🌟 500 💎":
        await buy_egg(update, context, 'Legendary', 0, 500)
    
    # Crystals
    elif message == "💎 100 ⭐️":
        await send_stars_invoice(update, context, 'crystals', 100, config.CRYSTAL_PACKAGES[100])
    elif message == "💎 500 ⭐️":
        await send_stars_invoice(update, context, 'crystals', 500, config.CRYSTAL_PACKAGES[500])
    elif message == "💎 1200 ⭐️":
        await send_stars_invoice(update, context, 'crystals', 1200, config.CRYSTAL_PACKAGES[1200])
    elif message == "💎 2700 ⭐️":
        await send_stars_invoice(update, context, 'crystals', 2700, config.CRYSTAL_PACKAGES[2700])
    
    # VIP
    elif message == "🥉 VIP Bronze 99⭐️":
        await send_stars_invoice(update, context, 'vip', 1, config.VIP_PRICES[1])
    elif message == "🥈 VIP Silver 499⭐️":
        await send_stars_invoice(update, context, 'vip', 2, config.VIP_PRICES[2])
    elif message == "🥇 VIP Gold 999⭐️":
        await send_stars_invoice(update, context, 'vip', 3, config.VIP_PRICES[3])
    elif message == "💎 VIP Platinum 1999⭐️":
        await send_stars_invoice(update, context, 'vip', 4, config.VIP_PRICES[4])

async def buy_egg(update: Update, context: ContextTypes.DEFAULT_TYPE, egg_type: str, gold_cost: int, crystals_cost: int):
    """Buy an egg"""
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        
        # Check if user can afford
        if gold_cost > 0 and user.gold >= gold_cost:
            UserService.remove_gold(session, user, gold_cost)
        elif crystals_cost > 0 and user.crystals >= crystals_cost:
            UserService.remove_crystals(session, user, crystals_cost)
        else:
            if gold_cost > 0:
                await update.message.reply_text(t(lang, 'shop_not_enough_gold'))
            else:
                await update.message.reply_text(t(lang, 'shop_not_enough_crystals'))
            return
        
        # Create egg
        from services import EggService
        egg = EggService.create_egg(session, user, egg_type)
        
        await update.message.reply_text(
            t(lang, 'shop_purchase_success', 
              emoji='🥚', type=egg_type)
        )

def register_shop_handlers(application):
    """Register shop handlers"""
    application.add_handler(CallbackQueryHandler(shop_menu, pattern="^shop_menu$"))
    application.add_handler(CallbackQueryHandler(show_eggs_shop, pattern="^shop_eggs$"))
    application.add_handler(CallbackQueryHandler(show_crystals_shop, pattern="^shop_crystals$"))
    application.add_handler(CallbackQueryHandler(show_vip_shop, pattern="^shop_vip$"))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('🥚|🔵|💎'), handle_shop_purchase))
    # Message handler for reply keyboard shop button
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('🛒 Магазин|🛒 Shop'),
        shop_menu
    ))
