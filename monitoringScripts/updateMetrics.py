import requests
import pandas as pd
import json
from pathlib import Path
import numpy as np
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
    
def calculate_volatility(coin_price, change_rate, change_period,compute_all_times=True):
    if change_rate <= 0 or change_period <= 0:
        raise ValueError("Both 'rate' and 'period' must be positive integers.")
         #Compute the changes in market data since the last change period
    rate_step = int(change_rate/5)+1
    #Compute the changes in market data since the last change period
    period_step = int(12*change_period)+1
    # if len(coin_price) < rate_step or len(coin_price) < period_step:
    #     raise ValueError("The input DataFrame must have at least "+str(rate_step)+" and "+str(period_step)+" rows.")
    
    # Initialize DataFrame to store results
    volatility_metrics = pd.DataFrame(index=coin_price.index, columns=["volatility","mean", "std"])

    # Compute the max-min difference for each sliding windoew of 'rate' rows
    rolling_diff = coin_price.rolling(window=rate_step).apply(lambda x: np.max(x) - np.min(x), raw=True)
    # Compute rolling mean and std for trailing differences
    for i in range(len(rolling_diff)):
        trailing_window = rolling_diff.iloc[max(0, i - period_step + 1):i + 1]
        volatility_metrics.loc[i, "volatility"] = rolling_diff.iloc[i]  #Volatility value
        volatility_metrics.loc[i, "mean"] = trailing_window.mean()  # Mean of Volatility
        volatility_metrics.loc[i, "std"] = trailing_window.std()  # Mean of Volatility
    return volatility_metrics




def main():
    compute_all_volatility = False
    # Check if the CSV file exists; if not, create it with appropriate headers
    if not volatility_data_path.exists():
        initial_data = {
        "Last Update": [],
        "Bitcoin Value": [],
        "Bitcoin Volatility 5:1": [],  # Placeholder values
        "Bitcoin Volatility 5:1 mean": [],  # Placeholder values
        "Bitcoin Volatility 5:1 std": [],  # Placeholder values
        "Bitcoin Volatility 5:8": [],  # Placeholder values
        "Bitcoin Volatility 5:8 mean": [],  # Placeholder values
        "Bitcoin Volatility 5:8 std": [],  # Placeholder values
        "Bitcoin Volatility 5:24": [],  # Placeholder values
        "Bitcoin Volatility 5:24 mean": [],  # Placeholder values
        "Bitcoin Volatility 5:24 std": [],  # Placeholder values
        "Bitcoin Volatility 30:8": [],  # Placeholder values
        "Bitcoin Volatility 30:8 mean": [],  # Placeholder values
        "Bitcoin Volatility 30:8 std": [],  # Placeholder values
        "Bitcoin Volatility 30:24": [],  # Placeholder values
        "Bitcoin Volatility 30:24 mean": [],  # Placeholder values
        "Bitcoin Volatility 30:24 std": [],  # Placeholder values
        "Bitcoin Volatility 30:168": [],  # Placeholder values
        "Bitcoin Volatility 30:168 mean": [],  # Placeholder values
        "Bitcoin Volatility 30:168 std": [],  # Placeholder values
        "Doge Value": df_market["Doge Value"],
        "Doge Volatility 5:1": doge_volatility_5_1["volatility"],  # Placeholder values
        "Doge Volatility 5:1 mean": doge_volatility_5_1["mean"],  # Placeholder values
        "Doge Volatility 5:1 std": doge_volatility_5_1["std"],  # Placeholder values
        "Doge Volatility 5:8": doge_volatility_5_8["volatility"],  # Placeholder values
        "Doge Volatility 5:8 mean": doge_volatility_5_8["mean"],  # Placeholder values
        "Doge Volatility 5:8 std": doge_volatility_5_8["std"],  # Placeholder values
        "Doge Volatility 5:24": doge_volatility_5_24["volatility"],  # Placeholder values
        "Doge Volatility 5:24 mean": doge_volatility_5_24["mean"],  # Placeholder values
        "Doge Volatility 5:24 std": doge_volatility_5_24["std"],  # Placeholder values
        "Doge Volatility 30:8": doge_volatility_30_8["volatility"],  # Placeholder values
        "Doge Volatility 30:8 mean": doge_volatility_30_8["mean"],  # Placeholder values
        "Doge Volatility 30:8 std": doge_volatility_30_8["std"],  # Placeholder values
        "Doge Volatility 30:24": doge_volatility_30_24["volatility"],  # Placeholder values
        "Doge Volatility 30:24 mean": doge_volatility_30_24["mean"],  # Placeholder values
        "Doge Volatility 30:24 std": doge_volatility_30_24["std"],  # Placeholder values
        "Doge Volatility 30:168": doge_volatility_30_168["volatility"],  # Placeholder values
        "Doge Volatility 30:168 mean": doge_volatility_30_168["mean"],  # Placeholder values
        "Doge Volatility 30:168 std": doge_volatility_30_168["std"]  # Placeholder values
        }
        pd.DataFrame(initial_data).to_csv(volatility_data_path, index=False)
    if not market_data_path.exists():
        initial_data = {
            "Last Update": [],
            "Bitcoin Value": [],
            "Doge Value": []
        }
        pd.DataFrame(initial_data).to_csv(market_data_path, index=False)

    # Load existing data from the CSV file
    df_market = pd.read_csv(market_data_path)
    df_volatility = pd.read_csv(volatility_data_path)
    #Check all coins are read in as floats
    df_market["Bitcoin Value"] = df_market["Bitcoin Value"].astype(float)
    df_market["Doge Value"] = df_market["Doge Value"].astype(float)
    
    #Compute Volatilities
    bitcoin_volatility_5_1 = calculate_volatility(df_market["Bitcoin Value"], 5, 1,compute_all_times=compute_all_volatility)
    doge_volatility_5_1 = calculate_volatility(df_market["Doge Value"], 5, 1,compute_all_times=compute_all_volatility)
    bitcoin_volatility_5_8 = calculate_volatility(df_market["Bitcoin Value"], 5, 8,compute_all_times=compute_all_volatility)
    doge_volatility_5_8 = calculate_volatility(df_market["Doge Value"], 5, 8,compute_all_times=compute_all_volatility)
    bitcoin_volatility_5_24 = calculate_volatility(df_market["Bitcoin Value"], 5, 24,compute_all_times=compute_all_volatility)
    doge_volatility_5_24 = calculate_volatility(df_market["Doge Value"], 5, 24,compute_all_times=compute_all_volatility)
    
    bitcoin_volatility_30_8 = calculate_volatility(df_market["Bitcoin Value"], 30, 8,compute_all_times=compute_all_volatility)
    doge_volatility_30_8 = calculate_volatility(df_market["Doge Value"], 30, 8,compute_all_times=compute_all_volatility)
    bitcoin_volatility_30_24 = calculate_volatility(df_market["Bitcoin Value"], 30, 24,compute_all_times=compute_all_volatility)
    doge_volatility_30_24 = calculate_volatility(df_market["Doge Value"], 30, 24,compute_all_times=compute_all_volatility)
    bitcoin_volatility_30_168 = calculate_volatility(df_market["Bitcoin Value"], 30, 168,compute_all_times=compute_all_volatility)
    doge_volatility_30_168 = calculate_volatility(df_market["Doge Value"], 30, 168,compute_all_times=compute_all_volatility)
    new_data_volatility = {
        "Last Update": df_market["Last Update"],
        "Bitcoin Value": df_market["Bitcoin Value"],
        "Bitcoin Volatility 5:1": bitcoin_volatility_5_1["volatility"],  # Placeholder values
        "Bitcoin Volatility 5:1 mean": bitcoin_volatility_5_1["mean"],  # Placeholder values
        "Bitcoin Volatility 5:1 std": bitcoin_volatility_5_1["std"],  # Placeholder values
        "Bitcoin Volatility 5:8": bitcoin_volatility_5_8["volatility"],  # Placeholder values
        "Bitcoin Volatility 5:8 mean": bitcoin_volatility_5_8["mean"],  # Placeholder values
        "Bitcoin Volatility 5:8 std": bitcoin_volatility_5_8["std"],  # Placeholder values
        "Bitcoin Volatility 5:24": bitcoin_volatility_5_24["volatility"],  # Placeholder values
        "Bitcoin Volatility 5:24 mean": bitcoin_volatility_5_24["mean"],  # Placeholder values
        "Bitcoin Volatility 5:24 std": bitcoin_volatility_5_24["std"],  # Placeholder values
        "Bitcoin Volatility 30:8": bitcoin_volatility_30_8["volatility"],  # Placeholder values
        "Bitcoin Volatility 30:8 mean": bitcoin_volatility_30_8["mean"],  # Placeholder values
        "Bitcoin Volatility 30:8 std": bitcoin_volatility_30_8["std"],  # Placeholder values
        "Bitcoin Volatility 30:24": bitcoin_volatility_30_24["volatility"],  # Placeholder values
        "Bitcoin Volatility 30:24 mean": bitcoin_volatility_30_24["mean"],  # Placeholder values
        "Bitcoin Volatility 30:24 std": bitcoin_volatility_30_24["std"],  # Placeholder values
        "Bitcoin Volatility 30:168": bitcoin_volatility_30_168["volatility"],  # Placeholder values
        "Bitcoin Volatility 30:168 mean": bitcoin_volatility_30_168["mean"],  # Placeholder values
        "Bitcoin Volatility 30:168 std": bitcoin_volatility_30_168["std"],  # Placeholder values
        "Doge Value": df_market["Doge Value"],
        "Doge Volatility 5:1": doge_volatility_5_1["volatility"],  # Placeholder values
        "Doge Volatility 5:1 mean": doge_volatility_5_1["mean"],  # Placeholder values
        "Doge Volatility 5:1 std": doge_volatility_5_1["std"],  # Placeholder values
        "Doge Volatility 5:8": doge_volatility_5_8["volatility"],  # Placeholder values
        "Doge Volatility 5:8 mean": doge_volatility_5_8["mean"],  # Placeholder values
        "Doge Volatility 5:8 std": doge_volatility_5_8["std"],  # Placeholder values
        "Doge Volatility 5:24": doge_volatility_5_24["volatility"],  # Placeholder values
        "Doge Volatility 5:24 mean": doge_volatility_5_24["mean"],  # Placeholder values
        "Doge Volatility 5:24 std": doge_volatility_5_24["std"],  # Placeholder values
        "Doge Volatility 30:8": doge_volatility_30_8["volatility"],  # Placeholder values
        "Doge Volatility 30:8 mean": doge_volatility_30_8["mean"],  # Placeholder values
        "Doge Volatility 30:8 std": doge_volatility_30_8["std"],  # Placeholder values
        "Doge Volatility 30:24": doge_volatility_30_24["volatility"],  # Placeholder values
        "Doge Volatility 30:24 mean": doge_volatility_30_24["mean"],  # Placeholder values
        "Doge Volatility 30:24 std": doge_volatility_30_24["std"],  # Placeholder values
        "Doge Volatility 30:168": doge_volatility_30_168["volatility"],  # Placeholder values
        "Doge Volatility 30:168 mean": doge_volatility_30_168["mean"],  # Placeholder values
        "Doge Volatility 30:168 std": doge_volatility_30_168["std"]  # Placeholder values
    }
    if compute_all_volatility:
        df_volatility = pd.DataFrame(new_data_volatility)
    else:
        df_volatility = pd.concat([df_volatility, pd.DataFrame([new_data_volatility])], ignore_index=True)
    # Save the updated DataFrame back to the CSV file
    df_volatility.to_csv(volatility_data_path, index=False)

    # Replace NaN values with "NaN" for JSON serialization and set 4 sigfigs
    new_data_volatility = {
        key: df.fillna(0)
        for key, df in new_data_volatility.items()
    }
    for key, df in new_data_volatility.items():
        # Ensure rounding only applies to numerical columns
        new_data_volatility[key] = df.apply(
            lambda x: int(x * 10000) / 10000 if isinstance(x, (float, int)) else x
        )

    # Save the latest data as JSON
    latest_data = {
        "Last Update": new_data_volatility["Last Update"].iloc[-1],
        "Bitcoin Value": new_data_volatility["Bitcoin Value"].iloc[-1],
        "Bitcoin Volatility 5:1": new_data_volatility["Bitcoin Volatility 5:1"].iloc[-1],
        "Bitcoin Volatility 5:1 mean": new_data_volatility["Bitcoin Volatility 5:1 mean"].iloc[-1],
        "Bitcoin Volatility 5:1 std": new_data_volatility["Bitcoin Volatility 5:1 std"].iloc[-1],
        "Bitcoin Volatility 5:8": new_data_volatility["Bitcoin Volatility 5:8"].iloc[-1],
        "Bitcoin Volatility 5:8 mean": new_data_volatility["Bitcoin Volatility 5:8 mean"].iloc[-1],
        "Bitcoin Volatility 5:8 std": new_data_volatility["Bitcoin Volatility 5:8 std"].iloc[-1],
        "Bitcoin Volatility 5:24": new_data_volatility["Bitcoin Volatility 5:24"].iloc[-1],
        "Bitcoin Volatility 5:24 mean": new_data_volatility["Bitcoin Volatility 5:24 mean"].iloc[-1],
        "Bitcoin Volatility 5:24 std": new_data_volatility["Bitcoin Volatility 5:24 std"].iloc[-1],
        "Doge Value": new_data_volatility["Doge Value"].iloc[-1],
        "Doge Volatility 5:1": new_data_volatility["Doge Volatility 5:1"].iloc[-1],
        "Doge Volatility 5:1 mean": new_data_volatility["Doge Volatility 5:1 mean"].iloc[-1],
        "Doge Volatility 5:1 std": new_data_volatility["Doge Volatility 5:1 std"].iloc[-1],
        "Doge Volatility 5:8": new_data_volatility["Doge Volatility 5:8"].iloc[-1],
        "Doge Volatility 5:8 mean": new_data_volatility["Doge Volatility 5:8 mean"].iloc[-1],
        "Doge Volatility 5:8 std": new_data_volatility["Doge Volatility 5:8 std"].iloc[-1],
        "Doge Volatility 5:24": new_data_volatility["Doge Volatility 5:24"].iloc[-1],
        "Doge Volatility 5:24 mean": new_data_volatility["Doge Volatility 5:24 mean"].iloc[-1],
        "Doge Volatility 5:24 std": new_data_volatility["Doge Volatility 5:24 std"].iloc[-1]
    }
    print(latest_data)
    with open(json_file_path, "w") as f:
        json.dump(latest_data, f)

    print("Updated data saved successfully.")

# Ensure the main function is called only when the script is run directly
if __name__ == "__main__":
    main()
