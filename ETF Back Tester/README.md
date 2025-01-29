# ETF Back Tester 📈

Welcome to the **ETF Back Tester**! This script allows you to simulate investments in ETFs using two methods: PAC (Periodic Accumulation Plan) and LUMP SUM (one-time investment).


## Features

- **View List of Available Indices**: Displays a list of available stock indices for simulation.
- **Simulate PAC**: Simulates a Periodic Accumulation Plan (PAC) with options for monthly, quarterly, and semiannual frequencies.
- **Simulate LUMP SUM**: Simulates a one-time investment on a specific date.

## Functionality

### 1. View List of Available Indices

This option displays a list of stock indices with their corresponding tickers that can be used for simulations.

### 2. Simulate PAC

This option allows you to simulate a PAC by entering:
- Index ticker
- Start date
- End date
- Frequency (monthly, quarterly, semiannual)
- PAC amount

The system will calculate the purchase dates, purchase prices, units purchased, and provide a summary of the investment results.

### 3. Simulate LUMP SUM

This option allows you to simulate a one-time investment by entering:
- Index ticker
- Investment date
- Evaluation end date
- Investment amount

The system will calculate the final value of the investment, total profit/loss, and percentage profit/loss.

## Dependencies

To run this script, the following Python libraries are required:
- `yfinance`
- `pandas`

You can install them using pip:
```bash
pip install yfinance pandas
```

## Technical Details
### Input Validation
The script includes validation functions for:

- Index tickers
- Dates in YYYY-MM-DD format
- Numeric amounts
- Download Historical Data

Uses the **yfinance library** to download historical stock index data.

### Investment Calculations
The script automatically calculates valid trading dates and purchase/sale values based on the downloaded historical data.

### Contributions
Contributions and suggestions are welcome! Feel free to open issues or pull requests in the repository.

## License
This project is licensed under the MIT License --->  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)