import pygame
import random
from game import *
# Define a class for the chest
class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Chest Images/chest.png")  # Replace with your chest image path
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))

    def interact(self, character):
        """Pauses the game and presents the chest options."""
        return open_chest(character)

# Function to spawn chests
def spawn_chests(group, platforms):
    if random.random() < 1.0:  # 10% chance to spawn a chest
        platform = random.choice(platforms)
        chest = Chest(platform.centerx, platform.top - 25)
        group.add(chest)

# Function to open the chest and handle options
def open_chest(character):
    """Handles the interaction when the player opens a chest."""
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont("Corbel", 40, bold=True)

    # Options for the chest
    options = [
        {"name": "Weapon Upgrade", "effect": lambda char: char.upgrade_weapon()},
        {"name": "Health Boost", "effect": lambda char: setattr(char, "health", min(char.max_health, char.health + 20))},
        {"name": "Extra Coins", "effect": lambda char: char.earn_coins(50)},
    ]

    # Randomize three options to present
    presented_options = random.sample(options, 3)

    # Chest UI
    screen.fill((30, 30, 30))
    chest_text = font.render("Choose a Reward!", True, (255, 255, 255))
    chest_text_rect = chest_text.get_rect(center=(width // 2, height // 4))
    screen.blit(chest_text, chest_text_rect)

    # Draw buttons for each option
    button_rects = []
    for i, option in enumerate(presented_options):
        button_rect = pygame.Rect(200 + i * 300, height // 2, 200, 60)
        pygame.draw.rect(screen, (100, 100, 255), button_rect)

        button_text = font.render(option["name"], True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        button_rects.append((button_rect, option["effect"]))

    pygame.display.flip()

    # Wait for the player to select an option
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, effect in button_rects:
                    if rect.collidepoint(mouse_pos):
                        effect(character)  # Apply the selected effect
                        return  # Resume the game

# Modify the game loop to integrate chests
def play_level_with_chests(screen, character, level, platforms):
    clock = pygame.time.Clock()
    background_image = pygame.image.load("backgrounds/game.webp")
    background_image = pygame.transform.scale(background_image, resolution)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    chests = pygame.sprite.Group()
    spawn_enemies(enemies, platforms)
    spawn_chests(chests, platforms)  # Add chest spawning

    running = True
    level_complete = False
    while running:
        screen.blit(background_image, (0, 0))
        clock.tick(fps)

        for platform in platforms:
            pygame.draw.rect(screen, deep_black, platform)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

        character.update()
        bullets.update()
        enemies.update(character)
        chests.update()

        # Check collisions with chests
        collected_chests = pygame.sprite.spritecollide(character, chests, True)
        for chest in collected_chests:
            chest.interact(character)

        handle_collisions(character, bullets, enemies)

        bullets.draw(screen)
        chests.draw(screen)
        enemies.draw(screen)
        character.draw(screen)
        draw_ui(screen, character)

        if level_complete:
            return level_end_screen(screen, level, character)

        if character.health <= 0:
            return game_over_screen(screen)

        pygame.display.flip()