import pygame
from config import resolution, white, grey, light_grey, deep_black


def draw_controls(screen, font):
    key_width, key_height = 50, 50
    spacing = 10

    # W Key Position (Top Center)
    w_x, w_y = 500, 375

    # A, D Key Positions (Bottom Left and Right)
    a_x, a_y = w_x - key_width - spacing, w_y + key_height + spacing
    d_x, d_y = w_x + key_width + spacing, w_y + key_height + spacing

    # Fonts for labels
    small_font = pygame.font.SysFont("Arial", 25, bold = True)
    title_font = pygame.font.Font(None, 60)
    # Controls Text
    controls_text = title_font.render("Controls", True, deep_black)
    screen.blit(controls_text, (445, 300))

    # Draw W Key
    pygame.draw.rect(screen, light_grey, (w_x, w_y, key_width, key_height))
    #pygame.draw.rect(screen, deep_black, (w_x, w_y, key_width, key_height), 2)
    w_text = font.render("W", True, deep_black)
    screen.blit(w_text, (w_x + 5, w_y +3))
    jump_text = small_font.render("Jump", True, deep_black)
    screen.blit(jump_text, (w_x + 0, w_y - 30))

    # Draw A Key
    pygame.draw.rect(screen, light_grey, (a_x, a_y, key_width, key_height))
    #pygame.draw.rect(screen, deep_black, (a_x, a_y, key_width, key_height), 2)
    a_text = font.render("A", True, deep_black)
    screen.blit(a_text, (a_x + 10, a_y + 3))
    left_text = small_font.render("Left", True, deep_black)
    screen.blit(left_text, (a_x + 5, a_y + key_height + 2))

    # Draw D Key
    pygame.draw.rect(screen, light_grey, (d_x, d_y, key_width, key_height))
    #pygame.draw.rect(screen, deep_black, (d_x, d_y, key_width, key_height), 2)
    d_text = font.render("D", True, deep_black)
    screen.blit(d_text, (d_x + 10, d_y + 3))
    right_text = small_font.render("Right", True,deep_black)
    screen.blit(right_text, (d_x + 3, d_y + key_height + 2))

    mouse_image = pygame.image.load("characters images/right click (1).png")
    mouse_image = pygame.transform.scale(mouse_image, (80, 90))
    screen.blit(mouse_image, (640, 410))
    mouse_text = small_font.render("Shoot", True, deep_black)
    screen.blit(mouse_text, (653, 388))

def draw_popup(screen, title, explanation):
    popup_width, popup_height = 500, 300
    popup_x = (resolution[0] - popup_width) // 2
    popup_y = (resolution[1] - popup_height) // 2

    # Draw the popup window
    pygame.draw.rect(screen, light_grey, (popup_x, popup_y, popup_width, popup_height), border_radius=10)
    pygame.draw.rect(screen, deep_black, (popup_x, popup_y, popup_width, popup_height), 3,  border_radius=10)

    # Title and explanation text
    title_font = pygame.font.SysFont("Corbel", 50, bold=True)
    explanation_font = pygame.font.SysFont("Arial", 25)

    title_text = title_font.render(title, True, deep_black)
    explanation_text = explanation_font.render(explanation, True, deep_black)

    screen.blit(title_text, (popup_x + 20, popup_y + 30))
    screen.blit(explanation_text, (popup_x + 20, popup_y + 100))

    # Back button
    close_button_color = grey
    close_rect = pygame.Rect(popup_x + popup_width - 80, popup_y + 20, 60, 40)
    pygame.draw.rect(screen, close_button_color, close_rect, border_radius=5)
    close_text = explanation_font.render("Back", True, white)
    screen.blit(close_text, (popup_x + popup_width - 75, popup_y + 25))

    return close_rect

def show_rules(screen, font, images, invencibility=None):
    """Displays the game rules on the screen."""

    # Main loop for Rules screen
    running = True
    popup_open = None  # Tracks which popup is active
    clock = pygame.time.Clock()

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Back button coordinates
                mouse = pygame.mouse.get_pos()
                if 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80:  # Back button area
                    running = False
                # Clicks on power-ups
                elif 135 <= mouse[0] <= 400 and 175 <= mouse[1] <= 210:
                    popup_open = ("Invincibility", "Tomátio doesn't lose health for 5 seconds")
                elif 135 <= mouse[0] <= 400 and 275 <= mouse[1] <= 310:
                    popup_open = ("Despawner", "A random number of enemies disappears")
                elif 135 <= mouse[0] <= 400 and 375 <= mouse[1] <= 410:
                    popup_open = ("Tomato Coin", "2x the amount of coins you receive when an enemy is killed")
                elif 135 <= mouse[0] <= 400 and 475 <= mouse[1] <= 510:
                    popup_open = ("Rapid Blast", "Constant shooting")
                elif 535 <= mouse[0] <= 830 and 165 <= mouse[1] <= 195:
                    popup_open = ("Treasure Chests", "Choose 1 of 3 rewards available")

                # Close popup
                if popup_open:
                    close_rect = draw_popup(screen, *popup_open)
                    if close_rect.collidepoint(mouse):
                        popup_open = None

        # Capture mouse position for hover effect
        mouse = pygame.mouse.get_pos()

        screen.fill((0, 0, 0))

        # Fonts
        small_font = pygame.font.SysFont("Arial", 25, bold=True)
        title_font = pygame.font.Font(None, 60)
        title_font_else = pygame.font.Font(None, 90)
        explain_font = pygame.font.Font(None, 20)
        corbel_font = pygame.font.SysFont("Corbel", 40, bold=True)

        # Images
        background_image = pygame.image.load("backgrounds/game.webp")
        background_image = pygame.transform.scale(background_image, resolution)
        screen.blit(background_image, (0, 0))



        # Chests
        chest_image = pygame.image.load("Chest Images/chest.png")
        chest_image = pygame.transform.scale(chest_image, (100, 100))
        screen.blit(chest_image, (450, 135))
        chest_text = corbel_font.render("Treasure Chests", True, white)
        chest_text_rect = chest_text.get_rect(topleft=(555, 175))
        #pygame.draw.rect(screen, grey, chest_text_rect.inflate(20, 10), border_radius=10)
        chest_hover = 535<= mouse[0] <= 735 and 165 <= mouse[1] <= 215
        chest_color = light_grey if chest_hover else grey
        pygame.draw.rect(screen, chest_color, chest_text_rect.inflate(20, 10), border_radius=10)
        screen.blit(chest_text, chest_text_rect.topleft)


        # POWER UPS
        powerups_text = title_font.render("Power-Ups", True, deep_black)
        screen.blit(powerups_text, (40, 100))

        invincibility = pygame.image.load("characters images/Shield 1.png")
        invincibility = pygame.transform.scale(invincibility, (80, 80))
        screen.blit(invincibility, (30, 150))
        invincibility_text = corbel_font.render("Invincibility", True, white)
        invincibility_text_rect = invincibility_text.get_rect(topleft=(135, 175))
        invincibility_hover = 115 <= mouse[0] <= 255 and 165 <= mouse[1] <= 205  # Adjust based on inflated rect
        invincibility_color = light_grey if invincibility_hover else grey
        pygame.draw.rect(screen, invincibility_color, invincibility_text_rect.inflate(20, 10), border_radius=10)
        screen.blit(invincibility_text, invincibility_text_rect.topleft)

        despawner = pygame.image.load("characters images/despawner.png")
        despawner = pygame.transform.scale(despawner, (80, 80))
        screen.blit(despawner, (30, 250))
        despawner_text = corbel_font.render("Despawner", True, white)
        despawner_text_rect = despawner_text.get_rect(topleft=(135, 275))
        despawner_hover = 115 <= mouse[0] <= 255 and 265 <= mouse[1] <= 305
        despawner_color = light_grey if despawner_hover else grey
        pygame.draw.rect(screen, despawner_color, despawner_text_rect.inflate(20, 10), border_radius=10)
        screen.blit(despawner_text, despawner_text_rect.topleft)


        tomato_coin = pygame.image.load("characters images/Tomato coin.png")
        tomato_coin = pygame.transform.scale(tomato_coin, (80, 80))
        screen.blit(tomato_coin, (30, 350))
        tomato_coin_text = corbel_font.render("Tomato Coin", True, white)
        tomato_coin_text_rect = tomato_coin_text.get_rect(topleft=(135, 375))
        tomato_coin_hover = 115 <= mouse[0] <= 255 and 365 <= mouse[1] <= 405
        tomato_coin_color = light_grey if tomato_coin_hover else grey
        pygame.draw.rect(screen, tomato_coin_color, tomato_coin_text_rect.inflate(20, 10), border_radius=10)
        screen.blit(tomato_coin_text, tomato_coin_text_rect.topleft)

        rapid_blast = pygame.image.load("characters images/rapid_blaster1.png")
        rapid_blast = pygame.transform.scale(rapid_blast, (100, 100))
        screen.blit(rapid_blast, (20, 450))
        rapid_blast_text = corbel_font.render("Rapid Blast", True, white)
        rapid_blast_text_rect = rapid_blast_text.get_rect(topleft=(135, 475))
        rapid_blast_hover = 115 <= mouse[0] <= 255 and 465 <= mouse[1] <= 505
        rapid_blast_color = light_grey if rapid_blast_hover else grey
        pygame.draw.rect(screen, rapid_blast_color, rapid_blast_text_rect.inflate(20, 10), border_radius=10)
        screen.blit(rapid_blast_text, rapid_blast_text_rect.topleft)

        draw_controls(screen, font)

        # Render the rules text
        rules_title = title_font_else.render("Game Rules", True, (255, 255, 255))
        screen.blit(rules_title, (320, 25))

        # Back Button
        back_hover = 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80
        button_color = light_grey if back_hover else grey  # Change color on hover
        pygame.draw.rect(screen, button_color, pygame.Rect(20, 20, 140, 60),
                         border_radius=10)  # Rectangle for the button
        back_text = corbel_font.render("Back", True, white)
        back_rect = back_text.get_rect(center=(90, 50))  # Centered within the rectangle
        screen.blit(back_text, back_rect)

        if popup_open:
            draw_popup(screen, *popup_open)

        # Update the display
        pygame.display.update()
        clock.tick(60)
