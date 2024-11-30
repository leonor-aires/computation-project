import pygame
def show_options(screen):
    """
    Display the options menu with the volume slider
    :param screen: The pygame display surface.
    """
    # Volume variables
    volume = pygame.mixer.music.get_volume()
    slider_x = 300 + int(volume * 200)  # Calculate slider thumb position based on volume
    slider_y = 300  # Fixed Y position for the slider
    slider_width = 200  # Width of the slider bar
    slider_height = 10  # Height of the slider bar
    thumb_width = 15  # Width of the slider thumb

    # Main loop for options screen
    running = True
    dragging = False # Keeps track of whether the slider thumb is being dragged
    while running:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the mouse is clicking the slider thumb
                if (slider_x - thumb_width // 2 <= mouse_x <= slider_x + thumb_width // 2 and slider_y - 10 <= mouse_y <= slider_y + 10):
                    # Enables dragging of volume
                    dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                # Move the slider thumb only horizontally within the bar
                mouse_x, _ = pygame.mouse.get_pos()  # Clamp between 300 and 500
                slider_x = max(300, min(500, mouse_x))

                # Update volume basd based on slider position
                # Normalize position (0 to 1)
                volume = (slider_x - 300) / 200
                pygame.mixer.music.set_volume(volume)

        # Draw the option menu background
        screen.fill((30, 30, 30)) # Dark gray

        # Fonts for text
        title_font = pygame.font.Font(None, 90)
        explain_font = pygame.font.Font(None, 30)

        # Draw title
        title_text = title_font.render("Options", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw the volume slider
        pygame.draw.rect(screen, (200, 200, 200), (300, slider_y, slider_width, slider_height))  # Slider bar
        pygame.draw.circle(screen, (255, 0, 0), (slider_x, slider_y + slider_height // 2), thumb_width // 2)  # Thumb

        # Volume text
        volume_text = explain_font.render(f"Volume: {int(volume * 100)}%", True, (255, 255, 255))
        volume_rect = volume_text.get_rect(center=(screen.get_width() // 2, slider_y - 40))
        screen.blit(volume_text, volume_rect)

        # Draw a "Back" button
        pygame.draw.rect(screen, (255, 0, 0), (20, 20, 140, 60))  # Red back button
        back_text = explain_font.render("Back", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 20 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Check for back button click
        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Left mouse click
            if 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80:
                running = False  # Exit options menu

        # Update display
        pygame.display.update()
