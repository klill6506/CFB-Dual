from fastapi import FastAPI
from fastapi.responses import FileResponse
import httpx
import os

from fetchers import CFBDClient, OddsClient

app = FastAPI(
    title="CFB Dual API",
    version="1.0.0",
    description="API for College Football Dual Model"
)

# --- Serve static OpenAPI JSON files ---
BASE_DIR = os.path.dirname(__file__)

@app.get("/static-openapi.json", include_in_schema=False)
async def get_openapi_json():
    """Serve the manually defined openapi.json file."""
    return FileResponse(os.path.join(BASE_DIR, "openapi.json"))

@app.get("/static-openapi-schema.json", include_in_schema=False)
async def get_openapi_schema():
    """Serve the manually defined openapi_schema.json file."""
    return FileResponse(os.path.join(BASE_DIR, "openapi_schema.json"))


# --- Root endpoint ---
@app.get("/")
async def root():
    return {"message": "CFB Dual API is running!"}


# --- Games endpoint ---
@app.get("/games")
async def get_games(team: str, year: int = 2025):
    client = CFBDClient()
    async with httpx.AsyncClient() as http_client:
        games = await client.get_games_for_team(http_client, year=year, team=team)
    return {"team": team, "year": year, "games": games}


# --- Predict endpoint ---
@app.get("/predict")
async def predict(model: str = "conservative", year: int = 2025):
    cfbd = CFBDClient()
    odds = OddsClient()

    async with httpx.AsyncClient() as client:
        stats = await cfbd.get_team_season_stats(client, year=year)
        ppa = await cfbd.get_team_ppa(client, year=year)
        venue_data = await cfbd.get_venues(client)
        sp_ratings = await cfbd.get_sp_ratings(client, year=year)
        odds_data = await odds.get_odds(client)

    return {
        "model_used": model,
        "year": year,
        "stats_count": len(stats),
        "ppa_count": len(ppa),
        "venues_count": len(venue_data),
        "sp_ratings_count": len(sp_ratings),
        "odds_count": len(odds_data),
        "prediction": "This is a stub prediction."
    }
