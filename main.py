import pygame
from interface import interface
from config import resolution


def main():
    """
    Main entry point for Tomatio's Escape.
    Handles main menu interaction.
    """

    # Create the screen
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Tomatio's Escape")

    # Run the interface (main menu)
    interface(screen)

if __name__ == "__main__":
    main()
