# Slot Machine Game

This Python script simulates a slot machine game where players can deposit money, place bets on up to 3 lines, and spin to win based on predefined symbol values and occurrences.

## Features

- **Deposit Money**: Players can deposit money to start playing and add more funds during the game.
- **Bet on Lines**: Choose to bet on 1 to 3 lines and specify the bet amount per line.
- **Spin the Slot Machine**: Generate random symbols in a 3x3 grid and check for winning lines.
- **Statistics Tracking**: Track winnings, losses, number of spins, ROI, and other metrics.
- **Interactive Feedback**: Get real-time updates on balance, winnings, and suggestions if the balance runs out.

## How It Works

1. **Symbols**:
   - The slot machine uses 4 symbols: `A`, `B`, `C`, and `D`.
   - Each symbol has a predefined count and value:
     - `A`: Count 2, Value 5
     - `B`: Count 4, Value 4
     - `C`: Count 6, Value 3
     - `D`: Count 8, Value 2
     --------------------------------------- 
    | Symbol | Frequency | Value (per line) |
    |--------|-----------|------------------|
    | A      | 2         | $5               |
    | B      | 4         | $4               |
    | C      | 6         | $3               |
    | D      | 8         | $2               |

Matching symbols on a line multiply the symbol's value by the bet amount.


2. **Winning Lines**:
   - A line is considered a winning line if all symbols in that line are the same.
   - Winnings are calculated as `symbol_value * bet per line`.

3. **Game Flow**:
   - Deposit money to start playing.
   - Choose the number of lines to bet on (1–3).
   - Specify the amount to bet per line (between $1 and $100).
   - Spin the slot machine and view the results.
   - Check winnings and update balance.
   - If the balance is zero, you can add more money or quit.

4. **Statistics**:
    The game provides detailed statistics, including:
   - Total spins
   - Total winnings and losses
   - Total amount bet
   - Number of spins with no winnings
   - Highest win and loss in a single spin
   - ROI (Return on Investment)

## How to Use

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/slot-machine.git
   ```

2. **Navigate to the Directory**:
   ```bash
   cd slot-machine
   ```

3. **Run the Script**:
   ```bash
   python slot_machine.py
   ```

4. **Follow the Prompts**:
   - Enter the amount to deposit.
   - Choose the number of lines to bet on.
   - Place a bet for each line.
   - Spin the slot machine and check the results.

5. **Quit or Continue**:
   - Press `q` to quit the game at any time.
   - Add more money if the balance runs out.



## Example Output

```
How much cash do you want to deposit? ($) 100
Enter the number of the lines to bet on (1-3)? 3
What would you like to bet on each line? $10
You are betting $10 on 3 lines. Total bet is equal to: $30

   B | B | B
   D | E | F
   G | H | I

You won $40.
Current balance is $110
...
```

## Additional Note
At the end of the game, a "secret" message will reveal the author's opinion on playing slot machines, encouraging thoughtful financial decisions.

## License
This project is licensed under the MIT License --->  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)