import yaml
from pathlib import Path

class Predictor:
    def __init__(self, config_path="config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self):
        with open(self.config_path, "r") as f:
            full_cfg = yaml.safe_load(f)

        # For v1 (flat) configs, just return the whole file
        return full_cfg

    def evaluate_game(self, game_data, odds_line):
        """
        Compare model prediction vs Vegas line and return recommendation.
        - game_data: dict with stats, ratings, injuries, etc.
        - odds_line: dict with spread / total lines.
        """
        risk_cfg = self.config.get("risk", {})

        predicted_spread = game_data.get("predicted_spread", 0)
        vegas_spread = odds_line.get("spread", 0)
        edge = predicted_spread - vegas_spread

        # Thresholds from config
        threshold = risk_cfg.get("edge_threshold_spread_pts", 2.0)
        big_edge = risk_cfg.get("big_edge_spread_pts", 4.0)

        if abs(edge) >= big_edge:
            confidence = "BIG"
        elif abs(edge) >= threshold:
            confidence = "SMALL"
        else:
            confidence = "PASS"

        return {
            "predicted_spread": predicted_spread,
            "vegas_spread": vegas_spread,
            "edge": edge,
            "recommendation": confidence,
        }
