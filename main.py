from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from fetchers import CFBDClient, OddsClient

app = FastAPI(
    title="CFB Dual API",
    version="1.0.0",
    description="API for College Football Dual Model"
)

# --- Embed static OpenAPI schema directly ---
static_openapi = {
  "openapi": "3.0.0",
  "info": {
    "title": "CFB Dual API",
    "version": "1.0.0",
    "description": "API for College Football Dual Model"
  },
  "servers": [
    {
      "url": "https://cfbdual2.onrender.com"
    }
  ],
  "paths": {
    "/": {
      "get": {
        "summary": "Root",
        "operationId": "root",
        "responses": {
          "200": {
            "description": "Root status",
            "content": {
              "application/json": {
                "example": { "message": "CFB Dual API is running!" }
              }
            }
          }
        }
      }
    },
    "/games": {
      "get": {
        "summary": "Get games for a team",
        "operationId": "get_games",
        "parameters": [
          {
            "name": "team",
            "in": "query",
            "required": True,
            "schema": { "type": "string" }
          },
          {
            "name": "year",
            "in": "query",
            "required": False,
            "schema": { "type": "integer", "default": 2025 }
          }
        ],
        "responses": {
          "200": {
            "description": "List of games",
            "content": {
              "application/json": {
                "example": {
                  "games": ["Game1", "Game2"]
                }
              }
            }
          }
        }
      }
    },
    "/predict": {
      "get": {
        "summary": "Run prediction",
        "operationId": "predict",
        "parameters": [
          {
            "name": "model",
            "in": "query",
            "required": False,
            "schema": { "type": "string", "default": "conservative" }
          },
          {
            "name": "year",
            "in": "query",
            "required": False,
            "schema": { "type": "integer", "default": 2025 }
          }
        ],
        "responses": {
          "200": {
            "description": "Prediction result",
            "content": {
              "application/json": {
                "example": {
                  "model_used": "conservative",
                  "year": 2025,
                  "prediction": "This is a stub prediction."
                }
              }
            }
          }
        }
      }
    }
  }
}

# Override FastAPI’s default schema
@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    return JSONResponse(content=static_openapi)


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
