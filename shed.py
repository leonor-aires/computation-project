import pygame
from config import*
from utils import*
from utils import under_construction


def shed(screen, player):
    background = pygame.image.load("Battlefields/cave.webp")
    background = pygame.transform.scale(background, resolution)
    clock = pygame.time.Clock()

    # Set player's position to the left of the screen
    player.rect.left = 30
    player_group = pygame.sprite.Group()
    player_group.add(player)

    special_area = pygame.Rect(530, 30, 140, 140)

    running = True
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Update player position
        player.update()

        # Detect if the user walks in the special area (e.g., interacts with it)
        if special_area.colliderect(player.rect):
            under_construction()
            player.rect.top = 200
            player.rect.left = 560

        # Allow the player to return to the main game
        if player.rect.left <= 0:
            return "main"  # Return to the main game

        # Draw player
        player_group.draw(screen)

        pygame.display.flip()
