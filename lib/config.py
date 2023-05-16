import pygame
from models import User, Score
from user import save_user, get_all_users, get_user_by_name
from score import save_score

# Define constants for the screen width and height
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Returns Press-Start-2P in the desired size
def get_font(size):
    return pygame.font.Font("./assets/font.ttf", size)

# Move these two out of config??
# Creates a user instance and sends to db
def capture_user(new_username):
    if new_username in [user.username for user in get_all_users()]:
        return get_user_by_name(new_username)
    else:
        new_user = User(username = new_username)
        save_user(new_user)
        return new_user

# Creates a score instance and sends to db
def capture_score(new_score, user):
    new_score = Score(score = new_score, user_id = user.id)
    save_score(new_score)