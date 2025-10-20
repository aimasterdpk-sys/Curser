from typing import List, Optional
from pydantic import BaseModel, Field

class PlayerCreate(BaseModel):
    name: str
    ign: Optional[str] = None

class TeamCreate(BaseModel):
    name: str
    players: List[PlayerCreate] = Field(default_factory=list)

class TournamentCreate(BaseModel):
    name: str
    game_mode: str = "squad"

class MatchCreate(BaseModel):
    map_name: str = "Bermuda"
    match_no: int = 1

class ResultCreate(BaseModel):
    team_id: int
    placement: int
    kills: int

class TeamOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class TournamentOut(BaseModel):
    id: int
    name: str
    game_mode: str
    class Config:
        from_attributes = True

class MatchOut(BaseModel):
    id: int
    tournament_id: int
    map_name: str
    match_no: int
    class Config:
        from_attributes = True

class ResultOut(BaseModel):
    id: int
    match_id: int
    team_id: int
    placement: int
    kills: int
    class Config:
        from_attributes = True
