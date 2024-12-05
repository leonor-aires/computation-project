from config import *
from character import Character
from enemy import Enemy
import pygame
from shed import shed


# Function to create platforms that change position in each level
def create_platforms(level):
    platforms = []
    if level == 1:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),  # Ground platform (esquerda)
            pygame.Rect(300, height - 150, 250, 10),  # Plataforma média (centro-esquerda)
            pygame.Rect(600, height - 250, 200, 10),  # Plataforma alta (centro-direita)
            pygame.Rect(width - 250, height - 350, 150, 10),  # Plataforma no canto superior direito
        ]
    elif level == 2:
        platforms = [
            pygame.Rect(100, height - 50, 200, 10),  # Ground platform (esquerda)
            pygame.Rect(400, height - 150, 200, 10),  # Plataforma baixa (centro)
            pygame.Rect(700, height - 250, 200, 10),  # Plataforma média (direita)
            pygame.Rect(400, height - 350, 200, 10),  # Plataforma alta (centro-direita)
            pygame.Rect(width - 200, height - 450, 150, 10),  # Plataforma no canto superior direito
        ]
    elif level == 3:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),  # Ground platform (esquerda)
            pygame.Rect(300, height - 200, 200, 10),  # Plataforma baixa (centro-esquerda)
            pygame.Rect(600, height - 300, 200, 10),  # Plataforma média (centro-direita)
            pygame.Rect(300, height - 400, 200, 10),  # Plataforma alta (esquerda)
            pygame.Rect(width - 200, height - 500, 150, 10),  # Plataforma no canto superior direito
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
            elif result == "main_menu":
                return
        elif current_state == "shed":
            current_state = shed(screen, character)


def execute_game(screen, character=None):
    game_loop(screen, character)


def play_level(screen, character, level, platforms):
    clock = pygame.time.Clock()
    background_image = pygame.image.load("Battlefields/battlefield.webp.jpg")
    background_image = pygame.transform.scale(background_image, resolution)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    spawn_enemies(enemies, count=5 * level, health=10 * level)

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

        if not on_platform and character.rect.bottom < height:
            character.rect.y += character.y_velocity
            character.y_velocity += character.gravity

        if character.rect.colliderect(platforms[-1]) and len(enemies) == 0:
            level_complete = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    character.shoot(bullets)

        character.update()
        bullets.update()
        enemies.update(character)

        handle_collisions(character, bullets, enemies)

        for platform in platforms:
            pygame.draw.rect(screen, deep_black, platform)

        if character.rect.right >= width and character.rect.bottom >= height - 50:
            return "shed"

        bullets.draw(screen)
        enemies.draw(screen)
        character.draw(screen)

        draw_ui(screen, character)

        if level_complete:
            return level_end_screen(screen, level)

        if character.health <= 0:
            return game_over_screen(screen)

        pygame.display.flip()


def spawn_enemies(group, count, health):
    for _ in range(count):
        enemy = Enemy()
        enemy.health = health
        enemy.max_health = health
        group.add(enemy)


def handle_collisions(character, bullets, enemies):
    for bullet in bullets:
        collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in collided_enemies:
            enemy.health -= 5
            bullet.kill()
            if enemy.health <= 0:
                enemy.kill()

    for enemy in enemies:
        if pygame.sprite.collide_rect(character, enemy):
            character.take_damage(10)


def draw_ui(screen, character):
    font = pygame.font.SysFont("Corbel", 30)
    health_text = font.render(f"Health: {character.health}/{character.max_health}", True, green)
    screen.blit(health_text, (10, 10))


def level_end_screen(screen, level):
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
