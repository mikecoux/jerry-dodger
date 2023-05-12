# Import pygame and pygmame.locals for easier access to key coordinates
import pygame
from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT)
# Import player and enemy classes
from classes.player import Player
from classes.enemy import Enemy
# Import global vars
import config

# Initialize pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
# Pygame defines events internally as integers, so you need to define a new event with a unique integer
# The last event pygame reserves is 'USEREVENT', so adding the '+1' ensures that it's unique
# .set_timer() creates a 'ADDENEMY' event at the specified interval
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

# Instantiate player sprite
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Set up the game loop
# Game loop processes user input, updates state of game objs, updates display & audio output, maintains game speed
# User input results in an event being generated. Events are placed in the event queue which then can be accessed & manipulated
# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        # Instantiate new enemies and add them to the enemy group
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get the set of keys pressed and check for user input
    # .get_pressed() returns a dict containing all the current keydown events in the queue
    pressed_keys = pygame.key.get_pressed()

    # Update enemy positions via the enemy group
    enemies.update()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Surface allows you to 'draw' to the screen
    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player on the screen with .blit()
    # .blit() stands for 'block transfer'. You can use to to copy the surface onto another one (e.g. the original screen)
    # .blit() takes two args: 1. the surface to draw 2. the location at which to draw on the source surface
    # Draw all sprites: any sprite in the group will be 'drawn' with every frame
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    # .spritecollideany() method accepts a sprite and group as parameters
    # looks at every object in the group to see if its '.rect' intersects with the '.rect' of the sprite. If so, returns TRUE
    if pygame.sprite.spritecollideany(player, enemies):
        # If collision occurs, remove the player sprite and exit the loop
        player.kill()
        running = False

    # Update the display with .flip()
    # .flip() updates the screen with everything that's been drawn since the last .flip()
    pygame.display.flip()
