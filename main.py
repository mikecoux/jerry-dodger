# Import pygame and pygmame.locals for easier access to key coordinates
import pygame, sys
from pygame.locals import (K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT)
# Import player and enemy classes
from classes.player import Player
from classes.enemy import Enemy
from classes.button import Button
# Import global vars
import config
import pygame_gui

# Initialize pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

# Create the main menu
def main_menu():
    pygame.display.set_caption("Main Menu")

    while True:
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Capture the mouse position
        menu_mouse_pos = pygame.mouse.get_pos()

        # Draw text to the screen
        menu_text = config.get_font(90).render("JERRY DODGER", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        # Instantiate buttons
        play_button = Button(image=pygame.image.load("assets/play-rect.png"), pos=(640, 250), text_input="PLAY",
                             font=config.get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        # Draw the menu text on the screen
        screen.blit(menu_text, menu_rect)

        # Run the button methods
        play_button.change_color(menu_mouse_pos)
        # Draw the button on the screen
        play_button.update(screen)

        # Look at every event in the queue
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    set_user()

        pygame.display.flip()

# Set your username
def set_user():
    pygame.display.set_caption("Create Username")

    # Create the GUI manager
    manager = pygame_gui.UIManager((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    # Create the clock??
    clock = pygame.time.Clock()
    # Create the text input
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 360), (500, 50)), 
                                                    manager=manager, object_id="#username_input")

    while True:
        # Sets the cursor refresh rate??
        ui_refresh_rate = clock.tick(60)/1000

        # ??
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#username_input":
                # Update the db
                config.capture_user(event.text)
                # Start the game!
                play_game()
            
            # Send the event to the gui manager??
            manager.process_events(event)
        
        #??
        manager.update(ui_refresh_rate)

        # Set the screen to black
        screen.fill((0, 0, 0))

        # ??
        manager.draw_ui(screen)

        # Load the content
        pygame.display.flip()

# Set up the game loop
# Game loop processes user input, updates state of game objs, updates display & audio output, maintains game speed
# User input results in an event being generated. Events are placed in the event queue which then can be accessed & manipulated
def play_game():
    pygame.display.set_caption("Jerry Dodger")

    # Variable to keep the main loop running
    running = True

    # Variable to track the score
    game_score = 0

    # Create a custom evens for adding a new enemy and adding to the score
    # Pygame defines events internally as integers, so you need to define a new event with a unique integer
    # The last event pygame reserves is 'USEREVENT', so adding the '+1' ensures that it's unique
    # .set_timer() creates a 'ADDENEMY' event at the specified interval
    ADDENEMY = pygame.USEREVENT + 0
    pygame.time.set_timer(ADDENEMY, 500)
    ADDSCORE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDSCORE, 1000)

    # Instantiate player sprite
    player = Player()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

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
            # Add to the game score every second
            elif event.type == ADDSCORE:
                game_score += 1

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

        # Draw score on the screen
        score_text = config.get_font(20).render(f"Score: {game_score}", True, "White")
        score_rect = score_text.get_rect(center=(100, 20))
        screen.blit(score_text, score_rect)

        # Draw the sprites on the screen with .blit()
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
            config.capture_score(game_score)
            running = False
            main_menu()

        # Update the display with .flip()
        # .flip() updates the screen with everything that's been drawn since the last .flip()
        pygame.display.flip()

# Show the Game Over screen
# def end_game():
#     pygame.display.set_caption("Game Over")

#     while True:
#         screen.fill((0,0,0))
#         # Draw text to the screen
#         user_score_text = config.get_font(90).render("JERRY DODGER", True, "#b68f40")
#         user_score_rect = menu_text.get_rect(center=(640, 100))



# Starts the game :)
main_menu()