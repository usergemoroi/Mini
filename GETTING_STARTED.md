# 🚀 Getting Started with Dragon Garden

Welcome to Dragon Garden! This guide will get you from zero to playing in just a few minutes.

## ⚡ Super Quick Start (5 Minutes)

### 1️⃣ Get Your Bot Token (2 minutes)
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Choose a name: "My Dragon Garden"
5. Choose a username: "my_dragon_garden_bot" (must end in 'bot')
6. Copy the token you receive (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2️⃣ Install & Configure (2 minutes)
```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and paste your token
nano .env
# or
notepad .env  # On Windows
```

In `.env`, change:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```
to:
```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```
(use your actual token)

### 3️⃣ Run the Bot (1 minute)
```bash
python bot.py
```

You should see:
```
INFO - Initializing database...
INFO - Database initialized successfully!
INFO - Creating bot application...
INFO - Registering handlers...
INFO - All handlers registered!
INFO - Starting bot...
INFO - Dragon Garden bot is now running! Press Ctrl+C to stop.
```

### 4️⃣ Play! (Now)
1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. Start collecting dragons! 🐉

---

## 🎮 First Steps in the Game

### Your First Actions
1. **Claim Free Egg**
   - Click "🥚 My Eggs"
   - Click "🎁 Claim Daily Free Egg"
   - Wait 48 hours (or see testing mode below)

2. **Plant Your First Crop**
   - Click "🌱 My Garden"
   - Click "🌱 Plant Crops"
   - Choose "Mushroom" (fastest, 30 minutes)
   - Come back in 30 min to harvest

3. **Earn Gold**
   - Harvest plants for gold
   - Use gold to buy more eggs
   - Plant more crops for more gold

4. **Collect Dragons**
   - Hatch eggs to get dragons
   - Feed dragons daily for XP
   - Watch them level up!

---

## 🧪 Testing Mode (Skip the Wait)

Want to test without waiting? Edit these files:

### Fast Egg Hatching
Edit `utils/constants.py`, line 105:
```python
# Change this:
'hatching_hours': 48,

# To this (6 minutes):
'hatching_hours': 0.1,
```

### Fast Plant Growth
Edit `utils/constants.py`, line 150:
```python
# Change this:
'growth_hours': 1,

# To this (1 minute):
'growth_hours': 0.017,
```

### Fast Daily Egg Cooldown
Edit `config.py`, line 11:
```python
# Change this:
DAILY_FREE_EGG_COOLDOWN = 24 * 60 * 60

# To this (1 minute):
DAILY_FREE_EGG_COOLDOWN = 60
```

**Restart the bot** after making changes.

---

## 📚 What to Read Next

### New Users
- ✅ You're here! (GETTING_STARTED.md)
- → **README.md** - Full game features and guide
- → **QUICKSTART.md** - Alternative quick guide

### Game Players
- **README.md** - Complete game documentation
- See in-game `/help` - Game guide in Telegram

### Developers
- **ARCHITECTURE.md** - System design
- **API_REFERENCE.md** - Code documentation
- **CONTRIBUTING.md** - Add features

### Deployers
- **DEPLOYMENT.md** - Production setup
- Choose VPS, Heroku, Docker, or Railway

---

## ❓ Common Issues

### "ModuleNotFoundError: No module named 'telegram'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "TELEGRAM_BOT_TOKEN not found"
**Solution**: Create `.env` file and add your token
```bash
cp .env.example .env
# Edit .env and add your token
```

### Bot doesn't respond in Telegram
**Solutions**:
1. Check if bot.py is running (look for the running message)
2. Verify token is correct in .env
3. Make sure you're messaging the right bot
4. Check console for error messages

### Database error
**Solution**: Delete database and restart
```bash
rm dragon_garden.db  # If using SQLite
python bot.py
```

### "pip command not found"
**Solution**: Install Python and pip
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# macOS
brew install python3

# Windows: Download from python.org
```

---

## 🎯 Quick Commands

### Run the Bot
```bash
python bot.py
```

### Check Setup
```bash
python setup.py
```

### Test Game Mechanics
```bash
python test_game.py
```

### Stop the Bot
Press `Ctrl+C` in the terminal

---

## 🌟 Game Features Overview

### What You Can Do
- 🥚 **Collect Eggs** - Daily free + purchasable eggs
- 🐉 **Hatch Dragons** - 60 unique dragons to discover
- 🍖 **Feed Dragons** - Daily feeding for XP and levels
- 🌱 **Grow Plants** - 8 plant types for profit
- 💰 **Earn Gold** - Harvest plants, complete activities
- 💎 **Use Crystals** - Premium currency for special eggs
- 📊 **Track Progress** - View your profile and stats

### 5 Dragon Rarities
- ⚪️ **Common** - Easy to find
- 🔵 **Rare** - Moderately uncommon
- 🟣 **Epic** - Valuable finds
- 🟡 **Legendary** - Very rare
- 🔴 **Mythic** - Extremely rare

### 8 Plant Types
- 🍄 Mushroom - Fast gold (30 min)
- 🌻 Sunflower - Good profit (1 hour)
- 🌷 Tulip - Balanced (1.5 hours)
- 🌹 Rose - Better returns (2 hours)
- 🌺 Hibiscus - Decent profit (2 hours)
- 💜 Lavender - Good gold/hr (1.5 hours)
- 🌸 Cherry Blossom - High value (2.5 hours)
- 🪷 Lotus - Best profit (3 hours)

---

## 🎓 Pro Tips

### Early Game Strategy
1. Claim daily free egg immediately
2. Plant Mushrooms for quick gold
3. Save 500 gold for Regular Egg
4. Keep planting and harvesting
5. Feed dragons daily for XP

### Best Plants for Gold/Hour
1. **Mushroom** - 100 gold/hour (fastest)
2. **Sunflower** - 100 gold/hour
3. **Cherry Blossom** - 140 gold/hour
4. **Lotus** - 167 gold/hour (best for long sessions)

### Egg Purchase Guide
- **Daily Free** - Always claim! Free dragons
- **Regular (500g)** - Good value, save up for these
- **Rare (2000g)** - Better rarity chances
- **Premium (200💎)** - Use crystals here
- **Legendary (500💎)** - Save crystals for best odds

### Resource Management
- Always keep planting crops
- Harvest regularly
- Feed dragons daily
- Don't waste crystals on low-tier eggs
- Save gold for Rare+ eggs

---

## 🆘 Need Help?

### In-Game Help
Send `/help` to your bot for a complete game guide

### Documentation
- **README.md** - Full documentation
- **INDEX.md** - Complete file guide
- **API_REFERENCE.md** - Developer docs

### Testing
```bash
# Verify your setup
python setup.py

# Test game mechanics
python test_game.py
```

### Common Commands
- `/start` - Main menu
- `/help` - Game help
- `/profile` - Your stats

---

## 📱 Using the Bot

### Navigation
- Use inline buttons to navigate
- "« Back" always returns to previous menu
- Click "🔄 Check" to refresh status

### Daily Activities
1. Claim free egg (once per 24h)
2. Feed all dragons (once per 24h each)
3. Check for ready eggs to hatch
4. Plant new crops
5. Harvest ready plants

### Progression Loop
```
Claim Egg → Wait → Hatch → Get Dragon
     ↓                           ↓
Plant Crops → Grow → Harvest → Gold
                                 ↓
                            Buy More Eggs
```

---

## 🎉 You're Ready!

### Checklist
- ✅ Bot token obtained
- ✅ Dependencies installed
- ✅ .env file configured
- ✅ Bot running
- ✅ First `/start` command sent
- ✅ Free egg claimed
- ✅ First plant growing

### What's Next?
1. Wait for your first egg to hatch
2. Plant more crops to earn gold
3. Buy more eggs with gold
4. Build your dragon collection
5. Feed dragons to level them up
6. Explore all the features!

---

## 🐉 Welcome to Dragon Garden!

**Start Playing Now**: Send `/start` to your bot!

**Have Fun Collecting Dragons!** ✨

---

## 📞 Quick Reference

| Command | Purpose |
|---------|---------|
| `python bot.py` | Start the bot |
| `python setup.py` | Check environment |
| `python test_game.py` | Test mechanics |
| `/start` | Main menu |
| `/help` | Game help |
| `/profile` | Your profile |

| Menu | Purpose |
|------|---------|
| 🥚 My Eggs | View and hatch eggs |
| 🐉 My Dragons | View and feed dragons |
| 🌱 My Garden | Plant and harvest |
| 👤 Profile | View your stats |
| 🛒 Shop | Buy eggs and seeds |
| ❓ Help | Game guide |

---

**Happy Dragon Breeding!** 🐉🌸

_If you need more detailed information, see README.md_
