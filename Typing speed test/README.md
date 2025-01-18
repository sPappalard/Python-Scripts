# Typing Speed Test

This script is a **Typing Speed Test** application built in Python using the `curses` library. It challenges users to type randomly generated sentences as quickly and accurately as possible while tracking their speed and errors.

## Features

- **Random Sentence Generation**: Sentences are dynamically created using a predefined set of words and structures.
- **Typing Speed Measurement**: Calculates typing speed in words per minute (WPM).
- **Error Tracking**: Highlights incorrect characters in real-time.
- **User Statistics**: Displays detailed statistics, including WPM, accuracy, total time, and errors.
- **Retry or Exit**: Allows users to retry the test or exit after completion or abandonment.

## How to Use

1. **Run the Script**: Execute the script using Python in a terminal that supports the `curses` library.
   ```bash
   python Typing_speed_test.py

2. **Start the Test**: Follow the on-screen instructions and press any key to begin.

3. **Typing:** Type the sentence displayed on the screen as accurately and quickly as possible.
- Correctly typed characters are highlighted in green.
- Incorrectly typed characters are highlighted in red.
4. **Abandon or Finish:**
- Press ESC to abandon the test. You will be prompted to retry or exit.
- Complete the sentence to view your statistics.

5. **Retry or Exit:** After completing or abandoning, choose to retry or exit the application.

## Dependencies
- Python 3.6 or later.
- The curses library (included in the Python standard library for most platforms).


## Functionality Breakdown
**Sentence Types**
The sentences are generated dynamically in three formats:

- Normal Sentences: Subject-Verb-Object structures with adjectives, adverbs, and conjunctions.
- Questions: Randomly generated questions.
- Dialogues: Sentences wrapped in dialogue starters and exclamations.

**Real-Time Feedback**
- Correct characters are displayed in green.
- Incorrect characters are displayed in red.

**Statistics**
After the test, the following metrics are displayed:

- Words per minute (WPM).
- Total time taken.
- Total characters typed.
- Total errors made.
- Accuracy percentage.

## Outup Example

**Start Screen**
```Welcome to the Speed Typing Test!
Press any key to begin!
...
```

**Typing View**
```The curious cat jumps over a delicious sandwich happily. But it was challenging near the river.
WPM: 45
...
```

**Statistics Screen**
```Test Complete!

Words per minute: 45
Total time: 25 seconds
Total characters typed: 62
Total errors: 3
Accuracy: 95.16%

Press any key to continue...
...
```

## Dependencies

To run this project, ensure you have the following:

- **Python 3.6 or later**: Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/).
- **Curses Library**: This library is included in the Python standard library for most Unix-based systems (Linux, macOS).  
  - **For Windows Users**: The `curses` library is not natively supported. Install the `windows-curses` package by running:
    ```bash
    pip install windows-curses
    ```
