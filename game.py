from config import *
from character import Character
from enemy import Enemy
import pygame
from shed import shed
import random
from powerups import *


# Function to create platforms that change position in each level
def create_platforms(level):
    platforms = []
    if level == 1:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),  # Ground platform (esquerda)
            pygame.Rect(300, height - 200, 200, 10),  # Plataforma média (centro-esquerda)
            pygame.Rect(600, height - 100, 200, 10),
            pygame.Rect(600, height - 400, 200, 10),
            pygame.Rect(width - 150, 100, 150, 10),  # Plataforma no canto superior direito
        ]
    elif level == 2:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),  # Ground platform (esquerda)
            pygame.Rect(400, height - 200, 200, 10),  # Plataforma baixa (centro)
            pygame.Rect(700, height - 300, 200, 10),  # Plataforma média (direita)
            pygame.Rect(300, height - 350, 200, 10),  # Plataforma alta (esquerda)
            pygame.Rect(width - 150, 100, 150, 10),  # Plataforma no canto superior direito
        ]
    elif level == 3:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),  # Ground platform (esquerda)
            pygame.Rect(300, height - 200, 200, 10),  # Plataforma média (centro-esquerda)
            pygame.Rect(600, height - 100, 200, 10),
            pygame.Rect(600, height - 400, 200, 10),
            pygame.Rect(width - 150, 100, 150, 10),  # Plataforma no canto superior direito
        ]
    return platforms


def game_loop(screen, character=None):
    if character is None:
        character = Character(image="characters images/Tomátio.png", x=150, y=150)

    current_level = 1
    current_state = "main"

    while True:
        if current_state == "main":
            platforms = create_platforms(current_level)
            result = play_level(screen, character, current_level, platforms)
            if result == "next_level":
                current_level += 1
                character.health = character.max_health
            elif result == "retry":
                character.health = character.max_health
            elif result == "shed":
                current_state = "shed"
            elif result == "break":
                break
            elif result == "main_menu":
                return
        elif current_state == "shed":
            current_state = shed(screen, character)


def execute_game(screen, character=None):
    game_loop(screen, character)


def play_level(screen, character, level, platforms):
    clock = pygame.time.Clock()
    background_image = pygame.image.load("Battlefields/battlefield.webp")
    background_image = pygame.transform.scale(background_image, resolution)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    spawn_enemies(enemies, platforms)  # Pass platforms to spawn enemies
    powerups = pygame.sprite.Group()

    # Spawn one power-up on a random platform
    platform = random.choice(platforms)
    powerup = InvincibilityPowerUp(platform.centerx, platform.top - 15)  # Position above the platform
    powerups.add(powerup)

    running = True
    level_complete = False
    while running:
        screen.blit(background_image, (0, 0))
        clock.tick(fps)

        # Check if the character collided with any platform
        on_platform = False
        for platform in platforms:
            if character.rect.colliderect(platform):
                if character.y_velocity >= 0:
                    character.rect.bottom = platform.top
                    on_platform = True
                    character.is_jumping = False
                    character.y_velocity = 0

        # Se não estiver em nenhuma plataforma e não estiver no chão, aplica gravidade
        if not on_platform and character.rect.bottom < height:
            character.rect.y += character.y_velocity
            character.y_velocity += character.gravity

        # Check if the character hit the top-right platform and killed all enemies
        if (character.rect.right >= platforms[-1].right and
                character.rect.bottom == platforms[-1].top and
                len(enemies) == 0):
            level_complete = True

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    character.shoot(bullets)
                    # Detect click on the "Back" button
                    if 430 <= mouse[0] <= 570 and 540 <= mouse[1] <= 600:
                        return "break"

        # Update game objects
        character.update()
        bullets.update()
        enemies.update(character)
        powerups.update()
        enemies.update()

        # Handle power-up collection
        collected_powerups = pygame.sprite.spritecollide(character, powerups, True)
        for powerup in collected_powerups:
            powerup.affect_player(character)

        # Handle collisions
        handle_collisions(character, bullets, enemies)

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, deep_black, platform)

        # Check if character moves to the shed
        if character.rect.right >= width and character.rect.bottom >= height - 50:
            return "shed"

        # Draw all game objects
        bullets.draw(screen)
        powerups.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)  # Use the enemy's draw method
        character.draw(screen)


        # Draw the UI (for example, health)
        draw_ui(screen, character)

        # Check if the level is completed
        if level_complete:
            return level_end_screen(screen, level)

        # Check if the character died
        if character.health <= 0:
            return game_over_screen(screen)

        corbel_font = pygame.font.SysFont("Corbel", 50)
        mouse = pygame.mouse.get_pos()
        pygame.draw.rect(screen, dark_red, [430, 540, 140, 60])
        back_text = corbel_font.render("Back", True, white)
        back_rect = back_text.get_rect(center=(430 + 140 // 2, 540 + 60 // 2))
        screen.blit(back_text, back_rect)
        pygame.display.flip()


def spawn_enemies(group, platforms):
    """
    Spawns one enemy per platform.

    Args:
        group (pygame.sprite.Group): Group to which the enemies are added.
        platforms (list): List of platforms (pygame.Rect).
    """
    for platform in platforms:
        enemy = Enemy(platform)  # Create an enemy restricted to the platform
        group.add(enemy)


def handle_collisions(character, bullets, enemies):
    """
    Handle collisions between bullets and enemies, and between enemies and the player.
    """
    # Check for bullet collisions with enemies
    for bullet in bullets:
        collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in collided_enemies:
            enemy.health -= 5
            bullet.kill()
            if enemy.health <= 0:
                enemy.kill()

    for enemy in enemies:
        if pygame.sprite.collide_rect(character, enemy):
            if not character.invincible:  # Prevent damage if the player is invincible
                character.take_damage(10)  # Adjust damage amount as needed


def draw_ui(screen, character):
    font = pygame.font.SysFont("Corbel", 30)
    health_text = font.render(f"Health: {character.health}/{character.max_health}", True, green)
    screen.blit(health_text, (10, 10))


def level_end_screen(screen, level):
    """
    Displays the end of level screen with options for the player.
    """
    font = pygame.font.SysFont("Corbel", 50)
    screen.fill((0, 0, 0))

    level_end_text = font.render(f"End of Level {level}", True, white)
    level_end_rect = level_end_text.get_rect(center=(width // 2, height // 3))
    screen.blit(level_end_text, level_end_rect)

    next_level_button = pygame.Rect(250, 400, 260, 60)
    menu_button = pygame.Rect(600, 400, 260, 60)
    pygame.draw.rect(screen, green, next_level_button)
    pygame.draw.rect(screen, dark_red, menu_button)

    next_level_text = font.render("Next Level", True, white)
    menu_text = font.render("Main Menu", True, white)
    screen.blit(next_level_text, next_level_button.move(40, 10).topleft)
    screen.blit(menu_text, menu_button.move(20, 10).topleft)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if next_level_button.collidepoint(mouse):
                    return "next_level"
                elif menu_button.collidepoint(mouse):
                    return "main_menu"


def game_over_screen(screen):
    """
    Displays the Game Over screen with options to retry or go back to the menu.
    """
    font = pygame.font.SysFont("Corbel", 50)
    screen.fill((0, 0, 0))

    game_over_text = font.render("Game Over", True, white)
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 3))
    screen.blit(game_over_text, game_over_rect)

    retry_button = pygame.Rect(200, 400, 200, 60)
    menu_button = pygame.Rect(600, 400, 260, 60)
    pygame.draw.rect(screen, green, retry_button)
    pygame.draw.rect(screen, dark_red, menu_button)

    retry_text = font.render("Retry", True, white)
    menu_text = font.render("Main Menu", True, white)
    screen.blit(retry_text, retry_button.move(50, 10).topleft)
    screen.blit(menu_text, menu_button.move(20, 10).topleft)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if retry_button.collidepoint(mouse):
                    return "retry"
                elif menu_button.collidepoint(mouse):
                    return "main_menu"
