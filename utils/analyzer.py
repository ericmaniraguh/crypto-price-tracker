# Analyze top gainers and losers
from typing import List, Dict

def get_top_gainers(data: List[Dict], limit=10):
    gainers = [c for c in data if c['price_change_24h'] > 0]
    top = sorted(gainers, key=lambda x: x['price_change_24h'], reverse=True)[:limit]
    for i, coin in enumerate(top, 1):
        coin['gainer_rank'] = i
    return top

def get_top_losers(data: List[Dict], limit=10):
    losers = [c for c in data if c['price_change_24h'] < 0]
    top = sorted(losers, key=lambda x: x['price_change_24h'])[:limit]
    for i, coin in enumerate(top, 1):
        coin['loser_rank'] = i
    return top

def generate_market_summary(data: List[Dict]):
    if not data: return {}
    total = len(data)
    gainers = [c for c in data if c['price_change_24h'] > 0]
    losers = [c for c in data if c['price_change_24h'] < 0]
    neutral = [c for c in data if c['price_change_24h'] == 0]
    top_gainer = max(data, key=lambda x: x['price_change_24h'])
    top_loser = min(data, key=lambda x: x['price_change_24h'])
    return {
        'total_coins': total,
        'gainers_count': len(gainers),
        'losers_count': len(losers),
        'neutral_count': len(neutral),
        'gainers_percentage': len(gainers) / total * 100,
        'losers_percentage': len(losers) / total * 100,
        'top_gainer': top_gainer,
        'top_loser': top_loser
    }
