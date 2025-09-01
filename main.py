import httpx
from fastapi import FastAPI
from predictor import Predictor
from fetchers import CFBDClient, OddsClient

app = FastAPI(
    title="College Football Predictions API",
    version="1.0.0",
    servers=[
        {"url": "https://cfbdual2.onrender.com", "description": "Render deployment"}
    ],
)

cfbd_client = CFBDClient()
odds_client = OddsClient()

# Reuse a single HTTP client for performance
http_client = httpx.AsyncClient(timeout=20.0)


@app.get("/")
async def root():
    return {"message": "CFB Prediction API is running"}


@app.get("/games")
async def get_games(team: str, year: int = 2025):
    try:
        games = await cfbd_client.get_games_for_team(http_client, year=year, team=team)
        return {"team": team, "year": year, "games": games}
    except Exception as e:
        return {"error": str(e)}


@app.get("/predict")
async def predict(model: str = "conservative", year: int = 2025):
    try:
        # Pick config file based on model name
        config_file = f"config_{model}.yaml"

        # Load predictor with just the config file
        predictor = Predictor(config_path=config_file)

        # Fetch stats + odds
        stats = await cfbd_client.get_team_season_stats(http_client, year=year)
        odds = await odds_client.get_odds(http_client)

        # Example evaluation (placeholder numbers until calc is wired in)
        example_game = {"predicted_spread": -3}
        example_odds = {"spread": -1}
        results = predictor.evaluate_game(example_game, example_odds)

        return {
            "model_used": model,
            "year": year,
            "stats_count": len(stats) if stats else 0,
            "odds_count": len(odds) if odds else 0,
            "results": results,
        }
    except Exception as e:
        return {"error": str(e)}


@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()
