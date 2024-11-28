import pygame
from interface import interface

def main():
    pygame.init()  # Initialize Pygame systems
    print("[DEBUG] Pygame initialized.")
    try:
        screen = pygame.display.set_mode((1000, 600))  # Set up the display once
        print("[DEBUG] Display initialized.")
        pygame.display.set_caption("Wilderness Explorer")
        interface(screen)  # Pass the screen to avoid redundant reinitializations
    finally:
        pygame.quit()  # Ensure Pygame quits cleanly

if __name__ == "__main__":
    main()