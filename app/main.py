from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .routers import tournaments, teams, matches, results, leaderboard
from . import models

app = FastAPI(title="Free Fire Tournament App")

app.include_router(tournaments.router)
app.include_router(teams.router)
app.include_router(matches.router)
app.include_router(results.router)
app.include_router(leaderboard.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    tournaments_list = db.query(models.Tournament).all()
    return templates.TemplateResponse("index.html", {"request": request, "tournaments": tournaments_list})
