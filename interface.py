from utils import *  # no need to import pygame because the import is in utils
from character import * # import player
from game import execute_game, game_loop
from utils import under_construction
from story import start_game_with_story
from Rules import show_rules
from options import show_options
from credits import credits_


def interface(screen):
    # initiating pygame
    pygame.init()
    pygame.mixer.music.load('Music/music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)

    # fonts
    corbel_font = pygame.font.SysFont("Corbel", 50)
    comicsans_font = pygame.font.SysFont("Comic Sans MS", 50)
    font = pygame.font.Font(None, 36)

    wilderness_text = corbel_font.render("Play", True, white)
    rules_text = corbel_font.render("Rules", True, white)
    options_text = corbel_font.render("Options", True, white)
    credits_text = corbel_font.render("Credits", True, white)
    quit_text = corbel_font.render("Quit", True, white)
    title_text = comicsans_font.render("Wilderness Explorer", True, glowing_light_red)

    # Load and scale the background image once
    image = pygame.image.load("backstory images/jump_scare.jpg")
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
    running = True
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
                if 200 <= mouse[0] <= 800 and 150 <= mouse[1] <= 210:  # Play button
                    start_game_with_story(screen)  # Start game with story
                elif 100 <= mouse[0] <= 240 and 380 <= mouse[1] <= 440:  # Rules button
                    show_rules(screen, corbel_font, {})
                elif 100 <= mouse[0] <= 240 and 500 <= mouse[1] <= 560:  # Options button
                    show_options(screen)  # Open options menu
                elif 750 <= mouse[0] <= 890 and 380 <= mouse[1] <= 440:  # Credits button
                    credits_(screen)  # Placeholder function for credits
                elif 750 <= mouse[0] <= 890 and 500 <= mouse[1] <= 560:  # Quit button
                    pygame.quit()
                    exit()

        # Draw the background image
        screen.blit(image, (0, 0))

        # Drawing the buttons

        # Play button - apperance
        tile_rect = wilderness_text.get_rect(center=(200 + 600 // 2, 150 + 60 // 2))
        screen.blit(wilderness_text, tile_rect)
        # get the mouse infomration
        mouse = pygame.mouse.get_pos()  # locates where the mouse is

        # Draw the buttons
        wilderness_rect = wilderness_text.get_rect(center=(200 + 600 // 2, 150 + 60 // 2))
        rules_rect = rules_text.get_rect(center=(100 + 140 // 2, 380 + 60 // 2))
        options_rect = options_text.get_rect(center=(100 + 140 // 2, 500 + 60 // 2))
        credits_rect = credits_text.get_rect(center=(750 + 140 // 2, 380 + 60 // 2))
        quit_rect = quit_text.get_rect(center=(750 + 140 // 2, 500 + 60 // 2))

        # Display the buttons
        screen.blit(wilderness_text, wilderness_rect)
        screen.blit(rules_text, rules_rect)
        screen.blit(options_text, options_rect)
        screen.blit(credits_text, credits_rect)
        screen.blit(quit_text, quit_rect)

        # Title
        screen.blit(title_text, (250, 20))

        # at the end
        pygame.display.update()

        # Limit the frame rate to 60 FPS
        clock.tick(60)

def rules_():
    show_rules()

def wilderness_explorer():
    execute_game()
    interface()




