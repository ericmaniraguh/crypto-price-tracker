# Fetch data from API
# utils/fetcher.py
import requests, time
from datetime import datetime
from typing import List, Dict, Optional

def fetch_crypto_data() -> Optional[List[Dict]]:
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': 1,
        'sparkline': False,
        'price_change_percentage': '24h'
    }

    try:
        print("Applying rate limit (6 seconds)...")
        time.sleep(6)
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"Fetched {len(data)} coins at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return data
    except Exception as e:
        print(f"Fetch error: {e}")
        return None
