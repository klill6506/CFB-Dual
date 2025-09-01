from fastapi import FastAPI, HTTPException
import httpx
import os

from fetchers import CFBDClient, OddsClient

app = FastAPI(
    title="CFB Dual API",
    version="1.0.0",
    description="API for College Football Dual Model"
)


@app.get("/")
async def root():
    return {"message": "CFB Dual API is running!"}


@app.get("/games")
async def get_games(team: str, year: int = 2025):
    client = CFBDClient()
    async with httpx.AsyncClient() as http_client:
        try:
            games = await client.get_games_for_team(http_client, year=year, team=team)
            return {"team": team, "year": year, "games": games}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code,
                                detail=f"CFBD API error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/predict")
async def predict(model: str = "conservative", year: int = 2025):
    cfbd = CFBDClient()
    odds = OddsClient()

    async with httpx.AsyncClient() as client:
        try:
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

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code,
                                detail=f"API error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
