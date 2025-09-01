import httpx
from fastapi import FastAPI, Query
from fetchers import CFBDClient, OddsClient
from predictor import Predictor

app = FastAPI()

cfbd_client = CFBDClient()
odds_client = OddsClient()

@app.get("/")
async def root():
    return {"message": "College Football Prediction API is live!"}


@app.get("/games")
async def get_games(team: str, year: int = 2025):
    async with httpx.AsyncClient(timeout=30.0) as http_client:
        games = await cfbd_client.get_games_for_team(http_client, year=year, team=team)
    return games


@app.get("/predict")
async def predict(
    model: str = Query("conservative", description="Prediction model type"),
    year: int = Query(2025, description="Season year"),
    team: str = Query("Alabama", description="Team to analyze")
):
    async with httpx.AsyncClient(timeout=30.0) as http_client:
        # Pull season stats + odds
        stats = await cfbd_client.get_team_season_stats(http_client, year=year)
        odds = await odds_client.get_odds(http_client)

    # For now: stub one game data
    # Replace this with real matchup stats later
    game_data = {
        "predicted_spread": -6.5,
        "team": team,
        "year": year,
    }

    # Example: pick the first odds line
    odds_line = {"spread": -3.5}

    predictor = Predictor(config_path="config.yaml", model=model)
    result = predictor.evaluate_game(game_data, odds_line)

    return {
        "model_used": model,
        "team": team,
        "year": year,
        "stats_count": len(stats),
        "odds_count": len(odds),
        "prediction": result,
    }
