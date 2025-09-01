import yaml
from pathlib import Path

class Predictor:
    def __init__(self, config_path="config.yaml", model="neutral"):
        self.config_path = Path(config_path)
        self.model = model
        self.config = self._load_config()

    def _load_config(self):
        with open(self.config_path, "r") as f:
            full_cfg = yaml.safe_load(f)

        # Support both v1 (flat config) and v2 (models: block)
        if "models" in full_cfg:
            cfg = full_cfg["models"].get(self.model)
            if not cfg:
                raise ValueError(f"Model '{self.model}' not found in config.yaml")
            return cfg
        else:
            return full_cfg  # fallback for old v1 format

    def evaluate_game(self, game_data, odds_line):
        """
        Compare model prediction vs Vegas line and return recommendation.
        - game_data: dict with stats, ratings, injuries, etc.
        - odds_line: dict with spread / total lines.
        """
        risk_cfg = self.config.get("risk", {})
        weights_cfg = self.config.get("weights", {})

        # Example: pretend we have a calculated predicted_spread
        predicted_spread = game_data.get("predicted_spread", 0)
        vegas_spread = odds_line.get("spread", 0)

        edge = predicted_spread - vegas_spread

        # Decide if we fire a play
        threshold = risk_cfg.get("edge_threshold_spread_pts", 2.0)
        big_edge = risk_cfg.get("big_edge_spread_pts", 4.0)

        if abs(edge) >= big_edge:
            confidence = "BIG"
        elif abs(edge) >= threshold:
            confidence = "SMALL"
        else:
            confidence = "PASS"

        return {
            "model": self.model,
            "predicted_spread": predicted_spread,
            "vegas_spread": vegas_spread,
            "edge": edge,
            "recommendation": confidence,
        }
