from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/tournaments", tags=["tournaments"])

@router.post("/", response_model=schemas.TournamentOut)
def create_tournament(payload: schemas.TournamentCreate, db: Session = Depends(get_db)):
    tournament = models.Tournament(name=payload.name, game_mode=payload.game_mode)
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return tournament

@router.get("/", response_model=List[schemas.TournamentOut])
def list_tournaments(db: Session = Depends(get_db)):
    return db.query(models.Tournament).all()
