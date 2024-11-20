from config import *
import math
import pygame
from character import Character
from enemy import Enemy


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
    player = Character("character.png", 100, 100, width=120, height=120)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    #background image
    image = pygame.image.load("teste.jpg")
    image_width, image_height = 1000, 600
    image = pygame.transform.scale(image, (image_width, image_height))
    #music
    pygame.init()
    pygame.mixer.music.load('teste.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #Initialize the bullet group
    bullets = pygame.sprite.Group()

    #Initialize the enemy group
    enemies =pygame.sprite.Group()
    enemy_spawn_timer = 0

    running = True
    while running:
        # Control frame rate
        clock.tick(fps)

        # Fill the background
        screen.blit(image, (0, 0))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop
                pygame.quit()
        #Shooting
        player.shoot(bullets)

        #Spawning the enemies
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            enemy_spawn_timer = 2 * fps #Every two seconds

        #Check for collisions between enenies and bulltes
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.health -= 5 #Decrease health by 5
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill() # Destroy the enemy

        # Check for collisions between player and enemy


        #Update the enemy spawn timer
        enemy_spawn_timer -=1

        # Update positions
        player_group.update()
        bullets.update()
        enemies.update(player)

        # Drawing the objects
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.flip()
