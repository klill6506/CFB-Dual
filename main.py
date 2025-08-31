from fastapi import FastAPI, Query
import httpx
from datetime import datetime
from typing import Dict, Any

from fetchers import CFBDClient, OddsClient

app = FastAPI(title="CFB Dual API", version="1.0.0")

# ---------- Helpers ----------

async def build_game_data(year: int) -> Dict[str, Any]:
    """Fetches combined CFB stats, ratings, and odds data for a given year."""
    cfbd = CFBDClient()
    odds_client = OddsClient()

    async with httpx.AsyncClient() as client:
        stats = await cfbd.get_team_season_stats(client, year=year)
        sp_ratings = await cfbd.get_sp_ratings(client, year=year)
        ppa = await cfbd.get_team_ppa(client, year=year)
        odds = await odds_client.get_odds(client)

    return {
        "year": year,
        "stats": stats,
        "sp_ratings": sp_ratings,
        "ppa": ppa,
        "odds": odds,
    }

# ---------- Routes ----------

@app.get("/")
async def root():
    return {"message": "Welcome to the CFB Dual API. Try /docs for available endpoints."}


@app.get("/games")
async def get_games(team: str, year: int = datetime.now().year):
    """Fetch games for a specific team and season."""
    cfbd = CFBDClient()
    async with httpx.AsyncClient() as client:
        games = await cfbd.get_games_for_team(client, year=year, team=team)
    return {"team": team, "year": year, "games": games}


@app.get("/predict")
async def predict(
    model: str = Query("conservative", enum=["conservative", "aggressive", "both"]),
    year: int = datetime.now().year,
):
    """Simple prediction stub combining data sources."""
    game_data = await build_game_data(year)

    # Example model logic (placeholder – you can replace with real handicapping)
    if model == "conservative":
        result = {"strategy": "Low risk picks", "games_analyzed": len(game_data["stats"])}
    elif model == "aggressive":
        result = {"strategy": "High risk/high reward picks", "games_analyzed": len(game_data["stats"])}
    else:  # both
        result = {
            "conservative": {"games_analyzed": len(game_data["stats"])},
            "aggressive": {"games_analyzed": len(game_data["stats"])},
        }

    return {"year": year, "model": model, "result": result}
