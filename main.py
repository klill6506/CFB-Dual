from fastapi import FastAPI
import httpx
import traceback

from fetchers import CFBDClient, OddsClient

app = FastAPI()

client = CFBDClient()
odds_client = OddsClient()


@app.get("/")
async def root():
    return {"message": "CFB Dual API is running"}


@app.get("/games")
async def get_games(team: str, year: int = 2025):
    async with httpx.AsyncClient() as http_client:
        try:
            games = await client.get_games_for_team(http_client, year=year, team=team)
            return {"team": team, "year": year, "games": games}
        except Exception as e:
            print("⚠️ ERROR in /games:", e)
            traceback.print_exc()
            return {"error": str(e)}


@app.get("/predict")
async def predict(model: str = "conservative", year: int = 2025):
    async with httpx.AsyncClient() as http_client:
        try:
            stats = await client.get_team_season_stats(http_client, year=year)
            odds = await odds_client.get_odds(http_client)

            return {
                "model_used": model,
                "year": year,
                "stats_count": len(stats) if isinstance(stats, list) else 0,
                "odds_count": len(odds) if isinstance(odds, list) else 0,
                "prediction": "Stub prediction with stats + odds"
            }
        except Exception as e:
            print("⚠️ ERROR in /predict:", e)
            traceback.print_exc()
            return {"error": str(e)}
