# Genarate a random number and ask to user to make a guess
#If not a valid number--> print an error
#If number < guess--> print " too low"
#If number > guess--> print "too hight"
#Else --> print "well done"


import random
import time
import threading
import sys
import pyautogui # type: ignore

def timer_background(duration,stop_event,game_over_event):    
    # print the initial timer
    print(f"\nTime left: {duration} seconds")

    while duration > 0:
        if stop_event.is_set():
            return
        time.sleep(1)
        duration -= 1
       
    
    if not game_over_event.is_set():
        # when the timer ends, print the final message
        print("\nTime's up! You lost!!")
        game_over_event.set()
        time.sleep(2)  
        pyautogui.press('enter')
     
def GenerationNumber(inf,sup):
    print("I'm generating a mysterious number between "+ str(inf) +" and "+ str(sup))
    for _ in range(5):  # Repeat the animation 3 times
        print("\r[ .  .  . ]", end="")
        time.sleep(0.2)
        print("\r[ .. .. .. ]", end="")
        time.sleep(0.2)
        print("\r[ ... ... ]", end="")
        time.sleep(0.2)
    print("\r             ", end="")  # Clear the row
    time.sleep(0.2)


def  Guess_the_number(number, inf, sup, game_over_event, start_time, timer, attempts_max):
    attempts=0
    while not game_over_event.is_set():  #continue until the end of the timer
        try:
            guess = int(input(f"\nGuess the number between {inf} and {sup}: "))

            
            end_time = time.time()
            spent_time = round(end_time - start_time, 2)
            attempts= attempts+1

            if (timer != 0):
                remaining_time = round(timer - spent_time, 2)
                print(f"\nTime remaining: {remaining_time} seconds.")
                


            if guess < number:
                if guess <inf:
                    print("I said between " + str(inf) + " and " + str(sup) + "!!!! \n")
                else:
                    print("Too low!\n")
                if attempts_max != 0 and attempts<attempts_max:
                    difference = (attempts_max - attempts)
                    print(f"You have {difference} attempts left! ")
                if attempts_max != 0 and attempts==attempts_max:
                    print(f"Oh no... you are out of attempts!") 
                    time.sleep(2)
                    game_over_event.set()  #finish the game
                    return True
                

            elif guess >number:
                if guess >sup:
                    print("I said between " + str(inf) + " and " + str(sup) + "!!!! \n")
                else:
                    print("Too high\n")
                if attempts_max != 0 and attempts<attempts_max:
                    difference = (attempts_max - attempts)
                    print(f"You have {difference} attempts left! ")
                if attempts_max != 0 and attempts==attempts_max:
                    print(f"Oh no... you are out of attempts!")
                    time.sleep(2)
                    game_over_event.set()  #finish the game
                    return True
           
            else:
                end_time = time.time()      #set the final time
                spent_time = round(end_time-start_time, 2)
                print(f"Congratulations! You guessed the number. Time spent: {spent_time} seconds. Number of attempts: {attempts} ")
                time.sleep(2)
                game_over_event.set()  #finish the game
                return True
        except ValueError:
               print("You have another possibility")


def reset_game():
    while True:
        choice = input("\nDo you want retry? (y/n) : ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            print("Thanks for playing")
            time.sleep(1)
            sys.exit()
        else:
            print("Response not valid. Insert 'y' or 'n' please.")

stop_event = threading.Event()
game_over_event = threading.Event()

exit_game=True

while exit_game:
    try:
        choice = (input("Do you want play a hilarious game? "))
        if choice.upper() == 'Y':
            while True:
                print("Choose the mode: A) Time limit     B) Attempts limit     C) Free")
                mode = (input("----> ")).strip().upper()

                game_running = True

                while game_running:
                    if mode == "A":
                        stop_event.clear()
                        game_over_event.clear()

                        print("Choose the difficulty: Easy(E)     Medium(M)       Hard(H)")
                        Difficulty = (input("---->")).strip().upper()
                        if Difficulty == ('E'):
                            timer = 180
                        elif Difficulty == ('M'):
                            timer = 90
                        elif Difficulty == ('H'):
                            timer = 60
                        else:
                            print ("Please enter a valid character")
                            game_running=False
                            break

                        print("OK! Choose the range:")
                        range_INF = (int(input("Lower limit--> ")))
                        range_SUP = (int(input("Upper limit--> ")))
                        number_to_guess = random.randint(range_INF,range_SUP)
                        GenerationNumber(range_INF,range_SUP)
                        
                        #start the timer in a separate thread
                        timer_thread = threading.Thread(
                            target=timer_background,
                            args=(timer, stop_event, game_over_event)
                        )
                        timer_thread.start()                    

                        # Register the start time
                        start_time = time.time()

                        # Start the game

                        victory = Guess_the_number(number_to_guess, range_INF, range_SUP, game_over_event, start_time,timer,0)
                        stop_event.set()
                        timer_thread.join()
                        
                        if not game_over_event.is_set():
                            # Handle timeout scenario
                                game_over_event.set()

                        if not reset_game():
                            exit_game = False
                            break
                        else:
                            game_running = False
                            break
                        
                                            
                            
                    elif mode.upper() == "B":
                        stop_event.clear()  
                        game_over_event.clear()

                        print("Choose the difficulty: Easy(E)     Medium(M)       Hard(H)")
                        Difficulty = (input("---->")).strip().upper()
                        if Difficulty == ('E'):
                            attempts = 10
                        elif Difficulty == ('M'):
                            attempts = 5
                        elif Difficulty == ('H'):
                            attempts = 3
                        else:
                            print ("Please enter a valid character")
                            continue

                        print("OK! Choose the range:")
                        range_INF = (int(input("Lower limit--> ")))
                        range_SUP = (int(input("Upper limit--> ")))
                        number_to_guess = random.randint(range_INF,range_SUP)
                        GenerationNumber(range_INF,range_SUP)

                        start_time = time.time()

                        Guess_the_number(number_to_guess, range_INF, range_SUP, game_over_event, start_time,0,attempts)
                        
                        if not reset_game():
                            exit_game=False
                            break
                        else:
                            game_running=False
                            break


                    elif mode.upper() == "C":
                        stop_event.clear()
                        game_over_event.clear()


                        print("OK! Choice the range:")
                        range_INF = (int(input("Lower limit--> ")))
                        range_SUP = (int(input("Upper limit--> ")))
                        number_to_guess = random.randint(range_INF,range_SUP)
                        
                        GenerationNumber(range_INF,range_SUP)
                        Guess_the_number(number_to_guess, range_INF, range_SUP, game_over_event, time.time(),0,0)
                        
                        if not reset_game():
                            exit_game=False
                            break
                        else:
                            game_running=False
                            break

                    else: 
                        print ("Please enter a valid character")
                        game_running=False
                        break

            
        elif choice.upper() == 'N' :
            print("Ok, sorry for the incovenience...")
            time.sleep(2)
            exit_game=False
            break
        else:
            print("Enter valid answer, please.")
    except ValueError:
        print("Invalid input. Please enter a valid input!")

 





