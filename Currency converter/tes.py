import requests

# Impostazioni API
BASE_URL_BANKITALIA = "https://api.banca-italia.it"  # URL base dell'API (verifica se è corretto)
HEADERS = {
    "Accept": "application/json"
}

# Funzione per ottenere i tassi di cambio mensili
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
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()  # Verifica che la risposta HTTP sia OK (200)
        data = response.json()
        
        # Se non ci sono dati nel campo "rates", significa che la valuta non è supportata
        if "rates" not in data or not data["rates"]:
            print(f"Errore con la valuta: {target_currency}")
            return False  # La valuta non è supportata
        return True  # La valuta è supportata
    
    except requests.exceptions.RequestException as e:
        print(f"Errore di richiesta con la valuta {target_currency}: {e}")
        return False  # La richiesta è fallita (errore generico nell'API)

# Lista dei codici delle valute
currency_codes = [
    "AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HRK", 
    "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", 
    "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"
]

# Definiamo i parametri per la richiesta
start_month = 1
start_year = 1999
end_month = 1
end_year = 2024

# Verifica supporto delle valute
supported_currencies = []
unsupported_currencies = []

for currency in currency_codes:
    print(f"Verifica valuta: {currency}")
    if get_annual_exchange_rates("EUR", currency, start_year, end_year):
        supported_currencies.append(currency)
    else:
        unsupported_currencies.append(currency)

# Stampa dei risultati
print("\nValute supportate:")
for currency in supported_currencies:
    print(currency)

print("\nValute non supportate:")
for currency in unsupported_currencies:
    print(currency)


    import requests

# Funzione per verificare se una valuta è supportata da Banca Italia
def check_supported_currency(currency):
    # Esegui una richiesta all'API di Banca Italia per verificare i dati di cambio
    response = get_annual_exchange_rates('EUR', currency, 2023, 2023)
    if response:  # Se ci sono dati validi
        print(f"Valuta {currency} supportata!")
        return True
    else:
        print(f"Valuta {currency} non supportata.")
        return False

# Lista delle valute da testare
currencies_to_test = [
    'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 
    'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 
    'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR'
]

# Ciclo per verificare ciascuna valuta
for currency in currencies_to_test:
    check_supported_currency(currency)

