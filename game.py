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

        corbel_font = pygame.font.SysFont("Corbel", 50)
        quit_text = corbel_font.render("Quit", True, white)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    player.shoot(bullets)
            # detecting if the user clicked on the quit button (750, 500 para 890, 560)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 750 <= mouse[0] <= 890 and 500 <= mouse[1] <= 560:
                    pygame.quit()



        # Update e Draw
        player_group.update()
        bullets.update()
        enemies.update(player)

        # Spawning the enemies
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            enemy_spawn_timer = 10 * fps  # Spawn a cada dois segundos

        # Verificar colisões entre balas e inimigos
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                bullet_damage = 3  # Dano causado pela bala
                enemy.health -= bullet_damage
                bullet.kill()  # Remover a bala após o impacto
                if enemy.health <= 0:
                    enemy.kill()  # Remover o inimigo se a saúde chegar a 0

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

        for enemy in enemies:
            enemy.draw(screen)  # Inclui barra de vida
        for bullet in bullets:
            bullet.draw(screen)

        # get the mouse information
        mouse = pygame.mouse.get_pos()
        # Quit button
        pygame.draw.rect(screen, grey, [750, 500, 140, 60])
        quit_rect = quit_text.get_rect(center=(750 + 140 // 2, 500 + 60 // 2))
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

