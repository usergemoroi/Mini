from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database import get_session
from services import UserService, EggService, DragonService
from utils.helpers import format_time_remaining, can_claim_daily_egg
from utils.constants import EGG_TYPES, RARITIES
from datetime import datetime

async def eggs_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        eggs = EggService.get_user_eggs(session, user)
        
        if not eggs:
            text = (
                "🥚 **Your Egg Collection**\n\n"
                "You don't have any eggs yet!\n\n"
                "💡 Claim your free daily egg or purchase eggs from the shop."
            )
        else:
            text = "🥚 **Your Egg Collection**\n\n"
            for i, egg in enumerate(eggs, 1):
                emoji = EGG_TYPES[egg.egg_type]['emoji']
                rarity_emoji = RARITIES[egg.rarity]['emoji']
                time_left = format_time_remaining(egg.hatches_at)
                status = "✅ Ready!" if egg.is_ready else f"⏰ {time_left}"
                
                text += f"{i}. {emoji} {egg.egg_type} Egg {rarity_emoji}\n"
                text += f"   Status: {status}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🎁 Claim Daily Free Egg", callback_data="claim_daily_egg")],
        [InlineKeyboardButton("🛒 Buy Eggs", callback_data="shop_eggs")],
        [InlineKeyboardButton("🔄 Check Eggs", callback_data="check_eggs")],
        [InlineKeyboardButton("« Back", callback_data="start_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def claim_daily_egg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        if not can_claim_daily_egg(user):
            time_since = (datetime.utcnow() - user.last_daily_egg).total_seconds()
            hours_remaining = 24 - (time_since / 3600)
            await query.answer(
                f"⏰ You can claim your next free egg in {hours_remaining:.1f} hours!",
                show_alert=True
            )
            return
        
        egg = EggService.create_egg(session, user, "Daily Free")
        UserService.update_daily_egg_time(session, user)
        
        text = (
            "🎉 **Daily Egg Claimed!**\n\n"
            f"You received a {EGG_TYPES['Daily Free']['emoji']} Daily Free Egg!\n"
            f"Rarity: {RARITIES[egg.rarity]['emoji']} {egg.rarity}\n\n"
            f"⏰ Hatches in: {format_time_remaining(egg.hatches_at)}\n\n"
            "Come back tomorrow for another free egg!"
        )
    
    keyboard = [[InlineKeyboardButton("« Back to Eggs", callback_data="eggs_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def check_eggs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        ready_eggs = EggService.check_ready_eggs(session, user)
        
        if ready_eggs:
            text = (
                "✨ **Eggs Ready to Hatch!**\n\n"
                f"You have {len(ready_eggs)} egg(s) ready!\n\n"
            )
            for egg in ready_eggs:
                text += f"🥚 {egg.egg_type} Egg ({RARITIES[egg.rarity]['emoji']} {egg.rarity})\n"
            
            keyboard = []
            for egg in ready_eggs:
                keyboard.append([
                    InlineKeyboardButton(
                        f"🐣 Hatch {egg.egg_type} Egg",
                        callback_data=f"hatch_egg_{egg.id}"
                    )
                ])
            keyboard.append([InlineKeyboardButton("« Back", callback_data="eggs_menu")])
            reply_markup = InlineKeyboardMarkup(keyboard)
        else:
            text = "⏰ No eggs are ready to hatch yet. Keep waiting!"
            keyboard = [[InlineKeyboardButton("« Back", callback_data="eggs_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def hatch_egg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    egg_id = int(query.data.split('_')[2])
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        egg = EggService.get_egg_by_id(session, egg_id, user.id)
        
        if not egg:
            await query.answer("❌ Egg not found!", show_alert=True)
            return
        
        if not egg.is_ready:
            await query.answer("⏰ This egg is not ready yet!", show_alert=True)
            return
        
        hatched_egg = EggService.hatch_egg(session, egg)
        dragon = DragonService.create_dragon(session, user, egg.rarity)
        
        dragon_info = dragon.dragon_type
        
        text = (
            "🎊 **Congratulations!**\n\n"
            f"Your {EGG_TYPES[egg.egg_type]['emoji']} egg has hatched!\n\n"
            f"🐉 You got: **{dragon.name}**\n"
            f"⭐ Rarity: {RARITIES[dragon.rarity]['emoji']} {dragon.rarity}\n"
            f"💪 Strength: {dragon.strength}\n"
            f"⚡ Agility: {dragon.agility}\n"
            f"🧠 Intelligence: {dragon.intelligence}\n\n"
            "Your new dragon is waiting in your collection!"
        )
    
    keyboard = [
        [InlineKeyboardButton("🐉 View My Dragons", callback_data="dragons_menu")],
        [InlineKeyboardButton("« Back to Eggs", callback_data="eggs_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def shop_eggs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        text = (
            "🛒 **Egg Shop**\n\n"
            f"Your Balance:\n"
            f"💰 {user.gold:,} Gold\n"
            f"💎 {user.crystals:,} Crystals\n\n"
            "Available Eggs:\n\n"
        )
        
        for egg_type, data in EGG_TYPES.items():
            if egg_type == "Daily Free":
                continue
            
            text += f"{data['emoji']} **{egg_type} Egg**\n"
            if data['cost_gold'] > 0:
                text += f"💰 Cost: {data['cost_gold']:,} Gold\n"
            if data['cost_crystals'] > 0:
                text += f"💎 Cost: {data['cost_crystals']:,} Crystals\n"
            text += f"⏰ Hatching: {data['hatching_hours']} hours\n"
            text += f"📊 Rarities:\n"
            for rarity, chance in data['rarities'].items():
                if chance > 0:
                    text += f"  {RARITIES[rarity]['emoji']} {rarity}: {chance}%\n"
            text += "\n"
    
    keyboard = [
        [InlineKeyboardButton("🥚 Buy Regular Egg (500 Gold)", callback_data="buy_egg_Regular")],
        [InlineKeyboardButton("🔵 Buy Rare Egg (2000 Gold)", callback_data="buy_egg_Rare")],
        [InlineKeyboardButton("💎 Buy Premium Egg (200 Crystals)", callback_data="buy_egg_Premium")],
        [InlineKeyboardButton("« Back", callback_data="eggs_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def buy_egg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    egg_type = query.data.split('_')[2]
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        can_purchase, message = EggService.can_purchase_egg(user, egg_type)
        
        if not can_purchase:
            await query.answer(f"❌ {message}", show_alert=True)
            return
        
        egg_data = EGG_TYPES[egg_type]
        
        if egg_data['cost_gold'] > 0:
            UserService.remove_gold(session, user, egg_data['cost_gold'])
        if egg_data['cost_crystals'] > 0:
            UserService.remove_crystals(session, user, egg_data['cost_crystals'])
        
        egg = EggService.create_egg(session, user, egg_type)
        
        await query.answer(f"✅ Purchased {egg_type} Egg!", show_alert=True)
        
        text = (
            "🎉 **Purchase Successful!**\n\n"
            f"You bought a {egg_data['emoji']} {egg_type} Egg!\n"
            f"Rarity: {RARITIES[egg.rarity]['emoji']} {egg.rarity}\n\n"
            f"⏰ Hatches in: {format_time_remaining(egg.hatches_at)}\n\n"
            f"Current Balance:\n"
            f"💰 {user.gold:,} Gold\n"
            f"💎 {user.crystals:,} Crystals"
        )
    
    keyboard = [
        [InlineKeyboardButton("🛒 Buy Another", callback_data="shop_eggs")],
        [InlineKeyboardButton("« Back to Eggs", callback_data="eggs_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def register_egg_handlers(application):
    application.add_handler(CallbackQueryHandler(eggs_menu, pattern="^eggs_menu$"))
    application.add_handler(CallbackQueryHandler(claim_daily_egg, pattern="^claim_daily_egg$"))
    application.add_handler(CallbackQueryHandler(check_eggs, pattern="^check_eggs$"))
    application.add_handler(CallbackQueryHandler(hatch_egg, pattern="^hatch_egg_"))
    application.add_handler(CallbackQueryHandler(shop_eggs, pattern="^shop_eggs$"))
    application.add_handler(CallbackQueryHandler(buy_egg, pattern="^buy_egg_"))
