import httpx

# 🔑 Hardcoded API keys
CFBD_API_KEY = "juKNtF767RJrxEQYHr/uyFsNnTw6IXtJdOvqmLyNEw6wc/JPKFr5WL+8ecFqc4VU"
ODDS_API_KEY = "e13fa7a40bc707bb7738b7e08a451760"


class CFBDClient:
    BASE_URL = "https://api.collegefootballdata.com"

    async def _safe_get(self, client: httpx.AsyncClient, endpoint: str, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {CFBD_API_KEY}"}
        resp = await client.get(url, headers=headers, params=params)

        if resp.status_code != 200:
            print("⚠️ CFBD ERROR", resp.status_code, resp.text)  # Debug info
            resp.raise_for_status()

        try:
            return resp.json()
        except Exception as e:
            print("⚠️ JSON decode failed from CFBD:", e, "Response was:", resp.text)
            raise

    async def get_games_for_team(self, client: httpx.AsyncClient, year: int, team: str):
        return await self._safe_get(client, "/games", params={"year": year, "team": team})

    async def get_team_season_stats(self, client: httpx.AsyncClient, year: int):
        return await self._safe_get(client, "/stats/season", params={"year": year})


class OddsClient:
    BASE_URL = "https://api.the-odds-api.com/v4"

    async def _safe_get(self, client: httpx.AsyncClient, endpoint: str, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"x-api-key": ODDS_API_KEY}
        resp = await client.get(url, headers=headers, params=params)

        if resp.status_code != 200:
            print("⚠️ ODDS API ERROR", resp.status_code, resp.text)  # Debug info
            resp.raise_for_status()

        try:
            return resp.json()
        except Exception as e:
            print("⚠️ JSON decode failed from Odds API:", e, "Response was:", resp.text)
            raise

    async def get_odds(self, client: httpx.AsyncClient, sport: str = "americanfootball_ncaaf", regions: str = "us"):
        """Fetch odds for college football games"""
        return await self._safe_get(client, f"/sports/{sport}/odds", params={"regions": regions})
