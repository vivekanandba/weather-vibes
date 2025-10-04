import json
from pathlib import Path
from typing import Dict, Any, List
from app.services.scoring_service import (
    score_low_is_better,
    score_high_is_better,
    score_optimal_range,
    calculate_weighted_score
)


class VibeEngine:
    """Core engine for managing vibes and calculating vibe scores."""

    def __init__(self, config_path: str = "config/vibe_dictionary.json"):
        self.config_path = Path(config_path)
        self.vibes: Dict[str, Any] = {}
        self.load_vibes()

    def load_vibes(self):
        """Load vibe configurations from JSON file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Vibe dictionary not found at {self.config_path}")

        with open(self.config_path, 'r') as f:
            self.vibes = json.load(f)

        print(f"Loaded {len(self.vibes)} vibes from {self.config_path}")

    def get_vibe_config(self, vibe_id: str) -> Dict[str, Any]:
        """
        Get configuration for a specific vibe.

        Args:
            vibe_id: The vibe identifier

        Returns:
            Dictionary containing vibe configuration

        Raises:
            ValueError: If vibe_id is not found
        """
        if vibe_id not in self.vibes:
            raise ValueError(f"Vibe '{vibe_id}' not found. Available vibes: {list(self.vibes.keys())}")
        return self.vibes[vibe_id]

    def get_required_parameters(self, vibe_id: str) -> List[str]:
        """
        Get list of required parameters for a vibe.

        Args:
            vibe_id: The vibe identifier

        Returns:
            List of parameter IDs required for this vibe
        """
        config = self.get_vibe_config(vibe_id)

        if config.get("type") == "advisor":
            return config["parameters"]

        return [param["id"] for param in config["parameters"]]

    def calculate_vibe_score(
        self,
        vibe_id: str,
        parameter_values: Dict[str, float]
    ) -> float:
        """
        Calculate the vibe score based on parameter values.

        Args:
            vibe_id: The vibe identifier
            parameter_values: Dictionary mapping parameter IDs to their values

        Returns:
            Score from 0-100

        Raises:
            ValueError: If vibe is an advisor type (advisors use custom logic)
        """
        config = self.get_vibe_config(vibe_id)

        if config.get("type") == "advisor":
            raise ValueError("Advisors use custom logic, not scoring")

        parameter_scores = {}
        weights = {}

        for param_config in config["parameters"]:
            param_id = param_config["id"]
            weight = param_config["weight"]
            scoring_method = param_config["scoring"]

            value = parameter_values.get(param_id)
            if value is None:
                continue

            # Score based on method
            if scoring_method == "low_is_better":
                score = score_low_is_better(
                    value,
                    param_config["min"],
                    param_config["max"]
                )
            elif scoring_method == "high_is_better":
                score = score_high_is_better(
                    value,
                    param_config["min"],
                    param_config["max"]
                )
            elif scoring_method == "optimal_range":
                score = score_optimal_range(
                    value,
                    param_config["optimal_min"],
                    param_config["optimal_max"],
                    param_config.get("falloff_rate", 2.0)
                )
            else:
                raise ValueError(f"Unknown scoring method: {scoring_method}")

            parameter_scores[param_id] = score
            weights[param_id] = weight

        return calculate_weighted_score(parameter_scores, weights)

    def list_vibes(self) -> List[Dict[str, str]]:
        """
        List all available vibes with their names and descriptions.

        Returns:
            List of dictionaries containing vibe metadata
        """
        return [
            {
                "id": vibe_id,
                "name": config.get("name", vibe_id),
                "description": config.get("description", ""),
                "type": config.get("type", "standard")
            }
            for vibe_id, config in self.vibes.items()
        ]


# Global instance - will be initialized in main.py
vibe_engine: VibeEngine = None


def get_vibe_engine() -> VibeEngine:
    """Get the global vibe engine instance."""
    if vibe_engine is None:
        raise RuntimeError("Vibe engine not initialized")
    return vibe_engine
