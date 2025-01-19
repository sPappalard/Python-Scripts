from requests import get
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "https://api.freecurrencyapi.com/v1/"
API_KEY = os.getenv("API_KEY")

#API For historical data
EXCHANGE_API_URL = "http://api.exchangeratesapi.io/v1/"
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

# Check if currency is valid
def is_valid_currency(currency, currencies):
    return any(currency == code for code, _ in currencies)

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
        else:
            print("Please enter a valid comand!")


if __name__ == "__main__":          #_name_ is a special variable that contains the name of the running module (If you run it directly - for example, python script.py - the value of __name__ will be "__main__".)
    main()
