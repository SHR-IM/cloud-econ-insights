import requests

BASE_URL = "https://api.worldbank.org/v2"

def fetch_indicator_value(country_code, indicator_code, year):
    """
    Fetches value of an indicator for a given country and year.
    Handles slow API responses gracefully.
    """

    url = f"{BASE_URL}/country/{country_code}/indicator/{indicator_code}"
    params = {
        "format": "json",
        "date": str(year),
        "per_page": 1     # speeds up response dramatically
    }

    try:
        resp = requests.get(url, params=params, timeout=25)
    except requests.exceptions.Timeout:
        print("World Bank API timeout")
        return None
    except Exception as e:
        print(f"API error: {e}")
        return None

    if not resp.ok:
        print(f"Bad response: {resp.status_code}")
        return None

    try:
        data = resp.json()
        records = data[1]       # second element contains the data array
        if not records:
            return None
        value = records[0].get("value")
        return value
    except Exception as e:
        print(f"JSON parse error: {e}")
        return None
