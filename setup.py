#!/usr/bin/env python3
"""
Setup script for Dragon Garden bot
This helps with initial configuration and testing
"""

import os
import sys

def check_python_version():
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    try:
        import telegram
        import sqlalchemy
        import dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e.name}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_env_file():
    if not os.path.exists('.env'):
        print("⚠️  .env file not found")
        print("   Creating from template...")
        
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src:
                content = src.read()
            with open('.env', 'w') as dst:
                dst.write(content)
            print("✅ .env file created from template")
            print("   Please edit .env and add your TELEGRAM_BOT_TOKEN")
            return False
        else:
            print("❌ .env.example template not found")
            return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_bot_token_here' in content or 'TELEGRAM_BOT_TOKEN=' not in content:
            print("⚠️  .env file exists but token not configured")
            print("   Please edit .env and add your TELEGRAM_BOT_TOKEN")
            return False
    
    print("✅ .env file configured")
    return True

def test_database():
    try:
        from database import init_db
        print("⏳ Testing database connection...")
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    print("🐉 Dragon Garden Bot - Setup Check\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Database", test_database),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        results.append(check_func())
    
    print("\n" + "="*50)
    
    if all(results):
        print("🎉 All checks passed!")
        print("\n✅ Your bot is ready to run!")
        print("   Start it with: python bot.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n📖 Quick Help:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Get bot token from @BotFather on Telegram")
        print("   3. Add token to .env file")
        print("   4. Run this script again: python setup.py")
    
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
