import os
import json
import pandas as pd
from datetime import datetime

def save_to_json(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"JSON saved successfully: {filename}")
        return True
    except Exception as e:
        print(f"Error saving JSON {filename}: {e}")
        return False

def save_to_csv(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"CSV saved successfully: {filename}")
        return True
    except Exception as e:
        print(f"Error saving CSV {filename}: {e}")
        return False

def save_all_datasets(raw_data, processed_data, top_gainers, top_losers):
    print("Saving all datasets...")

    # Ensure 'data/' directory exists
    os.makedirs('data', exist_ok=True)

    today = datetime.now().strftime('%d-%m-%Y')

    files = [
        (raw_data, os.path.join('data', f'crypto_data_{today}.json'), 'json'),
        (raw_data, os.path.join('data', f'crypto_data_{today}.csv'), 'csv'),
        (processed_data, os.path.join('data', f'processed_crypto_data_{today}.csv'), 'csv'),
        (top_gainers, os.path.join('data', f'top_10_positive_{today}.csv'), 'csv'),
        (top_losers, os.path.join('data', f'top_10_negative_{today}.csv'), 'csv'),
    ]

    success_count = 0
    for data, filename, ftype in files:
        if ftype == 'json':
            if save_to_json(data, filename):
                success_count += 1
        else:
            if save_to_csv(data, filename):
                success_count += 1

    print(f"Finished saving {success_count}/{len(files)} files.")
