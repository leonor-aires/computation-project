from character import * # import player
from game import execute_game, game_loop
from Rules import show_rules
from options import show_options
from credits import credits_
from config import light_grey, grey, dark_red
from story import start_game_with_story

def interface(screen):
    """
    The main menu interface for the game. It initializes the game menu screen, handles user interactions,
    and redirects to other parts of the game based on user input (Play, Rules, Options, Credits, Quit).

    Parameters
    ----------
    screen : pygame.Surface
        The pygame display surface to draw the menu interface.
    """
    save_file = "save_file.json"
    character = Character(image="characters images/Tomátio.png", x=10, y=height - 50)  # Start at bottom-left corner
    try:
        with open(save_file, 'r'):
            character.load_player_data(save_file)
    except FileNotFoundError:
        character.save_player_data(save_file)

    # initiating pygame
    pygame.init()
    pygame.mixer.music.load('Music/game-music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)

    # fonts
    corbel_font = pygame.font.SysFont("Corbel", 50)

    # Load and scale the background image once
    image = pygame.image.load("backstory images/main page.png")
    image_width, image_height = 1000, 600
    image = pygame.transform.scale(image, (image_width, image_height))

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Button definitions and text rendering
    buttons = {
        "play": {"rect": pygame.Rect(200, 470, 600, 60), "text": corbel_font.render("Play", True, white)},
        "rules": {"rect": pygame.Rect(10, 60, 180, 60), "text": corbel_font.render("Rules", True, white)},
        "options": {"rect": pygame.Rect(205, 60, 180, 60), "text": corbel_font.render("Options", True, white)},
        "story": {"rect": pygame.Rect(400, 60, 180, 60), "text": corbel_font.render("Story", True, white)},
        "credits": {"rect": pygame.Rect(605, 60, 180, 60), "text": corbel_font.render("Credits", True, white)},
        "quit": {"rect": pygame.Rect(805, 60, 180, 60), "text": corbel_font.render("Quit", True, white)},
    }

    # main game loop
    while True:
        # Get the mouse position
        mouse = pygame.mouse.get_pos()

        # Event handling
        for ev in pygame.event.get():
            # quitting the game with the close button on the window (X)
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Mouse click events
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if buttons["play"]["rect"].collidepoint(mouse):
                    pygame.mixer.music.stop()
                    character.load_player_data(save_file)
                    execute_game(screen, character)
                elif buttons["story"]["rect"].collidepoint(mouse):
                    start_game_with_story(screen, interface)
                elif buttons["rules"]["rect"].collidepoint(mouse):
                    show_rules(screen, corbel_font, {})
                elif buttons["options"]["rect"].collidepoint(mouse):
                    show_options(screen)
                elif buttons["credits"]["rect"].collidepoint(mouse):
                    credits_(screen)
                elif buttons["quit"]["rect"].collidepoint(mouse):
                    character.save_player_data("save_file.json")
                    pygame.quit()
                    exit()

        # Draw the background image
        screen.blit(image, (0, 0))

        # Define hover colors
        hover_colors = light_grey
        default_color = grey
        default_color_play = dark_red
        hover_color_play = glowing_light_red

        # Draw buttons with hover effect and text
        for button_key, button in buttons.items():
            is_hover = button["rect"].collidepoint(mouse)

            # Determine the color based on hover state
            if button_key == "play":
                color = hover_color_play if is_hover else default_color_play  # Red for default Play button
            else:
                color = hover_colors if is_hover else default_color  # Other buttons

            pygame.draw.rect(screen, color, button["rect"], border_radius=10)

            # Draw the button text centered
            text_rect = button["text"].get_rect(center=button["rect"].center)
            screen.blit(button["text"], text_rect)

        # Update the display
        pygame.display.update()
        clock.tick(60)  # Limit the frame rate to 60 FPS

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
