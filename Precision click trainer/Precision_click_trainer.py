import math
import random
import time
import pygame
import os

pygame.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "sounds")

# windows game dimensions 
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Precision Click Trainer")

# background colors
BG_COLORS = {
    "purple": (128, 0, 128),
    "orange":(255, 165, 0),
    "blue": (0, 25, 40), 
    "red": (40, 0, 0), 
    }

DIFFICULTIES = {
    "very easy": 2000, 
    "easy": 1000, 
    "medium": 600, 
    "hard": 400, 
    "very hard": 200
    }

# global variables
TARGET_INCREMENT = DIFFICULTIES["medium"]
BG_COLOR = BG_COLORS["blue"]
SOUNDS_ENABLED = True

# Sounds
CLICK_SOUND = pygame.mixer.Sound(os.path.join(ASSET_PATH, "click.wav"))
MISS_SOUND = pygame.mixer.Sound(os.path.join(ASSET_PATH, "miss.wav"))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join(ASSET_PATH, "game_over.wav"))

#costants of the game
TARGET_PADDING = 30
LIVES = 20
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)
TARGET_EVENT = pygame.USEREVENT

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

    #to draw concentric squares to represent the target with different colors and sizes
    def draw(self, win):
        size = int(self.size)
        pygame.draw.rect(win, self.COLOR, (self.x - size, self.y - size, size * 2, size * 2))
        pygame.draw.rect(win, self.SECOND_COLOR, (self.x - size * 0.8, self.y - size * 0.8, size * 1.6, size * 1.6))
        pygame.draw.rect(win, self.COLOR, (self.x - size * 0.6, self.y - size * 0.6, size * 1.2, size * 1.2))
        pygame.draw.rect(win, self.SECOND_COLOR, (self.x - size * 0.4, self.y - size * 0.4, size * 0.8, size * 0.8))

    #Checks if the mouse click is inside the target by calculating the distance between the mouse position and the target
    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.size

#to draw a button
class Button:
    def __init__(self, x, y, width, height, text, font, color, text_color, hover_color=None, border_color=None, shadow_color=None, border_radius=15):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color or color
        self.border_color = border_color
        self.shadow_color = shadow_color
        self.border_radius = border_radius


    def draw(self, win):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        # Draw shadow (if present)
        if self.shadow_color:
            shadow_rect = self.rect.move(3, 3)
            pygame.draw.rect(win, self.shadow_color, shadow_rect, border_radius=self.border_radius)

        # Draw main button
        pygame.draw.rect(win, current_color, self.rect, border_radius=self.border_radius)

        # Draw border (if present)
        if self.border_color:
            pygame.draw.rect(win, self.border_color, self.rect, width=3, border_radius=self.border_radius)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        win.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# start menu
def main_menu():
    global TARGET_INCREMENT, BG_COLOR, SOUNDS_ENABLED

    run = True
    title_font = pygame.font.SysFont("arialrounded", 50)
    BUTTON_FONT = pygame.font.SysFont("arialrounded", 40)


    difficulty = "medium"
    bg_color_choice = "blue"
    sounds_enabled = True

    buttons = {
        "difficulty": Button(WIDTH // 2 - 300, 200, 600, 70, f"Difficulty: {difficulty.capitalize()}", BUTTON_FONT, (50, 50, 50), "white"),
        "bg_color": Button(WIDTH // 2 - 300, 300, 600, 70, f"Background color: {bg_color_choice.capitalize()}", BUTTON_FONT, (50, 50, 50), "white"),
        "sounds": Button(WIDTH // 2 - 300, 400, 600, 70, f"Sounds: {'Active' if sounds_enabled else 'Disabled'}", BUTTON_FONT, (50, 50, 50), "white"),
        "play": Button(WIDTH // 2 - 300, 600, 600, 70, "Play", BUTTON_FONT, (0, 200, 0), "white")
    }

    dropdown_open = None

    while run:
        WIN.fill(BG_COLORS[bg_color_choice])            #menu background is colored according to the current choice

        # Title
        title_label = title_font.render("Precision Click Trainer - Menu", 1, "white")
        WIN.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, 50))

        # Draw the button
        for key, button in buttons.items():
            button.draw(WIN)

        # Draw dropdown if it is open
        dropdown_clicked = False  # to handle the clicks in the dropdow
        if dropdown_open == "difficulty":
            pygame.draw.rect(WIN, "white", (WIDTH // 2 - 300, 270, 600, len(DIFFICULTIES) * 60), border_radius=20)  # Background box
            pygame.draw.rect(WIN, "black", (WIDTH // 2 - 300, 270, 600, len(DIFFICULTIES) * 60), width=3, border_radius=20)  # Border

            for i, key in enumerate(DIFFICULTIES.keys()):
                option = Button(
                    x=WIDTH // 2 - 290, y=280 + i * 60, width=580, height=50,
                    text=key.capitalize(), font=BUTTON_FONT,
                    color="lightgrey", text_color="black",
                    hover_color="grey", border_color="black", shadow_color="darkgrey", border_radius=10
                )
                option.draw(WIN)
                if pygame.mouse.get_pressed()[0] and option.is_clicked(pygame.mouse.get_pos()):
                    difficulty = key
                    buttons["difficulty"].text = f"Difficulty: {difficulty.capitalize()}"
                    dropdown_open = None
                    dropdown_clicked = True

        elif dropdown_open == "bg_color":
            pygame.draw.rect(WIN, "white", (WIDTH // 2 - 300, 370, 600, len(BG_COLORS) * 60), border_radius=20)  # Background box
            pygame.draw.rect(WIN, "black", (WIDTH // 2 - 300, 370, 600, len(BG_COLORS) * 60), width=3, border_radius=20)  # Border

            for i, key in enumerate(BG_COLORS.keys()):
                option = Button(
                    x=WIDTH // 2 - 290, y=380 + i * 60, width=580, height=50,
                    text=key.capitalize(), font=BUTTON_FONT,
                    color="lightgrey", text_color="black",
                    hover_color="grey", border_color="black", shadow_color="darkgrey", border_radius=10
                )
                option.draw(WIN)
                if pygame.mouse.get_pressed()[0] and option.is_clicked(pygame.mouse.get_pos()):
                    bg_color_choice = key
                    buttons["bg_color"].text = f"Background color: {bg_color_choice.capitalize()}"
                    BG_COLOR = BG_COLORS[bg_color_choice] 
                    dropdown_open = None
                    dropdown_clicked = True

        pygame.display.update()

        #to handle event in start menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # if a dropdown options is clicked, ignore the other buttons
                if dropdown_clicked:
                    continue
                
                if buttons["difficulty"].is_clicked(pos):
                    dropdown_open = "difficulty" if dropdown_open != "difficulty" else None
                elif buttons["bg_color"].is_clicked(pos):
                    dropdown_open = "bg_color" if dropdown_open != "bg_color" else None
                elif buttons["sounds"].is_clicked(pos):
                    sounds_enabled = not sounds_enabled
                    buttons["sounds"].text = f"Sounds: {'Active' if sounds_enabled else 'Disable'}"
                elif buttons["play"].is_clicked(pos):
                    TARGET_INCREMENT = DIFFICULTIES[difficulty]
                    160
                    SOUNDS_ENABLED = sounds_enabled
                    run = False



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
    main_menu()
    
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
                if SOUNDS_ENABLED:
                    CLICK_SOUND.play()

        for target in targets:          #for each active targets
            target.update()               #update the dimensions of the target
 
            if target.size <= 0:
                targets.remove(target)
                misses += 1
                if SOUNDS_ENABLED:
                    MISS_SOUND.play()

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if misses >= LIVES:
            if SOUNDS_ENABLED:
                GAME_OVER_SOUND.play()
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        draw(WIN, targets)                                          #draw all the targets in the windows
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)    #draw the top bar in the windows
        pygame.display.update()                                     #update the display to show the changement

    pygame.quit()


if __name__ == "__main__":
    main()  