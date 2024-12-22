import pygame
from config import *

def apply_Ketchup_Kannon(character):
    """
    Apply the Ketchup Kannon weapon to the character.

    Parameters
    ----------
    character:  Character
    The character to whom the Ketchup Kannon will be applied.
    """
    character.weapon = 'Ketchup Kannon'
    character.bullet_damage = 6

def apply_Knife_of_Justice(character):
    """
    Apply the Knife of Justice weapon to the character.

    Parameters
    ----------
    character : Character
        The character to whom the Knife of Justice will be applied.
    """
    character.weapon = 'Knife of Justice'
    character.bullet_damage = 10

def apply_fridge_style(character):
    """
    Apply the Fridge Style  and egg weapon to the character.

    Parameters
    ----------
    character : Character
        The character to whom the Fridge Style will be applied.
    """
    character.image = pygame.image.load("characters images/fridge_style.png")
    character.image = pygame.transform.scale(character.image, (100, 100))
    character.rect = character.image.get_rect(topleft=(character.rect.x, character.rect.y))
    character.weapon = "egg"
    character.original_image = character.image

def apply_Tomato_slice(character):
    """
    Apply the Tomato Slice weapon to the character.

    Parameters
    ----------
    character : Character
        The character to whom the Tomato Slice will be applied.
    """
    character.weapon = 'Tomato Slice'
    character.bullet_damage = 4

def shop(screen, character):
    """
    Display and manage the shop where the character can purchase items.

    Parameters
    ----------
    screen : pygame.Surface
        The Pygame screen on which the shop interface will be drawn.
    character : Character
        The character interacting with the shop.
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
        {"name": "Fridge Style", "cost": 50, "currency": "diamonds", "action": apply_fridge_style},
    ]

    # Colors
    back_color = dark_red
    back_hover = (220, 70, 70)

    # Back button setup
    back_text = font.render("Back", True, white)
    back_rect = pygame.Rect(450, 550, 100, 46)

    # Message setup
    purchase_message = ""
    message_displayed = False

    running = True
    while running:
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()

        title_text = title_font.render("SHOP", True, (255, 255, 0))
        screen.blit(title_text, (430, 20))

        # Render shop items
        i = 0  # Initialize index manually
        for item in shop_items:
            card_rect = pygame.Rect(100, 100 + i * 110, 800, 90)
            if card_rect.collidepoint(mouse):
                pygame.draw.rect(screen, light_purple, card_rect, border_radius=10)
            else:
                pygame.draw.rect(screen, purple, card_rect, border_radius=10)

            # Determine the currency type (coins or diamonds)
            currency_type = "coins" if item["currency"] == "coins" else "diamonds"
            # Render item text with name, cost, and currency
            item_text = font.render(f"{item['name']} - {item['cost']} {currency_type}", True, white)
            screen.blit(item_text, (120, 120 + i * 110))

            i += 1  # Increment index manually

        # Render back button
        if back_rect.collidepoint(mouse):
            pygame.draw.rect(screen, back_hover, back_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, back_color, back_rect, border_radius=10)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        # Show purchase message there are purchases
        if message_displayed:
            pygame.draw.rect(screen, green, (100, 300, 800, 100), border_radius=10)
            purchase_text = font.render(purchase_message, True, white)
            purchase_text_rect = purchase_text.get_rect(center=(500, 350))
            screen.blit(purchase_text, purchase_text_rect)

        # Render coins
        coin_text = font.render(f"Coins: {character.coins}", True, yellow)
        screen.blit(coin_text, (10, 550))

        # Render diamonds
        diamond_text = font.render(f"Diamonds: {character.diamond_count}", True, blue)
        screen.blit(diamond_text, (750, 550))

        pygame.display.flip()
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(mouse):
                    return  # Exit the shop
                # Check if a shop item is clicked
                index = 0  # Initialize the index manually
                for item in shop_items:
                    item_rect = pygame.Rect(100, 100 + index * 110, 800, 90)
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
                    index += 1  # Increment the index manually




