from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/tournament/{tournament_id}", response_model=schemas.MatchOut)
def create_match(tournament_id: int, payload: schemas.MatchCreate, db: Session = Depends(get_db)):
    tournament = db.get(models.Tournament, tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    match = models.Match(tournament_id=tournament_id, map_name=payload.map_name, match_no=payload.match_no)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

@router.get("/tournament/{tournament_id}", response_model=List[schemas.MatchOut])
def list_matches(tournament_id: int, db: Session = Depends(get_db)):
    return db.query(models.Match).filter(models.Match.tournament_id == tournament_id).order_by(models.Match.match_no).all()
