import pygame
from config import *


def shop(screen, character):
    font = pygame.font.SysFont("Corbel", 50)
    clock = pygame.time.Clock()

    # Define shop items
    shop_items = [
        {"name": "Health Potion", "cost": 20, "action": lambda: setattr(character, 'health', character.max_health)},
        {"name": "Speed Boost", "cost": 50, "action": lambda: setattr(character, 'speed', character.speed + 1)},
    ]

    # Fonts for text
    corbel_font = pygame.font.SysFont("Corbel", 50)

    # Text for the back button
    back_text = corbel_font.render("Back", True, white)

    # Running flag
    running = True

    while running:
        screen.fill((50, 50, 50))  # Background color
        mouse = pygame.mouse.get_pos()  # Get mouse position

        # Render shop items
        for i, item in enumerate(shop_items):
            pygame.draw.rect(screen, green, (100, 100 + i * 100, 300, 80))  # Item boxes
            text = font.render(f"{item['name']} - {item['cost']} coins", True, white)
            screen.blit(text, (110, 110 + i * 100))  # Item text

        # Draw the back button
        pygame.draw.rect(screen, dark_red, [430, 540, 140, 60])  # Button box
        back_rect = back_text.get_rect(center=(500, 570))  # Center the text in the button
        screen.blit(back_text, back_rect)  # Render the text

        pygame.display.flip()  # Update the screen
        clock.tick(fps)  # Maintain frame rate

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if "back" button is clicked
                if 430 <= mouse[0] <= 570 and 540 <= mouse[1] <= 600:
                    return  # Exit the shop

                # Check if a shop item is clicked
                for i, item in enumerate(shop_items):
                    if pygame.Rect(100, 100 + i * 100, 300, 80).collidepoint(mouse):
                        if character.coins >= item["cost"]:
                            character.coins -= item["cost"]
                            item["action"]()  # Apply the item's effect
                        else:
                            print("Not enough coins!")  # Debug or feedback for insufficient funds

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Exit the shop with ESC key
