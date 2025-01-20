from requests import get
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt 

load_dotenv()

#API for general features
BASE_URL = "https://api.freecurrencyapi.com/v1/"
API_KEY = os.getenv("API_KEY")

#API for historical data
EXCHANGE_API_URL = "http://api.exchangeratesapi.io/v1/"
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

#API for monthly and annual historical graphs
BASE_URL_BANKITALIA = "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0"
HEADERS = {"Accept": "application/json"}

supported_currencies = ['EUR', 'USD','AUD', 'CNY', 'JPY', 'DKK']
#-----------------------------------CHEKS FUNCTIONS---------------------------------------------
# Check if currency is valid (for Freecurrencyapi's API)
def is_valid_currency(currency, currencies):
    return any(currency == code for code, _ in currencies)

# Check if currency is valid (for Banca Italia's API)
def is_valid_currency_BA(currency, currencies):
    return currency in currencies

# Check if amount is a valid number
def is_valid_amount(amount):
    try:
        float(amount)
        return True
    except ValueError:
        return False

# Check if date is in correct format and after 1999-01-01
def is_valid_date(date):
    try:
        input_date = datetime.strptime(date, "%Y-%m-%d")
        if input_date < datetime(1999, 1, 1):
            print("Error: Historical data is only available from 1999-01-01 onwards.")
            return False
        return True
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return False
    



#-----------------------------------------------------MONTHLY AND ANNUAL GRAPHS------------------------------------------------------------------

#to obtain avarage monthly exchange rates
def get_monthly_exchange_rates(base_currency, target_currency, start_month, start_year, end_month, end_year):    
    endpoint = f"/monthlyTimeSeries"
    params = {
        "startMonth": start_month,
        "startYear": start_year,
        "endMonth": end_month,
        "endYear": end_year,
        "baseCurrencyIsoCode": base_currency,
        "currencyIsoCode": target_currency,
        "lang": "it",
    }
    url = BASE_URL_BANKITALIA + endpoint
    response = requests.get(url, headers=HEADERS, params=params).json()
    
    if "rates" not in response or not response["rates"]:
        print("No data available for the requested period.")
        return None
    return response["rates"]

#to obtain avarage annual exchange rates
def get_annual_exchange_rates(base_currency, target_currency, start_year, end_year):
    endpoint = f"/annualTimeSeries"
    params = {
        "startYear": start_year,
        "endYear": end_year,
        "baseCurrencyIsoCode": base_currency,
        "currencyIsoCode": target_currency,
        "lang": "it",
    }
    url = BASE_URL_BANKITALIA + endpoint
    response = requests.get(url, headers=HEADERS, params=params).json()
    
    if "rates" not in response or not response["rates"]:
        print("No data available for the requested period.")
        return None
    return response["rates"]

# to plot the exchange rate graph (monthly or annual)
def plot_time_series(data, title, ylabel):
    dates = [entry["referenceDate"] for entry in data]
    rates = [float(entry["avgRate"]) for entry in data]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, rates, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel("Periodo")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# to handle graph feature
def handle_graph_command(currencies):
    option = input("Enter an option (months/years): ").lower()

    if option == "months":
        currency1 = input("Enter the base currency: ").upper()
        while not is_valid_currency_BA(currency1, supported_currencies):
            print(f"Currency {currency1} is not supported by Banca Italia for historical data.")
            print(f"Supported currencies by Banca Italia are:")
            print(supported_currencies)
            currency1 = input("Enter the base currency: ").upper()

        currency2 = input("Enter the target currency: ").upper()
        while not is_valid_currency_BA(currency2, supported_currencies):
            print(f"Currency {currency2} is not supported by Banca Italia for historical data.")
            print(f"Supported currencies by Banca Italia are:")
            print(supported_currencies)
            currency2 = input("Enter the target currency: ").upper()

        start_month = input("Enter the month of start (1-12): ")
        while not start_month.isdigit() or not (1 <= int(start_month) <= 12):
            print("Error: Invalid month. Please enter a number between 1 and 12.")
            start_month = input("Enter the start month (1-12): ")

        start_year = input("Enter the year of start (YYYY): ")
        while not start_year.isdigit() or not (1999 <= int(start_year) <= datetime.now().year):
            print(f"Error: Year must be between 1999 and {datetime.now().year}.")
            start_year = input("Enter the start year (YYYY): ")

        end_month = input("Enter the end of the month (1-12): ")
        while not end_month.isdigit() or not (1 <= int(end_month) <= 12):
            print("Error: Invalid month. Please enter a number between 1 and 12.")
            end_month = input("Enter the end month (1-12): ")

        end_year = input("Enter the end year (YYYY): ")
        while not end_year.isdigit() or not (1999 <= int(end_year) <= datetime.now().year):
            print(f"Error: Year must be between 1999 and {datetime.now().year}.")
            end_year = input("Enter the end year (YYYY): ")

        data = get_monthly_exchange_rates(currency1, currency2, start_month, start_year, end_month, end_year)
        if data:
            plot_time_series(data, f"Monthly fluctuations {currency1} -> {currency2}", "Exchange rate")

    elif option == "years":
        currency1 = input("Enter the base currency: ").upper()
        while not is_valid_currency_BA(currency1, supported_currencies):
            print(f"Currency {currency1} is not supported by Banca Italia for historical data.")
            print(f"Supported currencies by Banca Italia are:")
            print(supported_currencies)
            currency1 = input("Enter the base currency: ").upper()

        currency2 = input("Enter the target currency: ").upper()
        while not is_valid_currency_BA(currency2, supported_currencies):
            print(f"Currency {currency2} is not supported by Banca Italia for historical data.")
            print(f"Supported currencies by Banca Italia are:")
            print(supported_currencies)
            currency2 = input("Enter the target currency: ").upper()

        start_year = input("Enter the year of start (YYYY): ")
        while not start_year.isdigit() or not (1999 <= int(start_year) <= datetime.now().year):
            print(f"Error: Year must be between 1999 and {datetime.now().year}.")
            start_year = input("Enter the start year (YYYY): ")

        end_year = input("Enter the end year (YYYY): ")
        while not end_year.isdigit() or not (1999 <= int(end_year) <= datetime.now().year):
            print(f"Error: Year must be between 1999 and {datetime.now().year}.")
            end_year = input("Enter the end year (YYYY): ")

        data = get_annual_exchange_rates(currency1, currency2, start_year, end_year)
        if data:
            plot_time_series(data, f"Annual fluctuations {currency1} -> {currency2}", "Exhange rate")
    else:
        print("Invalid option! Use 'months' or 'years'.")


 #-----------------------------------------------------HISTORICAL------------------------------------------------------------------

 # #to return the exchange rate in a specific date
def historical_rate_exchangeratesapi(currency1, currency2, date):
    endpoint = f"/{date}?access_key={EXCHANGE_API_KEY}&base={currency1}&symbols={currency2}"
    url = EXCHANGE_API_URL + endpoint
    response = requests.get(url).json()

    if not response.get("success", False):
        print(f"API Error: {response.get('error', {}).get('info', 'Unknown error')}")
        return None

    rates = response.get("rates", {})
    rate = rates.get(currency2)
    if rate:
        print(f"Exchange rate on {date}: {currency1} -> {currency2}: {rate}")
        return rate
    else:
        print(f"Rate not available for {currency1} -> {currency2} on {date}.")
        return None

 #-----------------------------------------------------GENERAL FEATURES------------------------------------------------------------------

#to return - using API - the list of currenties (sorted alphabetically)
def get_currencies():
    endpoint = f"currencies?apikey={API_KEY}"
    url = BASE_URL + endpoint
    response = get(url).json()

    if "data" not in response:
        print("Error during currecy recovery")
        return []

    currencies = response["data"]
    sorted_currencies = sorted(currencies.items())  # Sort currencies alphabetically
    return sorted_currencies

#to print the list of currencies
def print_currencies(currencies):
    print("")
    for code, details in currencies:
        name = details.get("name", "Unknown")
        print(f"{code} - {name}")
    print("")

#to return the exchange rate between the two currencies
def exchange_rate(currency1, currency2):
    endpoint = f"latest?apikey={API_KEY}&base_currency={currency1}&currencies={currency2}"
    url = BASE_URL + endpoint
    response = get(url).json()

    if "data" not in response or currency2 not in response["data"]:
        print("Currencies not valid or requests error")
        return None

    rate = response["data"][currency2]
    print(f"Exchange rate {currency1} -> {currency2}: {rate}")
    return rate

#to convert currency
def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Amount not valid.")
        return
   
    converted_amount = rate * amount         #conversion
    print(f"{amount} {currency1} is equal to {converted_amount} {currency2}")
    return converted_amount


 #-----------------------------------------------------MAIN------------------------------------------------------------------

def main():
    currencies = get_currencies()

    if not currencies:
        print("API error. Verificate the API KEY and retry.")
        return

    print("Welcome in the currency converter! \nThis is the list of commands you can use:\n")
    print("[List] - Show the currencies avaible")
    print("[Convert] - Convert an amount from one currency to another")
    print("[Rate] - Show exchange rate between two currencies")
    print("[Historical] - Show historical exchange rate between two currencies")
    print("[Graph] - Show a graph of historical exchange rates between two currencies")
    print()

    while True:
        command = input("Insert a command (q to quit): ").lower()

        if command == "q":
            break

        elif command == "list":
            print_currencies(currencies)
        
        elif command == "convert":
            currency1 = input("Enter the starting currency: ").upper()
            while not is_valid_currency(currency1, currencies):
                print("Invalid currency code!")
                currency1 = input("Enter the starting currency: ").upper()
                
            amount = input(f"Enter an amount in {currency1}: ")
            while not is_valid_amount(amount):
                print("Invalid amount!")
                amount = input(f"Enter an amount in {currency1}: ")
                
            currency2 = input("Enter the currency to converter to : ").upper()
            while not is_valid_currency(currency2, currencies):
                print("Invalid currency code!")
                currency2 = input("Enter the currency to converter to : ").upper()
                
            convert(currency1, currency2, amount)
        
        elif command == "rate":
            currency1 = input("Enter the starting currency: ").upper()
            while not is_valid_currency(currency1, currencies):
                print("Invalid currency code!")
                currency1 = input("Enter the starting currency: ").upper()
            
            currency2 = input("Enter the ending currency: ").upper()
            while not is_valid_currency(currency2, currencies):
                print("Invalid currency code!")
                currency2 = input("Enter the ending currency: ").upper()
                
            exchange_rate(currency1, currency2)
        elif command == "historical":
            currency1 = input("Enter the starting currency: ").upper()
            while not is_valid_currency(currency1, currencies):
                print("Invalid currency code!")
                currency1 = input("Enter the starting currency: ").upper()
                
            currency2 = input("Enter the ending currency: ").upper()
            while not is_valid_currency(currency2, currencies):
                print("Invalid currency code!")
                currency2 = input("Enter the ending currency: ").upper()

            date = input("Enter the date (YYYY-MM-DD): ") 
            while not is_valid_date(date):
                
                date = input("Enter the date (YYYY-MM-DD): ")
            
            historical_rate_exchangeratesapi(currency1, currency2, date)
        
        elif command == "graph":
            handle_graph_command(currencies)

        else:
            print("Please enter a valid comand!")


if __name__ == "__main__":          #_name_ is a special variable that contains the name of the running module (If you run it directly - for example, python script.py - the value of __name__ will be "__main__".)
    main()
