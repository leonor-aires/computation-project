import pygame
import random
from game import *
from character import Character

# Define a class for the chest
class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize the Chest instance.

        Parameters
        ----------
        x : int
            The x-coordinate of the chest.
        y : int
            The y-coordinate of the chest.
        """
        super().__init__()
        self.image = pygame.image.load("Chest Images/chest.png")  # Replace with your chest image path
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))

    def interact(self, character):
        """
        Pauses the game and presents the chest options.

        Parameters
        ----------
        character : object
            The character interacting with the chest.
        """
        return open_chest(character)

# Function to spawn chests
def spawn_chests(group, platforms):
    """
    Spawn chests randomly on the  platforms.

    Parameters
    ----------
    group : pygame.sprite.Group
        The group to which the spawned chest will be added.
    platforms : list of pygame.Rect - in game.py
        The list of platform rectangles to spawn the chests on.
    """
    if random.random() < 0.3:  # Always spawn a chest
        platform = random.choice(platforms)
        chest = Chest(platform.centerx, platform.top - 25)
        group.add(chest)

def health_boost(character):
    """
    Fully restores the character's health.

    Parameters
    ----------
    character : object
        The character receiving the health boost.
    """
    character.health = min(character.max_health, character.max_health)

def extra_coins(character):
    """
    Grants the character an additional 100 coins.

    Parameters
    ----------
    character : object
        The character receiving the extra coins.
    """
    character.earn_coins(100)

def speed_boost(character):
    """
    Increases the character's speed by 1.

    Parameters
    ----------
    character : object
        The character receiving the speed boost.
    """
    character.speed += 1

def diamonds(character):
    """
    Grants the character an additional 50 diamonds.

    Parameters
    ----------
    character : object
        The character receiving the diamonds.
    """
    character.diamond_count += 50

def Ketchup_Kannon(character):
    """
    Apply a Ketchup Kannon weapon to the character.

    Args:
    character (object): The character who will be applied the Ketchup Kannon weapon.
    """
    character.weapon = 'Ketchup Kannon'
    character.bullet_damage = 6

# Function to open the chest and handle options
def open_chest(character):
    """
    Opens a chest and presents random reward options to the player.

    Parameters
    ----------
    character : object
        The character interacting with the chest.
    """
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont("Corbel", 40, bold=True)
    #mouse = pygame.mouse.get_pos()  # Get the current mouse position

    # Options for the chest
    options = [
        {"name": "Health Boost", "effect": health_boost},
        {"name": "100$", "effect": extra_coins},
        {"name": "Speed Boost", "effect": speed_boost},
        {"name": "50 diamonds", "effect": diamonds},
        {"name": "Ketchup Kannon", "effect": Ketchup_Kannon},
    ]

    # Randomize three options to present
    presented_options = random.sample(options, 3)

    # Chest UI
    background_image = pygame.image.load("backgrounds/factory.webp")
    background_image = pygame.transform.scale(background_image, resolution)
    screen.blit(background_image, (0, 0))
    chest_text = font.render("Choose a Reward!", True, deep_black)
    chest_text_rect = chest_text.get_rect(center=(width // 2, height // 4))
    screen.blit(chest_text, chest_text_rect)

    # Draw buttons for each option
    button_rects = []
    button_width, button_height = 300, 60
    button_margin = 30

    # Calculate starting X position to center the buttons
    total_button_width = 3 * button_width + 2 * button_margin  # Total width of all buttons
    start_x = (width - total_button_width) // 2  # Centering X position

    for i in range(3):
        option = presented_options[i]
        # Define button position and size
        button_rect = pygame.Rect(start_x + i * (button_width + button_margin), height // 2, button_width,button_height)

        # Draw the button with rounded corners (no hover effect)
        pygame.draw.rect(screen, purple, button_rect, border_radius=15)  # Button with rounded corners

        # Add button text
        button_text = font.render(option["name"], True, white)
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        # Store the button rect and its effect for later use
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
    """
    Plays the game level's with the addition of randomly spawned chests.

    Parameters
    ----------
    screen : pygame.Surface
        The Pygame screen where the level is displayed.
    character : object
        The character playing the level.
    level : int
        The current level number.
    platforms : list of pygame.Rect
        The list of platform rectangles in the level- - in game.py
    """
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