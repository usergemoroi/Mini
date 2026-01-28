#!/usr/bin/env python3
"""
Simple test script to verify game mechanics without running the full bot
"""

import sys
from datetime import datetime, timedelta

def test_imports():
    print("Testing imports...")
    try:
        from database import init_db, get_session, User, Dragon, Egg, Plant, Garden
        from services import UserService, DragonService, EggService, GardenService
        from utils import DRAGONS, EGG_TYPES, PLANTS, RARITIES
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    print("\nTesting database...")
    try:
        from database import init_db
        init_db()
        print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_game_data():
    print("\nTesting game data...")
    try:
        from utils import DRAGONS, EGG_TYPES, PLANTS, RARITIES
        
        total_dragons = sum(len(dragons) for dragons in DRAGONS.values())
        print(f"✅ {total_dragons} dragons loaded")
        print(f"   - Common: {len(DRAGONS['Common'])}")
        print(f"   - Rare: {len(DRAGONS['Rare'])}")
        print(f"   - Epic: {len(DRAGONS['Epic'])}")
        print(f"   - Legendary: {len(DRAGONS['Legendary'])}")
        print(f"   - Mythic: {len(DRAGONS['Mythic'])}")
        
        print(f"✅ {len(EGG_TYPES)} egg types loaded")
        print(f"✅ {len(PLANTS)} plant types loaded")
        print(f"✅ {len(RARITIES)} rarity tiers loaded")
        
        return True
    except Exception as e:
        print(f"❌ Game data error: {e}")
        return False

def test_services():
    print("\nTesting services...")
    try:
        from database import get_session, User
        from services import UserService, DragonService, EggService, GardenService
        from utils.helpers import get_random_dragon, determine_egg_rarity
        
        print("✅ All services loaded successfully")
        
        dragon = get_random_dragon('Epic')
        print(f"✅ Random dragon test: {dragon['name']} ({dragon['element']})")
        
        rarity = determine_egg_rarity('Premium')
        print(f"✅ Egg rarity test: {rarity}")
        
        return True
    except Exception as e:
        print(f"❌ Service test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_creation():
    print("\nTesting user creation...")
    try:
        from database import get_session
        from services import UserService
        
        class MockTelegramUser:
            def __init__(self):
                self.id = 12345678
                self.username = "test_user"
                self.first_name = "Test"
        
        with get_session() as session:
            mock_user = MockTelegramUser()
            user = UserService.get_or_create_user(session, mock_user)
            
            print(f"✅ User created: {user.first_name}")
            print(f"   Gold: {user.gold}")
            print(f"   Crystals: {user.crystals}")
            print(f"   VIP Level: {user.vip_level}")
            
            if user.garden:
                print(f"✅ Garden created: {user.garden.name}")
        
        return True
    except Exception as e:
        print(f"❌ User creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dragon_creation():
    print("\nTesting dragon creation...")
    try:
        from database import get_session
        from services import UserService, DragonService
        
        class MockTelegramUser:
            def __init__(self):
                self.id = 12345679
                self.username = "dragon_tester"
                self.first_name = "Dragon Tester"
        
        with get_session() as session:
            mock_user = MockTelegramUser()
            user = UserService.get_or_create_user(session, mock_user)
            
            dragon = DragonService.create_dragon(session, user, 'Legendary')
            
            print(f"✅ Dragon created: {dragon.name}")
            print(f"   Type: {dragon.dragon_type}")
            print(f"   Rarity: {dragon.rarity}")
            print(f"   Strength: {dragon.strength}")
            print(f"   Agility: {dragon.agility}")
            print(f"   Intelligence: {dragon.intelligence}")
        
        return True
    except Exception as e:
        print(f"❌ Dragon creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_egg_creation():
    print("\nTesting egg creation...")
    try:
        from database import get_session
        from services import UserService, EggService
        
        class MockTelegramUser:
            def __init__(self):
                self.id = 12345680
                self.username = "egg_tester"
                self.first_name = "Egg Tester"
        
        with get_session() as session:
            mock_user = MockTelegramUser()
            user = UserService.get_or_create_user(session, mock_user)
            
            egg = EggService.create_egg(session, user, 'Premium')
            
            print(f"✅ Egg created: {egg.egg_type}")
            print(f"   Rarity: {egg.rarity}")
            print(f"   Hatching time: {egg.hatching_time} hours")
            print(f"   Hatches at: {egg.hatches_at}")
        
        return True
    except Exception as e:
        print(f"❌ Egg creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_plant_creation():
    print("\nTesting plant creation...")
    try:
        from database import get_session
        from services import UserService, GardenService
        
        class MockTelegramUser:
            def __init__(self):
                self.id = 12345681
                self.username = "garden_tester"
                self.first_name = "Garden Tester"
        
        with get_session() as session:
            mock_user = MockTelegramUser()
            user = UserService.get_or_create_user(session, mock_user)
            
            plant, message = GardenService.plant_crop(session, user, 'Rose')
            
            if plant:
                print(f"✅ Plant created: {plant.plant_type}")
                print(f"   Planted at: {plant.planted_at}")
                print(f"   Ready at: {plant.ready_at}")
                print(f"   User gold after planting: {user.gold}")
                return True
            else:
                print(f"❌ Plant creation failed: {message}")
                return False
        
    except Exception as e:
        print(f"❌ Plant creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🐉 Dragon Garden - Game Mechanics Test\n")
    print("="*50)
    
    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("Game Data", test_game_data),
        ("Services", test_services),
        ("User Creation", test_user_creation),
        ("Dragon Creation", test_dragon_creation),
        ("Egg Creation", test_egg_creation),
        ("Plant Creation", test_plant_creation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            results.append(test_func())
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            results.append(False)
        print()
    
    print("="*50)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"🎉 All tests passed! ({passed}/{total})")
        print("\n✅ Game mechanics are working correctly!")
        print("   Your bot is ready to run with: python bot.py")
    else:
        print(f"⚠️  Some tests failed ({passed}/{total} passed)")
        print("\nPlease check the errors above and fix them.")
    
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
