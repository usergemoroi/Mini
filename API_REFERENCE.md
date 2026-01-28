# 🔧 API Reference - Dragon Garden

Complete reference for all services, models, and utilities in Dragon Garden.

## 📚 Table of Contents
- [Database Models](#database-models)
- [Services](#services)
- [Utilities](#utilities)
- [Constants](#constants)

---

## 🗄️ Database Models

### User Model
Location: `database/models.py`

```python
class User(Base):
    id: int                    # Primary key
    telegram_id: int           # Telegram user ID (unique)
    username: str              # Telegram username
    first_name: str            # User's first name
    gold: int                  # Gold currency (default: 1000)
    crystals: int              # Crystal currency (default: 50)
    vip_level: str             # VIP tier (default: 'Free')
    last_daily_egg: DateTime   # Last free egg claim time
    created_at: DateTime       # Account creation time
    updated_at: DateTime       # Last update time
    
    # Relationships
    dragons: List[Dragon]      # User's dragons
    eggs: List[Egg]            # User's eggs
    plants: List[Plant]        # User's plants
    garden: Garden             # User's garden
```

### Dragon Model
```python
class Dragon(Base):
    id: int                    # Primary key
    user_id: int               # Owner's ID (FK)
    dragon_type: str           # Dragon species name
    name: str                  # Custom dragon name
    rarity: str                # Common/Rare/Epic/Legendary/Mythic
    level: int                 # Dragon level (default: 1)
    experience: int            # Current XP (default: 0)
    hunger: int                # Hunger level 0-100 (default: 100)
    happiness: int             # Happiness 0-100 (default: 100)
    strength: int              # Strength stat
    agility: int               # Agility stat
    intelligence: int          # Intelligence stat
    last_fed: DateTime         # Last feeding time
    hatched_at: DateTime       # When dragon hatched
    
    owner: User                # Relationship to owner
```

### Egg Model
```python
class Egg(Base):
    id: int                    # Primary key
    user_id: int               # Owner's ID (FK)
    egg_type: str              # Egg type name
    rarity: str                # Determined rarity
    hatching_time: int         # Hours to hatch
    started_hatching_at: DateTime  # When egg started
    hatches_at: DateTime       # When egg will be ready
    is_hatched: bool           # Hatched status (default: False)
    
    owner: User                # Relationship to owner
```

### Plant Model
```python
class Plant(Base):
    id: int                    # Primary key
    user_id: int               # Owner's ID (FK)
    plant_type: str            # Plant species name
    planted_at: DateTime       # When planted
    ready_at: DateTime         # When ready to harvest
    is_ready: bool             # Ready status (default: False)
    is_harvested: bool         # Harvested status (default: False)
    
    owner: User                # Relationship to owner
```

### Garden Model
```python
class Garden(Base):
    id: int                    # Primary key
    user_id: int               # Owner's ID (FK, unique)
    name: str                  # Garden name (default: 'My Dragon Garden')
    description: str           # Garden description
    decorations: str           # JSON string of decorations
    theme: str                 # Garden theme (default: 'Classic')
    created_at: DateTime       # Garden creation time
    
    owner: User                # Relationship to owner
```

---

## 🛠️ Services

### UserService
Location: `services/user_service.py`

#### `get_or_create_user(session, telegram_user)`
Get existing user or create new one.
- **Parameters:**
  - `session`: SQLAlchemy session
  - `telegram_user`: Telegram User object
- **Returns:** User model instance
- **Creates:** User + Garden if new

#### `add_gold(session, user, amount)`
Add gold to user's account.
- **Parameters:**
  - `session`: SQLAlchemy session
  - `user`: User instance
  - `amount`: Gold amount (int)
- **Returns:** Updated user

#### `remove_gold(session, user, amount)`
Remove gold from user's account.
- **Parameters:**
  - `session`: SQLAlchemy session
  - `user`: User instance
  - `amount`: Gold amount (int)
- **Returns:** True if successful, False if insufficient funds

#### `add_crystals(session, user, amount)`
Add crystals to user's account.
- **Parameters:** Same as add_gold
- **Returns:** Updated user

#### `remove_crystals(session, user, amount)`
Remove crystals from user's account.
- **Parameters:** Same as remove_gold
- **Returns:** True if successful, False if insufficient

#### `update_daily_egg_time(session, user)`
Update last daily egg claim time to now.
- **Returns:** Updated user

---

### DragonService
Location: `services/dragon_service.py`

#### `create_dragon(session, user, rarity, custom_name=None)`
Create a new dragon for user.
- **Parameters:**
  - `session`: SQLAlchemy session
  - `user`: User instance
  - `rarity`: Rarity tier string
  - `custom_name`: Optional custom name
- **Returns:** Dragon instance
- **Logic:** Randomly selects dragon of given rarity, assigns base stats

#### `feed_dragon(session, dragon)`
Feed a dragon (24h cooldown).
- **Parameters:**
  - `session`: SQLAlchemy session
  - `dragon`: Dragon instance
- **Returns:** Tuple (success: bool, result: str/float)
  - Success: (True, "fed") or (True, "level_up")
  - Failure: (False, hours_remaining: float)
- **Effects:**
  - Hunger +50 (max 100)
  - Happiness +20 (max 100)
  - Experience +10
  - May level up (100 XP per level)

#### `get_user_dragons(session, user)`
Get all dragons owned by user.
- **Returns:** List[Dragon]

#### `get_dragon_by_id(session, dragon_id, user_id)`
Get specific dragon by ID (with ownership check).
- **Returns:** Dragon or None

#### `rename_dragon(session, dragon, new_name)`
Change dragon's name.
- **Returns:** Updated dragon

#### `decrease_dragon_hunger(session)`
Decrease hunger for all dragons (scheduled task).
- **Effects:** -10 hunger, -5 happiness for all dragons

---

### EggService
Location: `services/egg_service.py`

#### `create_egg(session, user, egg_type)`
Create new egg for user.
- **Parameters:**
  - `session`: SQLAlchemy session
  - `user`: User instance
  - `egg_type`: Egg type name
- **Returns:** Egg instance
- **Logic:**
  - Determines rarity based on egg type probabilities
  - Sets hatching timer
  - Creates egg record

#### `get_user_eggs(session, user, include_hatched=False)`
Get user's eggs.
- **Parameters:**
  - `include_hatched`: Include already hatched eggs
- **Returns:** List[Egg]

#### `get_egg_by_id(session, egg_id, user_id)`
Get specific egg by ID (with ownership check).
- **Returns:** Egg or None

#### `check_ready_eggs(session, user)`
Check for eggs ready to hatch.
- **Returns:** List[Egg] (ready eggs)
- **Effects:** Sets is_ready=True for ready eggs

#### `hatch_egg(session, egg)`
Mark egg as hatched.
- **Returns:** Egg instance or None
- **Effects:** Sets is_hatched=True

#### `can_purchase_egg(user, egg_type)`
Check if user can afford egg.
- **Returns:** Tuple (can_purchase: bool, message: str)

---

### GardenService
Location: `services/garden_service.py`

#### `plant_crop(session, user, plant_type)`
Plant a crop in garden.
- **Parameters:**
  - `session`: SQLAlchemy session
  - `user`: User instance
  - `plant_type`: Plant name
- **Returns:** Tuple (plant: Plant/None, message: str)
- **Effects:**
  - Deducts gold cost
  - Creates plant with growth timer
  - Returns error if insufficient gold

#### `get_user_plants(session, user, include_harvested=False)`
Get user's plants.
- **Returns:** List[Plant]

#### `get_plant_by_id(session, plant_id, user_id)`
Get specific plant by ID.
- **Returns:** Plant or None

#### `check_ready_plants(session, user)`
Check for plants ready to harvest.
- **Returns:** List[Plant] (ready plants)
- **Effects:** Sets is_ready=True for mature plants

#### `harvest_plant(session, user, plant)`
Harvest a plant for gold.
- **Returns:** Gold reward amount or None
- **Effects:**
  - Adds gold reward to user
  - Marks plant as harvested

#### `get_user_garden(session, user)`
Get user's garden.
- **Returns:** Garden instance

#### `update_garden(session, garden, name=None, description=None, theme=None)`
Update garden properties.
- **Returns:** Updated garden

---

## 🔧 Utilities

### Helpers
Location: `utils/helpers.py`

#### `format_time_remaining(target_time)`
Format datetime as human-readable countdown.
- **Parameters:** target_time (DateTime)
- **Returns:** String like "2d 5h 30m" or "Ready!"

#### `calculate_hatching_time(egg_type)`
Get hatching hours for egg type.
- **Returns:** int (hours)

#### `determine_egg_rarity(egg_type)`
Randomly determine rarity based on egg type.
- **Parameters:** egg_type (str)
- **Returns:** Rarity string
- **Logic:** Uses probability distribution from EGG_TYPES

#### `get_random_dragon(rarity)`
Get random dragon of given rarity.
- **Parameters:** rarity (str)
- **Returns:** Dragon data dict

#### `format_dragon_stats(dragon)`
Format dragon stats as display string.
- **Parameters:** dragon (Dragon instance)
- **Returns:** Formatted string with emoji

#### `format_user_profile(user)`
Format user profile as display string.
- **Parameters:** user (User instance)
- **Returns:** Formatted profile string

#### `can_claim_daily_egg(user)`
Check if user can claim daily free egg.
- **Parameters:** user (User instance)
- **Returns:** bool (True if 24h+ since last claim)

#### `format_gold(amount)`
Format gold with emoji.
- **Returns:** "💰 1,234"

#### `format_crystals(amount)`
Format crystals with emoji.
- **Returns:** "💎 1,234"

---

## 📊 Constants

### RARITIES
Location: `utils/constants.py`

```python
RARITIES = {
    'Common': {
        'emoji': '⚪️',
        'chance': 50,      # Base chance percentage
        'base_stats': 10   # Starting stats
    },
    'Rare': {
        'emoji': '🔵',
        'chance': 30,
        'base_stats': 15
    },
    'Epic': {
        'emoji': '🟣',
        'chance': 15,
        'base_stats': 25
    },
    'Legendary': {
        'emoji': '🟡',
        'chance': 4,
        'base_stats': 40
    },
    'Mythic': {
        'emoji': '🔴',
        'chance': 1,
        'base_stats': 60
    }
}
```

### DRAGONS
Dictionary mapping rarity → List of dragon data:

```python
DRAGONS = {
    'Common': [
        {
            'name': 'Spark Dragon',
            'emoji': '⚡',
            'color': 'Yellow',
            'element': 'Electric',
            'ability': 'Lightning Strike'
        },
        # ... 11 more Common dragons
    ],
    'Rare': [...],     # 12 dragons
    'Epic': [...],     # 12 dragons
    'Legendary': [...], # 12 dragons
    'Mythic': [...]    # 12 dragons
}
```
**Total: 60 unique dragons**

### EGG_TYPES
```python
EGG_TYPES = {
    'Daily Free': {
        'cost_gold': 0,
        'cost_crystals': 0,
        'hatching_hours': 48,
        'emoji': '🥚',
        'rarities': {
            'Common': 70,
            'Rare': 25,
            'Epic': 5,
            'Legendary': 0,
            'Mythic': 0
        }
    },
    # ... more egg types
}
```

**Available Types:**
- Daily Free (0 gold, 48h)
- Regular (500 gold, 48h)
- Rare (2000 gold, 72h)
- Premium (200 crystals, 96h)
- Legendary (500 crystals, 168h)

### PLANTS
```python
PLANTS = {
    'Sunflower': {
        'emoji': '🌻',
        'growth_hours': 1,
        'cost_gold': 50,
        'reward_gold': 150,
        'description': 'A bright magical sunflower'
    },
    # ... more plants
}
```

**Available Plants:**
- Mushroom (0.5h, 30g → 80g)
- Sunflower (1h, 50g → 150g)
- Tulip (1.5h, 75g → 225g)
- Rose (2h, 100g → 350g)
- Hibiscus (2h, 100g → 320g)
- Lavender (1.5h, 80g → 250g)
- Cherry Blossom (2.5h, 150g → 500g)
- Lotus (3h, 200g → 700g)

### DECORATIONS
```python
DECORATIONS = [
    {'name': 'Dragon Statue', 'emoji': '🗿', 'cost_gold': 1000},
    # ... more decorations
]
```

**10 decoration types** (for future Phase 2)

---

## 🎮 Handler Patterns

### Standard Handler Structure
```python
async def handler_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge callback
    
    # Database operations
    with get_session() as session:
        user = UserService.get_or_create_user(session, update.effective_user)
        # ... business logic ...
    
    # Build UI
    keyboard = [
        [InlineKeyboardButton("Text", callback_data="action")],
        [InlineKeyboardButton("« Back", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send response
    await query.edit_message_text(
        text="Message",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
```

### Callback Data Patterns
- `menu_name` - Navigate to menu
- `action_name` - Perform action
- `action_name_id` - Action with ID (e.g., "view_dragon_123")

---

## 🔐 Session Management

### Database Session Pattern
```python
from database import get_session

# Context manager (auto-commit/rollback)
with get_session() as session:
    user = UserService.get_or_create_user(session, telegram_user)
    # Changes auto-committed on success
    # Auto-rollback on exception
```

### Service Pattern
```python
class MyService:
    @staticmethod
    def my_method(session: Session, param1, param2):
        # Perform operations
        result = do_something()
        
        # Flush to save changes (don't commit)
        session.flush()
        
        return result
```

---

## 📝 Usage Examples

### Creating a Dragon
```python
with get_session() as session:
    user = UserService.get_or_create_user(session, telegram_user)
    dragon = DragonService.create_dragon(session, user, 'Epic')
    print(f"Created: {dragon.name} (Level {dragon.level})")
```

### Planting and Harvesting
```python
with get_session() as session:
    user = UserService.get_or_create_user(session, telegram_user)
    
    # Plant
    plant, msg = GardenService.plant_crop(session, user, 'Rose')
    if plant:
        print(f"Planted {plant.plant_type}")
    
    # Later... check if ready
    ready_plants = GardenService.check_ready_plants(session, user)
    
    # Harvest
    for plant in ready_plants:
        reward = GardenService.harvest_plant(session, user, plant)
        print(f"Harvested! Earned {reward} gold")
```

### Egg Lifecycle
```python
with get_session() as session:
    user = UserService.get_or_create_user(session, telegram_user)
    
    # Create egg
    egg = EggService.create_egg(session, user, 'Premium')
    print(f"Egg will hatch in {egg.hatching_time} hours")
    
    # Later... check ready
    ready_eggs = EggService.check_ready_eggs(session, user)
    
    # Hatch
    for egg in ready_eggs:
        EggService.hatch_egg(session, egg)
        dragon = DragonService.create_dragon(session, user, egg.rarity)
        print(f"Hatched {dragon.name}!")
```

---

## 🚀 Extension Points

### Adding New Services
1. Create file in `services/`
2. Define service class with @staticmethod methods
3. Add to `services/__init__.py`
4. Import in handlers

### Adding New Handlers
1. Create handler functions in `handlers/`
2. Create registration function
3. Add to `handlers/__init__.py`
4. Call registration in `bot.py`

### Adding New Models
1. Define model in `database/models.py`
2. Add relationships
3. Recreate database or use migrations

---

**For more examples, see CONTRIBUTING.md**
