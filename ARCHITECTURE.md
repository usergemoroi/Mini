# 🏗️ Architecture - Dragon Garden

Visual architecture and data flow documentation for Dragon Garden bot.

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         TELEGRAM BOT                             │
│                         (bot.py)                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │         python-telegram-bot Application                     │ │
│  │  - Polling for updates                                      │ │
│  │  - Handler registration                                     │ │
│  │  - Inline keyboard management                               │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         HANDLERS                                 │
│                      (handlers/*.py)                             │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐  │
│  │  start   │  dragon  │   egg    │  garden  │   profile    │  │
│  │  .py     │   .py    │   .py    │   .py    │    .py       │  │
│  │          │          │          │          │              │  │
│  │ /start   │ View     │ Claim    │ Plant    │ View         │  │
│  │ /help    │ Feed     │ Hatch    │ Harvest  │ Shop         │  │
│  │ Menu     │ List     │ Buy      │ Check    │ Stats        │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER                                 │
│                   (services/*.py)                                │
│  ┌──────────┬──────────────┬─────────────┬──────────────────┐  │
│  │  User    │   Dragon     │    Egg      │    Garden        │  │
│  │ Service  │   Service    │  Service    │   Service        │  │
│  │          │              │             │                  │  │
│  │ • Create │ • Create     │ • Create    │ • Plant crop     │  │
│  │ • Gold   │ • Feed       │ • Hatch     │ • Harvest        │  │
│  │ • Crystal│ • Level up   │ • Check     │ • Check ready    │  │
│  │ • Daily  │ • Stats      │ • Buy       │ • Update         │  │
│  └──────────┴──────────────┴─────────────┴──────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                                │
│                   (database/*.py)                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  SQLAlchemy ORM                             │ │
│  │                                                             │ │
│  │  Models:                                                    │ │
│  │  ┌──────┬────────┬──────┬───────┬────────┐               │ │
│  │  │ User │ Dragon │ Egg  │ Plant │ Garden │               │ │
│  │  └──────┴────────┴──────┴───────┴────────┘               │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE                                      │
│                                                                  │
│        PostgreSQL / SQLite                                       │
│                                                                  │
│  Tables:                                                         │
│  • users       - User accounts                                   │
│  • dragons     - Dragon collection                               │
│  • eggs        - Hatching eggs                                   │
│  • plants      - Growing plants                                  │
│  • gardens     - Garden customization                            │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### User Registration Flow
```
User sends /start
       ↓
start.py → start_command()
       ↓
UserService.get_or_create_user()
       ↓
Check if user exists in DB
       ↓
   ┌──NO──────────────YES─┐
   ↓                      ↓
Create User          Load User
Create Garden        Load Data
Save to DB              ↓
   ↓                      ↓
   └───────┬──────────────┘
           ↓
   Return welcome message
           ↓
   Display main menu
```

### Egg Hatching Flow
```
User clicks "🥚 My Eggs"
       ↓
egg.py → eggs_menu()
       ↓
EggService.get_user_eggs()
       ↓
Display eggs with timers
       ↓
User clicks "🔄 Check Eggs"
       ↓
EggService.check_ready_eggs()
       ↓
Filter eggs where hatches_at <= now
       ↓
Mark ready eggs: is_ready = True
       ↓
Display ready eggs
       ↓
User clicks "🐣 Hatch Egg"
       ↓
EggService.hatch_egg()
       ↓
Mark egg: is_hatched = True
       ↓
DragonService.create_dragon()
       ↓
Random dragon from egg's rarity
       ↓
Save dragon to DB
       ↓
Display congratulations + dragon stats
```

### Dragon Feeding Flow
```
User clicks "🐉 My Dragons"
       ↓
dragon.py → dragons_menu()
       ↓
DragonService.get_user_dragons()
       ↓
Display dragon list
       ↓
User selects dragon
       ↓
dragon.py → view_dragon()
       ↓
Display dragon stats
       ↓
User clicks "🍖 Feed Dragon"
       ↓
dragon.py → feed_dragon()
       ↓
DragonService.feed_dragon()
       ↓
Check if 24h passed since last_fed
       ↓
   ┌──NO───────────YES─┐
   ↓                   ↓
Return error    Update stats:
& hours         • hunger +50
remaining       • happiness +20
   ↓            • experience +10
   ↓                   ↓
Display         Check if level up
cooldown        (XP >= level * 100)
message              ↓
                ┌──NO───YES─┐
                ↓           ↓
           Return      Level up
           "fed"       Stats +5 each
                ↓           ↓
                └─────┬─────┘
                      ↓
              Display success
              (with level up if applicable)
```

### Plant Lifecycle Flow
```
User clicks "🌱 My Garden"
       ↓
garden.py → garden_menu()
       ↓
Display garden & active plants
       ↓
User clicks "🌱 Plant Crops"
       ↓
garden.py → plant_menu()
       ↓
Display available plants
       ↓
User selects plant
       ↓
garden.py → plant_crop()
       ↓
GardenService.plant_crop()
       ↓
Check if user has enough gold
       ↓
   ┌──NO───────────YES─┐
   ↓                   ↓
Return error    Deduct gold
message         Create plant:
   ↓            • planted_at = now
Display         • ready_at = now + growth_time
error                 ↓
                 Save to DB
                      ↓
              Display success
                      ↓
         ⏰ Wait for growth time
                      ↓
    User clicks "🔄 Check Plants"
                      ↓
    GardenService.check_ready_plants()
                      ↓
         Filter plants where ready_at <= now
                      ↓
         Mark ready: is_ready = True
                      ↓
         User clicks "🌾 Harvest All"
                      ↓
         garden.py → harvest_all()
                      ↓
    For each ready plant:
         GardenService.harvest_plant()
                      ↓
         • Add reward gold to user
         • Mark plant: is_harvested = True
                      ↓
         Display total gold earned
```

## 🗃️ Database Schema

### Entity Relationship Diagram
```
┌─────────────────────┐
│       User          │
│─────────────────────│
│ id (PK)             │
│ telegram_id (UNIQUE)│
│ username            │
│ first_name          │
│ gold                │
│ crystals            │
│ vip_level           │
│ last_daily_egg      │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N (has many)
           ├───────────────────────────┐
           │                           │
           ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐
│      Dragon         │    │        Egg          │
│─────────────────────│    │─────────────────────│
│ id (PK)             │    │ id (PK)             │
│ user_id (FK)        │    │ user_id (FK)        │
│ dragon_type         │    │ egg_type            │
│ name                │    │ rarity              │
│ rarity              │    │ hatching_time       │
│ level               │    │ started_hatching_at │
│ experience          │    │ hatches_at          │
│ hunger              │    │ is_hatched          │
│ happiness           │    └─────────────────────┘
│ strength            │
│ agility             │              │
│ intelligence        │              │ 1:N
│ last_fed            │              │
│ hatched_at          │              ▼
└─────────────────────┘    ┌─────────────────────┐
           │               │       Plant         │
           │ 1:N           │─────────────────────│
           │               │ id (PK)             │
           ▼               │ user_id (FK)        │
┌─────────────────────┐    │ plant_type          │
│      Garden         │    │ planted_at          │
│─────────────────────│    │ ready_at            │
│ id (PK)             │    │ is_ready            │
│ user_id (FK) UNIQUE │    │ is_harvested        │
│ name                │    └─────────────────────┘
│ description         │
│ decorations         │
│ theme               │
│ created_at          │
└─────────────────────┘

Legend:
PK = Primary Key
FK = Foreign Key
1:N = One-to-Many relationship
```

## 🎯 Handler Organization

### Command Structure
```
/start
   └── Main Menu
       ├── 🥚 My Eggs
       │   ├── 🎁 Claim Daily Free Egg
       │   ├── 🛒 Buy Eggs
       │   │   ├── Buy Regular Egg
       │   │   ├── Buy Rare Egg
       │   │   └── Buy Premium Egg
       │   └── 🔄 Check Eggs
       │       └── 🐣 Hatch Egg (if ready)
       │
       ├── 🐉 My Dragons
       │   ├── [Dragon 1]
       │   │   └── 🍖 Feed Dragon
       │   ├── [Dragon 2]
       │   │   └── 🍖 Feed Dragon
       │   └── 📋 View All Dragons
       │
       ├── 🌱 My Garden
       │   ├── 🌱 Plant Crops
       │   │   ├── Plant Sunflower
       │   │   ├── Plant Rose
       │   │   ├── Plant Tulip
       │   │   └── ... (8 plants)
       │   ├── 🌾 Harvest Ready Plants
       │   │   └── 🌾 Harvest All
       │   └── 🔄 Check Plants
       │
       ├── 👤 Profile
       │   ├── View Stats
       │   ├── 🐉 My Dragons
       │   ├── 🥚 My Eggs
       │   └── 🌱 My Garden
       │
       ├── 🛒 Shop
       │   ├── 🥚 Buy Eggs
       │   ├── 🌱 Buy Seeds
       │   └── 💎 Get Crystals
       │
       └── ❓ Help
           └── Game Guide

/help
   └── Help Guide

/profile
   └── User Profile
```

## 🔌 Service Layer Pattern

### Service Architecture
```
┌─────────────────────────────────────────────┐
│           Handler (Presentation)            │
│  • Receives user input                      │
│  • Formats output messages                  │
│  • Manages inline keyboards                 │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│         Service (Business Logic)            │
│  • Validates input                          │
│  • Applies game rules                       │
│  • Performs calculations                    │
│  • Coordinates multiple models              │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│           Model (Data Access)               │
│  • Represents database tables               │
│  • Handles relationships                    │
│  • Enforces constraints                     │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│          Database (Storage)                 │
│  • Persists data                            │
│  • Manages transactions                     │
│  • Ensures data integrity                   │
└─────────────────────────────────────────────┘
```

## 📦 Module Dependencies

```
bot.py
  ├── config.py
  ├── database/
  │   ├── __init__.py
  │   ├── db.py
  │   └── models.py
  ├── handlers/
  │   ├── __init__.py
  │   ├── start.py
  │   │   └── services.UserService
  │   ├── dragon.py
  │   │   ├── services.UserService
  │   │   └── services.DragonService
  │   ├── egg.py
  │   │   ├── services.UserService
  │   │   ├── services.EggService
  │   │   └── services.DragonService
  │   ├── garden.py
  │   │   ├── services.UserService
  │   │   └── services.GardenService
  │   └── profile.py
  │       └── services.UserService
  ├── services/
  │   ├── __init__.py
  │   ├── user_service.py
  │   │   └── database.models.User
  │   ├── dragon_service.py
  │   │   ├── database.models.Dragon
  │   │   └── utils.helpers
  │   ├── egg_service.py
  │   │   ├── database.models.Egg
  │   │   └── utils.helpers
  │   └── garden_service.py
  │       ├── database.models.Plant
  │       └── utils.constants
  └── utils/
      ├── __init__.py
      ├── constants.py
      └── helpers.py
```

## 🔐 Session Management

### Database Session Lifecycle
```
Request from Telegram
       ↓
Handler Function Called
       ↓
with get_session() as session:
       ↓
Session Created
       ↓
Service Methods Called
       ↓
  ┌───────────────┐
  │ Success Path  │  Failure Path
  ↓               ↓
Commit         Rollback
Changes        Changes
  ↓               ↓
  └───────┬───────┘
          ↓
Close Session
       ↓
Return Response
       ↓
Send to Telegram
```

## 🎨 UI Flow

### Main Menu Navigation
```
                    Main Menu
                        │
        ┌───────┬───────┼───────┬───────┐
        ▼       ▼       ▼       ▼       ▼
      Eggs   Dragons  Garden Profile  Shop
        │       │       │       │       │
        ▼       ▼       ▼       ▼       ▼
    [Actions][View]  [Plant] [Stats] [Buy]
        │       │       │       │       │
        └───────┴───────┴───────┴───────┘
                        │
                   « Back » (always returns to Main Menu)
```

## 🚀 Deployment Architecture

### Development Environment
```
Local Machine
    ├── Python 3.8+
    ├── SQLite Database
    ├── Bot runs via polling
    └── Direct console logs
```

### Production Environment (VPS)
```
Cloud Server (Ubuntu)
    ├── systemd service
    ├── PostgreSQL Database
    ├── Bot runs as daemon
    ├── journalctl logs
    ├── Nginx (optional, for webhooks)
    └── SSL certificates (optional)
```

### Docker Deployment
```
Docker Compose
    ├── Bot Container
    │   ├── Python application
    │   ├── Dependencies
    │   └── Environment variables
    └── PostgreSQL Container
        ├── Database
        ├── Persistent volume
        └── Network bridge
```

## 🔄 Future Architecture (Phases 2-4)

### Phase 2: Scheduled Tasks
```
Current: Manual checks
Future: APScheduler
    ├── Daily dragon hunger decrease
    ├── Daily reset tasks
    ├── Plant maturity checks
    ├── Egg hatching notifications
    └── VIP subscription renewals
```

### Phase 3: Payment Integration
```
Bot
 ↓
Payment Service
 ├── Stripe API
 │   └── Credit card processing
 └── Telegram Stars
     └── Telegram Payments
          ↓
      Webhook handlers
          ↓
      Update user balance
```

### Phase 4: Social Features
```
Bot
 ↓
Social Service
 ├── Gallery System
 │   ├── Garden snapshots
 │   └── Public profiles
 ├── Leaderboards
 │   ├── Top collections
 │   └── Garden rankings
 ├── Trading System
 │   ├── Dragon trading
 │   └── Gift system
 └── Guild System
     ├── Guild chat
     └── Cooperative features
```

---

## 📊 Performance Considerations

### Database Optimization
- **Indexes**: telegram_id (unique), user_id (foreign keys)
- **Connection Pooling**: Multiple concurrent users
- **Query Optimization**: Selective loading with filters

### Bot Performance
- **Non-blocking**: Async/await pattern
- **Rate Limiting**: Respect Telegram limits
- **Error Handling**: Graceful degradation

### Scalability
- **Horizontal**: Multiple bot instances (Phase 3+)
- **Vertical**: Resource optimization
- **Caching**: Redis for session data (Phase 3+)

---

**Architecture Overview Complete** 🏗️

For implementation details, see:
- **API_REFERENCE.md** - Service and model details
- **CONTRIBUTING.md** - Extension patterns
- **DEPLOYMENT.md** - Production setup
