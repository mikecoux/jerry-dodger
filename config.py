import pygame
from lib.models import User, Score
from lib.user import save_user
from lib.score import save_score

# Define constants for the screen width and height
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Returns Press-Start-2P in the desired size
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Creates a user instance and sends to db
def capture_user(new_username):
    new_user = User(username = new_username)
    save_user(new_user)

# Creates a score instance and sends to db
def capture_score(new_score):
    new_score = Score(score = new_score)
    save_score(new_score)