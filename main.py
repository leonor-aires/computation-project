import pygame
from interface import interface

def main():
    pygame.init()  # Initialize Pygame systems
    print("[DEBUG] Pygame initialized.")
    try:
        interface()  # Start the game interface
    finally:
        pygame.quit()  # Ensure Pygame quits when the program ends

if __name__ == "__main__":
    main()