class HandicappingModel:
    def __init__(self, config, label="model"):
        self.config = config
        self.label = label

    def calculate_edge(self, game_data):
        edge = 0.0

        # Injuries
        if game_data.get("qb1_out"):
            edge -= self.config["injuries"]["qb1_out_pts"]
        elif game_data.get("qb1_limited"):
            edge -= self.config["injuries"]["qb1_limited_pts"]

        for _ in game_data.get("important_starters_out", []):
            edge -= self.config["injuries"]["important_starter_out_pts"]

        # Situational
        if game_data.get("bye_week"):
            edge += self.config["situational"]["bye_week_bonus_pts"]
        if game_data.get("trap_game"):
            edge -= self.config["situational"]["trap_game_penalty_pts"]
        if game_data.get("east_to_west_travel"):
            edge -= self.config["situational"]["east_west_travel_penalty_pts"]

        # Matchups
        edge += min(self.config["matchups"]["max_nudge_pts"],
                    game_data.get("matchup_score", 0))

        # Explosiveness
        if game_data.get("explosiveness", 0) > 0:
            edge += self.config["explosiveness"]["boost_pts"]

        # Weather
        if game_data.get("bad_weather"):
            edge -= self.config["weather"]["bad_weather_penalty_pts"]
        if game_data.get("cold_weather_south_team"):
            edge -= self.config["weather"]["cold_weather_south_team_penalty_pts"]

        # Home field
        if game_data.get("home_team"):
            edge += self.config["home_field"]["base_hfa_pts"]

        return edge
