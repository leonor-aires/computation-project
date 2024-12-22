import pygame
from config import resolution, dark_red, deep_black, white, fps
def show_options(screen):
    """
    Display the options menu with the volume slider

    Parameters
    ----------
    Screen: pygame.Surface
        The pygame display surface.
    """
    # Music Volume, Sound Effects Volume and Brightness variables
    music_volume = pygame.mixer.music.get_volume()  # Current music volume

    slider_x_music = 300 + int(music_volume * 200)  # Music slider position

    slider_y_music = 300  # Fixed Y position for the music slider
    slider_width = 200  # Width of the slider bar
    slider_height = 10  # Height of the slider bar
    thumb_width = 10  # Width of the slider thumb

    # Main loop for options screen
    running = True
    dragging_music = False  # Keeps track of whether the slider thumb is being dragged

    # For managing frame rate
    clock = pygame.time.Clock()

    while running:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if the mouse is clicking the slider thumb
                if (slider_x_music - thumb_width // 2 <= mouse_x <= slider_x_music + thumb_width // 2
                        and slider_y_music - thumb_width <= mouse_y <= slider_y_music + thumb_width):
                    # Enables dragging of volume
                    dragging_music = True

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_music = False

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, _ = pygame.mouse.get_pos()

                if dragging_music:
                    slider_x_music = max(300, min(500, mouse_x))
                    music_volume = (slider_x_music - 300) / 200
                    pygame.mixer.music.set_volume(music_volume)

        # Draw the option menu background
        screen.fill((30, 30, 30)) # Dark gray

        # Fonts for text
        title_font = pygame.font.Font(None, 90)
        explain_font = pygame.font.Font(None, 30)
        bold_explain_font = pygame.font.Font(None, 50)  # Bold font for "Back" text
        bold_explain_font.set_bold(True)

        # Draw title
        title_text = title_font.render("Options", True, white)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw the volume slider
        pygame.draw.rect(screen, (200, 200, 200), (300, slider_y_music, slider_width, slider_height))  # Slider bar
        pygame.draw.circle(screen, (255, 0, 0), (slider_x_music, slider_y_music + slider_height // 2), thumb_width // 2)  # Thumb

        # Volume text
        volume_text = explain_font.render(f"Volume: {int(music_volume * 100)}%", True, (255, 255, 255))
        volume_rect = volume_text.get_rect(center=(screen.get_width() // 2, slider_y_music - 40))
        screen.blit(volume_text, volume_rect)

        # Draw a "Back" button
        back_text = bold_explain_font.render("Back", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 20 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Check for back button click
        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Left mouse click
            if 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80:
                running = False  # Exit options menu

        # Update display
        pygame.display.update()
        clock.tick(fps)