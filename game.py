import pygame
from character import Character  # Main character class
from enemy import Enemy  # Enemy class
from powerups import *  # Power-ups used in the game
from chest import spawn_chests
from shop import *

width, height = resolution


# Function to create platforms for each level
def create_platforms(level):
    """
    Create platforms for the specified level.

    Parameters
    ----------
    level : int
        The current level number.

    Returns
    -------
    list of pygame.Rect
        A list of platforms for the given level.
    """
    platforms = []
    moving_platforms = []
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
            pygame.Rect(300, height - 150, 200, 10),
            pygame.Rect(500, height - 250, 200, 10),
            pygame.Rect(800, height - 350, 200, 10),
            pygame.Rect(500, height - 470, 200, 10),
            last_platform,
        ]
    elif level == 3:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(55, height - 200, 200, 10),
            pygame.Rect(350, height - 200, 200, 10),
            pygame.Rect(405, height - 320, 200, 10),
            pygame.Rect(700, height - 400, 200, 10),
            last_platform,
        ]
    elif level == 4:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(80, height - 250, 200, 10),
            pygame.Rect(300, height - 440, 200, 10),
            pygame.Rect(600, height - 500, 200, 10),
            last_platform,
        ]
    elif level == 5:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(350, height - 80, 200, 10),
            pygame.Rect(600, height - 200, 200, 10),
            pygame.Rect(800, height - 350, 200, 10),
            last_platform,
        ]
    elif level == 6:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(250, height - 120, 200, 10),
            pygame.Rect(450, height - 220, 200, 10),
            last_platform,
        ]
        moving_platforms = [{"rect": pygame.Rect(650, height-320, 200, 10), "direction": "vertical", "speed": 1, "range": 100},]
    elif level == 7:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(560, height - 400, 200, 10),
            last_platform,
        ]
        moving_platforms = [{"rect": pygame.Rect(350, height - 150, 200, 10), "direction": "vertical", "speed": 1, "range": 150}, ]
    elif level == 8:
        platforms = [
            pygame.Rect(400, height - 250, 200, 10),
            pygame.Rect(600, height - 350, 200, 10),
            last_platform,
        ]
        moving_platforms = [{"rect": pygame.Rect(75, height - 50, 200, 10), "direction": "horizontal", "speed": 1, "range": 200}]
    elif level == 9:
        platforms = [
            pygame.Rect(50, height - 50, 200, 10),
            pygame.Rect(200, height - 400, 200, 10),
            last_platform,
        ]
        moving_platforms = [{"rect": pygame.Rect(50, height - 200, 200, 10), "direction": "vertical", "speed": 1, "range": 100},
                            {"rect": pygame.Rect(600, height - 450, 200, 10), "direction": "horizontal", "speed": 2, "range": 200}]

    elif level == 10:
        platforms = [
            pygame.Rect(20, height-50, 200, 10),
            pygame.Rect(650, 100, 150, 10),
            last_platform,
        ]
        moving_platforms = [{"rect": pygame.Rect(50, height - 100, 200, 10), "direction": "vertical", "speed": 1, "range": 100},
                            {"rect": pygame.Rect(500, height - 300, 200, 10), "direction": "horizontal", "speed": 2, "range": 200}
                            ]

    # Initialize moving platform positions
    for platform in moving_platforms:
        platform["initial_x"] = platform["rect"].x
        platform["initial_y"] = platform["rect"].y

    return platforms, moving_platforms


def update_moving_platforms(moving_platforms):
    for platform in moving_platforms:
        if platform["direction"] == "horizontal":
            platform["rect"].x += platform["speed"]
            if abs(platform["rect"].x - platform["initial_x"]) >= platform["range"]:
                platform["speed"] *= -1
        elif platform["direction"] == "vertical":
            platform["rect"].y += platform["speed"]
            if abs(platform["rect"].y - platform["initial_y"]) >= platform["range"]:
                platform["speed"] *= -1


def game_loop(screen, character=None):
    """
    Main game loop for managing the levels and states and memory system.

    Parameters
    ----------
    screen : pygame.Surface
        The game screen surface.
    character : Character
        The main character object. If None, a new character is created.
    """
    if character is None:
        character = Character(image="characters images/Tomátio.png", x=10, y=height - 50)  # Start at bottom-left corner

    current_level = character.current_level  # Continue from saved level
    current_state = "main"
    last_level = 10  # Define the last level

    while True:
        if current_state == "main":
            platforms, moving_platforms = create_platforms(current_level)
            result = play_level(screen, character, current_level, platforms, moving_platforms)

            if result == "next_level":
                if current_level < last_level:
                    current_level += 1
                    character.current_level = current_level  # Update the character's current level
                    character.health = character.max_health
                    character.rect.topleft = (10, height - 50)  # Reset character position
                    character.save_player_data("save_file.json")  # Save progress after advancing
                else:
                    # Final level completed
                    current_state = "last_level"

            elif result == "retry":
                # Retry resets character position but does not save progress
                character.health = character.max_health
                character.rect.topleft = (10, height - 50)  # Reset position on retry

            elif result == "break":
                # Save progress before breaking the game loop
                character.save_player_data("save_file.json")
                break

            elif result == "main_menu":
                # Save progress before returning to the main menu
                character.save_player_data("save_file.json")
                return

        if current_state == "last_level":
            if current_level >= last_level:
                character.reset_player_data("save_file.json")  # Reset progress
                return last_level_screen(screen)
            result = last_level_screen(screen)
            if result == "main_menu":
                return


def execute_game(screen, character=None):
    """
    Execute the game loop.

    Parameters
    ----------
    screen : pygame.Surface
        The game screen surface.
    character : Character
        The main character object. If None, a new character is created.
    """
    game_loop(screen, character)


def play_level(screen, character, level, platforms, moving_platforms):
    """
    Play the current level of the game.

    Parameters
    ----------
    screen : pygame.Surface
        The game screen surface.
    character : Character
        The main character.
    level : int
        The current level number.
    platforms : list of pygame.Rect
        A list of platform rectangles for the level.

    Returns
    -------
    The result of the level ("next_level", "retry", "shed", "break", or "main_menu").
    """
    clock = pygame.time.Clock()
    background_image = pygame.image.load("backgrounds/game.webp")
    background_image = pygame.transform.scale(background_image, resolution)

    bullets = pygame.sprite.Group()
    character.bullets = bullets  # Attach the bullets group to the character

    enemies = pygame.sprite.Group()
    chests = pygame.sprite.Group()
    spawn_enemies(enemies, platforms)
    spawn_chests(chests, platforms)
    powerups = pygame.sprite.Group()

    # Initialize game state to hold enemies
    game_state = {'enemies': enemies}  # Pass the current enemies group to game state

    # Add a random power-up to a random platform
    platform = random.choice(platforms)
    powerup_classes = [InvincibilityPowerUp, TomatoCoinPowerUp, RapidBlasterPowerUp, DespawnerPowerUp]
    powerup_weights = [50, 30, 30, 5]
    # Select a power-up based on weighted probabilities
    powerup = random.choices(powerup_classes, weights=powerup_weights, k=1)[0]
    powerup_instance = powerup(platform.centerx, platform.top - 15)
    powerups.add(powerup_instance)

    running = True
    level_complete = False

    while running:
        screen.blit(background_image, (0, 0))
        clock.tick(fps)

        update_moving_platforms(moving_platforms)

        # Check collisions with platforms
        on_platform = False
        for platform in platforms + [mp["rect"] for mp in moving_platforms]:
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
                character.save_player_data("save_file.json")
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    character.shoot(bullets)
                mouse = pygame.mouse.get_pos()
                # Detect click on the "Back" button
                if back_rect.collidepoint(mouse):
                    character.save_player_data("save_file.json")
                    return "break"
                # Detect click on the "Shop" button
                elif shop_rect.collidepoint(mouse):
                    character.save_player_data("save_file.json")
                    shop(screen, character)

        # Update game components
        character.update()
        bullets.update()
        enemies.update(character)
        chests.update()

        # Update active power-up timers
        for powerup in powerups:
            powerup.update()

        # Check collisions with chests
        collected_chests = pygame.sprite.spritecollide(character, chests, True)
        for chest in collected_chests:
            chest.interact(character)

        # Collecting power-ups
        collected_powerups = pygame.sprite.spritecollide(character, powerups, True)
        for powerup in collected_powerups:
            if powerup.requires_game_state:  # Check the flag
                powerup.affect_player(character, game_state)
            else:
                powerup.affect_player(character)

        # Fire bullets if RapidBlaster is active
        if character.rapid_blaster_active:
            character.shoot_automatic()

        handle_collisions(character, bullets, enemies)

        # Define a rectangle at the bottom of the screen
        ground_rect = pygame.Rect(0, height - 1, width, 1)
        # Check if the character's rectangle touches the ground rectangle
        if character.rect.colliderect(ground_rect):
            return game_over_screen(screen)

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, deep_black, platform)
        # Draw moving platforms
        for mp in moving_platforms:
            pygame.draw.rect(screen, deep_black, mp["rect"])

        bullets.draw(screen)
        powerups.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        character.draw(screen)
        chests.draw(screen)

        draw_ui(screen, character)

        if level_complete:
            # Expire all active power-ups before transitioning
            for powerup in powerups:
                powerup.expire()
            powerups.empty() # Clear all remaining power-ups
            character.image = character.original_image  # Restore to true original image
            character.rect.y = character.original_y  # Reset position
            return level_end_screen(screen, level, character)

        if character.health <= 0:
            return game_over_screen(screen)

        # Draw buttons
        corbel_font = pygame.font.SysFont("Corbel", 40, bold=True)
        mouse = pygame.mouse.get_pos()

        # Button styling function
        def draw_button(rect, text, color, hover_color):
            if rect.collidepoint(mouse):
                pygame.draw.rect(screen, hover_color, rect, border_radius=10)
            else:
                pygame.draw.rect(screen, color, rect, border_radius=10)
            text_surf = corbel_font.render(text, True, white)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        # Define button colors
        default_color = dark_red
        hover_color = glowing_light_red

        # Back button
        back_rect = pygame.Rect(15, 130, 120, 50)
        draw_button(back_rect, "Back", default_color, hover_color)

        # Shop button (below the Back button)
        shop_rect = pygame.Rect(15, 190, 120, 50)
        draw_button(shop_rect, "Shop", default_color, hover_color)

        pygame.display.flip()


def spawn_enemies(group, platforms):
    """
    Spawn enemies on the given platforms.

    Parameters
    ----------
    group : pygame.sprite.Group
        The group to which the enemies are added.
    platforms : list of pygame.Rect
        The platform rectangles to place enemies on.
    """
    for platform in platforms:
        enemy = Enemy(platform)
        group.add(enemy)


def handle_collisions(character, bullets, enemies):
    """
    Handle collisions between bullets, enemies, and the character.

    Parameters
    ----------
    character : Character
        The main character.
    bullets : pygame.sprite.Group
        The group of bullets.
    enemies : pygame.sprite.Group
        The group of enemies.
    """
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
    """
    Display the level-end screen and handle user interactions.

    Parameters
    ----------
    screen : pygame.Surface
        The game screen surface to render the UI elements on.
    level : int
        The current level that the player has completed.
    character : object
        The main character, which is used to update coins.

    Returns
    -------
    The next action based on user selection: "next_level" or "main_menu".
    """
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
                    character.save_player_data("save_file.json")
                    return "next_level"
                elif menu_button.collidepoint(mouse):
                    character.save_player_data("save_file.json")
                    return "main_menu"
def game_over_screen(screen):
    """
    Display the game-over screen and handle user interactions.

    Parameters
    ----------
    screen : pygame.Surface
        The game screen surface to render the UI elements on.

    Returns
    -------
    The next action based on user selection: "retry" or "main_menu".
    """
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
    """
    Display the last-level completion screen and handle user interactions.

    Parameters
    ----------
    screen : pygame.Surface
        The game screen surface to render the UI elements on.

    Returns
    -------
    The next action based on user selection: "main_menu".
    """
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

    menu_button = pygame.Rect(350, 400, 260, 60)
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
    """
    Draw the in-game UI elements showing the player's status.

    Parameters
    ----------
    screen : pygame.Surface
        The game screen surface to render the UI elements on.
    character : object
        The main character, which contains health, coins, diamonds, and level.
    """
    font = pygame.font.SysFont("Corbel", 30, bold=True)
    health_text = font.render(f"Health: {character.health}/{character.max_health}", True, green)
    screen.blit(health_text, (10, 10))
    coin_text = font.render(f"Coins: {character.coins}", True, yellow)
    screen.blit(coin_text, (10, 40))
    diamond_text = font.render(f"Diamonds: {character.diamond_count}", True, blue)
    screen.blit(diamond_text, (10, 70))
    level_text = font.render(f"Level: {character.current_level}", True, deep_black)
    screen.blit(level_text, (10, 100))

