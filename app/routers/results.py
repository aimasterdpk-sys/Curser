from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..services.scoring import calculate_points

router = APIRouter(prefix="/results", tags=["results"])

@router.post("/match/{match_id}")
def submit_result(match_id: int, payload: schemas.ResultCreate, db: Session = Depends(get_db)):
    match = db.get(models.Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    team = db.get(models.Team, payload.team_id)
    if not team or team.tournament_id != match.tournament_id:
        raise HTTPException(status_code=400, detail="Team not in this tournament")
    result = models.Result(match_id=match_id, team_id=payload.team_id, placement=payload.placement, kills=payload.kills)
    db.add(result)
    db.commit()
    db.refresh(result)
    return {"id": result.id}

@router.get("/match/{match_id}", response_model=List[schemas.ResultOut])
def list_results(match_id: int, db: Session = Depends(get_db)):
    return db.query(models.Result).filter(models.Result.match_id == match_id).order_by(models.Result.placement).all()
