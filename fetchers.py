import httpx
import os

class CFBDClient:
    def __init__(self):
        self.api_key = os.getenv("CFBD_API_KEY", "").strip()
        self.base_url = "https://api.collegefootballdata.com"

    async def _safe_get(self, client: httpx.AsyncClient, endpoint: str, params: dict = None):
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = await client.get(url, headers=headers, params=params)
        try:
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return {
                "error": resp.status_code,
                "url": url,
                "body": resp.text[:300]  # show first 300 chars
            }

    async def get_games_for_team(self, client, year: int, team: str):
        return await self._safe_get(client, "/games", params={"year": year, "team": team})

    async def get_team_season_stats(self, client, year: int):
        return await self._safe_get(client, "/stats/season", params={"year": year})

    async def get_team_ppa(self, client, year: int):
        return await self._safe_get(client, "/ppa/teams", params={"year": year})

    async def get_venues(self, client):
        return await self._safe_get(client, "/venues")

    async def get_sp_ratings(self, client, year: int):
        return await self._safe_get(client, "/ratings/sp", params={"year": year})


class OddsClient:
    def __init__(self):
        self.api_key = os.getenv("ODDS_API_KEY", "").strip()
        self.base_url = "https://api.the-odds-api.com/v4/sports/americanfootball_ncaaf"

    async def _safe_get(self, client: httpx.AsyncClient, endpoint: str, params: dict = None):
        url = f"{self.base_url}{endpoint}"
        if params is None:
            params = {}
        params["apiKey"] = self.api_key
        resp = await client.get(url, params=params)
        try:
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return {
                "error": resp.status_code,
                "url": url,
                "body": resp.text[:300]
            }

    async def get_odds(self, client):
        return await self._safe_get(client, "/odds", params={"regions": "us", "markets": "h2h"})
