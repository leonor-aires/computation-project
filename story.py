import pygame
from config import *
from music import play_background_music

def typewriter_effect_wrapped(screen, text, font, color, rect, speed=25):
    """
    Display text letter by letter with word wrapping inside a rectangle.
    When the text is fully displayed, show a semi-transparent rectangle.

    Parameters
    ----------
    screen : pygame.Surface
        The surface where the text will appear.
    text : str
        The text content to be displayed.
    font : pygame.font.Font
        The font used for the text.
    color : tuple of int
        The color of the text.
    rect : pygame.Rect
        The rectangle area within which the text should be displayed.
    speed : int, optional
        The delay in milliseconds between displaying each character (default is 25).

    Returns
    -------
    The fully displayed text content.
    """
    words = text.split()
    lines = []
    current_line = ""

    # Build lines that fit within the width of the rectangle
    for word in words:
        test_line = current_line + word + " "
        line_width, _ = font.size(test_line)
        if line_width > rect.width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line
    lines.append(current_line)  # Add the last line

    # Display text letter by letter
    y = rect.top
    displayed_text = "" # Reset displayed text
    screen_copy = screen.copy()  # Copy the screen before typing starts
    for line in lines:
        current_line_text = ""  # Track the current line being typed
        for char in line:
            current_line_text += char
            displayed_text += char
            screen.blit(screen_copy, (0, 0))  # Restore background
            # Render all text typed so far
            current_y = y
            for displayed_line in displayed_text.splitlines():
                rendered_line = font.render(displayed_line, True, color)
                screen.blit(rendered_line, (rect.left, current_y))
                current_y += font.get_linesize()
            pygame.display.flip()
            pygame.time.delay(speed)
        displayed_text += "\n"  # Move to the next line
        y += font.get_linesize()

    # Draw semi-transparent rectangle after all text is displayed
    transparent_rect = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    transparent_rect.fill((0, 0, 0, 150))  # Semi-transparent black
    screen.blit(transparent_rect, (rect.left, rect.top))

    # Re-render full text over the rectangle
    y = rect.top
    for line in lines:
        rendered_line = font.render(line, True, color)
        screen.blit(rendered_line, (rect.left, y))
        y += font.get_linesize()

    pygame.display.flip()
    return displayed_text  # Return the full text to keep it visible


def display_story_with_buttons(screen, return_to_menu):
    """
    Displays the game's backstory screen with buttons for navigation and skipping.

    Parameters
    ----------
    screen : pygame.Surface
        The surface on which the story slides will be displayed.
    """
    pygame.init()
    font = pygame.font.SysFont("Corbel", 25)
    button_font = pygame.font.SysFont("Corbel", 20)

    # Define the story text and corresponding image files
    story_slides = [
        ("", "backstory images/title slide 2.png"),
        ("Tomatio grew up on a peaceful farm with other tomatoes, enjoying the warm sun and gentle breeze.",
         "backstory images/Slide 2 .png"),
        ("One day, Tomatio was taken to the factory where tomatoes are turned into ketchup. But Tomatio wasn’t ready to give up his life so easily!",
         "backstory images/Slide 3.webp"),
        ("In the factory, Tomatio discovered that the ketchup bottles had come to life and wanted him to join them. But Tomatio decided to fight back!",
         "backstory images/Slide 4.webp"),
        ("Tomatio must jump, dodge, and fight to make his way out of the factory. Will he escape, or will he become ketchup?",
         "backstory images/Slide 5.webp"),
    ]

    # Play background music
    play_background_music("Music/soundtrack_story.mp3")

    running = True
    slide_index = 0
    previous_slide_index = None
    displayed_text = "" # Initialize displayed text

    while running:
        screen.fill((0, 0, 0))  # Black background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if "Next" or "Back" button is clicked
                if 820 <= mouse_pos[0] <= 920 and 540 <= mouse_pos[1] <= 580:
                    if slide_index < len(story_slides) - 1:  # Not the last slide
                        slide_index += 1
                    else:  # Last slide
                        return_to_menu(screen)  # Exit story loop to trigger return_to_menu
                        return
                # Check if "Skip" button is clicked
                if 20 <= mouse_pos[0] <= 120 and 540 <= mouse_pos[1] <= 580:
                    return_to_menu(screen) # Immediately go to the menu
                    return

            if event.type == pygame.KEYDOWN:
                # Skip story with Enter key
                if event.key == pygame.K_RETURN:
                    return_to_menu(screen)
                    return
                # Navigate forward with Right arrow
                if event.key == pygame.K_RIGHT:
                    slide_index += 1
                    if slide_index >= len(story_slides):  # Ensure bounds
                        slide_index = len(story_slides) - 1
                # Navigate backward with Left Arrow
                if event.key == pygame.K_LEFT:
                    slide_index -= 1
                    if slide_index < 0:
                        slide_index = 0 # Stay on first slide

        if slide_index < len(story_slides) - 1:
            # Load the current slide
            text, image_file = story_slides[slide_index]
            image = pygame.image.load(image_file)
            image = pygame.transform.scale(image, (1000, 600))  # Scale to fit the screen

            # Display the image
            screen.blit(image, (0, 0))

            # First slide: Skip rectangle and text rendering
            if slide_index == 0:
                pass  # Nothing extra needed for the first slide
            else:
                # Render the text with a typewriter effect
                text_rect = pygame.Rect(50, height - 120, 900, 100)  # Adjusted position (slightly lower)
                if previous_slide_index != slide_index:
                    displayed_text = typewriter_effect_wrapped(screen, text, font, (255, 255, 255), text_rect, speed=30)
                    previous_slide_index = slide_index  # Track the current slide index
                else:
                    # Keep rectangle and fully displayed text visible
                    transparent_rect = pygame.Surface((text_rect.width, text_rect.height), pygame.SRCALPHA)
                    transparent_rect.fill((0, 0, 0, 150))  # Semi-transparent rectangle
                    screen.blit(transparent_rect, (text_rect.left, text_rect.top))
                    render_wrapped_text(screen, displayed_text, font, (255, 255, 255), text_rect)

            # Add "Next"
            mouse_pos = pygame.mouse.get_pos()
            button_text = "Next >"
            button_color = (200, 200, 200) if 820 <= mouse_pos[0] <= 920 and 540 <= mouse_pos[1] <= 580 else (150, 150, 150)
            pygame.draw.rect(screen, button_color, [820, 540, 100, 40])  # Button background
            button_label = button_font.render(button_text, True, (0, 0, 0))
            button_rect = button_label.get_rect(center=(870, 560))
            screen.blit(button_label, button_rect)

            # Add "Skip" button with hover effect
            skip_button_color = (200, 50, 50) if 20 <= mouse_pos[0] <= 120 and 540 <= mouse_pos[1] <= 580 else (150, 50, 50)
            pygame.draw.rect(screen, skip_button_color, [20, 540, 100, 40])  # Button background
            skip_button_text = button_font.render("Skip", True, (255, 255, 255))
            skip_button_rect = skip_button_text.get_rect(center=(70, 560))
            screen.blit(skip_button_text, skip_button_rect)

            # Add Enter key hint
            hint_text = button_font.render("Press Enter to skip story", True, (255, 255, 255))
            hint_text_rect = hint_text.get_rect(center=(width // 2, height - 30))
            screen.blit(hint_text, hint_text_rect)

        elif slide_index == len(story_slides) - 1:
            # Load the current slide
            text, image_file = story_slides[slide_index]
            image = pygame.image.load(image_file)
            image = pygame.transform.scale(image, (1000, 600))  # Scale to fit the screen

            # Display the image
            screen.blit(image, (0, 0))

            # Display the text with typewriter effect inside limits
            text_rect = pygame.Rect(50, height - 120, 900, 100)  # Position lower on the screen
            if previous_slide_index != slide_index:
                displayed_text = typewriter_effect_wrapped(screen, text, font, (255, 255, 255), text_rect, speed=30)
                previous_slide_index = slide_index
            else:
                # Keep rectangle and fully displayed text visible
                transparent_rect = pygame.Surface((text_rect.width, text_rect.height), pygame.SRCALPHA)
                transparent_rect.fill((0, 0, 0, 150))
                screen.blit(transparent_rect, (text_rect.left, text_rect.top))
                render_wrapped_text(screen, displayed_text, font, (255, 255, 255), text_rect)

            # Back button
            mouse_pos = pygame.mouse.get_pos()
            button_text = "Back"
            button_color = (200, 200, 200) if 820 <= mouse_pos[0] <= 920 and 540 <= mouse_pos[1] <= 580 else (
            150, 150, 150)
            pygame.draw.rect(screen, button_color, [820, 540, 100, 40])  # Button background
            button_label = button_font.render(button_text, True, (0, 0, 0))
            button_rect = button_label.get_rect(center=(870, 560))
            screen.blit(button_label, button_rect)

        pygame.display.flip()

    # Stop background music
    pygame.mixer.music.stop()

# Function to wrap text so that it stays within a specific rectangle
def render_wrapped_text(screen, text, font, color, rect):
    """
    Render text with word wrapping inside a rectangle.

    Parameters
    ----------
    screen : pygame.Surface
        The surface where the text will be rendered.
    text : str
        The text content to be displayed.
    font : pygame.font.Font
        The font used for rendering text.
    color : tuple of int
        The color of the text.
    rect : pygame.Rect
        The rectangle area within which the text should be displayed.
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        line_width, _ = font.size(test_line)
        if line_width > rect.width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line
    lines.append(current_line)

    # Draw each line
    y = rect.top
    for line in lines:
        rendered_line = font.render(line, True, color)
        screen.blit(rendered_line, (rect.left, y))
        y += font.get_linesize()

def start_game_with_story(screen, return_to_menu):
    """
    Main function to start the game with a backstory, images, and transitions.

    Parameters
    ----------
    screen : pygame.Surface
        The screen on which the story and the game will be displayed.
    """
    # screen = pygame.display.set_mode(resolution)
    display_story_with_buttons(screen, return_to_menu)
