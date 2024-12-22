import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import pytz  # Library to handle time zones

# Path to JSON file
json_file_path = Path("public/data.json")
volatility_data_path = Path("data/volatility_data.csv")
market_data_path = Path("data/market_data.csv")

def fetch_crypto_prices(params):
    """Fetch the latest market data for Bitcoin and Dogecoin."""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"

        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": "CG-wpnLaqsmd1sGKmjW9yrPeEQV"
        }
        response = requests.get(url, headers=headers,params=params)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        # Extract prices for Bitcoin and Dogecoin
        bitcoin_price = data["bitcoin"]["usd"]
        dogecoin_price = data["dogecoin"]["usd"]

        # Get the current time in Central Time Zone
        central_tz = pytz.timezone("US/Central")
        current_time = datetime.now(central_tz).strftime("%Y-%m-%d %H:%M:%S")

        # Create a dictionary to hold the data
        prices = {
            "Last Update": [current_time],
            "Bitcoin Value": [bitcoin_price],
            "Doge Value": [dogecoin_price]
        }
        return prices

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinGecko: {e}")
        return {}

def main():
    # Check if the CSV file exists; if not, create it with appropriate headers
    if not volatility_data_path.exists():
        initial_data = {
            "Last Update": [],
            "Bitcoin Value": [],
            "Bitcoin Volatility 1": [],
            "Bitcoin Volatility 2": [],
            "Doge Value": [],
            "Doge Volatility 1": [],
            "Doge Volatility 2": []
        }
        pd.DataFrame(initial_data).to_csv(volatility_data_path, index=False)
    if not market_data_path.exists():
        initial_data = {
            "Last Update": [],
            "Bitcoin Value": [],
            "Doge Value": []
        }
        pd.DataFrame(initial_data).to_csv(market_data_path, index=False)

    # Pull latest market data from API
    params = {
        "ids": "bitcoin,dogecoin",  # The cryptocurrencies to fetch
        "vs_currencies": "usd"     # Convert the values to USD
    }

    market_data = fetch_crypto_prices(params)

    # If the market data is empty, return early
    if not market_data:
        return

    # Load existing data from the CSV file
    df_market = pd.read_csv(market_data_path)
    df_volatility = pd.read_csv(volatility_data_path)
    # Create new data to append
    current_time = market_data["Last Update"][0]
    new_data_market = {
        "Last Update": current_time,
        "Bitcoin Value": market_data["Bitcoin Value"][0],
        "Doge Value": market_data["Doge Value"][0],
    }
    new_data_volatility = {
        "Last Update": current_time,
        "Bitcoin Value": market_data["Bitcoin Value"][0],
        "Bitcoin Volatility 1": 0,  # Placeholder values
        "Bitcoin Volatility 2": 0,  # Placeholder values
        "Doge Value": market_data["Doge Value"][0],
        "Doge Volatility 1": 0,  # Placeholder values
        "Doge Volatility 2": 0   # Placeholder values
    }

    # Append the new data to the DataFrame
    df_market = pd.concat([df_market, pd.DataFrame([new_data_market])], ignore_index=True)
    df_volatility = pd.concat([df_volatility, pd.DataFrame([new_data_volatility])], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df_market.to_csv(market_data_path, index=False)
    df_volatility.to_csv(volatility_data_path, index=False)

    # Save the latest data as JSON
    latest_data = {
        "Last Update": new_data_volatility["Last Update"],
        "Bitcoin Value": new_data_volatility["Bitcoin Value"],
        "Bitcoin Volatility 1": new_data_volatility["Bitcoin Volatility 1"],
        "Bitcoin Volatility 2": new_data_volatility["Bitcoin Volatility 2"],
        "Doge Value": new_data_volatility["Doge Value"],
        "Doge Volatility 1": new_data_volatility["Doge Volatility 1"],
        "Doge Volatility 2": new_data_volatility["Doge Volatility 2"]
    }

    with open(json_file_path, "w") as f:
        json.dump(latest_data, f)

    print("Updated data saved successfully.")

# Ensure the main function is called only when the script is run directly
if __name__ == "__main__":
    main()
