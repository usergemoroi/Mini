# 🐉 Dragon Garden - Telegram Bot Game

A magical Telegram bot game where players breed dragons, cultivate enchanted gardens, and build their collection of mystical creatures!

## 🎮 Game Features (Phase 1 - MVP)

### ✨ Core Gameplay
- **Dragon Breeding**: Hatch eggs to discover 60+ unique dragons across 5 rarity tiers
- **Garden Management**: Plant and harvest magical crops for gold rewards
- **Resource System**: Earn gold from activities, crystals as premium currency
- **Daily Rewards**: Claim free eggs every 24 hours
- **Dragon Care**: Feed your dragons daily to level them up and improve their stats

### 🐲 Dragon System
- **5 Rarity Tiers**: Common ⚪️, Rare 🔵, Epic 🟣, Legendary 🟡, Mythic 🔴
- **60+ Unique Dragons**: Each with unique names, colors, elements, and abilities
- **Stats & Leveling**: Strength, Agility, Intelligence stats that grow with levels
- **Hunger & Happiness**: Keep your dragons fed and happy
- **Experience System**: Feed dragons daily to gain XP and level up

### 🥚 Egg System
- **Daily Free Egg**: Claim a free egg every 24 hours
- **Multiple Egg Types**:
  - Regular Egg: 500 Gold, 48h hatching
  - Rare Egg: 2,000 Gold, 72h hatching
  - Premium Egg: 200 Crystals, 96h hatching
- **Rarity-based Drops**: Different eggs have different chances for rare dragons
- **Hatching Timer**: Real-time countdown until eggs are ready

### 🌱 Garden System
- **8 Plant Types**: From quick-growing Mushrooms to valuable Lotus flowers
- **Growth Times**: 0.5 to 3 hours depending on plant type
- **Profit System**: Each plant has different costs and rewards
- **Harvest System**: Collect gold when plants are ready
- **Garden Customization**: Name your garden and customize it

### 💰 Economy
- **Gold Currency**: Earned from harvesting plants, activities, and rewards
- **Crystal Currency**: Premium currency (Phase 3 will add purchases)
- **Starting Resources**: 1,000 Gold + 50 Crystals for new players
- **Resource Management**: Smart spending for optimal dragon collection

## 🛠️ Technical Stack

- **Language**: Python 3.8+
- **Framework**: python-telegram-bot 20.7
- **Database**: SQLAlchemy with PostgreSQL/SQLite support
- **Scheduling**: APScheduler for timed events
- **Environment**: python-dotenv for configuration

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (optional, SQLite works too)
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd dragon-garden
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
DATABASE_URL=sqlite:///dragon_garden.db
BOT_USERNAME=your_bot_username
```

### Step 4: Run the Bot
```bash
python bot.py
```

## 🎯 How to Get a Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to choose a name and username
4. Copy the token provided by BotFather
5. Paste it in your `.env` file

## 🎮 How to Play

### Starting Out
1. Start a chat with your bot
2. Send `/start` to create your account
3. You'll receive 1,000 Gold and 50 Crystals as welcome bonus

### Claiming Your First Egg
1. Click "🥚 My Eggs" from the main menu
2. Click "🎁 Claim Daily Free Egg"
3. Wait for the egg to hatch (48 hours for daily eggs)
4. Come back and hatch your first dragon!

### Feeding Dragons
1. Go to "🐉 My Dragons"
2. Select a dragon to view its stats
3. Click "🍖 Feed Dragon" (once per 24 hours)
4. Watch your dragon gain XP and level up!

### Growing Plants
1. Go to "🌱 My Garden"
2. Click "🌱 Plant Crops"
3. Choose a plant type to grow
4. Wait for it to mature
5. Harvest for gold rewards!

### Buying More Eggs
1. Go to "🛒 Shop" → "🥚 Buy Eggs"
2. Choose an egg type
3. Spend gold or crystals
4. Wait for it to hatch!

## 📊 Database Schema

### Users Table
- User information, resources (gold/crystals), VIP status
- Tracks last daily egg claim time

### Dragons Table
- Dragon type, rarity, level, stats
- Hunger, happiness, and experience tracking
- Last fed timestamp

### Eggs Table
- Egg type, rarity, hatching time
- Timestamps for hatching countdown
- Hatched status

### Plants Table
- Plant type, planted time, ready time
- Harvested status

### Gardens Table
- Garden name, description, theme
- Decoration storage (for future updates)

## 🗺️ Project Structure

```
dragon-garden/
├── bot.py                 # Main entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── database/
│   ├── __init__.py
│   ├── db.py             # Database connection
│   └── models.py         # SQLAlchemy models
├── services/
│   ├── user_service.py   # User operations
│   ├── dragon_service.py # Dragon management
│   ├── egg_service.py    # Egg operations
│   └── garden_service.py # Garden/plant logic
├── handlers/
│   ├── start.py          # Start/help commands
│   ├── dragon.py         # Dragon handlers
│   ├── egg.py            # Egg handlers
│   ├── garden.py         # Garden handlers
│   └── profile.py        # Profile/shop handlers
└── utils/
    ├── constants.py      # Game data (dragons, eggs, plants)
    └── helpers.py        # Utility functions
```

## 🔮 Future Phases

### Phase 2: Full Resource & VIP System
- VIP subscription tiers (Bronze, Silver, Gold, Platinum)
- Monthly Battlepass with exclusive rewards
- Enhanced plant varieties and garden decorations
- VIP-exclusive dragons and seeds

### Phase 3: Premium Shop & Payments
- Stripe/Telegram Stars payment integration
- Premium dragon packs and bundles
- Exclusive decorations and dragon skins
- Dragon renaming and customization

### Phase 4: Social Features
- Garden gallery to showcase to other players
- Leaderboards (biggest dragon, most beautiful garden)
- Trading and gifting system
- Guilds and cooperative gameplay
- Monthly seasonal events with exclusive dragons

## 🎨 Game Design Highlights

### Dragon Rarities & Drop Rates
- **Common** (⚪️): 50-70% - Easy to collect
- **Rare** (🔵): 25-45% - Moderately uncommon
- **Epic** (🟣): 5-35% - Valuable finds
- **Legendary** (🟡): 1-35% - Very rare
- **Mythic** (🔴): 0-5% - Extremely rare

### Plant Economics
| Plant | Cost | Time | Reward | Profit |
|-------|------|------|--------|--------|
| Mushroom | 30g | 0.5h | 80g | +50g |
| Sunflower | 50g | 1h | 150g | +100g |
| Tulip | 75g | 1.5h | 225g | +150g |
| Rose | 100g | 2h | 350g | +250g |
| Lotus | 200g | 3h | 700g | +500g |

### Dragon Elements
- Fire 🔥, Water 💧, Nature 🍃, Earth 🪨
- Electric ⚡, Ice ❄️, Air 💨, Light ✨
- Dark 🌑, Crystal 💎, Cosmic 🌌, Divine 👑
- And many more unique elements!

## 🐛 Troubleshooting

### Bot doesn't respond
- Check if bot token is correct in `.env`
- Ensure bot is running (`python bot.py`)
- Check internet connection

### Database errors
- Delete `dragon_garden.db` file to reset database
- Check DATABASE_URL in `.env`
- Ensure PostgreSQL is running (if using PostgreSQL)

### Import errors
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+ required)

## 👨‍💻 Development

### Adding New Dragons
Edit `utils/constants.py` and add to the `DRAGONS` dictionary:
```python
'Rarity': [
    {'name': 'Dragon Name', 'emoji': '🐉', 'color': 'Color', 
     'element': 'Element', 'ability': 'Ability Name'},
]
```

### Adding New Plants
Edit `utils/constants.py` and add to the `PLANTS` dictionary:
```python
'Plant Name': {
    'emoji': '🌸',
    'growth_hours': 2,
    'cost_gold': 100,
    'reward_gold': 300,
    'description': 'Description here'
}
```

## 📝 Commands

- `/start` - Main menu and game overview
- `/help` - Show help guide
- `/profile` - View your profile and stats

## 🤝 Contributing

This is a Phase 1 MVP implementation. Future phases will add:
- Payment integration
- Event systems
- Social features
- Advanced customization

## 📄 License

This project is provided as-is for educational and entertainment purposes.

## 🎉 Credits

Created with ❤️ for Telegram bot game enthusiasts!

---

**Enjoy building your Dragon Garden! 🐉🌸**
