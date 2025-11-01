from src.data_fetch import fetch_close_series, save_series_to_csv

if __name__ == "__main__":
    # Download example data for Microsoft (MSFT)
    series = fetch_close_series("MSFT", "2023-01-01", "2023-12-31")
    print(series.head())  # Show first rows

    # Save to CSV
    save_path = save_series_to_csv(series, "MSFT_prices.csv")
    print("Saved to:", save_path)