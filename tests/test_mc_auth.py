from dotenv import load_dotenv
from mc_monitor_helper_package.auth import (
    get_monte_carlo_auth,
    get_monte_carlo_auth_from_env,
)

load_dotenv()


def test_get_auth_from_env():
    auth = get_monte_carlo_auth_from_env()
    assert auth.x_mcd_id == "X_MCD_ID"
    assert auth.x_mcd_token == "X_MCD_TOKEN"


def test_get_auth_headers():
    auth = get_monte_carlo_auth_from_env()
    headers = auth.auth_headers
    assert headers["x-mcd-id"] == "X_MCD_ID"
    assert headers["x-mcd-token"] == "X_MCD_TOKEN"


def test_get_auth_from_args():
    auth = get_monte_carlo_auth("X_MCD_ID", "X_MCD_TOKEN")
    assert auth.x_mcd_id == "X_MCD_ID"
    assert auth.x_mcd_token == "X_MCD_TOKEN"
