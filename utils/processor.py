# Process and clean data

from datetime import datetime
from typing import List, Dict

def add_enhanced_columns(data: List[Dict]) -> List[Dict]:
    today = datetime.now().strftime('%d-%m-%Y')
    for coin in data:
        price_change = coin.get('price_change_percentage_24h')
        coin['date'] = today
        coin['price_change_24h'] = float(price_change) if price_change else 0.0
        coin['change_symbol'] = "UP" if coin['price_change_24h'] > 0 else "DOWN"
    return data

def process_crypto_data(data: List[Dict]) -> List[Dict]:
    processed = []
    for coin in data:
        processed.append({
            'id': coin.get('id', ''),
            'rank': coin.get('market_cap_rank'),
            'name': coin.get('name', ''),
            'symbol': coin.get('symbol', '').upper(),
            'current_price': coin.get('current_price'),
            'price_change_24h': coin.get('price_change_24h', 0),
            'change_symbol': coin.get('change_symbol', 'DOWN'),
            'market_cap': coin.get('market_cap'),
            'volume_24h': coin.get('total_volume'),
            'ath': coin.get('ath'),
            'image': coin.get('image', ''),
            'date': coin.get('date', ''),
            'last_updated': coin.get('last_updated', '')
        })
    processed.sort(key=lambda x: x['rank'] if x['rank'] else float('inf'))
    for i, coin in enumerate(processed, 1):
        coin['number'] = i
    return processed
