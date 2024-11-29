import pygame

def show_rules(screen, font, images):
    """Displays the game rules on the screen."""
    # Main loop for Rules screen
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Back button coordinates
                mouse = pygame.mouse.get_pos()
                if 20 <= mouse[0] <= 20+140 and 20 <= mouse[1] <= 20+60:  # Back button area
                    running = False

        # Background for Rules screen
        screen.fill((0, 0, 0))  # Black background

        # Sizes
        title_font = pygame.font.Font(None, 90)
        explain_font = pygame.font.Font(None, 20)

        # Render the rules text
        rules_title = title_font.render("Game Rules", True, (255, 255, 255))
        powerups = font.render("Power-Ups", True, (255, 255, 255))
        chests = font.render("Chests", True, (255, 255, 255))
        movements = font.render("Movements", True, (255, 255, 255))


        # Blit rules text onto the screen
        screen.blit(rules_title, (320, 25))
        screen.blit(powerups, (40, 90))
        screen.blit(chests, (40, 280))
        screen.blit(movements, (40, 450))

        # POWER UPS
        powerup_keys = ["powerup1", "powerup2", "powerup3", "powerup4"]
        powerup_names = [
            "Invincibility",
            "Despawner",
            "Deadly Fire",
            "Crazy Fire"
        ]

        start_x = 100  # Starting x position for power-ups
        start_y = 130  # Starting y position for power-ups
        spacing_x = 250  # Space between power-up images

        # Blit power-up images and names
        for i, key in enumerate(powerup_keys):
            if key in images:  # Check if the image exists
                # Draw the power-up image
                screen.blit(images[key], (start_x + i * spacing_x, start_y))

                # Render the power-up name below the image
                powerup_text = font.render(powerup_names[i], True, (255, 255, 255))
                # Offset for text below the image
                screen.blit(powerup_text, ((start_x-25) + i * spacing_x, start_y + 90))

        # Explanation of the powerups below the powerup names
        explain_powerup1 = explain_font.render("Dragon doesn't loose health", True, (255, 255, 255))
        explain_powerup2 = explain_font.render("Freezes enemies for a period of time", True, (255, 255, 255))
        explain_powerup3 = explain_font.render("Blue fire causes +1 the damage", True, (255, 255, 255))
        explain_powerup4 = explain_font.render("Bigger fire", True, (255, 255, 255))
        # Position the explanation texts
        screen.blit(explain_powerup1, (start_x-45, start_y+120))
        screen.blit(explain_powerup2, (start_x+180, start_y+120))
        screen.blit(explain_powerup3, (start_x+450, start_y+120))
        screen.blit(explain_powerup4, (start_x+750, start_y+120))

        # CHESTS
        chest_keys = ["chest1", "chest2", "chest3", "chest4"]
        chest_names = [
            "Yellow",
            "Green",
            "Blue",
            "Pink"
        ]
        # Starting positions for chest
        chest_start_x = 100  # Starting x position for power-ups
        chest_start_y= 315  # Starting y position for power-ups
        chest_spacing_x = 250  # Space between power-up images

        # Blit chests images and names
        for i, key in enumerate(chest_keys):
            if key in images:  # Check if the image exists
                # Draw the power-up image
                screen.blit(images[key], (chest_start_x + i * chest_spacing_x, chest_start_y))
                # Render chest names below chest image
                chests_text = font.render(chest_names[i], True, (255, 255, 255))
                screen.blit(chests_text, ((chest_start_x+7) + i * chest_spacing_x, chest_start_y + 90))


        # MOVEMENTS
        # Movement keys and their positions
        movement_keys = [
            {"text": "W", "x": 300, "y": 470},  # W key position
            {"text": "A", "x": 240, "y": 530},  # A key position
            {"text": "S", "x": 300, "y": 530},  # S key position
            {"text": "D", "x": 360, "y": 530},  # D key position
        ]
        # Size of each key (rectangle)
        key_width, key_height = 50, 50
        # Loop through each key to render them
        for key in movement_keys:
            # Draw a white rectangle for the key
            pygame.draw.rect(screen, (255, 255, 255), (key["x"], key["y"], key_width, key_height))

            # Draw a black border around the rectangle
            pygame.draw.rect(screen, (0, 0, 0), (key["x"], key["y"], key_width, key_height), 2)

            # Render the key text
            movement_text = font.render(key["text"], True, (0, 0, 0))  # Black text

            # Center the text inside the rectangle
            text_x = key["x"] + key_width // 2
            text_y = key["y"] + key_height // 2
            text_rect = movement_text.get_rect(center=(text_x, text_y))

            # Blit the text onto the screen
            screen.blit(movement_text, text_rect)











        # Draw a back button [x, y, width, height]
        #pygame.draw.rect(screen, (255, 0, 0), [20, 20, 140, 60])  # Red back button
        back_text = font.render("Back", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 20 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Update the display
        pygame.display.update()


