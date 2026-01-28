from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import get_session
from services import UserService
from localization import t
from datetime import datetime

# Import callback handlers
from shop.shop_handler import shop_menu
from handlers.vip import vip_menu
from handlers.battlepass import battlepass_menu
from handlers.profile import profile_menu
from handlers.dragon import dragons_menu
from handlers.egg import eggs_menu

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        is_new_user = user.created_at and (user.updated_at - user.created_at).total_seconds() < 5
        lang = user.language
        
        if is_new_user:
            welcome_text = t(lang, 'start_welcome')
        else:
            eggs_count = len([e for e in user.eggs if not e.is_hatched])
            welcome_text = t(lang, 'start_welcome_back',
                             first_name=user.first_name,
                             gold=user.gold,
                             crystals=user.crystals,
                             dragons=len(user.dragons),
                             eggs=eggs_count)
    
    keyboard = [
        [
            InlineKeyboardButton(t(lang, 'nav_eggs'), callback_data="eggs_menu"),
            InlineKeyboardButton(t(lang, 'nav_dragons'), callback_data="dragons_menu")
        ],
        [
            InlineKeyboardButton(t(lang, 'nav_garden'), callback_data="garden_menu"),
            InlineKeyboardButton(t(lang, 'nav_profile'), callback_data="profile_menu")
        ],
        [
            InlineKeyboardButton(t(lang, 'nav_shop'), callback_data="shop_main"),
            InlineKeyboardButton(t(lang, 'nav_vip'), callback_data="vip_menu")
        ],
        [
            InlineKeyboardButton(t(lang, 'nav_battlepass'), callback_data="battlepass_menu"),
            InlineKeyboardButton(t(lang, 'nav_pay'), callback_data="pay_menu")
        ],
        [
            InlineKeyboardButton(t(lang, 'nav_language'), callback_data="language_select"),
            InlineKeyboardButton(t(lang, 'nav_help'), callback_data="help_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    help_text = t(lang, 'help_title')
    help_text += t(lang, 'help_eggs')
    help_text += t(lang, 'help_dragons')
    help_text += t(lang, 'help_garden')
    help_text += t(lang, 'help_resources')
    help_text += t(lang, 'help_commands')
    
    keyboard = [[InlineKeyboardButton(t(lang, 'nav_back'), callback_data="start_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=help_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=help_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change language"""
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
    
    text = t(lang, 'language_select')
    
    keyboard = [
        [InlineKeyboardButton(t('ru', 'language_russian'), callback_data="set_lang_ru")],
        [InlineKeyboardButton(t('en', 'language_english'), callback_data="set_lang_en")],
        [InlineKeyboardButton(t(lang, 'nav_back'), callback_data="start_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def set_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set language via callback"""
    query = update.callback_query
    await query.answer()
    
    # Extract language from callback_data (e.g., "set_lang_ru" or "set_lang_en")
    lang_code = query.data.split('_')[-1]
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        user.language = lang_code
        
        await query.edit_message_text(t(lang_code, 'language_changed'))
        # Return to main menu
        await start_command(update, context)

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_command(update, context)

def register_start_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language_command))
    
    # Main menu navigation callbacks
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^start_menu$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^help_menu$"))
    application.add_handler(CallbackQueryHandler(language_command, pattern="^language_select$"))
    application.add_handler(CallbackQueryHandler(set_language_callback, pattern="^set_lang_"))
    
    # Menu item callbacks (from main menu)
    application.add_handler(CallbackQueryHandler(shop_menu, pattern="^shop_main$"))
    application.add_handler(CallbackQueryHandler(vip_menu, pattern="^vip_menu$"))
    application.add_handler(CallbackQueryHandler(profile_menu, pattern="^profile_menu$"))
    application.add_handler(CallbackQueryHandler(battlepass_menu, pattern="^battlepass_menu$"))
