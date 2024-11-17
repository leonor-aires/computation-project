from config import *
import math
import pygame
from player import Player

def execute_game():
    """
     Main function to execute the game loop
    """
    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Player setup
    player = Player()
    # creating an empty group for the player
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)
    # creating an empty bullet group that will be given as input to the player.shoot() method
    bullets = pygame.sprite.Group()


    running = True
    while running:
        # Control frame rate
        clock.tick(fps)
        # Fill the background
        screen.fill(green)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # automatically shoot bullets from the player:
        player.shoot(bullets)

        # Update positions and visuals
        # calling the .update() method of all the instances in the player group
        player_group.update()

        # updating the bullets group
        bullets.update()

        # Drawing the objects
        player_group.draw(screen)

        # drawing the bullet sprites:
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.flip()
