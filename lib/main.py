# Import pygame and pygmame.locals for easier access to key coordinates
import pygame, sys, pygame_gui
from pygame.locals import (K_ESCAPE, K_SPACE, KEYDOWN, MOUSEBUTTONDOWN, QUIT)
# Import classes
from classes.player import Player
from classes.enemy import Enemy
from classes.button import Button
from classes.top_score import Top_Score
from classes.steeze import Steeze
# Import global vars and CRUD methods
import config
from score import get_top_scores, capture_score, get_last_score
from user import capture_user
from trick import capture_tricks

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
        play_button = Button(image=pygame.image.load("../assets/play-rect.png"), pos=(640, 360), text_input="PLAY",
                             font=config.get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        # Draw the menu text on the screen
        screen.blit(menu_text, menu_rect)

        # Draw the skier and jerry images on the screen
        skier_img = pygame.image.load("../assets/skier-mike-big.png")
        skier_rect = skier_img.get_rect(center=(200, 360))
        screen.blit(skier_img, skier_rect)

        jerry_img = pygame.image.load("../assets/jerry-big.png")
        jerry_rect = jerry_img.get_rect(center=(1080, 360))
        screen.blit(jerry_img, jerry_rect)


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
    # Create the clock to control the framerate
    clock = pygame.time.Clock()
    # Create the text input. Why not accessed??
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((405, 360), (460, 50)), 
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
                current_user = capture_user(event.text)
                # Start the game!
                play_game(current_user)
            
            # Send the event to the gui manager??
            manager.process_events(event)
        
        #??
        manager.update(ui_refresh_rate)

        # Set the screen to black
        screen.fill((0, 0, 0))

        # ??
        manager.draw_ui(screen)

        # Draw the username prompt
        user_text = config.get_font(30).render(f"Enter username:", True, "#b68f40")
        user_rect = user_text.get_rect(center=(640, 250))
        screen.blit(user_text, user_rect)

        # Load the content
        pygame.display.flip()

# Set up the game loop
# Game loop processes user input, updates state of game objs, updates display & audio output, maintains game speed
# User input results in an event being generated. Events are placed in the event queue which then can be accessed & manipulated
def play_game(user):
    pygame.display.set_caption("Jerry Dodger")
    clock = pygame.time.Clock()

    # Variable to keep the main loop running
    running = True

    # Variable to track the score
    game_score = 0

    # Variable to track the encountered steezes
    steeze_bag = []

    # Variable to track the steezes sent
    steezes_bagged = []

    # Create a custom events
    # Pygame defines events internally as integers, so you need to define a new event with a unique integer
    # The last event pygame reserves is 'USEREVENT', so adding the '+1' ensures that it's unique
    # .set_timer() creates the event at the specified interval
    # Spawn an enemy every two seconds
    ADDENEMY = pygame.USEREVENT + 0
    spawn_enemy_timer = 2000
    pygame.time.set_timer(ADDENEMY, spawn_enemy_timer)

    # Create an event to increase the enemy spawn rate every five seconds
    REDUCETIMER = pygame.USEREVENT + 1
    REDUCETIMERTIMER = 5000
    pygame.time.set_timer(REDUCETIMER, REDUCETIMERTIMER)

    # Increase the game score every second
    ADDSCORE = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDSCORE, 1000)

    # Spawn a trick every five seconds
    ADDSTEEZE = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDSTEEZE, 5000)

    # Instantiate player sprite
    player = Player()

    # Create groups to hold enemy sprites and friendly steezes
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    steezes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Main loop
    while running:
        # Look at every event in the queue
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    main_menu()
                elif event.key == K_SPACE:
                    if steeze_bag:
                        match steeze_bag[0]:
                            case '360':
                                game_score += 5
                                steezes_bagged.append('360')
                                steeze_bag.pop(0)
                            case '720':
                                game_score += 10
                                steeze_bag.pop(0)
                            case _:
                                pass
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Instantiate new enemies and add them to the enemy group
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            # Increase the enemy spawn rate
            elif event.type == REDUCETIMER:
                # Cancels out the previous enemy spawn event. Necessary??
                pygame.time.set_timer(ADDENEMY, 0)
                spawn_enemy_timer -= 200
                # Keeps rate above 200 milliseconds
                if spawn_enemy_timer <= 200:
                    spawn_enemy_timer = 200
                pygame.time.set_timer(ADDENEMY, spawn_enemy_timer)
            # Add to the game score every second
            elif event.type == ADDSCORE:
                game_score += 1
            # Create new steezes
            elif event.type == ADDSTEEZE:
                new_steeze = Steeze(steeze_input="360", font=config.get_font(20), color="#b68f40")
                steezes.add(new_steeze)
                all_sprites.add(new_steeze)

        # Get the set of keys pressed and check for user input
        # .get_pressed() returns a dict containing all the current keydown events in the queue
        pressed_keys = pygame.key.get_pressed()

        # Update sprite positions via their respective groups
        enemies.update()
        steezes.update()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        # Surface allows you to 'draw' to the screen
        # Fill the screen with black
        screen.fill((0,0,0))

        # Draw score on the screen
        score_text = config.get_font(20).render(f"Score: {game_score}", True, "White")
        score_rect = score_text.get_rect(center=(100, 20))
        screen.blit(score_text, score_rect)

        # Draw the steeze bag on the screen
        steeze_bag_text = config.get_font(20).render(f"Steeze Bag: {' '.join(steeze_bag)}", True, "White")
        steeze_bag_rect = steeze_bag_text.get_rect(center=(640, 700))
        screen.blit(steeze_bag_text, steeze_bag_rect)

        # Draw the sprites on the screen with .blit()
        # .blit() stands for 'block transfer'. You can use to to copy the surface onto another one (e.g. the original screen)
        # .blit() takes two args: 1. the surface to draw 2. the location at which to draw on the source surface
        # Draw all sprites: any sprite in the group will be 'drawn' with every frame
        for sprite in all_sprites:
            screen.blit(sprite.surf, sprite.rect)

        # .spritecollideany() method accepts a sprite and group as parameters
        # looks at every object in the group to see if its '.rect' intersects with the '.rect' of the sprite. If so, returns TRUE
        # Takes a callback function that determines the ratio of overlap that would determine a collision
        # might want to use pygame.sprite.collide_mask
        if pygame.sprite.spritecollideany(player, enemies, pygame.sprite.collide_rect_ratio(0.9)):
            # If collision occurs, remove the player sprite and exit the loop
            player.kill()
            capture_score(game_score, user)
            # possibly insert 'await' here
            capture_tricks(steezes_bagged, user, get_last_score())
            running = False
            end_game(user, game_score)
        elif pygame.sprite.spritecollideany(player, steezes):
            if len(steeze_bag) < 3:
                for steeze in pygame.sprite.spritecollide(player, steezes, False):                
                    steeze_bag.append(steeze.steeze_input)
                    steeze.kill()

        # Update the display with .flip()
        # .flip() updates the screen with everything that's been drawn since the last .flip()
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        clock.tick(30)

# Show the Game Over screen
def end_game(user, game_score):
    pygame.display.set_caption("Game Over")

    while True:
        screen.fill((0,0,0))

        # Create game over text
        game_over_text = config.get_font(90).render("GAME OVER", True, "#b68f40")
        game_over_rect = game_over_text.get_rect(center=(640, 100))

        # Draw the game over text on the screen
        screen.blit(game_over_text, game_over_rect)

        your_score_text = config.get_font(40).render(f"YOUR SCORE: {game_score}", True, "#b68f40")
        your_score_rect = your_score_text.get_rect(center=(640, 230))
        screen.blit(your_score_text, your_score_rect)

        # Draw the top 5 scores
        scores = get_top_scores(user.id)
        pos_x = 640
        pos_y = 370

        top_scores_text = config.get_font(20).render(f"Top scores for {user.username}:", True, "White")
        top_scores_rect = top_scores_text.get_rect(center=(640, 330))
        screen.blit(top_scores_text, top_scores_rect)

        for score in scores:
            new_score = Top_Score(pos=(pos_x, pos_y), score_input=score.score,
                                  font=config.get_font(20), color="White")
            new_score.update(screen)
            pos_y += 30

        # Capture the mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw the play again button
        play_again_button = Button(image=pygame.image.load("../assets/play-rect.png"), pos=(1050, 620), text_input="PLAY AGAIN",
                                   font=config.get_font(30), base_color="#d7fcd4", hovering_color="White")
        play_again_button.change_color(mouse_pos)
        play_again_button.update(screen)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if play_again_button.check_for_input(mouse_pos):
                    play_game(user)
        
        pygame.display.flip()


# Starts the game :)
main_menu()