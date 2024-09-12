import json

import requests
import settings


def auth() -> dict:
    """
    KIS ACCESS TOKEN
    """
    return requests.post(
        f"{settings.BASE_URL}/oauth2/tokenP",
        headers={"content-type": "application/json"},
        data=json.dumps(
            {
                "grant_type": "client_credentials",
                "appkey": settings.APP_KEY,
                "appsecret": settings.APP_SECRET,
            }
        ),
    ).json()
