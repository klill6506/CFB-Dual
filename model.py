class HandicappingModel:
    def __init__(self, config: dict, label: str = "default"):
        self.config = config
        self.label = label

    def calculate_edge(self, game_data: dict) -> dict:
        """
        Calculate betting edges based on spreads, totals, and adjustments.
        Expects game_data to include:
        - "odds": list of odds data (spreads, totals)
        - "stats": season stats
        - "ppa": team-level efficiency
        """
        results = []

        odds_list = game_data.get("odds", [])
        stats = game_data.get("stats", [])
        ppa = game_data.get("ppa", [])

        for game in odds_list:
            # Extract teams and lines
            home_team = game.get("home_team")
            away_team = game.get("away_team")
            bookmakers = game.get("bookmakers", [])

            # Default line placeholders
            spread, total = None, None

            # Grab average spread & total across books
            spread_values = []
            total_values = []

            for book in bookmakers:
                for market in book.get("markets", []):
                    if market["key"] == "spreads":
                        for outcome in market["outcomes"]:
                            if outcome.get("point") is not None:
                                spread_values.append(outcome["point"])
                    elif market["key"] == "totals":
                        for outcome in market["outcomes"]:
                            if outcome.get("point") is not None:
                                total_values.append(outcome["point"])

            if spread_values:
                spread = sum(spread_values) / len(spread_values)
            if total_values:
                total = sum(total_values) / len(total_values)

            # Base edge from config threshold
            edge = 0.0
            if spread is not None and abs(spread) >= self.config.get("spread_threshold", 3):
                edge += self.config.get("spread_weight", 1.0)

            if total is not None and (
                total <= self.config.get("low_total", 40) or total >= self.config.get("high_total", 65)
            ):
                edge += self.config.get("total_weight", 1.0)

            # Add bonuses from config
            edge += self.config.get("injury_qb", 0)
            edge += self.config.get("injury_other", 0)
            edge += self.config.get("travel_penalty", 0)
            edge += self.config.get("trap_game", 0)
            edge += self.config.get("matchup_adv", 0)
            edge += self.config.get("explosiveness", 0)
            edge += self.config.get("weather_penalty", 0)
            edge += self.config.get("cold_weather", 0)
            edge += self.config.get("home_field", 0)

            results.append({
                "home_team": home_team,
                "away_team": away_team,
                "spread": spread,
                "total": total,
                "edge": edge,
                "model": self.label,
            })

        return results
