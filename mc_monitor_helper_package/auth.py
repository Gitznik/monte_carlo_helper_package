import os
from dataclasses import dataclass


@dataclass
class MonteCarloAuth:
    x_mcd_id: str
    x_mcd_token: str


def get_monte_carlo_auth_from_env():
    return MonteCarloAuth(
        x_mcd_id=str(os.environ.get("X_MCD_ID")),
        x_mcd_token=str(os.environ.get("X_MCD_TOKEN")),
    )
