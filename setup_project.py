import os

# Base directory
base_dir = "cryptocurrency_project"

# Folders to create
folders = [
    base_dir,
    os.path.join(base_dir, "config"),
    os.path.join(base_dir, "data"),
    os.path.join(base_dir, "utils"),
]

# Files to create with optional starter content
files = {
    os.path.join(base_dir, "main.py"): "# Entry point\n\nif __name__ == '__main__':\n    print('Crypto Analyzer Started')\n",
    os.path.join(base_dir, "requirements.txt"): "requests\npandas\n",
    os.path.join(base_dir, "README.md"): "# Cryptocurrency Project\n\nFetch and analyze market data from CoinGecko.\n",
    os.path.join(base_dir, "config", "settings.py"): "# Settings and constants\n",
    os.path.join(base_dir, "utils", "fetcher.py"): "# Fetch data from API\n",
    os.path.join(base_dir, "utils", "processor.py"): "# Process and clean data\n",
    os.path.join(base_dir, "utils", "analyzer.py"): "# Analyze top gainers and losers\n",
    os.path.join(base_dir, "utils", "display.py"): "# Display functions\n",
    os.path.join(base_dir, "utils", "saver.py"): "# Save to JSON and CSV\n",
}

# Create directories
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Project structure created using Python")
