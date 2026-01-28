# 🚀 Quick Start Guide - Dragon Garden

Get your Dragon Garden bot up and running in 5 minutes!

## ⚡ Quick Setup

### 1. Get a Telegram Bot Token
1. Open Telegram, search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Install & Configure
```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your token
# TELEGRAM_BOT_TOKEN=your_token_here
```

### 3. Run the Bot
```bash
python bot.py
```

That's it! 🎉

## 🎮 First Steps in the Game

### For Players:
1. Start a chat with your bot
2. Send `/start`
3. Click "🥚 My Eggs"
4. Click "🎁 Claim Daily Free Egg"
5. Wait 48 hours (or change hatching time in config for testing)
6. Come back and hatch your dragon!

### Quick Commands:
- `/start` - Main menu
- `/help` - Game guide
- `/profile` - Your stats

## 🧪 Testing Mode

Want to test without waiting? Edit `config.py`:

```python
# Change these for faster testing:
DAILY_FREE_EGG_COOLDOWN = 60  # 1 minute instead of 24 hours
PLANT_GROWTH_TIME = 60        # 1 minute instead of 1 hour
```

And modify `utils/constants.py` for faster egg hatching:

```python
EGG_TYPES = {
    'Daily Free': {
        'hatching_hours': 0.1,  # 6 minutes instead of 48 hours
        # ...
    }
}
```

## 📊 Game Overview

### Resources You Start With:
- 💰 1,000 Gold
- 💎 50 Crystals

### What You Can Do:
1. **Eggs** 🥚
   - Claim free egg daily
   - Buy eggs with gold/crystals
   - Hatch to get dragons

2. **Dragons** 🐉
   - Feed once per 24h
   - Level up for better stats
   - Collect 60+ types

3. **Garden** 🌱
   - Plant crops (costs gold)
   - Harvest for profit
   - 8 plant types

4. **Shop** 🛒
   - Buy eggs
   - Buy plant seeds
   - (Premium features in Phase 3)

## 🎯 Pro Tips

### Early Game Strategy:
1. Claim your daily free egg immediately
2. Plant Mushrooms (fastest gold)
3. Save up 500 gold for Regular Egg
4. Feed dragons daily for XP
5. Harvest plants regularly

### Best Gold-Per-Hour Plants:
- **Mushroom**: 100g/hour profit
- **Sunflower**: 100g/hour profit
- **Cherry Blossom**: 200g/hour profit
- **Lotus**: 167g/hour profit (best for long sessions)

### Egg Strategy:
- **Daily Free**: Always claim (free dragons!)
- **Regular (500g)**: Good value, save up for these
- **Rare (2000g)**: Better rarity rates
- **Premium (200 crystals)**: Save crystals for these
- **Legendary (500 crystals)**: Best rarity rates

## 🐛 Common Issues

**Bot not responding?**
- Check token in `.env`
- Make sure bot is running
- Check console for errors

**Database error?**
- Delete `dragon_garden.db` to reset
- Run `python bot.py` again

**Import error?**
- Run: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.8+)

## 🎨 Customization

### Change Starting Resources
Edit `services/user_service.py`:
```python
user = User(
    telegram_id=telegram_user.id,
    username=telegram_user.username,
    first_name=telegram_user.first_name or 'Dragon Trainer',
    gold=10000,      # Give more gold
    crystals=500     # Give more crystals
)
```

### Add Your Own Dragon
Edit `utils/constants.py`:
```python
DRAGONS = {
    'Mythic': [
        # Add your custom dragon here:
        {'name': 'My Custom Dragon', 'emoji': '🔥', 
         'color': 'Rainbow', 'element': 'Custom', 
         'ability': 'Super Power'},
        # ...existing dragons...
    ]
}
```

## 📱 Using SQLite vs PostgreSQL

### SQLite (Default - Easy Setup):
```env
DATABASE_URL=sqlite:///dragon_garden.db
```
- Perfect for testing
- No setup required
- Single file database

### PostgreSQL (Production - Better Performance):
```env
DATABASE_URL=postgresql://username:password@localhost:5432/dragon_garden
```
- Better for multiple users
- More robust
- Requires PostgreSQL installation

## 🌟 Next Steps

Once you have the bot running:
1. Invite friends to play
2. Watch them collect dragons
3. Build your dragon collection
4. Customize the game to your liking
5. Wait for Phase 2-4 updates!

## 💡 Development Roadmap

- ✅ **Phase 1** (Current): Basic gameplay, dragons, eggs, garden
- 🔄 **Phase 2**: VIP system, Battlepass, more content
- 🔄 **Phase 3**: Payment integration, premium shop
- 🔄 **Phase 4**: Social features, events, leaderboards

---

**Happy Dragon Breeding! 🐉✨**

Need help? Check out the full [README.md](README.md) for detailed documentation.
