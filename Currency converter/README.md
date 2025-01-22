# Currency Converter and Exchange Rate Tool

This script provides a comprehensive solution for managing and analyzing currency exchange rates. It allows you to fetch real-time and historical exchange rates, plot graphs for currency trends, and perform currency conversion with ease.

## Features

- **Real-Time Exchange Rates**: Retrieve the latest exchange rates between supported currencies.
- **Currency Conversion**: Convert an amount from one currency to another.
- **Historical Rates**: Fetch exchange rates for a specific date starting from January 1, 1999.
- **Graphical Analysis**: Generate monthly or annual historical exchange rate graphs.
- **Currency List**: Display all supported currencies sorted alphabetically.

## Requirements

- Python 3.6+
- API Keys for:
  - [FreeCurrencyAPI](https://freecurrencyapi.com/)
  - [ExchangeRatesAPI](https://exchangeratesapi.io/)
- Required Python libraries:
  - `requests`
  - `matplotlib`
  - `python-dotenv`

## Setup

1. Clone this repository or download the script.
2. Install the required libraries using pip:
   ```bash
   pip install requests matplotlib python-dotenv
   ```
3. Create a .env file in the same directory as the script and add your API keys:
    API_KEY=your_freecurrencyapi_key
    EXCHANGE_API_KEY=your_exchangeratesapi_key

4. Run the script:
    python script_name.py

## Supported Commands

1. **list**: Displays all supported currencies.
2. **convert**: Converts an amount from one currency to another.
3. **rate**: Displays the current exchange rate between two currencies.
4. **historical**: Shows the exchange rate between two currencies on a specific date.
5. **graph**: Generates a graph of historical exchange rates over a specified period (monthly or annual).
6. **q**: Quits the application.

## Supported Currencies
The script supports the following currencies for graph generation via Banca d’Italia:
- EUR, USD, AUD, CNY, JPY, DKK

For real-time exchange rates, additional currencies may be supported depending on the API.

# Error Handling
Invalid inputs (e.g., unsupported currency codes, incorrect date formats) are validated, and descriptive error messages are displayed.
API errors are captured and handled gracefully.
- **Invalid Currency**: The script will notify you if a currency is unsupported and prompt you to try again.
- **Invalid Amount**: Non-numeric amounts will trigger an error message and a request for valid input.
-**Invalid Date**: The date must be in the format YYYY-MM-DD and not earlier than 1999-01-01.

 ## Example Output
 # Convert currency
```
    Enter the starting currency: USD
    Enter an amount in USD: 100
    Enter the currency to convert to: EUR
    
    Output: 100 USD is equal to 92.50 EUR

```
## Rate
```
    Insert a command (q to quit): rate
    Enter the starting currency: GBP
    Enter the ending currency: USD
    
    Outuput: Exchange rate GBP -> USD: 1.210

```
## Historical Exchange Rates
```
    Insert a command (q to quit): historical
    Enter the starting currency: EUR
    Enter the ending currency: JPY
    Enter the date (YYYY-MM-DD): 2022-12-31
    
    Output: Exchange rate on 2022-12-31: EUR -> JPY: 144.32

```
## Graphical Analysis
```
    Insert a command (q to quit): graph
    Enter an option (months/years): months
    Enter the base currency: EUR
    Enter the target currency: USD
    Enter the month of start (1-12): 1
    Enter the year of start (YYYY): 2023
    Enter the end of the month (1-12): 6
    Enter the end year (YYYY): 2023

    Output: Generating a graph for monthly fluctuations EUR -> USD from January 2023 to June 2023...

```
*A graph window displaying monthly exchange rate fluctuations for EUR -> USD from January 2023 to June 2023 will appear.*

## Annual Graph Example
```
    Insert a command (q to quit): graph
    Enter an option (months/years): years
    Enter the base currency: GBP
    Enter the target currency: USD
    Enter the year of start (YYYY): 2018
    Enter the end year (YYYY): 2023

    Output: Generating a graph for annual fluctuations GBP -> USD from 2018 to 2023...

```
*A graph window displaying annual exchange rate fluctuations for GBP -> USD from 2018 to 2023 will appear.*