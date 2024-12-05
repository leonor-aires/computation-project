from config import *
from character import Character
from enemy import Enemy
import pygame

# Function to create platforms that change position in each level
def create_platforms(level):
    platforms = []
    if level == 1:
        # Level 1: Introdução, plataformas acessíveis e uma no canto superior direito
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),  # Ground platform (esquerda)
            pygame.Rect(300, height - 150, 250, 10),  # Plataforma média (centro-esquerda)
            pygame.Rect(600, height - 250, 200, 10),  # Plataforma alta (centro-direita)
            pygame.Rect(width - 250, height - 350, 150, 10),  # Plataforma no canto superior direito
        ]
    elif level == 2:
        # Level 2: Plataformas mais espaçadas, desafio aumentado
        platforms = [
            pygame.Rect(100, height - 50, 200, 10),  # Ground platform (esquerda)
            pygame.Rect(400, height - 150, 200, 10),  # Plataforma baixa (centro)
            pygame.Rect(700, height - 250, 200, 10),  # Plataforma média (direita)
            pygame.Rect(400, height - 350, 200, 10),  # Plataforma alta (centro-direita)
            pygame.Rect(width - 200, height - 450, 150, 10),  # Plataforma no canto superior direito
        ]
    elif level == 3:
        # Level 3: Layout mais desafiador, plataformas menores e mais distantes
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),  # Ground platform (esquerda)
            pygame.Rect(300, height - 200, 200, 10),  # Plataforma baixa (centro-esquerda)
            pygame.Rect(600, height - 300, 200, 10),  # Plataforma média (centro-direita)
            pygame.Rect(300, height - 400, 200, 10),  # Plataforma alta (esquerda)
            pygame.Rect(width - 200, height - 500, 150, 10),  # Plataforma no canto superior direito
        ]
    return platforms




def game_loop(screen, character=None):
    """
    Main loop that transitions between levels or other game states.
    """
    if character is None:
        character = Character(image="characters images/Tomátio.png", x=150, y=150)
        current_state = "main"
        character = Character(image="character images/dragon.png", x=150, y=150)
    current_level = 1  # Start at level 1

    while True:
        # Create dynamic platforms for each level
        platforms = create_platforms(current_level)

        result = play_level(screen, character, current_level, platforms)
        if result == "next_level":
            current_level += 1
            character.health = character.max_health  # Reset health when changing level
        elif result == "main_menu":
            return  # Exit to the main menu


def execute_game(screen, character=None):
    """
    Entry point for executing the game.
    """
    game_loop(screen, character)

    if character is None:
        character = Character(image="characters images/Tomátio.png", x=150, y=150)

def play_level(screen, character, level, platforms):
    """
    Core function to play a level with customizable parameters, including platforms.
    """
    clock = pygame.time.Clock()
    background_image = pygame.image.load("Battlefields/battlefield.webp.jpg")
    background_image = pygame.transform.scale(background_image, resolution)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    spawn_enemies(enemies, count=5 * level, health=10 * level)  # Increase the number of enemies according to the level

    running = True
    level_complete = False  # Flag to check when the level is complete
    while running:
        screen.blit(background_image, (0, 0))
        clock.tick(fps)

        # Check if the character collided with any platform
        on_platform = False
        for platform in platforms:
            if character.rect.colliderect(platform):
                # Certifica-se de que o personagem está caindo antes de ajustar a posição
                if character.y_velocity >= 0:
                    character.rect.bottom = platform.top  # Mantém o personagem no topo da plataforma
                    on_platform = True
                    character.is_jumping = False  # Cancela o estado de salto
                    character.y_velocity = 0  # Reseta a velocidade vertical

        # Se não estiver em nenhuma plataforma e não estiver no chão, aplica gravidade
        if not on_platform and character.rect.bottom < height:
            character.rect.y += character.y_velocity
            character.y_velocity += character.gravity

        # Check if the character hit the top-right platform and killed all enemies
        if character.rect.colliderect(platforms[-1]) and len(enemies) == 0:
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

        # Update game objects
        character.update()
        bullets.update()
        enemies.update(character)

        # Handle collisions
        handle_collisions(character, bullets, enemies)

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, deep_black, platform)

        # Draw objects (character, enemies, etc.)
        bullets.draw(screen)
        enemies.draw(screen)
        character.draw(screen)

        # Draw the UI (for example, health)
        draw_ui(screen, character)

        # Check if the level is completed
        if level_complete:
            return level_end_screen(screen, level)

        # Check if the character died
        if character.health <= 0:
            return game_over_screen(screen)

        pygame.display.flip()


def level_end_screen(screen, level):
    """
    Displays the end of level screen with options for the player.
    """
    font = pygame.font.SysFont("Corbel", 50)
    screen.fill((0, 0, 0))

    level_end_text = font.render(f"End of Level {level}", True, white)
    level_end_rect = level_end_text.get_rect(center=(width // 2, height // 3))
    screen.blit(level_end_text, level_end_rect)

    next_level_button = pygame.Rect(200, 400, 200, 60)
    menu_button = pygame.Rect(600, 400, 200, 60)
    pygame.draw.rect(screen, green, next_level_button)
    pygame.draw.rect(screen, dark_red, menu_button)

    next_level_text = font.render("Next Level", True, white)
    menu_text = font.render("Main Menu", True, white)
    screen.blit(next_level_text, next_level_button.move(50, 10).topleft)
    screen.blit(menu_text, menu_button.move(20, 10).topleft)

    pygame.display.flip()

    running = True
    while running:
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
    menu_button = pygame.Rect(600, 400, 200, 60)
    pygame.draw.rect(screen, green, retry_button)
    pygame.draw.rect(screen, dark_red, menu_button)

    retry_text = font.render("Retry", True, white)
    menu_text = font.render("Main Menu", True, white)
    screen.blit(retry_text, retry_button.move(50, 10).topleft)
    screen.blit(menu_text, menu_button.move(20, 10).topleft)

    pygame.display.flip()

    running = True
    while running:
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


def spawn_enemies(group, count, health):
    """
    Generates a number of enemies with the specified health.
    """
    for _ in range(count):
        enemy = Enemy()
        enemy.health = health
        enemy.max_health = health
        group.add(enemy)


def handle_collisions(character, bullets, enemies):
    """
    Handles collisions between bullets and enemies, and between the character and enemies.
    """
    for bullet in bullets:
        collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in collided_enemies:
            enemy.health -= 5  # Damage caused by the bullet
            bullet.kill()
            if enemy.health <= 0:
                enemy.kill()

    for enemy in enemies:
        if pygame.sprite.collide_rect(character, enemy):
            character.take_damage(10)  # Damage taken by the character


def draw_ui(screen, character):
    """
    Draws the UI elements such as health and level.
    """
    font = pygame.font.SysFont("Corbel", 30)
    health_text = font.render(f"Health: {character.health}/{character.max_health}", True, green)
    screen.blit(health_text, (10, 10))





