# Cryptocurrency Market Analyzer

A comprehensive real-time cryptocurrency price tracker built with Python and the CoinGecko API. This project fetches and analyzes data on the top 250 cryptocurrencies ranked by market capitalization, making it perfect for data science enthusiasts and anyone interested in cryptocurrency market analysis.

## IMPORTANT: API Rate Limiting

**READ THIS BEFORE RUNNING THE PROJECT:**

CoinGecko's free API has strict rate limits that **MUST** be respected to avoid getting blocked:

- **Maximum 10-15 requests per minute**
- **Add 6+ second delays between requests**
- **Rapid consecutive requests will block your IP**
- **Blocked IPs may face temporary bans (hours to days)**

## Features

- **Real-time data retrieval** from CoinGecko API with built-in rate limiting
- **Top 250 cryptocurrencies** analysis by market cap
- **Market movers detection** - biggest gainers and losers (24h)
- **Multiple export formats** - JSON and CSV
- **Professional data display** with formatted tables
- **Safe ETL pipeline** with error handling
- **Market summary statistics** 
- **No API key required** - completely free to use

## Project Structure

```
cryptocurrency_project/
│
├── config/                 # Configuration settings
├── data/                   # Generated datasets
├── utils/                  # Helper modules
│   ├── fetcher.py         # Data collection from CoinGecko API
│   ├── processor.py       # Data cleaning and transformation
│   ├── saver.py          # Save data to CSV and JSON
│   └── display.py        # Console output and visualization
│
├── main.py               # Main orchestration script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/cryptocurrency_project.git
cd cryptocurrency_project
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv crypt_env
crypt_env\Scripts\activate

# macOS/Linux
python3 -m venv crypt_env
source crypt_env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
python main.py
```

### Sample Output

**Market Leaders:**
```
Top 10 Cryptocurrencies by Market Cap:
--------------------------------------------------------------------------------
Rank  Name                 Symbol    Price (USD)    24h Change     Market Cap
--------------------------------------------------------------------------------
1     Bitcoin             BTC       $29,543.12     +2.35%         $578,212,000,000
2     Ethereum            ETH       $1,857.34      +1.21%         $223,879,000,000
3     Tether              USDT      $1.00          +0.01%         $83,240,000,000
...
```

**Market Movers:**
```
Top 10 Market Gainers (24h):
--------------------------------------------------
Name                Symbol      24h Change
--------------------------------------------------
Dogecoin           DOGE        +10.22%
Polygon            MATIC       +8.45%
...

Top 10 Market Losers (24h):
--------------------------------------------------
Name                Symbol      24h Change
--------------------------------------------------
Terra Classic      LUNC        -5.67%
ApeCoin           APE         -4.23%
...
```

## Data Structure

### Generated Files:
- `data/raw_data.json` - Complete API response data
- `data/processed_data.csv` - Cleaned and sorted cryptocurrency data
- `data/top_gainers.csv` - Top 10 24-hour gainers
- `data/top_losers.csv` - Top 10 24-hour losers

### Key Data Fields:
| Field | Description | Type |
|-------|-------------|------|
| `rank` | Market cap ranking | Integer |
| `name` | Cryptocurrency name | String |
| `symbol` | Trading symbol | String |
| `current_price` | Current USD price | Float |
| `price_change_24h` | 24h price change % | Float |
| `market_cap` | Total market cap | Integer |
| `volume_24h` | 24h trading volume | Integer |
| `ath` | All-time high price | Float |

## Code Example

Here's the core data fetching function with proper rate limiting:

```python
import requests
import time
from datetime import datetime

def fetch_crypto_data():
    """
    Fetch cryptocurrency data with rate limiting
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
        # CRITICAL: Rate limiting to prevent API blocking
        print("Applying rate limit (6 seconds)...")
        time.sleep(6)
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully fetched {len(data)} cryptocurrencies")
            return data
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        print("Tip: You may have hit the rate limit. Wait before trying again.")
        return None
```

## Dependencies

Create `requirements.txt`:
```txt
requests>=2.28.0
pandas>=1.5.0
```

## Data Analysis Examples

### Market Statistics
```python
import pandas as pd

# Load processed data
df = pd.read_csv('data/processed_data.csv')

# Calculate market statistics
gainers = df[df['price_change_24h'] > 0]
losers = df[df['price_change_24h'] < 0]

print(f"Gainers: {len(gainers)} ({len(gainers)/len(df)*100:.1f}%)")
print(f"Losers: {len(losers)} ({len(losers)/len(df)*100:.1f}%)")

# Total market cap
total_market_cap = df['market_cap'].sum()
print(f"Total Market Cap: ${total_market_cap:,.0f}")
```

## Troubleshooting

### Common Issues:

**API Rate Limit Exceeded:**
```
Solution: Wait 1-24 hours before trying again, ensure 6+ second delays between requests
```

**Connection Errors:**
```
Solution: Check internet connection, verify CoinGecko API status
```

**Empty Data Response:**
```
Solution: Verify API endpoint, check for API service disruptions
```

## Future Enhancements

- [ ] **Automated scheduling** with proper rate limiting
- [ ] **Interactive dashboards** using Streamlit or Dash
- [ ] **Historical data analysis** and trend visualization
- [ ] **Price alerts** and notifications
- [ ] **Portfolio tracking** capabilities
- [ ] **Database integration** for data persistence
- [ ] **Technical indicators** (RSI, MACD, moving averages)
- [ ] **Machine learning** price prediction models

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational and informational purposes only. Cryptocurrency investments carry significant risks. Always conduct your own research before making investment decisions.

## 📞 Support

If you encounter issues:
If you have any questions or run into issues, please:
- Check the [Issues](https://github.com/ericmaniraguh/crypto-price-tracker/issues) page
- Create a new issue if your problem isn't already documented


## 🙏 Acknowledgments

- **CoinGecko API** for providing free cryptocurrency data
- **Python community** for excellent libraries and tools

---

**⭐ If you find this project helpful, please give it a star!**

**Made with ❤️ by Eric Maniraguha** | **Powered by CoinGecko API**