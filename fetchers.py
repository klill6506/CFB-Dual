import httpx

class CFBDClient:
    def __init__(self):
        # 🔑 Hardcoded CFBD API key
        self.api_key = "juKNtF767RJrxEQYHr/uyFsNnTw6IXtJdOvqmLyNEw6wc/JPKFr5WL+8ecFqc4VU"
        self.base_url = "https://api.collegefootballdata.com"

    async def _safe_get(self, client, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_games_for_team(self, client, year, team):
        return await self._safe_get(client, "/games", params={"year": year, "team": team})

    async def get_team_season_stats(self, client, year):
        return await self._safe_get(client, "/stats/season", params={"year": year})

    async def get_team_ppa(self, client, year):
        return await self._safe_get(client, "/ppa/teams", params={"year": year})

    async def get_venues(self, client):
        return await self._safe_get(client, "/venues")

    async def get_sp_ratings(self, client, year):
        return await self._safe_get(client, "/ratings/sp", params={"year": year})


class OddsClient:
    def __init__(self):
        # 🔑 Hardcoded Odds API key
        self.api_key = "e13fa7a40bc707bb7738b7e08a451760"
        self.base_url = "https://api.the-odds-api.com/v4"

    async def _safe_get(self, client, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        headers = {}
        if self.api_key:
            params = params or {}
            params["apiKey"] = self.api_key
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_odds(self, client, sport="americanfootball_ncaaf", regions="us", markets="h2h,spreads", oddsFormat="decimal"):
        return await self._safe_get(
            client,
            f"/sports/{sport}/odds",
            params={"regions": regions, "markets": markets, "oddsFormat": oddsFormat}
        )
