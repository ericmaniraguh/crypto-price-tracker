# utils/display.py

def display_market_cap_leaders(processed_data, limit=10):
    print(f"\nTop {limit} Cryptocurrencies by Market Cap:")
    print("-" * 80)
    print(f"{'Rank':<5} {'Name':<20} {'Symbol':<8} {'Price':<15} {'24h Change':<12} {'Market Cap':<15}")
    print("-" * 80)

    for coin in processed_data[:limit]:
        rank = coin.get('rank', 'N/A')
        name = coin.get('name', '')
        symbol = coin.get('symbol', '').upper()
        price = coin.get('current_price')
        price_change = coin.get('price_change_24h', 0)
        market_cap = coin.get('market_cap')

        price_str = f"${price:,.2f}" if price else "N/A"
        change_str = f"{price_change:+.2f}%" if price_change else "N/A"
        market_cap_str = f"${market_cap:,.0f}" if market_cap else "N/A"

        print(f"{rank:<5} {name:<20} {symbol:<8} {price_str:<15} {change_str:<12} {market_cap_str:<15}")


def display_top_gainers(top_gainers, limit=10):
    print(f"\nTop {limit} Market Gainers (24h):")
    print("-" * 50)
    print(f"{'Name':<20} {'Symbol':<10} {'24h Change':<10}")
    print("-" * 50)

    for coin in top_gainers[:limit]:
        name = coin.get('name', 'N/A')
        symbol = coin.get('symbol', 'N/A').upper()
        change = coin.get('price_change_24h', 0)
        print(f"{name:<20} {symbol:<10} +{change:.2f}%")


def display_top_losers(top_losers, limit=10):
    print(f"\nTop {limit} Market Losers (24h):")
    print("-" * 50)
    print(f"{'Name':<20} {'Symbol':<10} {'24h Change':<10}")
    print("-" * 50)

    for coin in top_losers[:limit]:
        name = coin.get('name', 'N/A')
        symbol = coin.get('symbol', 'N/A').upper()
        change = coin.get('price_change_24h', 0)
        print(f"{name:<20} {symbol:<10} {change:.2f}%")


def display_market_summary(summary):
    print("\nMarket Summary:")
    print("-" * 30)
    for key, value in summary.items():
        print(f"{key:<20}: {value}")
