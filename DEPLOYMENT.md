# 🚀 Deployment Guide - Dragon Garden Bot

This guide covers deploying Dragon Garden bot to production environments.

## 📋 Deployment Options

- **Option 1**: VPS/Cloud Server (Recommended)
- **Option 2**: Heroku
- **Option 3**: Docker Container
- **Option 4**: Railway/Render

## 🖥️ Option 1: VPS Deployment (Ubuntu/Debian)

### Prerequisites
- Ubuntu 20.04+ or Debian 11+
- Root or sudo access
- Domain name (optional)

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv postgresql nginx -y

# Install git
sudo apt install git -y
```

### Step 2: PostgreSQL Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE dragon_garden;
CREATE USER dragon_bot WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE dragon_garden TO dragon_bot;
\q
```

### Step 3: Clone and Setup Bot

```bash
# Create bot user
sudo useradd -m -s /bin/bash dragonbot
sudo su - dragonbot

# Clone repository
git clone <your-repo-url> dragon-garden
cd dragon-garden

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Create .env file
nano .env
```

Add your configuration:
```env
TELEGRAM_BOT_TOKEN=your_actual_bot_token
DATABASE_URL=postgresql://dragon_bot:your_secure_password@localhost/dragon_garden
BOT_USERNAME=your_bot_username
ADMIN_USER_IDS=your_telegram_id
```

### Step 5: Test Bot

```bash
python bot.py
# Press Ctrl+C after testing
```

### Step 6: Create Systemd Service

```bash
# Exit bot user
exit

# Create service file
sudo nano /etc/systemd/system/dragon-garden.service
```

Add this content:
```ini
[Unit]
Description=Dragon Garden Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
User=dragonbot
WorkingDirectory=/home/dragonbot/dragon-garden
Environment="PATH=/home/dragonbot/dragon-garden/venv/bin"
ExecStart=/home/dragonbot/dragon-garden/venv/bin/python /home/dragonbot/dragon-garden/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 7: Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable dragon-garden

# Start service
sudo systemctl start dragon-garden

# Check status
sudo systemctl status dragon-garden

# View logs
sudo journalctl -u dragon-garden -f
```

### Step 8: Firewall (Optional)

```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

## ☁️ Option 2: Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Step 1: Prepare for Heroku

Create `Procfile`:
```
worker: python bot.py
```

Create `runtime.txt`:
```
python-3.11.0
```

### Step 2: Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create dragon-garden-bot

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set BOT_USERNAME=your_bot_username

# Deploy
git push heroku main

# Scale worker
heroku ps:scale worker=1

# View logs
heroku logs --tail
```

## 🐳 Option 3: Docker Deployment

### Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run bot
CMD ["python", "bot.py"]
```

### Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: dragon_garden
      POSTGRES_USER: dragon_bot
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  bot:
    build: .
    depends_on:
      - db
    environment:
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      DATABASE_URL: postgresql://dragon_bot:secure_password@db:5432/dragon_garden
      BOT_USERNAME: ${BOT_USERNAME}
    restart: unless-stopped

volumes:
  postgres_data:
```

### Deploy with Docker:

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down

# Update
git pull
docker-compose up -d --build
```

## 🚂 Option 4: Railway Deployment

### Quick Deploy:

1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Connect repository
5. Add PostgreSQL database
6. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `BOT_USERNAME`
7. Deploy!

Railway auto-detects Python and runs `bot.py`.

## 🔒 Security Best Practices

### 1. Environment Variables
```bash
# Never commit .env file
# Use strong passwords
# Rotate tokens regularly
```

### 2. Database Security
```sql
-- Use strong passwords
-- Limit database user permissions
-- Enable SSL connections (production)
```

### 3. Bot Token
```bash
# Keep token secret
# Use @BotFather to revoke compromised tokens
# Don't share logs with tokens
```

### 4. Server Security
```bash
# Keep system updated
sudo apt update && sudo apt upgrade

# Use SSH keys, not passwords
# Enable firewall
# Use fail2ban for brute force protection
sudo apt install fail2ban
```

## 📊 Monitoring

### Log Monitoring

```bash
# Systemd logs (VPS)
sudo journalctl -u dragon-garden -f --lines=100

# Docker logs
docker-compose logs -f --tail=100

# Heroku logs
heroku logs --tail --app dragon-garden-bot
```

### Database Monitoring

```bash
# PostgreSQL connection count
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Database size
sudo -u postgres psql -d dragon_garden -c "SELECT pg_size_pretty(pg_database_size('dragon_garden'));"
```

### Bot Health Check

Create `health_check.py`:
```python
#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from telegram import Bot
import asyncio

load_dotenv()

async def check_bot():
    try:
        bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
        me = await bot.get_me()
        print(f"✅ Bot is online: @{me.username}")
        return True
    except Exception as e:
        print(f"❌ Bot error: {e}")
        return False

if __name__ == '__main__':
    asyncio.run(check_bot())
```

## 🔄 Updates and Maintenance

### Updating the Bot

```bash
# VPS deployment
sudo su - dragonbot
cd dragon-garden
source venv/bin/activate
git pull
pip install -r requirements.txt --upgrade
exit
sudo systemctl restart dragon-garden

# Docker deployment
git pull
docker-compose up -d --build

# Heroku deployment
git push heroku main
```

### Database Backups

```bash
# Backup PostgreSQL
sudo -u postgres pg_dump dragon_garden > backup_$(date +%Y%m%d).sql

# Restore
sudo -u postgres psql dragon_garden < backup_20240128.sql

# Automated backups (cron)
sudo crontab -e
# Add: 0 2 * * * pg_dump -U dragon_bot dragon_garden > /backups/dragon_$(date +\%Y\%m\%d).sql
```

### Database Migrations

For production, use Alembic:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new feature"

# Apply migration
alembic upgrade head
```

## 📈 Scaling

### Horizontal Scaling

For high traffic, consider:
- Load balancer (nginx)
- Multiple bot instances
- Redis for session management
- Separate database server

### Performance Optimization

```python
# In config.py - add connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

## 🚨 Troubleshooting

### Bot Not Starting

```bash
# Check logs
sudo journalctl -u dragon-garden -n 50

# Check if token is valid
python3 health_check.py

# Check database connection
psql -U dragon_bot -d dragon_garden -h localhost
```

### High Memory Usage

```bash
# Check memory
free -h

# Restart bot
sudo systemctl restart dragon-garden

# Add memory limits (systemd)
[Service]
MemoryLimit=512M
```

### Database Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connections
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Restart database
sudo systemctl restart postgresql
```

## 📞 Support

If you need help:
1. Check logs first
2. Verify environment variables
3. Test database connection
4. Review recent changes

## 🎯 Production Checklist

- [ ] Bot token configured
- [ ] Database setup and secured
- [ ] Environment variables set
- [ ] Bot starts successfully
- [ ] Systemd service created (VPS)
- [ ] Automatic restart enabled
- [ ] Logs accessible
- [ ] Database backups scheduled
- [ ] Monitoring in place
- [ ] Firewall configured
- [ ] SSL/TLS enabled (if using webhooks)
- [ ] Health checks working
- [ ] Admin contact info saved

---

**Good luck with your deployment! 🚀🐉**
