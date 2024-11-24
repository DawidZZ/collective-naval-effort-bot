from sqlalchemy import Column, Integer, String
from app.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(50))
    deposits = relationship("Deposit", back_populates="player")


class Resource(Base):
    __tablename__ = 'resource'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    deposits = relationship("Deposit", back_populates="resource")


class Deposit(Base):
    __tablename__ = 'deposit'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    player = relationship("Player", back_populates="deposits")
    resource = relationship("Resource", back_populates="deposits")
    player_id = Column(Integer, ForeignKey('player.id'))
    resource_id = Column(Integer, ForeignKey('resource.id'))


class AllowedRole(Base):
    __tablename__ = 'allowed_role'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    role_id = Column(String(100))
