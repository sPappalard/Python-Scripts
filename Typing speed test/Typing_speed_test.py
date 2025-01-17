import curses
from curses import wrapper
import time
import random


# Lists to generate senteces of completed meaning
SUBJECTS = ["The curious cat", "A brilliant programmer", "The patient teacher", "My adventurous friend", "The energetic dog"]
VERBS = ["writes", "jumps over", "eats", "solves", "creates", "discovers", "analyzes", "explains"]
OBJECTS = ["a complex program", "an interesting book", "a delicious sandwich", "the difficult problem", "an exciting story", "the mysterious case", "a new recipe"]
ADVERBS = ["quickly", "happily", "lazily", "efficiently", "slowly", "with great effort", "without hesitation", "in a creative way"]
ADJECTIVES = ["beautiful", "challenging", "unexpected", "fascinating", "complex", "strange"]
PREPOSITIONS = ["in the park", "on the table", "under the tree", "at the library", "near the river", "inside the house"]
CONJUNCTIONS = ["and then", "but", "because", "while", "although", "so that"]
QUESTIONS = ["Why did the cat", "How can a programmer", "When will the teacher", "What does my friend", "Where should the dog"]
ACTIONS = ["solve", "find", "understand", "improve", "complete"]
CONDITIONALS = ["if it rains", "when the sun rises", "after the meeting", "before dinner", "while everyone is sleeping"]
DIALOGUE_STARTERS = ["He said,", "She asked,", "They shouted,", "He whispered,", "She replied,"]
EXCLAMATIONS = ["Wow!", "Oh no!", "Fantastic!", "Unbelievable!", "That's great!"]


#to generate random sentece of completed meaning
def generate_random_sentence(sentence_type):

    if sentence_type == "random":
        sentence_type = random.choice(["normal", "question", "dialogue"])

    if sentence_type == "normal":
        subject = random.choice(SUBJECTS)
        verb = random.choice(VERBS)
        obj = random.choice(OBJECTS)
        adverb = random.choice(ADVERBS)
        adjective = random.choice(ADJECTIVES)
        preposition = random.choice(PREPOSITIONS)
        conjunction = random.choice(CONJUNCTIONS)
        first_part = f"{subject} {verb} {obj} {adverb}."
        second_part = f"{conjunction} it was {adjective} {preposition}.".capitalize()
        return f"{first_part} {second_part}"
    elif sentence_type == "question":
        question = random.choice(QUESTIONS)
        action = random.choice(ACTIONS)
        obj = random.choice(OBJECTS)
        conditional = random.choice(CONDITIONALS)
        return f"{question} {action} {obj} {conditional}?"
    elif sentence_type == "dialogue":
        dialogue_starter = random.choice(DIALOGUE_STARTERS)
        exclamation = random.choice(EXCLAMATIONS)
        sentence = generate_random_sentence("normal").capitalize()  
        return f"{dialogue_starter} \"{sentence} {exclamation}\""

#to calculate and display statistics        
def show_statistics(stdscr, wpm, time_elapsed, errors, total_characters):
    stdscr.clear()
    stdscr.addstr("Test Complete!\n\n")
    stdscr.addstr(f"Words per minute: {wpm}\n")
    stdscr.addstr(f"Total time: {round(time_elapsed, 2)} seconds\n")
    stdscr.addstr(f"Total characters typed: {total_characters}\n")
    stdscr.addstr(f"Total errors: {errors}\n")
    accuracy = ((total_characters - errors) / total_characters) * 100 if total_characters > 0 else 0
    stdscr.addstr(f"Accuracy: {round(accuracy, 2)}%\n")
    stdscr.addstr("\nPress any key to continue...")
    stdscr.refresh() 
    stdscr.getkey()

#stdscr is the principal window handled by Curses (Python Library)
def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)                   #show the target text in the screen
	stdscr.addstr(1, 0, f"WPM: {wpm}")      #show the wpm in the second line of the screen
    
    #cycle to higlight the characters
    #for each character digitated 
	for i, char in enumerate(current):      
		correct_char = target[i]            #take the correct character from the target phrase and save it in "correct char"
		color = curses.color_pair(1)        #set the default color to "correct color(green)"
		if char != correct_char:                #if character digitated is different from "correct_char"--> change the coulor in "incorrect color (red)"
			color = curses.color_pair(2)

		stdscr.addstr(0, i, char, color)        #write the characte digitated in the screen, in the correct position and with the appropriate color (green or red)



def wpm_test(stdscr):
    target_text = generate_random_sentence("random")   # Read the phrase to digit
    current_text = []
    wpm = 0                     # Words per minute
    errors = 0                  # Error counter
    start_time = time.time()    # Record the start time of the test         
    stdscr.nodelay(True)        # Makes the terminal non-blocking (does not wait input, just continue to run the cycle)
    
    abandoned = False  #to track if the user drops out of the game

    while True:
        time_elapsed = max(time.time() - start_time, 1)  # Time from the beginning of the test
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)  # Calculate the wpm

        # Update the screen
        stdscr.clear()                                          # Clear the screen
        display_text(stdscr, target_text, current_text, wpm)    # Show target text, current text (the one typed so far) and actual WPM
        stdscr.refresh()                                        # Update the screen with the new content

        # Check if we finished the test
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)                   # Make the terminal blocking (useful when we want to stop the running until a specific input is provided)
            break

        try:
            key = stdscr.getkey()           # Try to read a button pressed by the user
        except:
            continue                        # If the user doesn't press any button, the run continues

        if key == "\x1b":                 # If the button pressed is ESC  --> cycle is broken, and the run is stopped
            stdscr.nodelay(False)  
            abandoned = True
            break

        # Ignore arrow keys and other special keys
        if key.startswith("KEY_"):
            continue

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):          # If the user presses BACKSPACE
            if len(current_text) > 0:                           # And there are still characters in current_text
                current_text.pop()                                  # The last character was removed
                
        elif len(current_text) < len(target_text):          # If the button pressed is different from BACKSPACE and there are still characters to type
            current_text.append(key)
            if key != target_text[len(current_text)-1]:  # If the typed character is wrong
                errors += 1  
    
    if abandoned:
        stdscr.clear()
        stdscr.addstr("You abandoned the test.\n")
        stdscr.addstr("Press 'R' to retry or 'ESC' to exit.\n")
        stdscr.refresh()
        while True:
            key = stdscr.getkey()
            if key.lower() == 'r':  # Retry
                return True
            elif key == "\x1b":  # ESC
                return False
    else:
        total_characters = len(target_text)
        stdscr.nodelay(False)  
        show_statistics(stdscr, wpm, time_elapsed, errors, total_characters)
        return True

#MAIN
def main(stdscr):
    # Initialize colors to highlight characters
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)     
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Show the initial window
    start_screen(stdscr)
    
    while True:
        retry = wpm_test(stdscr)  # Esegue il test e restituisce True (riprova) o False (esci)
        if not retry:
            break

    stdscr.clear()
    stdscr.addstr("Thank you for playing! Goodbye!"
    )
    stdscr.refresh()
    time.sleep(2)

wrapper(main)
