from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    game_mode = Column(String, default="squad")
    created_at = Column(DateTime, default=datetime.utcnow)

    teams = relationship("Team", back_populates="tournament", cascade="all, delete-orphan")
    matches = relationship("Match", back_populates="tournament", cascade="all, delete-orphan")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"))

    tournament = relationship("Tournament", back_populates="teams")
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="team", cascade="all, delete-orphan")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ign = Column(String, nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))

    team = relationship("Team", back_populates="players")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"))
    map_name = Column(String, default="Bermuda")
    match_no = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    tournament = relationship("Tournament", back_populates="matches")
    results = relationship("Result", back_populates="match", cascade="all, delete-orphan")

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"))
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    placement = Column(Integer, nullable=False)  # 1..n
    kills = Column(Integer, default=0)

    match = relationship("Match", back_populates="results")
    team = relationship("Team", back_populates="results")
