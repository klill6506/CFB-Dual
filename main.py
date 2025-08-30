from fastapi import FastAPI, Query
import yaml
import httpx
from model import HandicappingModel
from fetchers import CFBDClient, OddsClient

app = FastAPI()

# -----------------------
# Config Loader
# -----------------------
def load_config(choice: str):
    filename = f"config_{choice}.yaml"
    with open(filename, "r") as f:
        return yaml.safe_load(f)

# -----------------------
# Predict Endpoint
# -----------------------
@app.get("/predict")
def predict(model: str = Query("conservative", enum=["aggressive", "conservative", "both"])):
    from fetchers import fetch_game_data  # fallback placeholder
    game_data = fetch_game_data()

    if model == "both":
        results = {}
        for choice in ["aggressive", "conservative"]:
            config = load_config(choice)
            m = HandicappingModel(config, label=choice)
            results[choice] = m.calculate_edge(game_data)
        return results
    else:
        config = load_config(model)
        m = HandicappingModel(config, label=model)
        edge = m.calculate_edge(game_data)
        return {model: edge}

# -----------------------
# College Football Data API
# -----------------------
@app.get("/games")
async def get_games(team: str, year: int = 2024):
    client = CFBDClient()
    async with httpx.AsyncClient() as http_client:
        games = await client.get_games_for_team(http_client, year=year, team=team)
    return {"games": games}

@app.get("/venues")
async def get_venues():
    client = CFBDClient()
    async with httpx.AsyncClient() as http_client:
        venues = await client.get_venues(http_client)
    return {"venues": venues}

@app.get("/sp_ratings")
async def get_sp_ratings(year: int = 2024):
    client = CFBDClient()
    async with httpx.AsyncClient() as http_client:
        ratings = await client.get_sp_ratings(http_client, year=year)
    return {"ratings": ratings}

@app.get("/stats")
async def get_team_season_stats(year: int = 2024):
    client = CFBDClient()
    async with httpx.AsyncClient() as http_client:
        stats = await client.get_team_season_stats(http_client, year=year)
    return {"stats": stats}

@app.get("/ppa")
async def get_team_ppa(year: int = 2024):
    client = CFBDClient()
    async with httpx.AsyncClient() as http_client:
        ppa = await client.get_team_ppa(http_client, year=year)
    return {"ppa": ppa}

# -----------------------
# Odds API
# -----------------------
@app.get("/odds")
async def get_odds():
    client = OddsClient()
    async with httpx.AsyncClient() as http_client:
        odds = await client.get_odds(http_client)
    return {"odds": odds}

# -----------------------
# Local Run
# -----------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
