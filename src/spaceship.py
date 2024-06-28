import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk  # Ensure you have Pillow installed: pip install pillow
import random
import os

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 50
STAR_WIDTH = 30
STAR_HEIGHT = 30
ASTEROID_WIDTH = 40
ASTEROID_HEIGHT = 40
MOVEMENT_STEP = 20
STAR_POINTS = 10
FALLING_STEP = 5  # Speed of falling objects

# Initialize the main window
root = tk.Tk()
root.title("Spaceship Adventure Game")
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

# Load and resize images
base_path = os.path.dirname(__file__)  # Get the directory of the script

background_img = Image.open(os.path.join(base_path, 'images', 'background.png'))
background_img = background_img.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)
background_img = ImageTk.PhotoImage(background_img)

spaceship_img = Image.open(os.path.join(base_path, 'images', 'spaceship.png'))
spaceship_img = spaceship_img.resize((SPACESHIP_WIDTH, SPACESHIP_HEIGHT), Image.Resampling.LANCZOS)
spaceship_img = ImageTk.PhotoImage(spaceship_img)

star_img = Image.open(os.path.join(base_path, 'images', 'star.png'))
star_img = star_img.resize((STAR_WIDTH, STAR_HEIGHT), Image.Resampling.LANCZOS)
star_img = ImageTk.PhotoImage(star_img)

asteroid_img = Image.open(os.path.join(base_path, 'images', 'asteroid.png'))
asteroid_img = asteroid_img.resize((ASTEROID_WIDTH, ASTEROID_HEIGHT), Image.Resampling.LANCZOS)
asteroid_img = ImageTk.PhotoImage(asteroid_img)

# Game variables
spaceship = None
stars = []
asteroids = []
score = 0

def show_intro():
    """ Display the intro message and get the username """
    global username
    intro_msg = "Welcome to Spaceship Adventure!\nPlease enter your username."
    username = simpledialog.askstring("Username", intro_msg)
    if not username:
        username = "Player"
    start_game()

def start_game():
    """ Initialize the game elements """
    global spaceship, score
    score = 0
    canvas.create_image(0, 0, image=background_img, anchor=tk.NW)  # Add the background image
    spaceship = canvas.create_image(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100, image=spaceship_img)
    spawn_stars()
    spawn_asteroids()
    update_game()

def spawn_stars():
    """ Create stars at random positions """
    for _ in range(5):
        x = random.randint(0, WINDOW_WIDTH - STAR_WIDTH)
        y = random.randint(-WINDOW_HEIGHT, 0)
        star = canvas.create_image(x, y, image=star_img)
        stars.append(star)

def spawn_asteroids():
    """ Create asteroids at random positions """
    for _ in range(3):
        x = random.randint(0, WINDOW_WIDTH - ASTEROID_WIDTH)
        y = random.randint(-WINDOW_HEIGHT, 0)
        asteroid = canvas.create_image(x, y, image=asteroid_img)
        asteroids.append(asteroid)

def move_spaceship(event):
    """ Move the spaceship left or right """
    x, y = canvas.coords(spaceship)
    if event.keysym == 'Left' and x > SPACESHIP_WIDTH // 2:
        canvas.move(spaceship, -MOVEMENT_STEP, 0)
    elif event.keysym == 'Right' and x < WINDOW_WIDTH - SPACESHIP_WIDTH // 2:
        canvas.move(spaceship, MOVEMENT_STEP, 0)

def update_game():
    """ Update the game state """
    global score
    for star in stars:
        canvas.move(star, 0, FALLING_STEP)
        if canvas.coords(star)[1] > WINDOW_HEIGHT:
            canvas.delete(star)
            stars.remove(star)
            continue
        if check_collision(spaceship, star):
            canvas.delete(star)
            stars.remove(star)
            score += STAR_POINTS
    
    for asteroid in asteroids:
        canvas.move(asteroid, 0, FALLING_STEP)
        if canvas.coords(asteroid)[1] > WINDOW_HEIGHT:
            canvas.delete(asteroid)
            asteroids.remove(asteroid)
            continue
        if check_collision(spaceship, asteroid):
            end_game()
            return
    
    if not stars:
        spawn_stars()
    if not asteroids:
        spawn_asteroids()
    
    canvas.after(50, update_game)

def check_collision(obj1, obj2):
    """ Check if two objects collide """
    x1, y1 = canvas.coords(obj1)
    x2, y2 = canvas.coords(obj2)
    if (abs(x1 - x2) < SPACESHIP_WIDTH // 2 + STAR_WIDTH // 2) and (abs(y1 - y2) < SPACESHIP_HEIGHT // 2 + STAR_HEIGHT // 2):
        return True
    return False

def end_game():
    """ Display the game over message and score """
    messagebox.showinfo("Game Over", f"Game Over!\nYour score: {score}")
    root.destroy()

# Bind keys for spaceship movement
root.bind("<Left>", move_spaceship)
root.bind("<Right>", move_spaceship)

# Start the game
show_intro()
root.mainloop()
