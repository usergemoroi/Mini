from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    gold = Column(Integer, default=1000)
    crystals = Column(Integer, default=50)
    language = Column(String(5), default='ru')
    vip_level = Column(Integer, default=0)
    vip_expiration = Column(DateTime, nullable=True)
    vip_auto_renew = Column(Boolean, default=False)
    vip_subscription_id = Column(String(255), nullable=True)
    last_daily_egg = Column(DateTime, nullable=True)
    last_daily_gold_claim = Column(DateTime, nullable=True)
    last_premium_seeds_claim = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    dragons = relationship('Dragon', back_populates='owner', cascade='all, delete-orphan')
    eggs = relationship('Egg', back_populates='owner', cascade='all, delete-orphan')
    plants = relationship('Plant', back_populates='owner', cascade='all, delete-orphan')
    garden = relationship('Garden', back_populates='owner', uselist=False, cascade='all, delete-orphan')
    battlepass = relationship('Battlepass', back_populates='user', uselist=False, cascade='all, delete-orphan')
    purchases = relationship('Purchase', back_populates='user', cascade='all, delete-orphan')
    crypto_transactions = relationship('CryptoTransaction', back_populates='user', cascade='all, delete-orphan')

class Dragon(Base):
    __tablename__ = 'dragons'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    dragon_type = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    rarity = Column(String(50), nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    hunger = Column(Integer, default=100)
    happiness = Column(Integer, default=100)
    strength = Column(Integer, default=10)
    agility = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    last_fed = Column(DateTime, nullable=True)
    hatched_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship('User', back_populates='dragons')

class Egg(Base):
    __tablename__ = 'eggs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    egg_type = Column(String(50), nullable=False)
    rarity = Column(String(50), nullable=True)
    hatching_time = Column(Integer, nullable=False)
    started_hatching_at = Column(DateTime, default=datetime.utcnow)
    hatches_at = Column(DateTime, nullable=False)
    is_hatched = Column(Boolean, default=False)
    
    owner = relationship('User', back_populates='eggs')

class Plant(Base):
    __tablename__ = 'plants'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plant_type = Column(String(100), nullable=False)
    planted_at = Column(DateTime, default=datetime.utcnow)
    ready_at = Column(DateTime, nullable=False)
    is_ready = Column(Boolean, default=False)
    is_harvested = Column(Boolean, default=False)
    
    owner = relationship('User', back_populates='plants')

class Garden(Base):
    __tablename__ = 'gardens'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    name = Column(String(100), default='My Dragon Garden')
    description = Column(Text, default='A magical place where dragons roam')
    decorations = Column(Text, default='')
    theme = Column(String(50), default='Classic')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship('User', back_populates='garden')

class Battlepass(Base):
    __tablename__ = 'battlepasses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    season_number = Column(Integer, default=1)
    is_active = Column(Boolean, default=False)
    purchase_date = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    current_progress = Column(Integer, default=0)  # Days logged in
    rewards_claimed = Column(JSON, default=dict)  # Day numbers claimed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='battlepass')

class Purchase(Base):
    __tablename__ = 'purchases'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    payment_type = Column(String(50))  # 'stars', 'crypto'
    amount_stars = Column(Integer, nullable=True)
    amount_crypto = Column(Float, nullable=True)
    currency = Column(String(10), nullable=True)  # BTC, ETH, USDT, TON
    item_type = Column(String(50))  # 'crystals', 'vip', 'battlepass'
    item_data = Column(JSON, default=dict)  # Details of purchased item
    status = Column(String(20), default='pending')  # pending, completed, failed, cancelled
    telegram_payment_charge_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship('User', back_populates='purchases')

class CryptoTransaction(Base):
    __tablename__ = 'crypto_transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    invoice_id = Column(String(255), unique=True, nullable=False)
    currency = Column(String(10), nullable=False)  # BTC, ETH, USDT, TON
    amount = Column(Float, nullable=False)
    address = Column(Text, nullable=True)
    status = Column(String(20), default='pending')  # pending, completed, failed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    confirmed_at = Column(DateTime, nullable=True)
    
    user = relationship('User', back_populates='crypto_transactions')
