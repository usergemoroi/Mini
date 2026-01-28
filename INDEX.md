# 📚 Dragon Garden - Complete File Index

Quick reference to all files in the project and their purposes.

## 📖 Documentation Files (Read First!)

### Getting Started
- **README.md** - Complete project documentation, features, and usage guide
- **QUICKSTART.md** - Fast 5-minute setup guide for new users
- **PROJECT_SUMMARY.md** - High-level overview of the entire project

### Development
- **API_REFERENCE.md** - Complete API documentation for all services and models
- **CONTRIBUTING.md** - Guidelines for adding content and features
- **ARCHITECTURE.md** - System architecture, data flow, and design patterns
- **DEPLOYMENT.md** - Production deployment guide for various platforms

### Legal
- **LICENSE** - MIT License for the project

---

## 🐍 Core Application Files

### Main Entry Point
- **bot.py** - Main bot application, initializes and runs the Telegram bot
  - Initializes database
  - Registers all handlers
  - Starts polling for updates
  - Entry point: `python bot.py`

### Configuration
- **config.py** - Application configuration settings
  - Loads environment variables
  - Database connection string
  - Bot token and settings
  - Cooldown timers

### Dependencies
- **requirements.txt** - Python package dependencies
  - python-telegram-bot==20.7
  - sqlalchemy==2.0.23
  - psycopg2-binary==2.9.9
  - python-dotenv==1.0.0
  - APScheduler==3.10.4
  - alembic==1.13.1

### Environment
- **.env.example** - Template for environment variables
  - TELEGRAM_BOT_TOKEN
  - DATABASE_URL
  - BOT_USERNAME
  - ADMIN_USER_IDS

### Git Configuration
- **.gitignore** - Files and directories to exclude from git
  - Python cache files
  - Virtual environments
  - Database files
  - Environment files

---

## 🗄️ Database Layer (`database/`)

### Package
- **database/__init__.py** - Package initialization and exports
  - Exports: init_db, get_session, all models

### Core Database
- **database/db.py** - Database connection and session management
  - SQLAlchemy engine setup
  - Session factory
  - Context manager for safe transactions
  - init_db() function

### Data Models
- **database/models.py** - All SQLAlchemy ORM models
  - **User** - User accounts, resources, VIP status
  - **Dragon** - Dragon collection with stats and progression
  - **Egg** - Eggs with hatching timers
  - **Plant** - Growing plants with timers
  - **Garden** - Garden customization and decorations

---

## 🔧 Service Layer (`services/`)

Business logic layer - handles all game mechanics.

### Package
- **services/__init__.py** - Service package exports
  - Exports: UserService, DragonService, EggService, GardenService

### User Management
- **services/user_service.py** - User operations
  - `get_or_create_user()` - Registration and login
  - `add_gold()` / `remove_gold()` - Gold management
  - `add_crystals()` / `remove_crystals()` - Crystal management
  - `update_daily_egg_time()` - Daily reward tracking

### Dragon Operations
- **services/dragon_service.py** - Dragon management
  - `create_dragon()` - Create new dragons
  - `feed_dragon()` - Feed with cooldown and XP
  - `get_user_dragons()` - Retrieve dragon collection
  - `get_dragon_by_id()` - Get specific dragon
  - `rename_dragon()` - Custom dragon naming
  - `decrease_dragon_hunger()` - Scheduled hunger decrease

### Egg Operations
- **services/egg_service.py** - Egg management
  - `create_egg()` - Create eggs with rarity determination
  - `get_user_eggs()` - Retrieve egg collection
  - `check_ready_eggs()` - Check hatching status
  - `hatch_egg()` - Hatch ready eggs
  - `can_purchase_egg()` - Purchase validation

### Garden Operations
- **services/garden_service.py** - Garden and plant management
  - `plant_crop()` - Plant with gold cost
  - `get_user_plants()` - Retrieve plants
  - `check_ready_plants()` - Check maturity
  - `harvest_plant()` - Harvest for gold
  - `get_user_garden()` - Get garden info
  - `update_garden()` - Customize garden

---

## 🎮 Bot Handlers (`handlers/`)

User interface layer - handles Telegram interactions.

### Package
- **handlers/__init__.py** - Handler registration exports
  - Exports: All register_*_handlers functions

### Start & Help
- **handlers/start.py** - Main menu and help system
  - `/start` command - Main menu with welcome message
  - `/help` command - Game guide and instructions
  - Main menu navigation
  - Help menu display

### Dragon Interface
- **handlers/dragon.py** - Dragon collection interface
  - `dragons_menu()` - View dragon collection
  - `view_dragon()` - Individual dragon stats
  - `feed_dragon()` - Feed dragon with cooldown
  - `dragons_list()` - Full dragon list
  - Collection statistics

### Egg Interface
- **handlers/egg.py** - Egg collection interface
  - `eggs_menu()` - View egg collection
  - `claim_daily_egg()` - Daily free egg claim
  - `check_eggs()` - Check ready eggs
  - `hatch_egg()` - Hatch ready eggs
  - `shop_eggs()` - Egg purchase menu
  - `buy_egg()` - Purchase eggs

### Garden Interface
- **handlers/garden.py** - Garden management interface
  - `garden_menu()` - View garden and plants
  - `plant_menu()` - Plant shop display
  - `plant_crop()` - Plant crops
  - `check_plants()` - Check plant maturity
  - `harvest_menu()` - View harvestable plants
  - `harvest_all()` - Batch harvest

### Profile & Shop
- **handlers/profile.py** - User profile and shop
  - `/profile` command - User profile display
  - `profile_menu()` - Profile statistics
  - `shop_menu()` - Main shop interface
  - `shop_crystals()` - Crystal purchase (Phase 3)

---

## 🛠️ Utilities (`utils/`)

Helper functions and game data.

### Package
- **utils/__init__.py** - Utility exports
  - Exports: All constants and helper functions

### Game Data
- **utils/constants.py** - All game content and data
  - **RARITIES** - 5 rarity tiers with stats
  - **DRAGONS** - 60 unique dragons (12 per rarity)
  - **EGG_TYPES** - 5 egg types with probabilities
  - **PLANTS** - 8 plant types with economics
  - **DECORATIONS** - 10 garden decorations

### Helper Functions
- **utils/helpers.py** - Utility functions
  - `format_time_remaining()` - Countdown formatting
  - `calculate_hatching_time()` - Egg timer calculation
  - `determine_egg_rarity()` - Random rarity selection
  - `get_random_dragon()` - Random dragon selection
  - `format_dragon_stats()` - Dragon display formatting
  - `format_user_profile()` - Profile display formatting
  - `can_claim_daily_egg()` - Daily reward check
  - `format_gold()` / `format_crystals()` - Currency formatting

---

## 🧪 Testing & Setup Tools

### Setup Checker
- **setup.py** - Environment validation script
  - Checks Python version
  - Verifies dependencies
  - Validates .env configuration
  - Tests database connection
  - Run: `python setup.py`

### Game Testing
- **test_game.py** - Game mechanics test suite
  - Tests all imports
  - Validates database creation
  - Tests game data loading
  - Tests service operations
  - Tests user/dragon/egg/plant creation
  - Run: `python test_game.py`

---

## 📊 Project Statistics

### Total Files
- **33 files** (excluding .git and cache)
  - 8 Documentation files
  - 19 Python source files
  - 6 Configuration/setup files

### Python Modules
- **19 source files**, organized into:
  - 1 main application file
  - 3 database files
  - 4 service files
  - 5 handler files
  - 2 utility files
  - 2 configuration files
  - 2 testing/setup files

### Lines of Code
- **~3,500+ lines** of Python code
- **~2,000+ lines** of documentation

### Game Content
- **60 unique dragons** (5 rarities × 12 dragons)
- **8 plant types** with full economics
- **5 egg types** with drop rate systems
- **10 decorations** (for Phase 2+)

---

## 🗂️ File Organization by Purpose

### 📖 Read These First
1. **README.md** - Start here!
2. **QUICKSTART.md** - Fast setup
3. **PROJECT_SUMMARY.md** - Overview

### 🔧 Development
1. **API_REFERENCE.md** - API documentation
2. **CONTRIBUTING.md** - Add features
3. **ARCHITECTURE.md** - System design

### 🚀 Deployment
1. **DEPLOYMENT.md** - Production guide
2. **setup.py** - Verify setup
3. **.env.example** - Configuration template

### 💻 Source Code
1. **bot.py** - Run this to start
2. **config.py** - Configuration
3. **database/** - Data layer
4. **services/** - Business logic
5. **handlers/** - User interface
6. **utils/** - Helpers and data

### 🧪 Testing
1. **test_game.py** - Test suite
2. **setup.py** - Setup checker

---

## 🎯 Quick File Lookup

### Need to...
- **Start the bot?** → `python bot.py`
- **Check setup?** → `python setup.py`
- **Test game?** → `python test_game.py`
- **Configure?** → `.env` (copy from `.env.example`)
- **Add dragons?** → `utils/constants.py` → DRAGONS
- **Add plants?** → `utils/constants.py` → PLANTS
- **Add features?** → `CONTRIBUTING.md` (guide)
- **Deploy?** → `DEPLOYMENT.md` (guide)
- **API reference?** → `API_REFERENCE.md`
- **Understand architecture?** → `ARCHITECTURE.md`

### Looking for...
- **User registration?** → `services/user_service.py`
- **Dragon creation?** → `services/dragon_service.py`
- **Egg hatching?** → `services/egg_service.py`
- **Plant harvesting?** → `services/garden_service.py`
- **Main menu?** → `handlers/start.py`
- **Dragon UI?** → `handlers/dragon.py`
- **Egg UI?** → `handlers/egg.py`
- **Garden UI?** → `handlers/garden.py`
- **Database models?** → `database/models.py`
- **Game data?** → `utils/constants.py`
- **Helper functions?** → `utils/helpers.py`

---

## 📋 Recommended Reading Order

### For Users
1. README.md
2. QUICKSTART.md
3. .env.example (setup)
4. Run: `python setup.py`
5. Run: `python bot.py`

### For Developers
1. README.md
2. PROJECT_SUMMARY.md
3. ARCHITECTURE.md
4. API_REFERENCE.md
5. CONTRIBUTING.md
6. Source code (database → services → handlers)

### For Deployment
1. README.md
2. DEPLOYMENT.md
3. setup.py (verify environment)
4. Follow deployment guide

---

## 🔍 Search by Feature

### User System
- Registration: `services/user_service.py`
- Profile: `handlers/profile.py`
- Resources: `services/user_service.py`

### Dragon System
- Data: `utils/constants.py` → DRAGONS
- Logic: `services/dragon_service.py`
- UI: `handlers/dragon.py`

### Egg System
- Data: `utils/constants.py` → EGG_TYPES
- Logic: `services/egg_service.py`
- UI: `handlers/egg.py`

### Garden System
- Data: `utils/constants.py` → PLANTS
- Logic: `services/garden_service.py`
- UI: `handlers/garden.py`

### Database
- Connection: `database/db.py`
- Models: `database/models.py`
- Init: `database/__init__.py`

---

## 🎓 Learning Path

### Beginner
1. Read README.md
2. Run setup.py
3. Start bot.py
4. Play the game!

### Intermediate
1. Read ARCHITECTURE.md
2. Explore handlers/
3. Read services/
4. Understand database/

### Advanced
1. Read API_REFERENCE.md
2. Read CONTRIBUTING.md
3. Modify utils/constants.py
4. Add new features
5. Create handlers

---

## ✅ Quick Checklist

### Before Running
- [ ] Read README.md
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy .env.example to .env
- [ ] Add bot token to .env
- [ ] Run setup.py to verify
- [ ] Run test_game.py to test

### For Development
- [ ] Read ARCHITECTURE.md
- [ ] Read API_REFERENCE.md
- [ ] Read CONTRIBUTING.md
- [ ] Understand service layer pattern
- [ ] Follow coding conventions

### For Deployment
- [ ] Read DEPLOYMENT.md
- [ ] Choose deployment platform
- [ ] Setup PostgreSQL
- [ ] Configure environment
- [ ] Test before production

---

**Complete File Index** 📚

All 33 files documented and cross-referenced!

For more information on any file, open it directly or refer to the appropriate documentation.
