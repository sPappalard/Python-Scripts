import random
import time

# ASCII design of the dice
dice_faces = {
    1: ("┌───────┐", "│       │", "│   •   │", "│       │", "└───────┘"),
    2: ("┌───────┐", "│ •     │", "│       │", "│     • │", "└───────┘"),
    3: ("┌───────┐", "│ •     │", "│   •   │", "│     • │", "└───────┘"),
    4: ("┌───────┐", "│ •   • │", "│       │", "│ •   • │", "└───────┘"),
    5: ("┌───────┐", "│ •   • │", "│   •   │", "│ •   • │", "└───────┘"),
    6: ("┌───────┐", "│ •   • │", "│ •   • │", "│ •   • │", "└───────┘"),
}


while True:
    try:
        num_dice = int(input("How many dice do you want to roll? "))
        if num_dice > 0:
            break
        else:
            print("Enter a positive integer, please.")
    except ValueError:
        print("Invalid input. Please enter a number!")

# Function to show the animation of the loading (in accordind to the number of the dice to roll)
def roll_animation():
    if num_dice<5:
        print("Rolling the dice...")
        for _ in range(3):  # Repeat the animation 3 times
            print("\r[ .  .  . ]", end="")
            time.sleep(0.2)
            print("\r[ .. .. .. ]", end="")
            time.sleep(0.2)
            print("\r[ ... ... ]", end="")
            time.sleep(0.2)
        print("\r             ", end="")  # Clear the row
    elif num_dice>5 and num_dice<20:
        print("Rolling the dice...")
        for _ in range(6):  # Repeat the animation 6 times
            print("\r[ .  .  . ]", end="")
            time.sleep(0.2)
            print("\r[ .. .. .. ]", end="")
            time.sleep(0.2)
            print("\r[ ... ... ]", end="")
            time.sleep(0.2)
        print("\r             ", end="")  # Clear the row
    elif num_dice>20:
        print("Rolling the dice...")
        for _ in range(10):  # Repeat the animation 10 times
            print("\r[ .  .  . ]", end="")
            time.sleep(0.2)
            print("\r[ .. .. .. ]", end="")
            time.sleep(0.2)
            print("\r[ ... ... ]", end="")
            time.sleep(0.2)
        print("\r             ", end="")  # Clear the row



# function to print the dice
def print_dice(results, max_per_row=10):
    for i in range(0, len(results), max_per_row):
        chunk = results[i:i + max_per_row]  # obtain a row of dice
        dice_lines = [""] * 5  # each die has 5 ASCII's rows
        for die in chunk:
            face = dice_faces[die]
            for j in range(5):
                dice_lines[j] += face[j] + "  "  # add space between the dice
        for line in dice_lines:
            print(line)
        print()  # add an empty row beetwen rows of the dice

while True:
    choice = input("Roll the dice? (y/n): ").lower()
    if choice == 'y':
        roll_animation()  # show the loading animation
        results = [random.randint(1, 6) for _ in range(num_dice)]
        print("\nResults:")
        print_dice(results)  # show the dice
    elif choice == 'n':
        print("Thanks for playing!")
        time.sleep(2)
        break
    else:
        print("Invalid choice!")
