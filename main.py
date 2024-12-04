import pygame
from interface import interface
from config import resolution
import options
def main():
    pygame.init()  # Initialize Pygame systems
    print("[DEBUG] Pygame initialized.")
    try:
        screen = pygame.display.set_mode((1000, 600))  # Set up the display once
        print("[DEBUG] Display initialized.")
        pygame.display.set_caption("Wilderness Explorer")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Pass a signal to check for an "Options" click
            user_action = interface(screen)  # Assume 'interface' returns actions, e.g., "OPTIONS"
            if user_action == "OPTIONS":
                options.show_options(screen)  # Show the Options menu

            interface(screen)  # Pass the screen to avoid redundant reinitializations
        print("[DEBUG] Game exited cleanly.")
    finally:
        pygame.quit()  # Ensure Pygame quits cleanly


if __name__ == "__main__":
    main()
