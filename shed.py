import pygame
from config import *
from shop import shop


def shed(screen, player):
    """
    Set up and manage the player interaction with the shed background.

    Parameters
    ----------
    screen : pygame.Surface
        The pygame display surface where the shed interface will be drawn.
    player : Character
        The  player interacting with the shed.

    Returns
    -------
    "main" if the player exits the shed, otherwise it continues in shed.
    """
    # Load and scale the background
    background = pygame.image.load("backgrounds/cave.webp")
    background = pygame.transform.scale(background, resolution)
    clock = pygame.time.Clock()

    # Set player's initial position in the shed
    player.rect.left = 30

    # Define the shop interaction area
    shop_area = pygame.Rect(300, height - 100, 100, 100)

    running = True
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Update player movement and position
        player.update()

        # Check if the player enters the shop area
        if shop_area.colliderect(player.rect):
            shop(screen, player)
            player.rect.left = 50  # Reset player's position after shopping
            player.rect.top = height - 150  # Adjust as needed for aesthetics

        # Check if the player exits the shed
        if player.rect.left <= 0:
            return "main"  # Return to the main game state

        # Draw player and shop area
        player_group = pygame.sprite.Group(player)
        player_group.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), shop_area, 2)  # Optional: Visualize shop area

        pygame.display.flip()
