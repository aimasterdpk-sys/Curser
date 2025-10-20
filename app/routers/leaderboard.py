from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from ..database import get_db
from .. import models
from ..services.scoring import calculate_points

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/tournament/{tournament_id}")
def leaderboard(tournament_id: int, db: Session = Depends(get_db)):
    teams = db.query(models.Team).filter(models.Team.tournament_id == tournament_id).all()
    matches = db.query(models.Match).filter(models.Match.tournament_id == tournament_id).all()

    team_points: Dict[int, int] = {t.id: 0 for t in teams}

    for match in matches:
        results = db.query(models.Result).filter(models.Result.match_id == match.id).all()
        for r in results:
            team_points[r.team_id] += calculate_points(r.placement, r.kills)

    summary = [
        {
            "team_id": t.id,
            "team_name": t.name,
            "points": team_points.get(t.id, 0)
        }
        for t in teams
    ]

    summary.sort(key=lambda x: x["points"], reverse=True)
    return summary
