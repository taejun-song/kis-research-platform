from datetime import datetime

import pandas as pd
import requests
from settings import APP_KEY, APP_SECRET, AUTH_TOKEN, BASE_URL


def historical_OHLCV(
    stock_code: str, start_date: str, end_date: str, period: str, adjusted: str
) -> pd.DataFrame | None:
    """
    :param stock_code: code of a stock eg) '005930' in general, 'Q500001' for ETN
    :param start_date: the initial date("YYYYMMDD") to look up eg) "20240909"
    :param end_date: the last date("YYYYMMDD") to look up eg) "20240910"
    :param period: "D" : daily candlesticks, "W": weekly candlesticks,
    "M": monthly candlesticks, "Y": yearly candlesticks
    :param adjusted: "0" if adjusted else "1"

    :return: dict
    """
    DOHLCV = [
        "stck_bsop_date",
        "stck_oprc",
        "stck_hgpr",
        "stck_lwpr",
        "stck_clpr",
        "acml_vol",
    ]

    # 호출
    res = requests.get(
        f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice",
        headers={
            "Content-Type": "application/json",
            "authorization": f"Bearer {AUTH_TOKEN}",
            "appKey": APP_KEY,
            "appSecret": APP_SECRET,
            "tr_id": "FHKST03010100",
        },
        params={
            "fid_cond_mrkt_div_code": "J",
            "fid_input_date_1": start_date,
            "fid_input_date_2": end_date,
            "fid_input_iscd": stock_code,
            "fid_org_adj_prc": "0",
            "fid_period_div_code": "D",
        },
    )

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        daily_ohlcv = dict()
        for daily_data in res.json()["output2"]:
            date, open, high, low, close, volume = map(
                lambda key: int(daily_data[key]),
                filter(lambda k: k in daily_data, DOHLCV),
            )
            daily_ohlcv[datetime.strptime(str(date), "%Y%m%d")] = {
                "o": open,
                "h": high,
                "l": low,
                "c": close,
                "v": volume,
            }
        return pd.DataFrame(daily_ohlcv).T.sort_index()
    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None
