import os
import httpx


class CFBDClient:
    BASE_URL = "https://api.collegefootballdata.com"

    def __init__(self):
        # ✅ Use env var if available, else fallback to your provided key
        self.api_key = os.getenv("CFBD_API_KEY", "juKNtF767RJrxEQYHr/uyFsNnTw6IXtJdOvqmLyNEw6wc/JPKFr5WL+8ecFqc4VU")

    async def get_games_for_team(self, client: httpx.AsyncClient, year: int, team: str):
        url = f"{self.BASE_URL}/games"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"year": year, "team": team}
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_team_season_stats(self, client: httpx.AsyncClient, year: int):
        url = f"{self.BASE_URL}/team/stats/season"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"year": year}
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_team_ppa(self, client: httpx.AsyncClient, year: int):
        url = f"{self.BASE_URL}/ppa/teams"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"year": year}
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_venues(self, client: httpx.AsyncClient):
        url = f"{self.BASE_URL}/venues"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    async def get_sp_ratings(self, client: httpx.AsyncClient, year: int):
        url = f"{self.BASE_URL}/ratings/sp"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"year": year}
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()


class OddsClient:
    BASE_URL = "https://api.the-odds-api.com/v4"

    def __init__(self):
        # ✅ Use env var if available, else fallback to your provided key
        self.api_key = os.getenv("ODDS_API_KEY", "e13fa7a40bc707bb7738b7e08a451760")

    async def get_odds(self, client: httpx.AsyncClient, sport="americanfootball_ncaaf", regions="us"):
        url = f"{self.BASE_URL}/sports/{sport}/odds"
        params = {
            "apiKey": self.api_key,
            "regions": regions,
        }
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
