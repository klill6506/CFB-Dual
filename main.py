from fastapi import FastAPI, Query
import httpx
import yaml
import os

from fetchers import CFBDClient, OddsClient
from model import HandicappingModel

app = FastAPI()


def load_config(model_name: str):
    """
    Load YAML config for either 'aggressive' or 'conservative' model.
    """
    filename = f"config_{model_name}.yaml"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Config file {filename} not found")
    with open(filename, "r") as f:
        return yaml.safe_load(f)


async def build_game_data(year: int = 2024):
    """
    Collects stats, PPA, and odds into a single dictionary.
    """
    game_data = {}
    cfbd = CFBDClient()
    odds = OddsClient()

    async with httpx.AsyncClient() as client:
        stats = await cfbd.get_team_season_stats(client, year=year)
        ppa = await cfbd.get_team_ppa(client, year=year)
        odds_data = await odds.get_odds(client)

    game_data["stats"] = stats
    game_data["ppa"] = ppa
    game_data["odds"] = odds_data
    return game_data


@app.get("/games")
async def get_games(team: str, year: int = 2024):
    """
    Fetch games for a specific team.
    """
    client = CFBDClient()
    async with httpx.AsyncClient() as http_client:
        games = await client.get_games_for_team(http_client, year=year, team=team)
    return {"games": games}


@app.get("/predict")
async def predict(
    model: str = Query("conservative", enum=["aggressive", "conservative", "both"]),
    year: int = 2024,
):
    """
    Run predictions using aggressive, conservative, or both models.
    """
    game_data = await build_game_data(year)

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