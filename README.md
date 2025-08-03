# Cryptocurrency Prices by Market Cap (Real-Time Analysis)

A comprehensive real-time cryptocurrency price tracker built with Python and the free CoinGecko API. This project fetches and processes data on over 250 cryptocurrencies ranked by market capitalization, making it perfect for data science and analytics enthusiasts seeking hands-on experience with API integration, ETL pipelines, and automation.

## Critical: API Rate Limiting Guidelines

**BEFORE YOU START - READ THIS CAREFULLY:**

CoinGecko's free API has strict rate limits that **MUST** be respected:

### Rate Limit Rules:
- **Maximum 10-15 requests per minute**
- **Add 6+ second delays between requests**
- **Rapid consecutive requests will block your IP**
- **Blocked IPs may face temporary bans (hours to days)**

### Best Practices:
```python
import time

# GOOD: Rate-limited approach
def safe_api_call():
    time.sleep(6)  # Wait 6 seconds between requests
    response = requests.get(url, params=params)
    return response

# BAD: This will get you blocked!
def unsafe_api_call():
    for i in range(10):
        response = requests.get(url)  # No delay = instant ban
```

### If You Get Blocked:
1. **Stop making requests immediately**
2. **Wait 1-24 hours before trying again**
3. **Implement proper rate limiting**
4. **Consider upgrading to CoinGecko Pro API for higher limits**

## Features

- **Real-time data retrieval** using CoinGecko API with proper rate limiting
- **Top 250 cryptocurrencies** by market cap coverage
- **Built-in rate limiting** to prevent API blocking
- **Automatic sorting** by market capitalization rank
- **Sequential numbering** for easy data reference
- **Dual file export** - JSON and CSV formats
- **Clean and structured data** ready for analysis
- **Safe ETL pipeline** implementation using Python
- **Error handling** for API failures and rate limit violations
- **Market summary statistics** with gainers/losers analysis
- **Professional table display** with formatted output
- **No API key required** - completely free to use

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ericmaniraguh/crypto-price-tracker.git
cd crypto-price-tracker
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python crypto_tracker.py
```

## Sample Code: Complete Implementation

```python
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
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully fetched {len(data)} cryptocurrencies")
            
            # Add new columns and save data
            enhanced_data = add_columns(data)
            save_files(enhanced_data)
            
            return enhanced_data
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        print("Tip: You may have hit the rate limit. Wait a few minutes before trying again.")
        return None

def process_crypto_data(data):
    """
    Process, sort, and add numbering to cryptocurrency data
    """
    processed_data = []
    
    for coin in data:
        processed_coin = {
            'id': coin.get('id'),
            'rank': coin.get('market_cap_rank'),
            'name': coin.get('name'),
            'symbol': coin.get('symbol', '').upper(),
            'current_price': coin.get('current_price'),
            'price_change_24h': coin.get('price_change_24h', 0),
            'change_symbol': coin.get('change_symbol', 'DOWN'),
            'market_cap': coin.get('market_cap'),
            'volume_24h': coin.get('total_volume'),
            'ath': coin.get('ath'),
            'date': coin.get('date'),
            'last_updated': coin.get('last_updated')
        }
        processed_data.append(processed_coin)
    
    # Sort by market cap rank (ascending order - rank 1 first)
    processed_data.sort(key=lambda x: x['rank'] if x['rank'] is not None else float('inf'))
    
    # Add sequential numbering column
    for i, coin in enumerate(processed_data, 1):
        coin['number'] = i
    
    return processed_data

def display_results(processed_data):
    """
    Display formatted cryptocurrency data and market summary
    """
    print(f"\nTop 10 Cryptocurrencies by Market Cap:")
    print("-" * 100)
    print(f"{'No.':<4} {'Rank':<5} {'Name':<20} {'Symbol':<8} {'Price (USD)':<12} {'24h Change':<12} {'Market Cap':<15}")
    print("-" * 100)
    
    for i, coin in enumerate(processed_data[:10], 1):
        price_change = coin.get('price_change_24h', 0)
        change_symbol = coin.get('change_symbol', 'DOWN')
        rank = coin.get('rank', 'N/A')
        
        price = coin.get('current_price')
        market_cap = coin.get('market_cap')
        
        price_str = f"${price:,.2f}" if price else "N/A"
        change_str = f"{change_symbol} {price_change:.2f}%" if price_change else "N/A"
        market_cap_str = f"${market_cap:,.0f}" if market_cap else "N/A"
        
        print(f"{i:<4} {rank:<5} {coin['name'][:18]:<20} {coin['symbol']:<8} {price_str:<12} {change_str:<12} {market_cap_str:<15}")

# Example usage
def main():
    """
    Main function to fetch, process, and display cryptocurrency data
    """
    print("Starting Cryptocurrency Data Fetcher")
    print("Note: This process includes rate limiting to prevent API blocking")
    print("-" * 70)
    
    crypto_data = fetch_crypto_data()
    
    if crypto_data:
        processed_data = process_crypto_data(crypto_data)
        display_results(processed_data)
        
        print(f"\nTotal cryptocurrencies processed: {len(processed_data)}")
        print("Data fetch and processing completed successfully!")
    else:
        print("Failed to fetch cryptocurrency data. Please try again later.")

if __name__ == "__main__":
    main()
```

## Requirements

Create a `requirements.txt` file with the following dependencies:

```txt
requests>=2.28.0
pandas>=1.5.0
csv
json
time
datetime
```

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Data Structure & Output Files

### Generated Files:
1. **`crypto_data_DD-MM-YYYY.json`** - Raw API data with enhancements
2. **`crypto_data_DD-MM-YYYY.csv`** - Raw data in CSV format
3. **`processed_crypto_data_DD-MM-YYYY.csv`** - Cleaned and sorted data

### CSV Column Structure:
The processed CSV files include columns in this order:
```
number | rank | name | symbol | current_price | price_change_24h | change_symbol | market_cap | volume_24h | ath | id | image | date | last_updated
```

### Key Data Fields:

| Field | Description | Type |
|-------|-------------|------|
| `number` | Sequential numbering (1, 2, 3...) | Integer |
| `rank` | Market capitalization ranking | Integer |
| `name` | Full name of cryptocurrency | String |
| `symbol` | Trading symbol (uppercase) | String |
| `current_price` | Current price in USD | Float |
| `price_change_24h` | 24-hour price change percentage | Float |
| `change_symbol` | Price direction indicator (UP/DOWN) | String |
| `market_cap` | Total market capitalization | Integer |
| `volume_24h` | 24-hour trading volume | Integer |
| `ath` | All-time high price | Float |
| `date` | Data fetch date (DD-MM-YYYY) | String |
| `last_updated` | API last update timestamp | String |

## Usage Examples

### Basic Data Retrieval (Rate-Limited)
```python
from crypto_tracker import main

# Safe approach with built-in rate limiting
main()  # Fetches data, processes, and saves files automatically
```

### Data Analysis with Pandas
```python
import pandas as pd
from datetime import datetime

# Load processed data
today = datetime.now().strftime('%d-%m-%Y')
df = pd.read_csv(f'processed_crypto_data_{today}.csv')

# Analyze top gainers
top_gainers = df[df['change_symbol'] == 'UP'].nlargest(10, 'price_change_24h')
print("Top 10 Gainers (24h):")
print(top_gainers[['number', 'name', 'symbol', 'price_change_24h']])

# Market cap analysis
total_market_cap = df['market_cap'].sum()
print(f"Total Market Cap: ${total_market_cap:,.0f}")
```

### Market Statistics
```python
# Calculate market statistics
gainers = df[df['price_change_24h'] > 0]
losers = df[df['price_change_24h'] < 0]

print(f"Gainers: {len(gainers)} ({len(gainers)/len(df)*100:.1f}%)")
print(f"Losers: {len(losers)} ({len(losers)/len(df)*100:.1f}%)")
```

## API Documentation & Rate Limiting

This project uses the **CoinGecko API v3** - a free and comprehensive cryptocurrency API.

- **Base URL**: `https://api.coingecko.com/api/v3/`
- **Rate Limit**: 10-50 requests per minute (free tier)
- **Authentication**: No API key required
- **Documentation**: [CoinGecko API Docs](https://www.coingecko.com/en/api/documentation)

### IMPORTANT: Rate Limiting Implementation

**CoinGecko enforces strict rate limits on their free API tier:**

- **Make only a few requests per minute** (maximum 10-15 requests/minute)
- **Add delays between requests** using `time.sleep(6)`
- **Excessive requests will result in API blocking/temporary ban**
- **For high-frequency data needs, consider CoinGecko Pro API**

**Our implementation includes:**
```python
# Automatic 6-second delay before each request
time.sleep(6)
response = requests.get(url, params=params)
```

### Key Endpoints Used:
- `/coins/markets` - Market data for cryptocurrencies (primary endpoint)
- Returns comprehensive data including prices, market caps, volumes, and 24h changes

## Future Enhancements

### Automation & Scheduling
- [ ] **Scheduled data collection** using `cron`, `Apache Airflow`, or Windows `Task Scheduler` (with proper rate limiting)
- [ ] **Email alerts** for significant price movements (max 1-2 requests per hour)
- [ ] **Slack/Discord notifications** for portfolio updates (rate-limited)

### Visualization & Analytics
- [ ] **Interactive dashboards** using Plotly, Streamlit, or Dash
- [ ] **Historical trend analysis** with moving averages
- [ ] **Volatility metrics** and risk assessment
- [ ] **Portfolio tracking** and performance analysis
- [ ] **Price correlation analysis** between cryptocurrencies

### Data Storage & Management
- [ ] **Database integration** (PostgreSQL, MongoDB, SQLite)
- [ ] **Data warehousing** for historical analysis
- [ ] **Cloud storage** integration (AWS S3, Google Cloud Storage)
- [ ] **Data backup and versioning** systems

### Advanced Features
- [ ] **Machine learning predictions** using historical data
- [ ] **Technical indicators** (RSI, MACD, Bollinger Bands)
- [ ] **News sentiment analysis** integration
- [ ] **Multi-exchange price comparison**
- [ ] **Real-time price alerts** and notifications

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational and informational purposes only. Cryptocurrency investments carry significant risk, and past performance does not guarantee future results. Always do your own research before making investment decisions.

## Support

If you have any questions or run into issues, please:
- Check the [Issues](https://github.com/ericmaniraguh/crypto-price-tracker/issues) page
- Create a new issue if your problem isn't already documented

---

**Made with dedication by Eric Maniraguha** | **Powered by CoinGecko API**