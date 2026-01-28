from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
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
    vip_level = Column(String(50), default='Free')
    last_daily_egg = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    dragons = relationship('Dragon', back_populates='owner', cascade='all, delete-orphan')
    eggs = relationship('Egg', back_populates='owner', cascade='all, delete-orphan')
    plants = relationship('Plant', back_populates='owner', cascade='all, delete-orphan')
    garden = relationship('Garden', back_populates='owner', uselist=False, cascade='all, delete-orphan')

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
