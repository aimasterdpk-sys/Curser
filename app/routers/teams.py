from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/teams", tags=["teams"])

@router.post("/tournament/{tournament_id}")
def create_team(tournament_id: int, payload: schemas.TeamCreate, db: Session = Depends(get_db)):
    tournament = db.get(models.Tournament, tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    team = models.Team(name=payload.name, tournament_id=tournament_id)
    db.add(team)
    db.flush()
    for p in payload.players:
        db.add(models.Player(name=p.name, ign=p.ign, team=team))
    db.commit()
    db.refresh(team)
    return {"id": team.id, "name": team.name}

@router.get("/tournament/{tournament_id}", response_model=List[schemas.TeamOut])
def list_teams(tournament_id: int, db: Session = Depends(get_db)):
    return db.query(models.Team).filter(models.Team.tournament_id == tournament_id).all()
