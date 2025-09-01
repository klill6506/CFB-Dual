import os
import httpx

class CFBDClient:
    BASE_URL = "https://api.collegefootballdata.com"

    def __init__(self):
        self.api_key = os.getenv("CFBD_API_KEY", "juKNtF767RJrxEQYHr/uyFsNnTw6IXtJdOvqmLyNEw6wc/JPKFr5WL+8ecFqc4VU")  # fallback for Pyto

    async def get_games_for_team(self, client, year: int, team: str):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.BASE_URL}/games?year={year}&team={team}"
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
