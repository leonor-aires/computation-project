import pygame
from config import *
from character import Character
from bullet import Bullet


def apply_Ketchup_Kannon(character):
    """
    Apply a Ketchup Kannon to the character.

    Args:
    character (object): The character who will be applied the Ketchup Kannon.

    Returns:
    None
    """
    character.weapon = 'Ketchup Kannon'
    character.bullet_damage = 6

def apply_Knife_of_Justice(character):
    """
    Apply a lightning bullets to the character.

    Args:
    character (object): The character who will be applied the lightning bullets.

    Returns:
    None
    """
    character.weapon = 'Knife of Justice'
    character.bullet_damage = 10

def apply_fridge_style(character):
    """
    Change the character and  the bullet design

    Args:
    character (object): The character who will be applied the fridge style.

    Returns:
    None
        """
    character.image = pygame.image.load("characters images/fridge_style.png")
    character.image = pygame.transform.scale(character.image, (100, 100))
    character.rect = character.image.get_rect(topleft=(character.rect.x, character.rect.y))
    character.weapon = "egg"  # Set the weapon type for gameplay bullets

def apply_Tomato_slice(character):
    """
    Apply a Tomato slice to the character.

    Args:
    character (object): The character who will be applied the Tomato slice.

    Returns:
    None
    """
    character.weapon = 'Tomato Slice'
    character.bullet_damage = 4

def shop(screen, character):
    """
    Display and manage the shop. Allows the character to purchase items.

    Args:
    screen (pygame.Surface): The Pygame screen to draw the shop on.
    character (object): The character accessing the shop

    Returns:
    None
    """
    pygame.init()
    font = pygame.font.SysFont("Corbel", 40,  bold = True)
    title_font = pygame.font.SysFont("Corbel", 60, bold=True)
    clock = pygame.time.Clock()

    # Define shop items
    shop_items = [
        {"name": "Tomato Slice", "cost": 100, "currency": "coins", "action": apply_Tomato_slice},
        {"name": "Ketchup Kannon", "cost": 200, "currency": "coins", "action": apply_Ketchup_Kannon},
        {"name": "Knife of Justice", "cost": 300, "currency": "coins", "action": apply_Knife_of_Justice},
        {"name": "Fridge Style", "cost": 150, "currency": "diamonds", "action": apply_fridge_style},
    ]

    # Colors
    card_color = (70, 70, 120)  # Card background
    card_highlight = (90, 140, 200)  # Highlight for hover
    back_color = dark_red
    back_hover = (220, 70, 70)

    # Back button setup
    back_text = font.render("Back", True, white)
    back_rect = pygame.Rect(450, 550, 100, 46)  # Position the button

    # Message setup
    purchase_message = ""
    message_displayed = False

    # Running flag
    running = True

    while running:
        screen.fill((0, 0, 0))  # Clear the screen with a black background
        mouse = pygame.mouse.get_pos()  # Get the current mouse position

        # Render title
        title_text = title_font.render("SHOP", True, (255, 255, 0))
        screen.blit(title_text, (430, 20))

        # Render shop items
        i = 0  # Initialize index manually
        for item in shop_items:
            card_rect = pygame.Rect(100, 100 + i * 110, 800, 90)
            # Highlight the card if hovered over
            if card_rect.collidepoint(mouse):
                pygame.draw.rect(screen, card_highlight, card_rect, border_radius=10)
            else:
                pygame.draw.rect(screen, card_color, card_rect, border_radius=10)

            # Determine the currency type (coins or diamonds)
            currency_type = "coins" if item["currency"] == "coins" else "diamonds"
            # Render item text with name, cost, and currency
            item_text = font.render(f"{item['name']} - {item['cost']} {currency_type}", True, white)
            screen.blit(item_text, (120, 120 + i * 110))  # Render item text with spacing

            i += 1  # Increment index manually

        # Render back button
        if back_rect.collidepoint(mouse):
            pygame.draw.rect(screen, back_hover, back_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, back_color, back_rect, border_radius=10)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        # Show purchase message if any
        if message_displayed:
            pygame.draw.rect(screen, green, (100, 300, 800, 100), border_radius=10)
            purchase_text = font.render(purchase_message, True, white)
            purchase_text_rect = purchase_text.get_rect(center=(500, 350))
            screen.blit(purchase_text, purchase_text_rect)

        # Render coins
        coin_text = font.render(f"Coins: {character.coins}", True, yellow)
        screen.blit(coin_text, (10, 550))  # Ensure coins are rendered continuously

        # Render diamantes
        diamond_text = font.render(f"Diamonds: {character.diamond_count}", True, blue)  # Cor azul clara
        screen.blit(diamond_text, (750, 550))

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Maintain a frame rate of 60 FPS

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if "back" button is clicked
                if back_rect.collidepoint(mouse):
                    return  # Exit the shop

                # Check if a shop item is clicked
                for i, item in enumerate(shop_items):
                    item_rect = pygame.Rect(100, 100 + i * 110, 800, 90)
                    if item_rect.collidepoint(mouse):
                        if item["currency"] == "coins":
                            if character.coins >= item["cost"]:
                                character.coins -= item["cost"]
                                item["action"](character)  # Apply the item's effect
                                purchase_message = f"Purchased {item['name']}!"
                                message_displayed = True
                            else:
                                purchase_message = "Not enough coins!"
                                message_displayed = True
                        elif item["currency"] == "diamonds":
                            if character.diamond_count >= item["cost"]:
                                character.diamond_count -= item["cost"]
                                item["action"](character)  # Apply the item's effect
                                purchase_message = f"Purchased {item['name']}!"
                                message_displayed = True
                            else:
                                purchase_message = "Not enough diamonds!"
                                message_displayed = True




