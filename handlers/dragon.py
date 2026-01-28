from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from database import get_session
from services import UserService, DragonService
from utils.helpers import format_dragon_stats
from utils.constants import RARITIES
from localization import t

async def dragons_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    is_callback = query is not None
    
    if is_callback:
        await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        dragons = DragonService.get_user_dragons(session, user)
        
        if not dragons:
            text = t(lang, 'dragons_empty')
            keyboard = [
                [InlineKeyboardButton(t(lang, 'eggs_go_shop'), callback_data="eggs_menu")],
                [InlineKeyboardButton(t(lang, 'dragons_back'), callback_data="start_menu")]
            ]
        else:
            text = t(lang, 'dragons_title', count=len(dragons))
            
            rarity_counts = {}
            for dragon in dragons:
                rarity_counts[dragon.rarity] = rarity_counts.get(dragon.rarity, 0) + 1
            
            text += t(lang, 'dragons_collection_stats')
            for rarity in ['Common', 'Rare', 'Epic', 'Legendary', 'Mythic']:
                count = rarity_counts.get(rarity, 0)
                if count > 0:
                    text += f"{RARITIES[rarity]['emoji']} {rarity}: {count}\n"
            
            text += t(lang, 'dragons_list')
            for i, dragon in enumerate(dragons[:10], 1):
                hunger_bar = "🟩" * (dragon.hunger // 20) + "⬜" * (5 - dragon.hunger // 20)
                text += f"\n{i}. {RARITIES[dragon.rarity]['emoji']} **{dragon.name}** (Lv.{dragon.level})\n"
                text += f"   Hunger: {hunger_bar} {dragon.hunger}%\n"
            
            if len(dragons) > 10:
                text += t(lang, 'dragons_more', count=len(dragons) - 10)
            
            keyboard = []
            for dragon in dragons[:5]:
                keyboard.append([
                    InlineKeyboardButton(
                        f"{RARITIES[dragon.rarity]['emoji']} {dragon.name}",
                        callback_data=f"view_dragon_{dragon.id}"
                    )
                ])
            
            if len(dragons) > 5:
                keyboard.append([InlineKeyboardButton(t(lang, 'dragons_view_all'), callback_data="dragons_list")])
            
            keyboard.append([InlineKeyboardButton(t(lang, 'dragons_back'), callback_data="start_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
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

async def view_dragon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    dragon_id = int(query.data.split('_')[2])
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        dragon = DragonService.get_dragon_by_id(session, dragon_id, user.id)
        
        if not dragon:
            await query.answer("❌ Dragon not found!", show_alert=True)
            return
        
        text = "🐉 **Dragon Details**\n\n"
        text += format_dragon_stats(dragon)
        
        from datetime import datetime
        if dragon.last_fed:
            time_since_fed = (datetime.utcnow() - dragon.last_fed).total_seconds() / 3600
            if time_since_fed < 24:
                text += f"\n\n⏰ Can feed again in {24 - time_since_fed:.1f} hours"
            else:
                text += "\n\n✅ Ready to be fed!"
        else:
            text += "\n\n🍖 Never been fed - feed me!"
    
    keyboard = [
        [InlineKeyboardButton("🍖 Feed Dragon", callback_data=f"feed_dragon_{dragon.id}")],
        [InlineKeyboardButton("« Back to Dragons", callback_data="dragons_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def feed_dragon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    dragon_id = int(query.data.split('_')[2])
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        dragon = DragonService.get_dragon_by_id(session, dragon_id, user.id)
        
        if not dragon:
            await query.answer("❌ Dragon not found!", show_alert=True)
            return
        
        success, result = DragonService.feed_dragon(session, dragon)
        
        if not success:
            hours_remaining = result
            await query.answer(
                f"⏰ You can feed this dragon again in {hours_remaining:.1f} hours!",
                show_alert=True
            )
            return
        
        if result == "level_up":
            await query.answer("🎉 Your dragon leveled up!", show_alert=True)
            text = (
                "🎉 **Level Up!**\n\n"
                f"{RARITIES[dragon.rarity]['emoji']} **{dragon.name}** reached Level {dragon.level}!\n\n"
                "**New Stats:**\n"
                f"💪 Strength: {dragon.strength}\n"
                f"⚡ Agility: {dragon.agility}\n"
                f"🧠 Intelligence: {dragon.intelligence}\n\n"
                f"❤️ Hunger: {dragon.hunger}%\n"
                f"😊 Happiness: {dragon.happiness}%"
            )
        else:
            await query.answer("✅ Dragon fed successfully!", show_alert=True)
            text = (
                "🍖 **Dragon Fed!**\n\n"
                f"{RARITIES[dragon.rarity]['emoji']} **{dragon.name}** enjoyed the meal!\n\n"
                f"❤️ Hunger: {dragon.hunger}%\n"
                f"😊 Happiness: {dragon.happiness}%\n"
                f"⭐ Experience gained: +10\n\n"
                "Come back tomorrow to feed again!"
            )
    
    keyboard = [
        [InlineKeyboardButton("📊 View Stats", callback_data=f"view_dragon_{dragon.id}")],
        [InlineKeyboardButton("« Back to Dragons", callback_data="dragons_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def dragons_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        dragons = DragonService.get_user_dragons(session, user)
        
        text = f"🐉 **All Your Dragons** ({len(dragons)} total)\n\n"
        
        for i, dragon in enumerate(dragons, 1):
            text += f"{i}. {RARITIES[dragon.rarity]['emoji']} {dragon.name} (Lv.{dragon.level})\n"
            
            if i % 15 == 0 and i < len(dragons):
                text += "\n"
        
        keyboard = [
            [InlineKeyboardButton("« Back to Dragons", callback_data="dragons_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def register_dragon_handlers(application):
    application.add_handler(CallbackQueryHandler(dragons_menu, pattern="^dragons_menu$"))
    application.add_handler(CallbackQueryHandler(view_dragon, pattern="^view_dragon_"))
    application.add_handler(CallbackQueryHandler(feed_dragon, pattern="^feed_dragon_"))
    application.add_handler(CallbackQueryHandler(dragons_list, pattern="^dragons_list$"))
    # Message handlers for reply keyboard buttons
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('🐉 Драконы|🐉 Dragons'),
        dragons_menu
    ))
