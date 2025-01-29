# Guess the Number Game

This script is a fun and interactive "Guess the Number" game with different modes and features. The game generates a random number within a specified range, and the user must guess the number. The script provides multiple difficulty levels, a timer, and a limited number of attempts for extra challenge.

## Features

1. **Game Modes:**
   - **Time Limit Mode (A)**: You have a limited time to guess the number.
   - **Attempts Limit Mode (B)**: You have a limited number of attempts to guess the number.
   - **Free Mode (C)**: No time or attempt limits, just guess until you get it right.

2. **Difficulty Levels:**
   - **Easy**: Easier mode with more time or attempts.
   - **Medium**: Moderate time/attempts for a balanced challenge.
   - **Hard**: A more challenging mode with limited time or attempts.

3. **Random Number Generation:**
   - The user selects a range for the number, and the script generates a random number within that range.
   - The game provides a visual countdown animation before the number is revealed.

4. **Input Validation:**
   - The script handles invalid inputs, such as non-numeric guesses or invalid difficulty/choice selections.

5. **Timer Functionality:**
   - In Time Limit mode, a countdown timer starts as soon as the game begins, and if time runs out, the user loses the game.
   - The time left is displayed during the guessing process.

6. **Attempt Tracking:**
   - In Attempts Limit mode, the user is given a set number of attempts to guess the number. If the attempts run out, the game ends.

7. **Feedback on Guesses:**
   - After each guess, the script provides feedback:
     - "Too low" if the guess is below the target number.
     - "Too high" if the guess is above the target number.
     - "Well done" when the guess is correct.

8. **Replay Option:**
   - After each game, the user can choose to play again or exit.

## Requirements

- `pyautogui`: Used to automatically press 'enter' after the game is over (for timer ends).

## How to Play

1. When prompted, type `Y` to start a new game or `N` to exit the game.
2. Choose a game mode:
   - **A** for Time Limit Mode
   - **B** for Attempts Limit Mode
   - **C** for Free Mode
3. Select a difficulty level and a number range for your guess.
4. Guess the number based on the feedback provided.
5. When you guess correctly or run out of time/attempts, the game ends, and you can choose to play again.

## License
This project is licensed under the MIT License --->  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



