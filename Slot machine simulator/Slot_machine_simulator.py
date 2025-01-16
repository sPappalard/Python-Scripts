import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

#the count of the symbol (A:2 and B:4 means that we have two times A A three times B--> 'A' 'A' 'B' 'B' 'B' 'B')
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

#simulate the slot machine's spin
def get_slot_machine_spin(rows, cols, symbols):
    #create a list with all the symbol ['A','A','B','B','B','B','C','C','C','C','C','C','D'....(8 times)]
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    
    #generate the columns
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]            #copy the list all_symbols in current_symbols to avoid changes in the original list
        
        #for each row of the column, we select randomly a symbol (from current symbols) --> this symbol is removed from current symbols (to avoid duplicates in the same column) and the symbol is added in the column
        for _ in range(rows):
            value = random.choice(current_symbols)      #Take a random symbol from "current_symbols"
            current_symbols.remove(value)
            column.append(value)                        #add this symbol to Columns

        columns.append(column)      #since the column is completed, it is added in COLUMNS

    return columns


#to print the result of a slot_machine's result

#columns is a list of list  (with 3 rows)
#Example:
#columns = [
#  ['A', 'B', 'C'],  first column
#  ['D', 'E', 'F'],  second column
#  ['G', 'H', 'I']   third column
#]
# with the print funcion, this is the output:

#   A | D | G
#   B | E | H
#   C | F | I

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):        #for each symbol in the current row
            if i != len(columns) - 1:                       #if the column isn't the last
                print(column[row], end=" | ")                   #print symbol + |
            else:
                print(column[row], end="")                      #print only the symbol (without |)

        print()




#to check the winnings and calculate the total winning (based on the bet and symbol values)
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    #win check
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]          
            if symbol != symbol_to_check:           #If the symbol is different in one of the columns, the line is not winning, and the inner cycle is broken.
                break
        else:   #winner case--> if the for cicle comes to end without meeting a break
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines          #return the total amount won and a list of winning lines




#User inserts the deposit
def deposit():
    while True:
        amount = input("How much cash do you want to deposit? ($)")
        if amount.isdigit():
            amount=int(amount)
            if amount>0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount

#User chooses the number of line to bet
def get_number_of_lines():
    while True:
        lines = input("Enter the number of the lines to bet on (1-"+str(MAX_LINES) +")?")
        if lines.isdigit():
            lines = int(lines) 
            if 1<= lines <=MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines

#user choses the amount to bet in each line
def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")
    return amount



def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet *lines

        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
        else:
            break
    
    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet


#MAIN
def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
    if balance == 0:
        print("You have run out of money!")
        print(f"Thanks for playing!\nYou left with ${balance}")

main()