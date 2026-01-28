from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from database import get_session
from services import UserService
from localization import t
from datetime import datetime
from shop.shop_handler import shop_menu
from handlers.vip import vip_menu

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
        [t(lang, 'nav_eggs'), t(lang, 'nav_dragons')],
        [t(lang, 'nav_garden'), t(lang, 'nav_profile')],
        [t(lang, 'nav_shop'), t(lang, 'nav_vip')],
        [t(lang, 'nav_battlepass'), t(lang, 'nav_pay')],
        [t(lang, 'nav_language'), t(lang, 'nav_help')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
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
    
    keyboard = [[t(lang, 'nav_start')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
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
        [t('ru', 'language_russian')],
        [t('en', 'language_english')],
        [t(lang, 'nav_back')]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set language"""
    message_text = update.message.text
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        # Parse language from message
        if 'Русский' in message_text or 'Russian' in message_text:
            user.language = 'ru'
        elif 'English' in message_text:
            user.language = 'en'
        
        lang = user.language
        
        await update.message.reply_text(t(lang, 'language_changed'))
        # Return to main menu
        await start_command(update, context)

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_command(update, context)

def register_start_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^start_menu$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^help_menu$"))
    application.add_handler(MessageHandler(
        filters.TEXT & (filters.Regex('Главное меню|Main Menu') | filters.Regex('Назад|Back')),
        back_to_menu
    ))
    # Message handlers for reply keyboard buttons
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('🛒 Магазин|🛒 Shop'),
        shop_menu
    ))
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('👑 VIP'),
        vip_menu
    ))
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('🌐 Язык|🌐 Language'),
        language_command
    ))
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('❓ Справка|❓ Help'),
        help_command
    ))
