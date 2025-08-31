from fastapi import FastAPI, Query
import httpx
import os
from fetchers import CFBDClient

app = FastAPI()


# -------------------------------
# Debugging Endpoint
# -------------------------------
@app.get("/debug-env")
def debug_env():
    return {
        "cfbd_key_set": bool(os.getenv("CFBD_KEY")),
        "odds_key_set": bool(os.getenv("ODDS_KEY"))
    }


# -------------------------------
# Helper function to collect game data
# -------------------------------
async def build_game_data(year: int = 2024):
    cfbd = CFBDClient()
    async with httpx.AsyncClient() as client:
        stats = await cfbd.get_team_season_stats(client, year=year)
        sp = await cfbd.get_sp_ratings(client, year=year)
        ppa = await cfbd.get_team_ppa(client, year=year)
    return {"stats": stats, "sp": sp, "ppa": ppa}


# -------------------------------
# Prediction Endpoint
# -------------------------------
@app.get("/predict")
async def predict(model: str = Query("conservative", enum=["conservative", "aggressive", "both"]), year: int = 2024):
    game_data = await build_game_data(year)

    if model == "conservative":
        return {"model": "conservative", "result": "Conservative prediction logic TBD", "data": game_data}
    elif model == "aggressive":
        return {"model": "aggressive", "result": "Aggressive prediction logic TBD", "data": game_data}
    else:
        return {
            "model": "both",
            "conservative_result": "Conservative prediction logic TBD",
            "aggressive_result": "Aggressive prediction logic TBD",
            "data": game_data,
        }
