from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import httpx
from fetchers import CFBDClient, OddsClient

app = FastAPI(
    title="CFB Dual API",
    version="1.0.0"
)

def custom_openapi():
    print("🔧 custom_openapi override is running!")  # Debug marker
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="API for College Football Dual Model",
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {"url": "https://cfbdual2.onrender.com"}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Force override
app.openapi = custom_openapi

@app.get("/")
async def root():
    return {"message": "CFB Dual API is running!"}

@app.get("/games")
async def get_games(team: str, year: int = 2025):
    client = CFBDClient()
    async with httpx.AsyncClient() as http_client:
        games = await client.get_games_for_team(http_client, year=year, team=team)
    return {"team": team, "year": year, "games": games}

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

# ✅ Force schema rebuild on startup
@app.on_event("startup")
async def startup_event():
    app.openapi_schema = custom_openapi()
