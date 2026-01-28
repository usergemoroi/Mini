# 🤝 Contributing to Dragon Garden

Thank you for your interest in contributing to Dragon Garden! This guide will help you add new features, dragons, and content to the game.

## 📋 Table of Contents
- [Adding New Dragons](#adding-new-dragons)
- [Adding New Plants](#adding-new-plants)
- [Adding New Egg Types](#adding-new-egg-types)
- [Creating New Handlers](#creating-new-handlers)
- [Database Changes](#database-changes)
- [Testing](#testing)

## 🐉 Adding New Dragons

### Step 1: Edit `utils/constants.py`

Add your dragon to the appropriate rarity tier in the `DRAGONS` dictionary:

```python
DRAGONS = {
    'Epic': [
        # Add your new dragon here
        {
            'name': 'Thunder Phoenix Dragon',
            'emoji': '⚡',
            'color': 'Electric Blue',
            'element': 'Thunder',
            'ability': 'Lightning Storm'
        },
        # ... existing dragons ...
    ]
}
```

### Dragon Template:
```python
{
    'name': 'Dragon Name',        # Unique name for the dragon
    'emoji': '🐉',                # Visual emoji representation
    'color': 'Color Description', # Color/appearance description
    'element': 'Element Type',    # Fire, Water, Electric, etc.
    'ability': 'Ability Name'     # Special ability name
}
```

### Tips for Dragon Design:
- **Common**: Basic elements (Fire, Water, Earth, Air)
- **Rare**: Advanced elements (Ice, Thunder, Forest)
- **Epic**: Unique elements (Shadow, Light, Plasma)
- **Legendary**: Powerful elements (Celestial, Void, Solar)
- **Mythic**: Cosmic/Ultimate elements (Origin, Chaos, Infinity)

## 🌱 Adding New Plants

### Edit `utils/constants.py`

Add to the `PLANTS` dictionary:

```python
PLANTS = {
    'Orchid': {
        'emoji': '🌺',
        'growth_hours': 4,      # How long to grow
        'cost_gold': 300,       # Purchase cost
        'reward_gold': 1000,    # Harvest reward
        'description': 'Rare orchid flowers'
    },
    # ... existing plants ...
}
```

### Plant Economics Guide:
- **Profit Margin**: Reward should be 2-3x the cost
- **Time Balance**: Longer growth = higher profit per investment
- **Gold/Hour**: Calculate: (reward - cost) / growth_hours

### Example Plant Economics:
| Time | Cost | Reward | Profit | Gold/Hour |
|------|------|--------|--------|-----------|
| 0.5h | 30   | 80     | 50     | 100/h     |
| 1h   | 50   | 150    | 100    | 100/h     |
| 2h   | 100  | 350    | 250    | 125/h     |
| 4h   | 300  | 1000   | 700    | 175/h     |

## 🥚 Adding New Egg Types

### Edit `utils/constants.py`

Add to the `EGG_TYPES` dictionary:

```python
EGG_TYPES = {
    'Mystic': {
        'cost_gold': 0,
        'cost_crystals': 1000,
        'hatching_hours': 336,  # 14 days
        'emoji': '🌟',
        'rarities': {
            'Common': 0,
            'Rare': 0,
            'Epic': 20,
            'Legendary': 50,
            'Mythic': 30
        }
    },
    # ... existing egg types ...
}
```

### Egg Design Guidelines:
- **Free/Low Cost**: Higher Common/Rare rates
- **Medium Cost**: Balanced distribution
- **High Cost**: Favor Legendary/Mythic
- **Hatching Time**: Balance gameplay (2-7 days typical)
- **Total Rarity %**: Must add up to 100%

## 🎮 Creating New Handlers

### Example: Adding a Battle System

1. **Create Handler File**: `handlers/battle.py`

```python
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database import get_session
from services import UserService, DragonService

async def battle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        dragons = DragonService.get_user_dragons(session, user)
        
        text = "⚔️ **Battle Arena**\n\nSelect your dragon to battle!"
        
        keyboard = [
            [InlineKeyboardButton("« Back", callback_data="start_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def register_battle_handlers(application):
    application.add_handler(CallbackQueryHandler(battle_menu, pattern="^battle_menu$"))
```

2. **Register in `bot.py`**:

```python
from handlers import register_battle_handlers

# In main():
register_battle_handlers(application)
```

3. **Add to Main Menu** (`handlers/start.py`):

```python
keyboard = [
    # ... existing buttons ...
    [InlineKeyboardButton("⚔️ Battle", callback_data="battle_menu")],
]
```

## 🗄️ Database Changes

### Adding New Tables

1. **Define Model** in `database/models.py`:

```python
class Battle(Base):
    __tablename__ = 'battles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    opponent_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    dragon_id = Column(Integer, ForeignKey('dragons.id'), nullable=False)
    result = Column(String(50))  # 'win', 'lose', 'draw'
    reward_gold = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User')
    dragon = relationship('Dragon')
```

2. **Create Service** in `services/battle_service.py`:

```python
from database.models import Battle
from sqlalchemy.orm import Session

class BattleService:
    @staticmethod
    def create_battle(session: Session, user, dragon, opponent=None):
        battle = Battle(
            user_id=user.id,
            dragon_id=dragon.id,
            opponent_id=opponent.id if opponent else None
        )
        session.add(battle)
        session.flush()
        return battle
```

3. **Update Database**:
   - Delete `dragon_garden.db` (for testing)
   - Or use Alembic for migrations (production)

### Adding Fields to Existing Tables

1. **Edit Model** in `database/models.py`:

```python
class Dragon(Base):
    # ... existing fields ...
    battle_wins = Column(Integer, default=0)  # New field
    battle_losses = Column(Integer, default=0)  # New field
```

2. **Recreate Database** (testing):
```bash
rm dragon_garden.db
python bot.py
```

## 🧪 Testing

### Manual Testing

1. **Run Test Script**:
```bash
python test_game.py
```

2. **Test in Telegram**:
   - Start bot: `python bot.py`
   - Chat with bot on Telegram
   - Try all features

### Testing New Features

Create test functions in `test_game.py`:

```python
def test_my_new_feature():
    print("\nTesting my new feature...")
    try:
        # Your test code here
        from services import MyNewService
        
        result = MyNewService.do_something()
        print(f"✅ Feature works: {result}")
        return True
    except Exception as e:
        print(f"❌ Feature error: {e}")
        return False
```

## 📝 Code Style Guidelines

### General Rules
- Use descriptive variable names
- Add comments for complex logic
- Follow existing code patterns
- Use emoji for visual appeal in messages
- Keep functions focused and small

### Service Layer
```python
class MyService:
    @staticmethod
    def method_name(session: Session, param1, param2):
        # Business logic here
        session.flush()  # Save changes
        return result
```

### Handler Functions
```python
async def handler_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    with get_session() as session:
        # Database operations
        pass
    
    keyboard = [[InlineKeyboardButton("Text", callback_data="action")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Message",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
```

## 🎨 UI/UX Guidelines

### Message Formatting
```python
text = (
    "🎮 **Title in Bold**\n\n"
    "Regular text here\n"
    f"Dynamic value: {value}\n\n"
    "📊 **Section Header:**\n"
    "• List item 1\n"
    "• List item 2\n"
)
```

### Keyboard Layout
```python
keyboard = [
    # Primary actions (top)
    [InlineKeyboardButton("🎯 Main Action", callback_data="action")],
    
    # Secondary actions (middle)
    [
        InlineKeyboardButton("📊 Stats", callback_data="stats"),
        InlineKeyboardButton("⚙️ Settings", callback_data="settings")
    ],
    
    # Navigation (bottom)
    [InlineKeyboardButton("« Back", callback_data="back")]
]
```

### Emoji Usage
- Use emoji consistently across similar features
- Common emoji meanings:
  - ✅ Success, ❌ Error, ⚠️ Warning
  - 🎉 Celebration, 💰 Gold, 💎 Crystals
  - ⏰ Time/Waiting, 🔄 Refresh, 🎯 Action
  - 🐉 Dragons, 🥚 Eggs, 🌱 Plants

## 🚀 Feature Ideas for Future Phases

### Phase 2 Ideas:
- VIP subscription system
- Battlepass with seasons
- More plant varieties
- Garden decorations placement
- Dragon training mini-games

### Phase 3 Ideas:
- Payment integration (Stripe/Telegram Stars)
- Premium dragon skins
- Garden themes and templates
- Dragon breeding combinations
- Achievement system

### Phase 4 Ideas:
- PvP battles
- Guild system
- Garden sharing gallery
- Dragon trading/gifting
- Monthly events with exclusive dragons
- Leaderboards

## 📞 Getting Help

If you need help:
1. Check the README.md for documentation
2. Look at existing code for patterns
3. Test your changes with `test_game.py`
4. Start with small changes first

## 🎓 Learning Resources

- [python-telegram-bot docs](https://docs.python-telegram-bot.org/)
- [SQLAlchemy docs](https://docs.sqlalchemy.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**Happy Contributing! 🐉✨**
