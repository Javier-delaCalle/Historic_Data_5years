import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import statistics
import os

def fetch_and_analyze(ticker_symbol):
    print(f"\nProcessing ticker: {ticker_symbol}")
    # 1) Date range for the last 5 years
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=5*365)

    # 2) Download historical data
    stock = yf.Ticker(ticker_symbol)
    data  = stock.history(start=start, end=end)
    if data.empty:
        print(f"No data retrieved for {ticker_symbol}. Please check the symbol or your connection.")
        return

    # 3) Preview raw data
    print(f"\nSample data for {ticker_symbol}:")
    print(data.head())

    # 4) Calculate daily returns (%)
    data['Daily Return'] = data['Close'].pct_change() * 100

    # 5) Compute summary stats
    initial_price        = data['Close'].iloc[0]
    final_price          = data['Close'].iloc[-1]
    total_return         = (final_price / initial_price - 1) * 100
    years                = (end - start).days / 365.25
    annualized_return    = (final_price / initial_price) ** (1 / years) - 1
    geometric_mean_close = statistics.geometric_mean(data['Close'])

    # 6) Print summary with two decimals
    print(f"\nTotal return over 5 years: {total_return:.2f}%")
    print(f"Annualized return: {annualized_return*100:.2f}%")
    print(f"Geometric mean of closing price: {geometric_mean_close:.2f}")

    # 7) Round all numeric columns to two decimals
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    data[numeric_cols] = data[numeric_cols].round(2)

    # 8) Format numbers for CSV: commas as thousands, dots as decimals
    #    (exclude Daily Return until next step)
    for col in numeric_cols:
        if col != 'Daily Return':
            data[col] = data[col].apply(lambda x: f"{x:,.2f}")

    # 9) Format Daily Return separately as percentage
    data['Daily Return'] = data['Daily Return'].apply(lambda x: f"{x:,.2f}%")

    # 10) Ensure CSV_Files folder exists next to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir    = os.path.join(script_dir, "CSV_Files")
    os.makedirs(csv_dir, exist_ok=True)

    # 11) Export to CSV using ';' as delimiter
    csv_path = os.path.join(csv_dir, f"{ticker_symbol}_5_years.csv")
    try:
        data.to_csv(csv_path, sep=';', index_label='Date')
        print(f"\nData successfully exported to '{csv_path}'.")
    except Exception as e:
        print(f"Error exporting CSV: {e}")

    # 12) Plotting (convert strings back to floats)
    plt.figure(figsize=(14, 10))
    plt.suptitle(f"5‑Year Chart: {ticker_symbol}", fontsize=16)

    # Closing Price
    plt.subplot(2, 1, 1)
    close_vals = data['Close'].str.replace(',', '').astype(float)
    plt.plot(data.index, close_vals, label='Closing Price', color='blue')
    plt.ylabel('Price ($)')
    plt.legend()

    # Daily Return
    plt.subplot(2, 1, 2)
    dr_vals = close_vals.pct_change() * 100
    plt.plot(data.index, dr_vals, label='Daily Return (%)', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Percentage (%)')
    plt.legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    plt.close('all')

def display_menu():
    print("\nWelcome to the Python Financial Analyzer")
    print("Please select one of your Permanent Portfolio assets:")
    print("1. Vanguard S&P 500 ETF (VOO)")
    print("2. EURO STOXX SPDR ETF (FEZ)")
    print("3. Invesco Physical Gold ETC (8PSG.DE)")
    print("4. iShares EUR Govt. Bond 15‑30y (IBCL.DE)")
    print("5. iShares US Treasury Bond 0‑1y (IB01.L)")
    print("6. Enter a custom ticker")
    choice = input("Enter the number of your choice: ").strip()

    mapping = {
        "1": "VOO",
        "2": "FEZ",
        "3": "8PSG.DE",
        "4": "IBCL.DE",
        "5": "IB01.L"
    }
    if choice in mapping:
        return mapping[choice]
    elif choice == "6":
        custom = input("Enter the ticker symbol: ").strip().upper()
        return custom if custom else None
    else:
        print("Invalid option.")
        return None

if __name__ == "__main__":
    pd.set_option("display.max_rows", None)

    while True:
        ticker = display_menu()
        if ticker:
            fetch_and_analyze(ticker)
        else:
            print("\nExiting program due to invalid selection.")
            break

        again = input("\nWould you like to analyze another asset? (y/n): ").strip().lower()
        if again != "y":
            print("\nProgram terminated.")
            break
