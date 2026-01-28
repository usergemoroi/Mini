# Dragon Garden Phase 2 Implementation Guide

## Overview

Phase 2 implements major monetization and localization features including Russian localization, VIP system, Battlepass, and payment integrations (Telegram Stars + CryptoBot).

## New Features

### 1. Russian Localization 🇷🇺

#### Files Created
- `localization/__init__.py` - Localization system
- `localization/ru.py` - Russian translations (default)
- `localization/en.py` - English translations

#### Usage
```python
from localization import t

# Get localized message
text = t(user.language, 'start_welcome', name=user.first_name)
```

#### Language Switching
- Default: Russian (`ru`)
- Command: `/language`
- Switch between Russian and English

### 2. Reply Keyboards 🔘

All inline keyboards replaced with `ReplyKeyboardMarkup` for better mobile UX:

```python
from telegram import ReplyKeyboardMarkup

keyboard = [
    ["🐉 Драконы", "🥚 Яйца"],
    ["🌱 Сад", "👤 Профиль"],
    ["🛒 Магазин", "👑 VIP"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
```

### 3. VIP System 👑

#### VIP Levels (0-4)

| Level | Name | Stars/Month | Gold Bonus | Max Dragons | Daily Gold | Seeds/Week |
|-------|------|-------------|------------|-------------|------------|------------|
| 0 | Free | - | 0% | 1 | 0 | 0 |
| 1 | Bronze | 99 | +20% | 2 | 0 | 1 |
| 2 | Silver | 499 | +40% | 3 | 100 | 3 |
| 3 | Gold | 999 | +60% | 5 | 300 | 7 |
| 4 | Platinum | 1999 | +100% | 10 | 500 | 15 |

#### Database Changes
```python
# User model additions
vip_level = Column(Integer, default=0)
vip_expiration = Column(DateTime, nullable=True)
vip_auto_renew = Column(Boolean, default=False)
vip_subscription_id = Column(String(255), nullable=True)
last_daily_gold_claim = Column(DateTime, nullable=True)
```

#### VIP Service Usage
```python
from services import VIPService

# Get VIP level
level = VIPService.get_vip_level(user)

# Check if active
if VIPService.is_vip_active(user):
    bonus = VIPService.get_daily_gold_bonus(user)
    UserService.add_gold(session, user, bonus)

# Get benefits
benefits = VIPService.get_vip_benefits(user)
gold_multiplier = benefits['gold_bonus']  # 0.2 for 20%
```

### 4. Battlepass System 🎖️

#### Features
- 30-day seasons
- 50 daily rewards
- Price: 200 Crystals
- Weekly milestones (days 7, 14, 21, 30, 50)

#### Database Changes
```python
class Battlepass(Base):
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    season_number = Column(Integer, default=1)
    is_active = Column(Boolean, default=False)
    purchase_date = Column(DateTime)
    expiration_date = Column(DateTime)
    current_progress = Column(Integer, default=0)  # Days logged in
    rewards_claimed = Column(JSON, default=dict)
```

#### Battlepass Service Usage
```python
from services import BattlepassService

# Activate battlepass
bp = BattlepassService.activate_battlepass(session, user)

# Record daily login
BattlepassService.check_daily_login(session, user)

# Claim reward
success, message, rewards = BattlepassService.claim_reward(
    session, bp, day=7
)
```

### 5. Telegram Stars Payment ⭐

#### Products
- Crystals: 100 (99⭐), 500 (499⭐), 1200 (999⭐), 2700 (1999⭐)
- VIP: All levels
- Battlepass: 200 Crystals

#### Implementation
```python
from telegram import LabeledPrice

# Send invoice
prices = [LabeledPrice("100 Crystals", 9900)]  # In cents

await context.bot.send_invoice(
    chat_id=user_id,
    title="100 Кристаллов",
    description="Пакет 100 кристаллов",
    payload="crystals:100",
    provider_token="",
    currency="XTR",
    prices=prices
)
```

#### Payment Flow
1. User clicks purchase button
2. Bot sends invoice via `send_invoice()`
3. `PreCheckoutQueryHandler` validates purchase
4. `SuccessfulPaymentHandler` grants items
5. Transaction recorded in `Purchase` table

### 6. CryptoBot Integration 🪙

#### Supported Currencies
- Bitcoin (BTC)
- Ethereum (ETH)
- USDT/USDC
- TON (Ton network)

#### API Wrapper
```python
from payment import CryptoBotAPI

cryptobot = CryptoBotAPI(api_token=...)

# Create invoice
result = await cryptobot.create_invoice(
    amount=10.0,
    currency='USDT',
    description='Dragon Garden - 100 Crystals'
)

# Check status
status = await cryptobot.get_invoice(invoice_id)
```

#### Payment Flow
1. User selects cryptocurrency
2. Bot creates invoice via CryptoBot API
3. User receives payment link
4. Bot checks invoice status periodically
5. On success, grants Crystals

## File Structure

### New Directories
```
/home/engine/project/
├── localization/          # Language system
├── payment/              # Payment handlers
└── shop/                # Shop system
```

### Updated Files
- `config.py` - VIP benefits, pricing, payment config
- `database/models.py` - Battlepass, Purchase, CryptoTransaction
- `database/db.py` - Import new models
- `handlers/start.py` - Russian texts, reply keyboards
- `handlers/profile.py` - VIP/Battlepass display
- `bot.py` - Register new handlers
- `requirements.txt` - Added httpx
- `.env.example` - CRYPTOBOT_API_TOKEN

## Database Migrations

### Automatic Migration
The database will be automatically updated on next run. New tables:
- `battlepasses`
- `purchases`
- `crypto_transactions`

### Manual Migration (if needed)
```bash
# Backup existing database
cp dragon_garden.db dragon_garden.db.backup

# Delete old database to recreate
rm dragon_garden.db

# Bot will recreate with new schema
python bot.py
```

## Configuration

### Environment Variables

```bash
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional
DATABASE_URL=postgresql://user:pass@localhost/db
BOT_USERNAME=dragon_garden_bot
ADMIN_USER_IDS=123456789

# CryptoBot (optional, for crypto payments)
CRYPTOBOT_API_TOKEN=your_cryptobot_token
CRYPTOBOT_API_URL=https://pay.crypt.bot/api
```

### VIP Configuration

Edit `config.py` to adjust:
- VIP benefits per level
- VIP pricing
- Gold bonuses
- Dragon limits

### Battlepass Configuration

Edit `config.py`:
```python
BATTLEPASS_PRICE = 200  # Crystals
BATTLEPASS_DURATION_DAYS = 30
BATTLEPASS_MAX_DAYS = 50
```

## Testing

### Manual Testing Checklist

#### Localization
- [ ] Russian texts display correctly
- [ ] Language switch works
- [ ] All menus localized

#### VIP System
- [ ] VIP levels display correctly
- [ ] VIP benefits apply (gold bonus, dragon limit)
- [ ] VIP purchase with Stars works
- [ ] Daily gold bonus claim works
- [ ] VIP expiration works

#### Battlepass
- [ ] Battlepass purchase works
- [ ] Daily login progress increases
- [ ] Reward claiming works
- [ ] Weekly milestones work
- [ ] Expiration works

#### Payments
- [ ] Stars invoices send correctly
- [ ] Stars payments complete
- [ ] Crypto invoices create
- [ ] Crypto payment status checks
- [ ] Transaction history records

#### Shop
- [ ] All shop categories work
- [ ] Egg purchases work
- [ ] Crystal purchases work
- [ ] VIP purchases work
- [ ] Navigation works

### Test Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your values

# Run bot
python bot.py

# Test with Telegram BotFather commands
/start
/language
/vip
/battlepass
/profile
/pay
```

## Known Limitations

1. **CryptoBot Webhooks**: Currently using polling to check payment status. Webhooks should be implemented for production.

2. **VIP Auto-Renewal**: Subscription ID is stored but auto-renewal logic not fully implemented (requires payment processor integration).

3. **Battlepass Rewards**: Simplified reward system. More complex rewards (exclusive eggs, decorations) need additional implementation.

4. **Currency Rates**: Fixed Crystal packages in Stars. Dynamic pricing not implemented.

5. **Premium Seeds**: VIP seed weekly limit not fully implemented (reset logic needed).

## Deployment

### Render.com Deployment

1. Update `render.yaml` (if using):
   ```yaml
   env:
     - key: CRYPTOBOT_API_TOKEN
   ```

2. Deploy:
   ```bash
   git push origin main
   ```

3. Set environment variables in Render dashboard:
   - TELEGRAM_BOT_TOKEN
   - DATABASE_URL
   - CRYPTOBOT_API_TOKEN (optional)

### Database Migration on Deployment

Since SQLite database is recreated on each deployment, consider:
1. Using PostgreSQL for persistent storage
2. Setting up migration scripts with Alembic
3. Backing up data before major changes

## Troubleshooting

### Bot Doesn't Start
- Check `TELEGRAM_BOT_TOKEN` is set correctly
- Verify bot token in BotFather
- Check logs for errors

### Payment Errors
- Ensure payment handlers are registered
- Check CryptoBot API token
- Verify Stars integration (empty provider_token for XTR)

### Database Errors
- Delete `dragon_garden.db` to recreate schema
- Check SQLAlchemy version compatibility
- Verify all models are imported in `db.py`

### Localization Issues
- Check `localization/` files exist
- Verify `t()` function is imported
- Ensure user.language is set

## Support

For issues:
1. Check logs: `tail -f bot.log`
2. Review error messages
3. Verify all environment variables
4. Test payment integration in sandbox mode

## Next Steps (Phase 3)

- Additional payment methods (Stripe, etc.)
- Advanced VIP features (exclusive dragons, skins)
- Enhanced Battlepass with cosmetic rewards
- Social features (gifting, trading)
- Events and tournaments
- Leaderboards
