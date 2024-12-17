from utils import *  # no need to import pygame because the import is in utils
from character import * # import player
from game import execute_game, game_loop
from utils import under_construction
from story import start_game_with_story
from Rules import show_rules
from options import show_options
from credits import credits_
from config import light_grey, grey


def interface(screen):
    """
    The main menu interface for the game. It initializes the game menu screen, handles user interactions,
    and redirects to other parts of the game based on user input (Play, Rules, Options, Credits, Quit).

    Parameters
    ----------
    screen : pygame.Surface
        The pygame display surface to draw the menu interface.
    """
    # initiating pygame
    pygame.init()
    pygame.mixer.music.load('Music/music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)

    # fonts
    corbel_font = pygame.font.SysFont("Corbel", 50)

    play_text = corbel_font.render("Play", True, white)
    rules_text = corbel_font.render("Rules", True, white)
    options_text = corbel_font.render("Options", True, white)
    credits_text = corbel_font.render("Credits", True, white)
    quit_text = corbel_font.render("Quit", True, white)

    # Load and scale the background image once
    image = pygame.image.load("backgrounds/main page.png")
    image_width, image_height = 1000, 600
    image = pygame.transform.scale(image, (image_width, image_height))

    # Placeholder images for Rules screen
    images = {
        "powerup1": pygame.image.load("Power-Up Images/invicibility.png"),
        "powerup2": pygame.image.load("Power-Up Images/Despawner.png"),
        "powerup3": pygame.image.load("Power-Up Images/deadly fire.png"),
        "powerup4": pygame.image.load("Power-Up Images/crazyfire.png"),
        "chest1": pygame.image.load("Chest Images/chest1.png"),
        "chest2": pygame.image.load("Chest Images/chest2.png"),
        "chest3": pygame.image.load("Chest Images/chest3.png"),
        "chest4": pygame.image.load("Chest Images/chest4.png"),
    }

    # Optionally resize the images
    for key in images.keys():
        images[key] = pygame.transform.scale(images[key], (80, 80))  # Resize to X x Y pixels

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # main game loop
    while True:
        # Get the mouse position
        mouse = pygame.mouse.get_pos()

        # event handling
        for ev in pygame.event.get():
            # quitting the game with the close button on the window (X)
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Detect clicks on buttons
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 200 <= mouse[0] <= 800 and 470 <= mouse[1] <= 550:  # Play button
                    start_game_with_story(screen)  # Start game with story
                elif 50 <= mouse[0] <= 150 and 60 <= mouse[1] <= 120:  # Rules button
                    show_rules(screen, corbel_font, {})
                elif 210 <= mouse[0] <= 390 and 60 <= mouse[1] <= 120:  # Options button
                    show_options(screen)  # Open options menu
                elif 610 <= mouse[0] <= 770 and 60 <= mouse[1] <= 120:  # Credits button
                    credits_(screen)  # Placeholder function for credits
                elif 850 <= mouse[0] <= 950 and 60 <= mouse[1] <= 120:  # Quit button
                    pygame.quit()
                    exit()

        # Draw the background image
        screen.blit(image, (0, 0))

        # Drawing the buttons with hover effect
        play_hover = 200 <= mouse[0] <= 800 and 470 <= mouse[1] <= 550
        rules_hover = 50 <= mouse[0] <= 160 and 60 <= mouse[1] <= 100
        options_hover = 210 <= mouse[0] <= 390 and 60 <= mouse[1] <= 100
        credits_hover = 610 <= mouse[0] <= 770 and 60 <= mouse[1] <= 100
        quit_hover = 850 <= mouse[0] <= 950 and 60 <= mouse[1] <= 100

        # Define Hover Colors
        hover_colors = light_grey
        default_color = grey
        hover_color_play = glowing_light_red

        # Draw buttons with hover effect
        pygame.draw.rect(screen, hover_color_play if play_hover else dark_red, pygame.Rect(200, 470, 600, 60), border_radius=10)
        pygame.draw.rect(screen, hover_colors if rules_hover else default_color, pygame.Rect(40, 60, 120, 60), border_radius=10)
        pygame.draw.rect(screen, hover_colors if options_hover else default_color, pygame.Rect(210, 60, 180, 60), border_radius=10)
        pygame.draw.rect(screen, hover_colors if credits_hover else default_color, pygame.Rect(610, 60, 160, 60), border_radius=10)
        pygame.draw.rect(screen, hover_colors if quit_hover else default_color, pygame.Rect(850, 60, 100, 60), border_radius=10)

        # Drawing the buttons

        # Play button-appearance
        tile_rect = play_text.get_rect(center=(500, 500))
        screen.blit(play_text, tile_rect)

        # get the mouse information
        #mouse = pygame.mouse.get_pos()  # locates where the mouse is


        # Draw the buttons
        wilderness_rect = play_text.get_rect(center=(500, 500))
        rules_rect = rules_text.get_rect(center=(100, 90))
        options_rect = options_text.get_rect(center=(300, 90))
        credits_rect = credits_text.get_rect(center=(690, 90))
        quit_rect = quit_text.get_rect(center=(900, 90))

        # Display the buttons
        screen.blit(play_text, wilderness_rect)
        screen.blit(rules_text, rules_rect)
        screen.blit(options_text, options_rect)
        screen.blit(credits_text, credits_rect)
        screen.blit(quit_text, quit_rect)

        # at the end
        pygame.display.update()

        # Limit the frame rate to 60 FPS
        clock.tick(60)

def rules_():
    """
    Displays the rules screen.
    Calls the `show_rules` function to render the rules.
    """
    show_rules()

def wilderness_explorer():
    """
    Starts the main game. This function executes the game and returns the user to the main interface once complete.
    """
    execute_game()
    interface()




