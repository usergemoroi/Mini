from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from database import get_session
from services import UserService, GardenService
from utils.helpers import format_time_remaining
from utils.constants import PLANTS
from localization import t

async def garden_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    is_callback = query is not None
    
    if is_callback:
        await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        lang = user.language
        garden = GardenService.get_user_garden(session, user)
        plants = GardenService.get_user_plants(session, user)
        
        text = t(lang, 'garden_title')
        text += f"_{garden.description}_\n\n"
        text += f"🎨 Theme: {garden.theme}\n"
        text += f"💰 Gold: {user.gold:,}\n\n"
        
        if plants:
            text += "**Your Plants:**\n"
            for plant in plants[:10]:
                plant_emoji = PLANTS[plant.plant_type]['emoji']
                if plant.is_ready:
                    status = "✅ Ready to harvest!"
                else:
                    status = f"⏰ {format_time_remaining(plant.ready_at)}"
                text += f"{plant_emoji} {plant.plant_type} - {status}\n"
            
            if len(plants) > 10:
                text += f"\n...and {len(plants) - 10} more plants growing!"
        else:
            text = t(lang, 'garden_empty')
    
    keyboard = [
        [InlineKeyboardButton("🌱 Plant Crops", callback_data="plant_menu")],
        [InlineKeyboardButton("🌾 Harvest Ready Plants", callback_data="harvest_menu")],
        [InlineKeyboardButton("🔄 Check Plants", callback_data="check_plants")],
        [InlineKeyboardButton(t(lang, 'garden_back'), callback_data="start_menu")]
    ]
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

async def plant_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        text = (
            "🌱 **Plant Shop**\n\n"
            f"Your Gold: 💰 {user.gold:,}\n\n"
            "Available Plants:\n\n"
        )
        
        for plant_name, data in PLANTS.items():
            text += f"{data['emoji']} **{plant_name}**\n"
            text += f"💰 Cost: {data['cost_gold']} Gold\n"
            text += f"⏰ Growth: {data['growth_hours']} hours\n"
            text += f"💵 Reward: {data['reward_gold']} Gold\n"
            profit = data['reward_gold'] - data['cost_gold']
            text += f"📈 Profit: +{profit} Gold\n"
            text += f"_{data['description']}_\n\n"
    
    keyboard = []
    for plant_name in list(PLANTS.keys())[:6]:
        keyboard.append([
            InlineKeyboardButton(
                f"{PLANTS[plant_name]['emoji']} Plant {plant_name}",
                callback_data=f"plant_{plant_name.replace(' ', '_')}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("« Back to Garden", callback_data="garden_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def plant_crop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    plant_name = query.data.split('_', 1)[1].replace('_', ' ')
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        
        plant, message = GardenService.plant_crop(session, user, plant_name)
        
        if not plant:
            await query.answer(f"❌ {message}", show_alert=True)
            return
        
        plant_data = PLANTS[plant_name]
        
        await query.answer(f"✅ Planted {plant_name}!", show_alert=True)
        
        text = (
            "🌱 **Plant Successful!**\n\n"
            f"You planted {plant_data['emoji']} **{plant_name}**!\n\n"
            f"💰 Cost: -{plant_data['cost_gold']} Gold\n"
            f"⏰ Ready in: {format_time_remaining(plant.ready_at)}\n"
            f"💵 Will earn: {plant_data['reward_gold']} Gold\n\n"
            f"Current Gold: 💰 {user.gold:,}"
        )
    
    keyboard = [
        [InlineKeyboardButton("🌱 Plant Another", callback_data="plant_menu")],
        [InlineKeyboardButton("« Back to Garden", callback_data="garden_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def check_plants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        ready_plants = GardenService.check_ready_plants(session, user)
        
        if ready_plants:
            text = (
                "✨ **Plants Ready!**\n\n"
                f"You have {len(ready_plants)} plant(s) ready to harvest!\n\n"
            )
            for plant in ready_plants:
                plant_data = PLANTS[plant.plant_type]
                text += f"{plant_data['emoji']} {plant.plant_type} - 💰 {plant_data['reward_gold']} Gold\n"
            
            keyboard = [[InlineKeyboardButton("🌾 Harvest All", callback_data="harvest_all")]]
        else:
            text = "⏰ No plants are ready yet. Keep waiting!"
            keyboard = []
        
        keyboard.append([InlineKeyboardButton("« Back to Garden", callback_data="garden_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def harvest_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        plants = GardenService.get_user_plants(session, user)
        ready_plants = [p for p in plants if p.is_ready]
        
        if not ready_plants:
            text = "⏰ No plants are ready to harvest yet!"
            keyboard = [
                [InlineKeyboardButton("🔄 Check Plants", callback_data="check_plants")],
                [InlineKeyboardButton("« Back to Garden", callback_data="garden_menu")]
            ]
        else:
            text = f"🌾 **Ready to Harvest** ({len(ready_plants)} plants)\n\n"
            total_gold = 0
            
            for plant in ready_plants:
                plant_data = PLANTS[plant.plant_type]
                total_gold += plant_data['reward_gold']
                text += f"{plant_data['emoji']} {plant.plant_type} - 💰 {plant_data['reward_gold']} Gold\n"
            
            text += f"\n💰 **Total Value: {total_gold:,} Gold**"
            
            keyboard = [
                [InlineKeyboardButton("🌾 Harvest All", callback_data="harvest_all")],
                [InlineKeyboardButton("« Back to Garden", callback_data="garden_menu")]
            ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def harvest_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        plants = GardenService.get_user_plants(session, user)
        ready_plants = [p for p in plants if p.is_ready]
        
        if not ready_plants:
            await query.answer("❌ No plants ready to harvest!", show_alert=True)
            return
        
        total_gold = 0
        harvested_plants = []
        
        for plant in ready_plants:
            reward = GardenService.harvest_plant(session, user, plant)
            if reward:
                total_gold += reward
                harvested_plants.append(plant.plant_type)
        
        await query.answer(f"✅ Harvested {len(harvested_plants)} plants!", show_alert=True)
        
        text = (
            "🎉 **Harvest Complete!**\n\n"
            f"You harvested {len(harvested_plants)} plant(s)!\n\n"
        )
        
        plant_counts = {}
        for plant_type in harvested_plants:
            plant_counts[plant_type] = plant_counts.get(plant_type, 0) + 1
        
        for plant_type, count in plant_counts.items():
            plant_emoji = PLANTS[plant_type]['emoji']
            text += f"{plant_emoji} {plant_type} x{count}\n"
        
        text += f"\n💰 **Total Earned: {total_gold:,} Gold**\n"
        text += f"💰 New Balance: {user.gold:,} Gold"
    
    keyboard = [
        [InlineKeyboardButton("🌱 Plant More", callback_data="plant_menu")],
        [InlineKeyboardButton("« Back to Garden", callback_data="garden_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def register_garden_handlers(application):
    application.add_handler(CallbackQueryHandler(garden_menu, pattern="^garden_menu$"))
    application.add_handler(CallbackQueryHandler(plant_menu, pattern="^plant_menu$"))
    application.add_handler(CallbackQueryHandler(plant_crop, pattern="^plant_"))
    application.add_handler(CallbackQueryHandler(check_plants, pattern="^check_plants$"))
    application.add_handler(CallbackQueryHandler(harvest_menu, pattern="^harvest_menu$"))
    application.add_handler(CallbackQueryHandler(harvest_all, pattern="^harvest_all$"))
    # Message handlers for reply keyboard buttons
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex('🌱 Сад|🌱 Garden'),
        garden_menu
    ))
