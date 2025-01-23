import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600            #dimensions of the game window(pixels)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))      #creates the window
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 4000                          #interval (in milliseconds) at which a new target appears
TARGET_EVENT = pygame.USEREVENT                 #custom event defined for handling the target generation

TARGET_PADDING = 30                         #space from the edges of the window where targets can appear

BG_COLOR = (0, 25, 40)                      #background color of the window
LIVES = 20                                   # numbers of lives the player has
TOP_BAR_HEIGHT = 50                         # the height of the top bar that displays information

LABEL_FONT = pygame.font.SysFont("comicsans", 24)           #font used to render text in the game (font,dimensions)


#represents a target object that the player tries to hit
class Target:
    MAX_SIZE = 30           #the maximum size the target will grow to
    GROWTH_RATE = 0.2       #The rate at which the target grows or shrinks
    COLOR = "red"                       
    SECOND_COLOR = "white"

    #x,y= coordinates of the target
    #size= current size of the target
    #grow= a boolean indicating if the target should keep growing or start shrinking
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    #to control the growth and shrinkng of the target
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    #to draw concentric circles to represent the target with different colors and sizes
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR,(self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    #Checks if the mouse click is inside the target by calculating the distance between the mouse position and the target
    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.size

#to draw the background and all the active targets
def draw(win, targets):
    win.fill(BG_COLOR)          #clears the screen

    for target in targets:      
        target.draw(win)            #draws all the targets


#to format the elapsed time into a string (minutes:seconds.milliseconds)
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

# Draws the top bar showing the game stats like time, speed (targets per second), hits, and remaining lives.
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))            #draw the top bar
    
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black") #create a text label for time

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")          #create a text label for speed

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")      #create a text label for hits

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")    #create a text label for remaining lives

    #place the labels in the windows
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

#to show end screen with Game statistics when the player loses all lives
def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)                                                                  #fill the window with the background color 
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")     #create a text label for time  

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")              #create a text label for speed

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")          #create a text label for hits

    if clicks>0:
        accuracy = round(targets_pressed / clicks * 100, 1)
    else:
        accuracy=0

    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")        #create a text label for the accurency

    #place the labels in the center of the windows
    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()                 #update the windows to show the changements

    run = True
    while run:                                  #Waits for the user to close the window or press a key to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


# to calculate the Horizontal central position for a graphic element on the game window (surface is a Pygame element, such as a text label of which I want to calculate the horizontal central position)
def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2


def main():
    #-----initializations-----
    run = True
    targets = []                    #lilst of active targets
    clock = pygame.time.Clock()     #clock object of Pygame to handle the frame rate

    targets_pressed = 0             #counter of targets pressed
    clicks = 0                      #counter of clicks did by the player
    misses = 0                      #counter of targets missed
    
    start_time = time.time()        #Saves the start time of the game

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)       #set a timer to generate a TARGET_EVENT at regular intervals defined by TARGET_INCREMENT

    #-----main cycle of the game-----
    while run:
        clock.tick(60)          #set 60 FPS frame rate
        click = False           #set click=FALSE at the beginning of each frame
        mouse_pos = pygame.mouse.get_pos()              #to obtain the current position of the mouse
        elapsed_time = time.time() - start_time         #calculate the elapsed time

        #---event handle---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               #if player close the window
                run = False                 
                break

            if event.type == TARGET_EVENT:                                              #if the TARGET_EVENT occurs    
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)              #it creates a new target in a random position
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)           
                targets.append(target)              #add the new target element in the list Targets

            if event.type == pygame.MOUSEBUTTONDOWN:        #if a mouse click occurs 
                click = True
                clicks += 1

        for target in targets:          #for each active targets
            target.update()               #update the dimensions of the target

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        draw(WIN, targets)                                          #draw all the targets in the windows
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)    #draw the top bar in the windows
        pygame.display.update()                                     #update the display to show the changement

    pygame.quit()


if __name__ == "__main__":
    main()  