from pathlib import Path
from decouple import config
import typer


def recent_access_token() -> str:
    """
    Extract the most recent access token from auth.csv
    csv headers: authenticated_at, revoked_at, access_token

    :returns: recent access token
    """
    try:
        with open(AUTH_CSV_PATH) as f:
            return f.readlines()[-1].split(",")[2].strip()
    except FileNotFoundError:
        return ""


APP_NAME = "kis-research-platform"
APP_DIR = typer.get_app_dir(APP_NAME)
APP_KEY = config("APP_KEY")
APP_SECRET = config("APP_SECRET")
BASE_URL = "https://openapi.koreainvestment.com:9443"  # Actual account
AUTH_CSV_PATH = Path(APP_DIR) / "auth.csv"
AUTH_CSV_PATH.parent.mkdir(exist_ok=True, parents=True)
AUTH_TOKEN = recent_access_token()
