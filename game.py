from config import *
import math
import pygame
from character import Character
from enemy import Enemy
from shed import shed
from player import Player

def game_loop():
    character = Character(image="dragon.png", x=150, y=150)  # Provide valid arguments
    current_state = "main"

    while True:
        if current_state == "main":
            current_state = execute_game(character)
        elif current_state == "shed":
            current_state = shed(character)

def execute_game(character = None ):
    """
    Main function to execute the game loop
    """
    if character is None:
        character = Character(image="dragon.png", x=150, y=150)  # Provide valid arguments

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Player setup
    player_group = pygame.sprite.Group()
    player_group.add(character)

    #background image
    image = pygame.image.load("battlefield.webp")
    image = pygame.transform.scale(image, (1000, 600))
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

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    character.shoot(bullets)
                    # Detectar clique no botão "Back"
                if 430 <= mouse[0] <= 570 and 540 <= mouse[1] <= 600:
                    running = False  # Sai do loop do jogo e volta à interface principal

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
        for enemy in enemies:
            if pygame.sprite.collide_rect(character, enemy):
                character.take_damage(5)  # Dano de 5 por colisão
                if character.health <= 0:
                    print("Game Over!")
                    running = False

        #Update the enemy spawn timer
        enemy_spawn_timer -= 1

        # Update positions
        player_group.update()
        bullets.update()
        enemies.update(character)

        # chackning if tghe user goes into the shed area
        if character.rect.right >= width:
            # change the game to state to shed
            return "shed"

        # Drawing the objects
        player_group.draw(screen)
        enemies.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)  # Inclui barra de vida
        for bullet in bullets:
            bullet.draw(screen)
        for player in player_group:
            player.draw(screen)

        mouse = pygame.mouse.get_pos()  # Obter posição do mouse
        pygame.draw.rect(screen, dark_red, [430, 540, 140, 60])
        back_text = corbel_font.render("Back", True, white)
        back_rect = back_text.get_rect(center=(430 + 140 // 2, 540 + 60 // 2))
        screen.blit(back_text, back_rect)

        pygame.display.flip()

