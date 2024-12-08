import pygame
from config import *


def shop(screen, character):
    pygame.init()
    font = pygame.font.SysFont("Corbel", 40)
    title_font = pygame.font.SysFont("Corbel", 60, bold=True)
    clock = pygame.time.Clock()

    # Define shop items
    shop_items = [
        {"name": "Health Potion", "cost": 20,
         "action": lambda: setattr(character, 'health', min(character.max_health, character.max_health))},
        {"name": "Speed Boost", "cost": 50, "action": lambda: setattr(character, 'speed', character.speed + 1)},
        {"name": "Explosive Bullets", "cost": 100, "action": lambda: setattr(character, 'weapon', 'explosive')},
        {"name": "Lightning Bullets", "cost": 150, "action": lambda: setattr(character, 'weapon', 'lightning')},
    ]

    # Colors
    card_color = (70, 70, 120)  # Card background
    card_highlight = (90, 140, 200)  # Highlight for hover
    back_color = (180, 50, 50)
    back_hover = (220, 70, 70)

    # Back button setup
    back_text = font.render("Back", True, white)
    back_rect = pygame.Rect(450, 550, 100, 46)  # Position the button

    # Initialize message display variables
    feedback_message = ""
    message_timer = 0  # Timer for message duration (in frames)

    # Running flag
    running = True

    while running:
        screen.fill(deep_black)
        mouse = pygame.mouse.get_pos()  # Get mouse position

        # Render title
        title_text = title_font.render("SHOP", True, yellow)
        screen.blit(title_text, (430, 20))

        # Render shop items
        for i, item in enumerate(shop_items):
            card_rect = pygame.Rect(100, 100 + i * 110, 800, 90)
            if card_rect.collidepoint(mouse):
                pygame.draw.rect(screen, card_highlight, card_rect, border_radius=10)
            else:
                pygame.draw.rect(screen, card_color, card_rect, border_radius=10)

            item_text = font.render(f"{item['name']} - {item['cost']} coins", True, white)
            screen.blit(item_text, (120, 120 + i * 110))  # Render item text with spacing

        # Render back button
        if back_rect.collidepoint(mouse):
            pygame.draw.rect(screen, back_hover, back_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, back_color, back_rect, border_radius=10)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        # Show feedback message if any
        if message_timer > 0:
            feedback_text = font.render(feedback_message, True, white)
            feedback_text_rect = feedback_text.get_rect(center=(500, 75))
            screen.blit(feedback_text, feedback_text_rect)
            message_timer -= 1  # Decrease timer

        pygame.display.flip()  # Update the screen
        clock.tick(fps)  # Maintain frame rate

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
                        if character.coins >= item["cost"]:
                            character.coins -= item["cost"]
                            item["action"]()  # Apply the item's effect
                            feedback_message = f"Purchased {item['name']}!"
                            message_timer = 120  # Display message for 120 frames (~2 seconds at 60 FPS)
                        else:
                            feedback_message = "Not enough coins!"
                            message_timer = 120  # Display message for 120 frames (~2 seconds at 60 FPS)
