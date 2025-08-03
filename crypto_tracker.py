import requests
import json
import csv
import pandas as pd
import time
from datetime import datetime

def fetch_crypto_data():
    """
    Fetch cryptocurrency data from CoinGecko API
    Returns top 250 cryptocurrencies by market cap
    
    IMPORTANT: Includes rate limiting to prevent API blocking
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
        # Rate limiting: Wait 6 seconds before making request
        print("Applying rate limit (6 seconds)...")
        time.sleep(6)
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully fetched {len(data)} cryptocurrencies")
            print(f"Data fetched at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Add new columns to the data
            enhanced_data = add_columns(data)
            
            # Save data to JSON and CSV files
            today = datetime.now().strftime('%d-%m-%Y')
            
            # Save as JSON
            json_filename = f'crypto_data_{today}.json'
            with open(json_filename, 'w') as f:
                json.dump(enhanced_data, f, indent=4)
            print(f"JSON data saved to: {json_filename}")
            
            # Save as CSV
            csv_filename = f'crypto_data_{today}.csv'
            save_to_csv(enhanced_data, csv_filename)
            print(f"CSV data saved to: {csv_filename}")
            
            return enhanced_data
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        print("Tip: You may have hit the rate limit. Wait a few minutes before trying again.")
        return None

def save_to_csv(data, filename):
    """
    Save cryptocurrency data to CSV file with proper column ordering
    """
    if not data:
        print("No data to save to CSV")
        return
    
    try:
        # Method 1: Using pandas (recommended)
        df = pd.DataFrame(data)
        
        # Reorder columns to put number and rank first
        columns = ['number', 'rank', 'name', 'symbol', 'current_price', 'price_change_24h', 
                  'change_symbol', 'market_cap', 'volume_24h', 'ath', 'id', 'image', 
                  'date', 'last_updated']
        
        # Only use columns that exist in the dataframe
        available_columns = [col for col in columns if col in df.columns]
        remaining_columns = [col for col in df.columns if col not in available_columns]
        final_columns = available_columns + remaining_columns
        
        df = df[final_columns]
        df.to_csv(filename, index=False)
        print(f"CSV saved successfully using pandas")
        
    except ImportError:
        # Method 2: Using built-in csv module (fallback)
        print("Pandas not available, using built-in csv module...")
        save_to_csv_builtin(data, filename)

def save_to_csv_builtin(data, filename):
    """
    Save to CSV using built-in csv module (fallback method)
    """
    try:
        # Get all possible fieldnames from the data
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"CSV saved successfully using built-in csv module")
        
    except Exception as e:
        print(f"Error saving CSV: {e}")

def add_columns(data):
    """
    Add new columns to the cryptocurrency data
    """
    today = datetime.now().strftime('%d-%m-%Y')  # Get today's date in dd-mm-yyyy format
    
    for coin in data:
        # Add today's date
        coin['date'] = today
        
        # Ensure price change is present and handle None values
        price_change = coin.get('price_change_percentage_24h')
        coin['price_change_24h'] = price_change if price_change is not None else 0
        
        # Add change symbol based on price change
        coin['change_symbol'] = "UP" if coin['price_change_24h'] > 0 else "DOWN"
    
    return data

def process_crypto_data(data):
    """
    Process and clean the cryptocurrency data
    """
    processed_data = []
    
    for coin in data:
        processed_coin = {
            'id': coin.get('id'),  # Unique identifier for the cryptocurrency
            'rank': coin.get('market_cap_rank'),  # Market cap rank
            'name': coin.get('name'),  # Full name of the cryptocurrency
            'symbol': coin.get('symbol', '').upper(),  # Symbol in uppercase
            'ath': coin.get('ath'),  # All-Time High
            'current_price': coin.get('current_price'),  # Current price in USD
            'image': coin.get('image'),  # Image URL
            'market_cap': coin.get('market_cap'),  # Market cap in USD
            'volume_24h': coin.get('total_volume'),  # 24h trading volume in USD
            'price_change_24h': coin.get('price_change_24h', 0),  # Price change in the last 24 hours
            'change_symbol': coin.get('change_symbol', 'DOWN'),  # Change symbol
            'date': coin.get('date'),  # Date when data was fetched
            'last_updated': coin.get('last_updated')  # Last updated timestamp
        }
        processed_data.append(processed_coin)
    
    # Sort by market cap rank (ascending order - rank 1 first)
    processed_data.sort(key=lambda x: x['rank'] if x['rank'] is not None else float('inf'))
    
    # Add numbering column
    for i, coin in enumerate(processed_data, 1):
        coin['number'] = i
    
    return processed_data

def display_top_cryptos(processed_data, top_n=10):
    """
    Display top N cryptocurrencies in a formatted way
    """
    print(f"\nTop {top_n} Cryptocurrencies by Market Cap:")
    print("-" * 100)
    print(f"{'No.':<4} {'Rank':<5} {'Name':<20} {'Symbol':<8} {'Price (USD)':<12} {'24h Change':<12} {'Market Cap':<15}")
    print("-" * 100)
    
    for i, coin in enumerate(processed_data[:top_n], 1):
        price_change = coin.get('price_change_24h', 0)
        change_symbol = coin.get('change_symbol', 'DOWN')
        rank = coin.get('rank', 'N/A')
        
        # Handle None values for price and market cap
        price = coin.get('current_price')
        market_cap = coin.get('market_cap')
        
        price_str = f"${price:,.2f}" if price else "N/A"
        change_str = f"{change_symbol} {price_change:.2f}%" if price_change else "N/A"
        market_cap_str = f"${market_cap:,.0f}" if market_cap else "N/A"
        
        print(f"{i:<4} {rank:<5} {coin['name'][:18]:<20} {coin['symbol']:<8} {price_str:<12} {change_str:<12} {market_cap_str:<15}")

def get_market_summary(processed_data):
    """
    Generate a market summary from the processed data
    """
    if not processed_data:
        return "No data available for market summary."
    
    # Calculate market statistics
    total_coins = len(processed_data)
    gainers = [coin for coin in processed_data if coin.get('price_change_24h', 0) > 0]
    losers = [coin for coin in processed_data if coin.get('price_change_24h', 0) < 0]
    
    # Find top gainer and loser
    top_gainer = max(processed_data, key=lambda x: x.get('price_change_24h', 0))
    top_loser = min(processed_data, key=lambda x: x.get('price_change_24h', 0))
    
    print(f"\nMarket Summary:")
    print("-" * 50)
    print(f"Total Gainers: {len(gainers)} ({len(gainers)/total_coins*100:.1f}%)")
    print(f"Total Losers: {len(losers)} ({len(losers)/total_coins*100:.1f}%)")
    print(f"Top Gainer: {top_gainer['name']} (+{top_gainer.get('price_change_24h', 0):.2f}%)")
    print(f"Top Loser: {top_loser['name']} ({top_loser.get('price_change_24h', 0):.2f}%)")

# Example usage
def main():
    """
    Main function to prevent duplicate execution
    """
    print("Starting Cryptocurrency Data Fetcher")
    print("Note: This process includes rate limiting to prevent API blocking")
    print("-" * 70)
    
    # Fetch cryptocurrency data
    crypto_data = fetch_crypto_data()
    
    if crypto_data:
        # Process the data
        processed_data = process_crypto_data(crypto_data)
        
        # Display results
        display_top_cryptos(processed_data, top_n=10)
        get_market_summary(processed_data)
        
        print(f"\nTotal cryptocurrencies processed: {len(processed_data)}")
        print("Data fetch and processing completed successfully!")
        
        # Also save processed data to CSV
        today = datetime.now().strftime('%d-%m-%Y')
        processed_csv_filename = f'processed_crypto_data_{today}.csv'
        save_to_csv(processed_data, processed_csv_filename)
        print(f"Processed data also saved to: {processed_csv_filename}")
        
    else:
        print("Failed to fetch cryptocurrency data. Please try again later.")
    
    print("\nPro Tip: For frequent updates, consider upgrading to CoinGecko Pro API")

if __name__ == "__main__":
    main()