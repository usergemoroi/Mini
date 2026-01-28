from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database import get_session
from services import UserService

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        is_new_user = user.created_at and (user.updated_at - user.created_at).total_seconds() < 5
        
        if is_new_user:
            welcome_text = (
                "🐉 **Welcome to Dragon Garden!** 🌸\n\n"
                "A magical world where you can:\n"
                "🥚 Collect and hatch dragon eggs\n"
                "🐲 Raise and train mighty dragons\n"
                "🌱 Cultivate enchanted gardens\n"
                "💰 Earn gold and crystals\n"
                "✨ Build your dragon collection\n\n"
                f"You've received:\n"
                f"💰 1,000 Gold (starting gift)\n"
                f"💎 50 Crystals (welcome bonus)\n\n"
                "🎁 Claim your first FREE egg now!"
            )
        else:
            welcome_text = (
                f"🐉 **Welcome back to Dragon Garden!** 🌸\n\n"
                f"👤 {user.first_name}\n"
                f"💰 Gold: {user.gold:,}\n"
                f"💎 Crystals: {user.crystals:,}\n"
                f"🐉 Dragons: {len(user.dragons)}\n"
                f"🥚 Eggs: {len([e for e in user.eggs if not e.is_hatched])}\n\n"
                "What would you like to do?"
            )
    
    keyboard = [
        [
            InlineKeyboardButton("🥚 My Eggs", callback_data="eggs_menu"),
            InlineKeyboardButton("🐉 My Dragons", callback_data="dragons_menu")
        ],
        [
            InlineKeyboardButton("🌱 My Garden", callback_data="garden_menu"),
            InlineKeyboardButton("👤 Profile", callback_data="profile_menu")
        ],
        [
            InlineKeyboardButton("🛒 Shop", callback_data="shop_menu"),
            InlineKeyboardButton("❓ Help", callback_data="help_menu")
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
    help_text = (
        "📖 **Dragon Garden - Help Guide**\n\n"
        "**🥚 Eggs:**\n"
        "• Claim a free egg daily\n"
        "• Purchase eggs from the shop\n"
        "• Eggs hatch after 2-7 days\n"
        "• Check egg status anytime\n\n"
        "**🐉 Dragons:**\n"
        "• Feed dragons daily for XP\n"
        "• Level up to increase stats\n"
        "• Collect 60+ unique dragons\n"
        "• 5 rarity tiers: Common to Mythic\n\n"
        "**🌱 Garden:**\n"
        "• Plant magical crops\n"
        "• Harvest for gold rewards\n"
        "• Customize your garden\n"
        "• Different plants = different profits\n\n"
        "**💰 Resources:**\n"
        "• Gold - earned from plants & activities\n"
        "• Crystals - premium currency\n\n"
        "**Commands:**\n"
        "/start - Main menu\n"
        "/help - Show this help\n"
        "/profile - View your profile\n"
    )
    
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data="start_menu")]]
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

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_command(update, context)

def register_start_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^start_menu$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^help_menu$"))
