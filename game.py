import pygame
import random
from config import *  # Basic game settings (such as colors, resolution)
from character import Character  # Main character class
from enemy import Enemy  # Enemy class
from shed import shed  # Shop system (shed)
from powerups import *  # Power-ups used in the game
from chest import Chest, spawn_chests

# Function to create platforms for each level
def create_platforms(level):
    platforms = []
    last_platform = pygame.Rect(width - 150, 100, 150, 10)  # Always the final platform

    if level == 1:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(300, height - 150, 200, 10),
            pygame.Rect(600, height - 250, 200, 10),
            pygame.Rect(850, height - 350, 200, 10),
            last_platform,
        ]
    elif level == 2:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(250, height - 100, 200, 10),
            pygame.Rect(500, height - 200, 200, 10),
            pygame.Rect(750, height - 300, 200, 10),
            pygame.Rect(500, height - 400, 200, 10),
            last_platform,
        ]
    elif level == 3:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(200, height - 120, 200, 10),
            pygame.Rect(450, height - 220, 200, 10),
            pygame.Rect(700, height - 320, 200, 10),
            pygame.Rect(800, height - 420, 200, 10),
            last_platform,
        ]
    elif level == 4:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(200, height - 100, 200, 10),
            pygame.Rect(400, height - 180, 200, 10),
            pygame.Rect(600, height - 280, 200, 10),
            pygame.Rect(800, height - 380, 200, 10),
            last_platform,
        ]
    elif level == 5:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(200, height - 100, 200, 10),
            pygame.Rect(400, height - 180, 200, 10),
            pygame.Rect(600, height - 280, 200, 10),
            last_platform,
        ]
    elif level == 6:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(250, height - 120, 200, 10),
            pygame.Rect(450, height - 220, 200, 10),
            pygame.Rect(650, height - 320, 200, 10),
            pygame.Rect(850, height - 420, 200, 10),
            last_platform,
        ]
    elif level == 7:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(150, height - 100, 200, 10),
            pygame.Rect(350, height - 200, 200, 10),
            pygame.Rect(550, height - 300, 200, 10),
            pygame.Rect(750, height - 400, 200, 10),
            last_platform,
        ]
    elif level == 8:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(200, height - 150, 200, 10),
            pygame.Rect(400, height - 250, 200, 10),
            pygame.Rect(600, height - 350, 200, 10),
            pygame.Rect(800, height - 450, 200, 10),
            last_platform,
        ]
    elif level == 9:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(150, height - 100, 200, 10),
            pygame.Rect(300, height - 150, 200, 10),
            pygame.Rect(500, height - 250, 200, 10),
            pygame.Rect(700, height - 350, 200, 10),
            pygame.Rect(800, height - 450, 200, 10),
            last_platform,
        ]
    elif level == 10:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(150, height - 100, 200, 10),
            pygame.Rect(300, height - 200, 200, 10),
            pygame.Rect(500, height - 300, 200, 10),
            pygame.Rect(700, height - 400, 200, 10),
            last_platform,
        ]
    return platforms


def game_loop(screen, character=None):
    if character is None:
        character = Character(image="characters images/Tomátio.png", x=10, y=height - 50)  # Start at bottom-left corner

    current_level = 1
    current_state = "main"
    last_level = 10  # Define the last level

    while True:
        if current_state == "main":
            platforms = create_platforms(current_level)
            result = play_level(screen, character, current_level, platforms)

            if result == "next_level":
                if current_level < last_level:
                    current_level += 1
                    character.health = character.max_health
                    character.rect.topleft = (10, height - 50)  # Reset character position
                    character.current_level +=1
                else:
                    # Final level completed
                    current_state = "last_level"

            elif result == "retry":
                character.health = character.max_health
                character.rect.topleft = (10, height - 50)  # Reset position on retry
            elif result == "shed":
                current_state = "shed"
            elif result == "break":
                break
            elif result == "main_menu":
                return
        elif current_state == "shed":
            current_state = shed(screen, character)
        elif current_state == "last_level":
            if current_level > last_level:
                # All levels completed, transition to a final screen or main menu
                return "all_levels_completed"
            result = last_level_screen(screen)
            if result == "main_menu":
                return


def execute_game(screen, character=None):
    game_loop(screen, character)


def play_level(screen, character, level, platforms):
    clock = pygame.time.Clock()
    background_image = pygame.image.load("backgrounds/game.webp")
    background_image = pygame.transform.scale(background_image, resolution)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    chests = pygame.sprite.Group()
    spawn_enemies(enemies, platforms)
    spawn_chests(chests, platforms)
    powerups = pygame.sprite.Group()

    # Add a random power-up to a random platform
    platform = random.choice(platforms)
    powerup = random.choice([InvincibilityPowerUp, TomatoCoinPowerUp])
    print(f"[DEBUG] Selected Power-Up: {powerup.__name__}")
    powerup_instance = powerup(platform.centerx, platform.top - 15)
    powerups.add(powerup_instance)
    print(f"[DEBUG] Power-Up Spawned: {powerup.__name__} at ({platform.centerx}, {platform.top - 15})")

    running = True
    level_complete = False

    while running:
        screen.blit(background_image, (0, 0))
        clock.tick(fps)

        # Check collisions with platforms
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

        # Check level completion
        if (character.rect.right >= platforms[-1].right and
                character.rect.bottom == platforms[-1].top and
                len(enemies) == 0):
            level_complete = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    character.shoot(bullets)
                    # Detect click on the "Back" button
                if 10 <= mouse[0] <= 110 and 100 <= mouse[1] <= 155:
                    return "break"

        character.update()
        bullets.update()
        enemies.update(character)
        chests.update()
        powerups.update()

        # Check collisions with chests
        collected_chests = pygame.sprite.spritecollide(character, chests, True)
        for chest in collected_chests:
            chest.interact(character)

        # Collecting power-ups
        collected_powerups = pygame.sprite.spritecollide(character, powerups, True)
        for powerup in collected_powerups:
            powerup.affect_player(character)

        handle_collisions(character, bullets, enemies)

        for platform in platforms:
            pygame.draw.rect(screen, deep_black, platform)

        if character.rect.right >= width and character.rect.bottom >= height - 50:
            return "shed"

        bullets.draw(screen)
        powerups.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        character.draw(screen)
        chests.draw(screen)

        draw_ui(screen, character)

        if level_complete:
            return level_end_screen(screen, level, character)

        if character.health <= 0:
            return game_over_screen(screen)

        corbel_font = pygame.font.SysFont("Corbel", 40, bold=True)
        mouse = pygame.mouse.get_pos()
        #button styling
        def draw_button(rect, text, color):
            pygame.draw.rect(screen, color, rect, border_radius=10)  # Rounded corners
            text_surf = corbel_font.render(text, True, white)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)


        back_rect = pygame.Rect(15, 130, 120, 50)  # Position the button
        draw_button(back_rect, "Back", dark_red)  # Green button for retry

        pygame.display.flip()


def spawn_enemies(group, platforms):
    for platform in platforms:
        enemy = Enemy(platform)
        group.add(enemy)


def handle_collisions(character, bullets, enemies):
    for bullet in bullets:
        collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in collided_enemies:
            # Apply bullet damage based on character's bullet_damage attribute
            enemy.health -= character.bullet_damage
            bullet.kill()
            if enemy.health <= 0:
                # Apply coin multiplier when earning coins
                character.earn_coins(character.coin_reward)  # Earn coins for defeated enemies
                enemy.kill()

    for enemy in enemies:
        if pygame.sprite.collide_rect(character, enemy):
            if not character.invincible:
                character.take_damage(10)





def level_end_screen(screen, level, character):
    # Load background image
    background_image = pygame.image.load("backgrounds/game.webp")
    background_image = pygame.transform.scale(background_image, resolution)
    screen.blit(background_image, (0, 0))  # Draw the background image

    font = pygame.font.SysFont("Corbel", 50, bold=True)
    character.earn_coins(level * 10)

    level_end_text = font.render(f"End of Level {level}", True, deep_black)
    level_end_rect = level_end_text.get_rect(center=(width // 2, height // 3))
    screen.blit(level_end_text, level_end_rect)

    # Button Styling
    def draw_button(rect, text, color):
        pygame.draw.rect(screen, color, rect, border_radius=10)  # Rounded corners
        text_surf = font.render(text, True, white)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    next_level_button = pygame.Rect(150, 400, 260, 60)
    menu_button = pygame.Rect(600, 400, 260, 60)

    draw_button(next_level_button, "Next Level", dark_red)  # Green button for retry
    draw_button(menu_button, "Main Menu", dark_red)  # Dark red button for main menu

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
    # Load background image
    background_image = pygame.image.load("backgrounds/game.webp")
    background_image = pygame.transform.scale(background_image, resolution)
    screen.blit(background_image, (0, 0))  # Draw the background image
    # UI elements
    font = pygame.font.SysFont("Corbel", 50, bold=True)
    # Game Over Text
    game_over_text = font.render("Game Over", True, deep_black)
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 3))
    screen.blit(game_over_text, game_over_rect)

    # Button Styling
    def draw_button(rect, text, color):
        pygame.draw.rect(screen, color, rect, border_radius=10)  # Rounded corners
        text_surf = font.render(text, True, white)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    # Buttons
    retry_button = pygame.Rect(200, 400, 200, 60)
    menu_button = pygame.Rect(600, 400, 260, 60)

    draw_button(retry_button, "Retry", green)  # Green button for retry
    draw_button(menu_button, "Main Menu", dark_red)  # Dark red button for main menu

    # Update display
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


def last_level_screen(screen):
    # Load background image
    background_image = pygame.image.load("backgrounds/game.webp")
    background_image = pygame.transform.scale(background_image, resolution)
    screen.blit(background_image, (0, 0))  # Draw the background image
    #Font that will be use in the text
    font = pygame.font.SysFont("Corbel", 50, bold=True)

    message_text = font.render("Amazing work! More adventures coming soon!", True, deep_black)
    message_rect = message_text.get_rect(center=(width // 2, height // 3))
    screen.blit(message_text, message_rect)

    # Button Styling
    def draw_button(rect, text, color):
        pygame.draw.rect(screen, color, rect, border_radius=10)  # Rounded corners
        text_surf = font.render(text, True, white)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    menu_button = pygame.Rect(3500, 400, 260, 60)
    draw_button(menu_button, "Main Menu", dark_red)  # Dark red button for main menu

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if menu_button.collidepoint(mouse):
                    return "main_menu"
def draw_ui(screen, character):
    font = pygame.font.SysFont("Corbel", 30, bold=True)
    health_text = font.render(f"Health: {character.health}/{character.max_health}", True, green)
    screen.blit(health_text, (10, 10))
    coin_text = font.render(f"Coins: {character.coins}", True, yellow)
    screen.blit(coin_text, (10, 40))
    diamond_text = font.render(f"Diamonds: {character.diamond_count}", True, blue)
    screen.blit(diamond_text, (10, 70))
    level_text = font.render(f"Level: {character.current_level}", True, deep_black)
    screen.blit(level_text, (10, 100))