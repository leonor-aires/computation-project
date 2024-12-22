import pygame
from interface import interface
import options
from config import resolution
#ffrom music import play_game_music
def main():
    """
    Main entry point for the Tomatio's escape game.
    The game runs in a loop until the user closes the application.

    Note:
    This function initializes the Pygame system, sets up the game window, and handles the main event loop.
    It uses the interface function to render the main menu and manages transitions to other parts of the game,
    such as the Options menu.

    """
   # pygame.init()  # Initialize Pygame systems
    screen = pygame.display.set_mode(resolution)
   # pygame.display.set_caption("Platformer Game")
   # play_game_music("Music/game-music.mp3")
   # game_loop(screen)
    try:
        screen = pygame.display.set_mode((1000, 600))  # Set up the display once
        pygame.display.set_caption("Tomatio's Escape")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Pass a signal to check for an "Options" click
                user_action = interface(screen)  # Asddddddddddasume 'interface' returns actions, e.g., "OPTIONS"
                if user_action == "OPTIONS":
                    options.show_options(screen)  # Show the Options menu

                interface(screen)  # Pass the screen to avoid redundant reboots
    finally:
        pygame.quit()  # Ensure Pygame quits cleanly


if __name__ == "__main__":
    main()

