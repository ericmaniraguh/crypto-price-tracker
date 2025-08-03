# main.py
from utils.fetcher import fetch_crypto_data
from utils.processor import add_enhanced_columns, process_crypto_data
from utils.analyzer import get_top_gainers, get_top_losers, generate_market_summary
from utils.display import (
    display_market_cap_leaders,
    display_top_gainers,
    display_top_losers,
    display_market_summary,
)
from utils.saver import save_all_datasets

def main():
    print("=" * 60)
    print("🚀 Starting Cryptocurrency Data Fetch & Analysis")
    print("=" * 60)

    raw_data = fetch_crypto_data()
    if not raw_data:
        print("No data fetched. Exiting.")
        return

    enhanced = add_enhanced_columns(raw_data)
    processed = process_crypto_data(enhanced)

    top_gainers = get_top_gainers(processed)
    top_losers = get_top_losers(processed)
    summary = generate_market_summary(processed)

    display_market_cap_leaders(processed, 10)
    display_top_gainers(top_gainers)
    display_top_losers(top_losers)
    display_market_summary(summary)

    save_all_datasets(enhanced, processed, top_gainers, top_losers)

    print("\n✅ Analysis complete. Data saved successfully.")

if __name__ == '__main__':
    main()
else:
    print('Crypto Analyzer Started (imported as a module)')
