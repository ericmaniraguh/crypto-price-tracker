import requests
import json
import csv
import pandas as pd
import time
from datetime import datetime
from typing import List, Dict, Optional

# =============================================================================
# DATA FETCHING FUNCTIONS
# =============================================================================

def fetch_crypto_data() -> Optional[List[Dict]]:
    """
    Fetch cryptocurrency data from CoinGecko API
    Returns top 250 cryptocurrencies by market cap
    """
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
        
        if response.status_code == 200:
            data = response.json()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Successfully fetched {len(data)} cryptocurrencies at {timestamp}")
            return data
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        print("Tip: You may have hit the rate limit. Wait a few minutes before trying again.")
        return None

# =============================================================================
# DATA PROCESSING FUNCTIONS
# =============================================================================

def add_enhanced_columns(data: List[Dict]) -> List[Dict]:
    """
    Add new columns to the cryptocurrency data
    """
    today = datetime.now().strftime('%d-%m-%Y')
    
    for coin in data:
        # Add today's date
        coin['date'] = today
        
        # Handle price change safely - fix for None values
        price_change = coin.get('price_change_percentage_24h')
        if price_change is None:
            coin['price_change_24h'] = 0.0
            coin['change_symbol'] = "DOWN"
        else:
            coin['price_change_24h'] = float(price_change)
            coin['change_symbol'] = "UP" if price_change > 0 else "DOWN"
    
    return data

def process_crypto_data(data: List[Dict]) -> List[Dict]:
    """
    Process and clean the cryptocurrency data
    """
    processed_data = []
    
    for coin in data:
        # Safely handle all potential None values
        price_change = coin.get('price_change_24h', 0)
        if price_change is None:
            price_change = 0.0
        
        processed_coin = {
            'id': coin.get('id', ''),
            'rank': coin.get('market_cap_rank'),
            'name': coin.get('name', ''),
            'symbol': coin.get('symbol', '').upper(),
            'current_price': coin.get('current_price'),
            'price_change_24h': price_change,
            'change_symbol': coin.get('change_symbol', 'DOWN'),
            'market_cap': coin.get('market_cap'),
            'volume_24h': coin.get('total_volume'),
            'ath': coin.get('ath'),
            'image': coin.get('image', ''),
            'date': coin.get('date', ''),
            'last_updated': coin.get('last_updated', '')
        }
        processed_data.append(processed_coin)
    
    # Sort by market cap rank (ascending order - rank 1 first)
    processed_data.sort(key=lambda x: x['rank'] if x['rank'] is not None else float('inf'))
    
    # Add sequential numbering
    for i, coin in enumerate(processed_data, 1):
        coin['number'] = i
    
    return processed_data

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def get_top_gainers(processed_data: List[Dict], limit: int = 10) -> List[Dict]:
    """
    Get top N cryptocurrencies with highest positive price changes
    """
    # Filter only positive changes and sort by price change (descending)
    gainers = []
    for coin in processed_data:
        price_change = coin.get('price_change_24h', 0)
        if price_change is not None and price_change > 0:
            gainers.append(coin)
    
    # Sort by price change (highest first)
    top_gainers = sorted(gainers, key=lambda x: x.get('price_change_24h', 0), reverse=True)[:limit]
    
    # Add gainer ranking
    for i, coin in enumerate(top_gainers, 1):
        coin['gainer_rank'] = i
    
    return top_gainers

def get_top_losers(processed_data: List[Dict], limit: int = 10) -> List[Dict]:
    """
    Get top N cryptocurrencies with highest negative price changes
    """
    # Filter only negative changes and sort by price change (ascending - most negative first)
    losers = []
    for coin in processed_data:
        price_change = coin.get('price_change_24h', 0)
        if price_change is not None and price_change < 0:
            losers.append(coin)
    
    # Sort by price change (most negative first)
    top_losers = sorted(losers, key=lambda x: x.get('price_change_24h', 0))[:limit]
    
    # Add loser ranking
    for i, coin in enumerate(top_losers, 1):
        coin['loser_rank'] = i
    
    return top_losers

def generate_market_summary(processed_data: List[Dict]) -> Dict:
    """
    Generate comprehensive market summary
    """
    if not processed_data:
        return {}
    
    total_coins = len(processed_data)
    gainers = [coin for coin in processed_data if coin.get('price_change_24h', 0) > 0]
    losers = [coin for coin in processed_data if coin.get('price_change_24h', 0) < 0]
    neutral = [coin for coin in processed_data if coin.get('price_change_24h', 0) == 0]
    
    # Find top performer and worst performer
    top_gainer = max(processed_data, key=lambda x: x.get('price_change_24h', 0) if x.get('price_change_24h') is not None else 0)
    top_loser = min(processed_data, key=lambda x: x.get('price_change_24h', 0) if x.get('price_change_24h') is not None else 0)
    
    summary = {
        'total_coins': total_coins,
        'gainers_count': len(gainers),
        'losers_count': len(losers),
        'neutral_count': len(neutral),
        'gainers_percentage': (len(gainers) / total_coins * 100) if total_coins > 0 else 0,
        'losers_percentage': (len(losers) / total_coins * 100) if total_coins > 0 else 0,
        'top_gainer': top_gainer,
        'top_loser': top_loser
    }
    
    return summary

# =============================================================================
# DISPLAY FUNCTIONS
# =============================================================================

def display_market_cap_leaders(processed_data: List[Dict], limit: int = 10) -> None:
    """
    Display top cryptocurrencies by market cap
    """
    print(f"\nTop {limit} Cryptocurrencies by Market Cap:")
    print("-" * 100)
    print(f"{'No.':<4} {'Rank':<5} {'Name':<20} {'Symbol':<8} {'Price (USD)':<12} {'24h Change':<12} {'Market Cap':<15}")
    print("-" * 100)
    
    for coin in processed_data[:limit]:
        number = coin.get('number', 'N/A')
        rank = coin.get('rank', 'N/A')
        price_change = coin.get('price_change_24h', 0)
        change_symbol = coin.get('change_symbol', 'DOWN')
        
        # Handle None values safely
        price = coin.get('current_price')
        market_cap = coin.get('market_cap')
        
        price_str = f"${price:,.2f}" if price is not None else "N/A"
        change_str = f"{change_symbol} {abs(price_change):.2f}%" if price_change is not None else "N/A"
        market_cap_str = f"${market_cap:,.0f}" if market_cap is not None else "N/A"
        
        print(f"{number:<4} {rank:<5} {coin['name'][:18]:<20} {coin['symbol']:<8} {price_str:<12} {change_str:<12} {market_cap_str:<15}")

def display_top_gainers(top_gainers: List[Dict]) -> None:
    """
    Display top gainers in a formatted way
    """
    if not top_gainers:
        print("\nNo gainers found in the current data.")
        return
        
    print(f"\nTop {len(top_gainers)} Gainers (24h Price Change):")
    print("-" * 100)
    print(f"{'No.':<4} {'Rank':<5} {'Name':<20} {'Symbol':<8} {'Price (USD)':<12} {'24h Change':<12} {'Market Cap':<15}")
    print("-" * 100)
    
    for coin in top_gainers:
        gainer_rank = coin.get('gainer_rank', 'N/A')
        rank = coin.get('rank', 'N/A')
        price_change = coin.get('price_change_24h', 0)
        
        # Handle None values safely
        price = coin.get('current_price')
        market_cap = coin.get('market_cap')
        
        price_str = f"${price:,.2f}" if price is not None else "N/A"
        change_str = f"UP {price_change:.2f}%" if price_change is not None else "N/A"
        market_cap_str = f"${market_cap:,.0f}" if market_cap is not None else "N/A"
        
        print(f"{gainer_rank:<4} {rank:<5} {coin['name'][:18]:<20} {coin['symbol']:<8} {price_str:<12} {change_str:<12} {market_cap_str:<15}")

def display_top_losers(top_losers: List[Dict]) -> None:
    """
    Display top losers in a formatted way
    """
    if not top_losers:
        print("\nNo losers found in the current data.")
        return
        
    print(f"\nTop {len(top_losers)} Losers (24h Price Change):")
    print("-" * 100)
    print(f"{'No.':<4} {'Rank':<5} {'Name':<20} {'Symbol':<8} {'Price (USD)':<12} {'24h Change':<12} {'Market Cap':<15}")
    print("-" * 100)
    
    for coin in top_losers:
        loser_rank = coin.get('loser_rank', 'N/A')
        rank = coin.get('rank', 'N/A')
        price_change = coin.get('price_change_24h', 0)
        
        # Handle None values safely
        price = coin.get('current_price')
        market_cap = coin.get('market_cap')
        
        price_str = f"${price:,.2f}" if price is not None else "N/A"
        change_str = f"DOWN {abs(price_change):.2f}%" if price_change is not None else "N/A"
        market_cap_str = f"${market_cap:,.0f}" if market_cap is not None else "N/A"
        
        print(f"{loser_rank:<4} {rank:<5} {coin['name'][:18]:<20} {coin['symbol']:<8} {price_str:<12} {change_str:<12} {market_cap_str:<15}")

def display_market_summary(summary: Dict) -> None:
    """
    Display market summary statistics
    """
    if not summary:
        print("\nNo market summary data available.")
        return
        
    print(f"\nMarket Summary:")
    print("-" * 60)
    print(f"Total Coins Analyzed: {summary['total_coins']}")
    print(f"Gainers: {summary['gainers_count']} ({summary['gainers_percentage']:.1f}%)")
    print(f"Losers: {summary['losers_count']} ({summary['losers_percentage']:.1f}%)")
    print(f"Neutral: {summary['neutral_count']}")
    
    top_gainer = summary['top_gainer']
    top_loser = summary['top_loser']
    
    gainer_change = top_gainer.get('price_change_24h', 0)
    loser_change = top_loser.get('price_change_24h', 0)
    
    print(f"Biggest Gainer: {top_gainer['name']} (+{gainer_change:.2f}%)")
    print(f"Biggest Loser: {top_loser['name']} ({loser_change:.2f}%)")

# =============================================================================
# FILE SAVING FUNCTIONS
# =============================================================================

def save_to_csv(data: List[Dict], filename: str) -> bool:
    """
    Save data to CSV file with error handling
    """
    if not data:
        print(f"No data to save to {filename}")
        return False
    
    try:
        df = pd.DataFrame(data)
        
        # Define preferred column order
        preferred_columns = ['number', 'rank', 'gainer_rank', 'loser_rank', 'name', 'symbol', 
                           'current_price', 'price_change_24h', 'change_symbol', 'market_cap', 
                           'volume_24h', 'ath', 'id', 'image', 'date', 'last_updated']
        
        # Reorder columns
        available_columns = [col for col in preferred_columns if col in df.columns]
        remaining_columns = [col for col in df.columns if col not in available_columns]
        final_columns = available_columns + remaining_columns
        
        df = df[final_columns]
        df.to_csv(filename, index=False)
        print(f"CSV saved successfully: {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving CSV {filename}: {e}")
        return False

def save_to_json(data: List[Dict], filename: str) -> bool:
    """
    Save data to JSON file with error handling
    """
    if not data:
        print(f"No data to save to {filename}")
        return False
        
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"JSON saved successfully: {filename}")
        return True
    except Exception as e:
        print(f"Error saving JSON {filename}: {e}")
        return False

def save_all_datasets(raw_data: List[Dict], processed_data: List[Dict], 
                     top_gainers: List[Dict], top_losers: List[Dict]) -> None:
    """
    Save all datasets to their respective files
    """
    today = datetime.now().strftime('%d-%m-%Y')
    
    print("\nSaving data files...")
    
    # Define all files to save
    files_to_save = [
        (raw_data, f'crypto_data_{today}.json', 'json'),
        (raw_data, f'crypto_data_{today}.csv', 'csv'),
        (processed_data, f'processed_crypto_data_{today}.csv', 'csv'),
        (top_gainers, f'top_10_positive_{today}.csv', 'csv'),
        (top_losers, f'top_10_negative_{today}.csv', 'csv')
    ]
    
    # Save each file
    success_count = 0
    for data, filename, file_type in files_to_save:
        if file_type == 'json':
            if save_to_json(data, filename):
                success_count += 1
        else:  # csv
            if save_to_csv(data, filename):
                success_count += 1
    
    print(f"\nSuccessfully saved {success_count}/{len(files_to_save)} files")

# =============================================================================
# MAIN EXECUTION FUNCTION
# =============================================================================

def main():
    """
    Main function to orchestrate all cryptocurrency data operations
    """
    print("=" * 70)
    print("CRYPTOCURRENCY DATA FETCHER & ANALYZER")
    print("=" * 70)
    print("Note: This process includes rate limiting to prevent API blocking")
    
    try:
        # Step 1: Data Fetching
        print("\n1. FETCHING DATA")
        print("-" * 30)
        raw_data = fetch_crypto_data()
        
        if not raw_data:
            print("Failed to fetch cryptocurrency data. Exiting...")
            return
        
        # Step 2: Data Processing
        print("\n2. PROCESSING DATA")
        print("-" * 30)
        enhanced_data = add_enhanced_columns(raw_data)
        processed_data = process_crypto_data(enhanced_data)
        
        # Step 3: Data Analysis
        print("\n3. ANALYZING PERFORMANCE")
        print("-" * 30)
        top_gainers = get_top_gainers(processed_data, 10)
        top_losers = get_top_losers(processed_data, 10)
        market_summary = generate_market_summary(processed_data)
        
        print(f"Analysis complete:")
        print(f"  - Processed {len(processed_data)} cryptocurrencies")
        print(f"  - Found {len(top_gainers)} top gainers")
        print(f"  - Found {len(top_losers)} top losers")
        
        # Step 4: Display Results
        print("\n4. DISPLAYING RESULTS")
        print("-" * 30)
        display_market_cap_leaders(processed_data, 10)
        display_top_gainers(top_gainers)
        display_top_losers(top_losers)
        display_market_summary(market_summary)
        
        # Step 5: Save Data
        print("\n5. SAVING DATA")
        print("-" * 30)
        save_all_datasets(enhanced_data, processed_data, top_gainers, top_losers)
        
        # Step 6: Final Summary
        print("\n6. COMPLETION SUMMARY")
        print("-" * 30)
        print("✅ All operations completed successfully!")
        
        today = datetime.now().strftime('%d-%m-%Y')
        print(f"\nFiles created today ({today}):")
        print(f"  1. crypto_data_{today}.json (raw data)")
        print(f"  2. crypto_data_{today}.csv (enhanced raw data)")
        print(f"  3. processed_crypto_data_{today}.csv (processed data)")
        print(f"  4. top_10_positive_{today}.csv (top gainers)")
        print(f"  5. top_10_negative_{today}.csv (top losers)")
        
        print(f"\n📊 Statistics:")
        print(f"  - Total cryptocurrencies: {len(processed_data)}")
        print(f"  - Market gainers: {market_summary['gainers_count']} ({market_summary['gainers_percentage']:.1f}%)")
        print(f"  - Market losers: {market_summary['losers_count']} ({market_summary['losers_percentage']:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error in main execution: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n💡 Pro Tip: For frequent updates, consider upgrading to CoinGecko Pro API")
    print("=" * 70)

if __name__ == "__main__":
    main()