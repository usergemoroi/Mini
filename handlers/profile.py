from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from database import get_session
from services import UserService
from utils.helpers import format_user_profile
from utils.constants import RARITIES

async def profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        text = "👤 **Your Profile**\n\n"
        text += format_user_profile(user)
        
        rarity_counts = {}
        for dragon in user.dragons:
            rarity_counts[dragon.rarity] = rarity_counts.get(dragon.rarity, 0) + 1
        
        if rarity_counts:
            text += "\n\n🐉 **Dragon Collection:**\n"
            for rarity in ['Common', 'Rare', 'Epic', 'Legendary', 'Mythic']:
                count = rarity_counts.get(rarity, 0)
                if count > 0:
                    text += f"{RARITIES[rarity]['emoji']} {rarity}: {count}\n"
        
        active_eggs = len([e for e in user.eggs if not e.is_hatched])
        active_plants = len([p for p in user.plants if not p.is_harvested])
        
        text += f"\n📊 **Active Items:**\n"
        text += f"🥚 Hatching: {active_eggs}\n"
        text += f"🌱 Growing: {active_plants}\n"
    
    keyboard = [
        [InlineKeyboardButton("🐉 My Dragons", callback_data="dragons_menu")],
        [InlineKeyboardButton("🥚 My Eggs", callback_data="eggs_menu")],
        [InlineKeyboardButton("🌱 My Garden", callback_data="garden_menu")],
        [InlineKeyboardButton("« Back", callback_data="start_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await profile_menu(update, context)

async def shop_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        text = (
            "🛒 **Dragon Garden Shop**\n\n"
            f"Your Balance:\n"
            f"💰 Gold: {user.gold:,}\n"
            f"💎 Crystals: {user.crystals:,}\n\n"
            "What would you like to buy?\n"
        )
    
    keyboard = [
        [InlineKeyboardButton("🥚 Buy Eggs", callback_data="shop_eggs")],
        [InlineKeyboardButton("🌱 Buy Seeds", callback_data="plant_menu")],
        [InlineKeyboardButton("💎 Get Crystals", callback_data="shop_crystals")],
        [InlineKeyboardButton("« Back", callback_data="start_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def shop_crystals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = (
        "💎 **Crystal Shop**\n\n"
        "Crystals are the premium currency in Dragon Garden.\n"
        "Use them to buy premium eggs, exclusive items, and more!\n\n"
        "**Available Packages:**\n\n"
        "💎 100 Crystals - $0.99\n"
        "💎 500 Crystals - $4.99\n"
        "💎 1,000 Crystals - $9.99\n"
        "💎 5,000 Crystals - $39.99\n\n"
        "⚠️ Payment integration coming in Phase 3!"
    )
    
    keyboard = [[InlineKeyboardButton("« Back to Shop", callback_data="shop_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def register_profile_handlers(application):
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CallbackQueryHandler(profile_menu, pattern="^profile_menu$"))
    application.add_handler(CallbackQueryHandler(shop_menu, pattern="^shop_menu$"))
    application.add_handler(CallbackQueryHandler(shop_crystals, pattern="^shop_crystals$"))
