import yfinance as yf
import pandas as pd
from datetime import datetime

def main():
    print("Welcome to the ETF Back Tester!\n")
    while True:
        print("Menu:")
        print("1. View List of Available Indices")
        print("2. Simulate PAC")
        print("3. Simulate LUMP SUM")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            view_available_indices()
        elif choice == "2":
            simulate_pac()
        elif choice == "3":
            simulate_lump_sum()
        elif choice == "4":
            print("Thank you for using the ETF Back Tester. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")

#to show the list of available indices
def view_available_indices():
    available_indices = {
        "S&P 500": "^GSPC",
        "NASDAQ 100": "^NDX",
        "Dow Jones": "^DJI",
        "FTSE 100": "^FTSE",
        "DAX": "^GDAXI"
    }
    print("Available Indices:")
    for name, ticker in available_indices.items():
        print(f"- {name} ({ticker})")
    print()

#--------------------------validator functions---------------------------------------------

def get_valid_ticker():
    available_tickers = {
        "^GSPC", "^NDX", "^DJI", "^FTSE", "^GDAXI"
    }
    while True:
        ticker = input("Enter the index ticker (e.g., ^GSPC): ").upper()
        if ticker in available_tickers:
            return ticker
        print("Invalid ticker. Please enter a valid index from the available list.")

def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please enter a date in YYYY-MM-DD format.")

def get_valid_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Value must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_trading_date(df, date):
    date = pd.Timestamp(date)  #  Convert dates to timestamp for compatibility
    
    if date < df.index[0] or date > df.index[-1]:
        print("Date out of range for available data.")
        return None

    while date not in df.index:
        date += pd.Timedelta(days=1)
        if date > df.index[-1]:  # If it exceeds the last available date, returns None
            print("No valid trading day found within range.")
            return None

    return date

#-------------------------------------------------------------------------------------------

#to download historical data
def download_historical_data(ticker, start_date, end_date):
    try:
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        df = df[['Close']]
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None



#--------PAC----------
def simulate_pac():
    ticker = get_valid_ticker()
    start_date = get_valid_date("Enter the PAC start date (YYYY-MM-DD): ")
    
    while True:
        end_date = get_valid_date("Enter the PAC end date (YYYY-MM-DD): ")
        if end_date > start_date:
            break
        print("End date must be after the start date.")

    frequencies = {"monthly": 30, "quarterly": 90, "semiannual": 180}
    while True:
        frequency = input("Enter the PAC frequency (monthly, quarterly, semiannual): ").lower()
        if frequency in frequencies:
            step = frequencies[frequency]
            break
        print("Invalid frequency. Please choose monthly, quarterly, or semiannual.")

    pac_amount = get_valid_number("Enter the PAC amount: ")

    df = download_historical_data(ticker, start_date, end_date)
    if df is None or df.empty:
        print("Error: No data available for the selected period.")
        return

    pac_dates = pd.date_range(start=start_date, end=end_date, freq=f'{step}D')
    total_investment, total_units = 0, 0

    for date in pac_dates:
        trade_date = get_valid_trading_date(df, date)
        if trade_date:
            price = df.loc[trade_date, 'Close']
            if isinstance(price, pd.Series):  # If it is a Series, we take the first value
                price = price.iloc[0]
            units = pac_amount / price
            total_investment += pac_amount
            total_units += units
            print(f"Date: {trade_date.strftime('%Y-%m-%d')}, Price: {price:.2f}, Units Purchased: {units:.2f}")
        else:
            print(f"No trading data available around {date.strftime('%Y-%m-%d')}")

    final_date = df.index[-1]
    final_price = df.loc[final_date, 'Close']
    if isinstance(final_price, pd.Series):  # If it is a Series, we take the first value
        final_price = final_price.iloc[0]
    total_value = total_units * final_price
    profit_loss = total_value - total_investment
    profit_loss_percent = (profit_loss / total_investment) * 100

    print("\nPAC Investment Results:")
    print(f"Final Price: {final_price:.2f}")
    print(f"Average Purchase Price: {total_investment / total_units:.2f}")
    print(f"Total Investment: {total_investment:.2f}")
    print(f"Total Units Value: {total_value:.2f}")
    print(f"Total Profit/Loss: {profit_loss:.2f} ({profit_loss_percent:.2f}%)\n")


#------LUMP SUM-------
def simulate_lump_sum():
    ticker = get_valid_ticker()
    investment_date = get_valid_date("Enter the investment date (YYYY-MM-DD): ")

    while True:
        end_date = get_valid_date("Enter the end date for evaluation (YYYY-MM-DD): ")
        if end_date > investment_date:
            break
        print("End date must be after the investment date.")

    amount = get_valid_number("Enter the investment amount: ")

    df = download_historical_data(ticker, investment_date, end_date)
    if df is None or df.empty:
        print("Error: No data available for the selected period.")
        return

    purchase_date = get_valid_trading_date(df, investment_date)
    if not purchase_date:
        print("No valid trading day found for the investment date.")
        return

    final_date = get_valid_trading_date(df, end_date)
    if not final_date:
        final_date = df.index[-1]
        print(f"End date exceeded available data. Using last trading day: {final_date.strftime('%Y-%m-%d')}")

    price_at_purchase = df.loc[purchase_date, 'Close']
    if isinstance(price_at_purchase, pd.Series):  
        price_at_purchase = price_at_purchase.iloc[0]  # If it is a Series, we take the first value

    price_at_end = df.loc[final_date, 'Close']
    if isinstance(price_at_end, pd.Series):  
        price_at_end = price_at_end.iloc[0]  # If it is a Series, we take the first value

    units = amount / price_at_purchase
    total_value = units * price_at_end
    profit_loss = total_value - amount
    profit_loss_percent = (profit_loss / amount) * 100

    print("\nLUMP SUM Investment Results:")
    print(f"Investment Date: {purchase_date.strftime('%Y-%m-%d')}")
    print(f"End Date: {final_date.strftime('%Y-%m-%d')} (Adjusted if necessary)")
    print(f"Purchase Price: {price_at_purchase:.2f}")
    print(f"Final Price: {price_at_end:.2f}")
    print(f"Total Units Purchased: {units:.2f}")
    print(f"Total Investment Value: {total_value:.2f}")
    print(f"Total Profit/Loss: {profit_loss:.2f} ({profit_loss_percent:.2f}%)\n")

if __name__ == "__main__":
    main()
