import pygame
from config import resolution, dark_red, deep_black, white, fps, light_grey, grey

def show_options(screen):
    """
    Display the options menu with the volume slider

    Parameters
    ----------
    Screen: pygame.Surface
        The pygame display surface.
    """

    # Image Background
    background_image = pygame.image.load("backgrounds/game.webp")
    background_image = pygame.transform.scale(background_image, resolution)

    # Music Volume, Sound Effects Volume and Brightness variables
    music_volume = pygame.mixer.music.get_volume()  # Current music volume

    # Adjust the initial position of the slider to start at 400
    slider_x_music = 400 + int(music_volume * 200)  # Updated initial slider position
    slider_y_music = 300  # Fixed Y position for the music slider
    slider_width = 200  # Width of the slider bar
    slider_height = 15  # Height of the slider bar
    thumb_width = 15  # Width of the slider thumb

    # Main loop for options screen
    running = True
    dragging_music = False  # Keeps track of whether the slider thumb is being dragged

    # For managing frame rate
    clock = pygame.time.Clock()

    while running:
        # Initialize mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position

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

                # Check for Back button click
                if (20 <= mouse_x <= 160) and (20 <= mouse_y <= 80):
                    running = False  # Exit options menu to go back

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_music = False

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Update mouse position

                if dragging_music:
                    slider_x_music = max(400, min(600, mouse_x))  # Updated min/max values for the slider
                    music_volume = (slider_x_music - 400) / 200  # Adjusted based on new starting point
                    pygame.mixer.music.set_volume(music_volume)

        # Draw the option menu background
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Fonts for text
        title_font = pygame.font.Font(None, 90)
        explain_font = pygame.font.Font(None, 50)
        bold_explain_font = pygame.font.Font(None, 50)  # Bold font for "Back" text
        bold_explain_font.set_bold(True)
        corbel_font = pygame.font.SysFont("Corbel", 40, bold=True)

        # Draw title
        title_text = title_font.render("Options", True, deep_black)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw the volume slider
        pygame.draw.rect(screen, deep_black, (400, slider_y_music, slider_width, slider_height))  # Updated x position
        pygame.draw.circle(screen, (255, 0, 0), (slider_x_music, slider_y_music + slider_height // 2),
                           thumb_width // 2)  # Thumb

        # Volume text
        volume_text = explain_font.render(f"Volume: {int(music_volume * 100)}%", True, deep_black)
        volume_rect = volume_text.get_rect(center=(screen.get_width() // 2, slider_y_music - 40))
        screen.blit(volume_text, volume_rect)

        # Back Button
        back_hover = 20 <= mouse_x <= 160 and 20 <= mouse_y <= 80
        button_color = light_grey if back_hover else grey  # Change color on hover
        pygame.draw.rect(screen, button_color, pygame.Rect(20, 20, 140, 60),
                         border_radius=10)  # Rectangle for the button

        back_text = corbel_font.render("Back", True, white)
        back_rect = back_text.get_rect(center=(90, 50))  # Centered within the rectangle
        screen.blit(back_text, back_rect)

        # Update display
        pygame.display.update()
        clock.tick(fps)



