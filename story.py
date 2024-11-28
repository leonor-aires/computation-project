import pygame
from config import *
from game import execute_game, game_loop
from player import Player
from character import Character

def typewriter_effect(screen, text, font, color, position, speed=25):
    """
    Display text one letter at a time on the screen.
    """
    displayed_text = ""
    for char in text:
        displayed_text += char
        rendered_text = font.render(displayed_text, True, color)
        screen.blit(rendered_text, position)
        pygame.display.flip()
        pygame.time.delay(speed)
    return displayed_text  # Return the full text to keep it visible

def play_background_music(music_file):
    """
    Play background music for the story.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(0.5)  # Adjust volume as needed
    pygame.mixer.music.play(-1)  # Loop indefinitely

def display_story_with_buttons(screen):
    """
    Displays the game's backstory screen with buttons for navigation and skipping.
    """
    pygame.init()
    font = pygame.font.SysFont("Corbel", 25)
    button_font = pygame.font.SysFont("Corbel", 20)

    # Define the story text and corresponding image files
    story_slides = [
        ("Long ago, dragons roamed the skies, acting as ancient guardians of the natural world.",
         "backstory images/slide 1.jpeg"),
        ("They maintained the delicate balance of nature, ensuring harmony across the land.",
         "backstory images/slide 2.jpeg"),
        ("But as humans expanded, their greed for power and resources knew no bounds.", "backstory images/slide 3.jpeg"),
        ("Led by a ruthless king, they began hunting the dragons, seeking their magical powers.",
         "backstory images/slide 4.jpeg"),
        ("One by one, the dragons fell, their magic stolen to fuel the king’s dark ambitions.",
         "backstory images/slide 5.jpeg"),
        ("Now, only one dragon remains: Vermax, the last of the ancient guardians.", "backstory images/slide 6.jpeg"),
        ("The humans have fortified their stronghold, draining the last remnants of dragon magic.",
         "backstory images/slide 8.jpeg"),
        ("But Vermax will stop at nothing to end their tyranny and bring harmony back to the world.",
         "backstory images/slide 9.jpeg"),
        ("Your quest begins now. Unleash your fury, reclaim the magic, and save the world!",
         "backstory images/slide 10.jpeg"),
    ]

    # Play background music
    play_background_music("Music/soundtrack_story.mp3")

    running = True
    slide_index = 0

    while running:
        screen.fill((0, 0, 0))  # Black background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if "Next" or "Play" button is clicked
                if 820 <= mouse_pos[0] <= 920 and 540 <= mouse_pos[1] <= 580:
                    if slide_index >= len(story_slides) - 1: # Last slide
                        pygame.mixer.music.stop()
                        running = False  # End story
                        break
                    else:
                        slide_index += 1
                # Check if "Skip" button is clicked
                if 20 <= mouse_pos[0] <= 120 and 540 <= mouse_pos[1] <= 580:
                    running = False  # End story
                    break
            if event.type == pygame.KEYDOWN:
                # Skip story with Enter key
                if event.key == pygame.K_RETURN:
                    running = False
                    break
                # Navigate forward with Right arrow
                if event.key == pygame.K_RIGHT:
                    slide_index += 1
                    if slide_index == len(story_slides) - 1:
                        running = False  # End story and start the game
                        break
                # Navigate backward with Left Arrow
                if event.key == pygame.K_LEFT:
                    slide_index -= 1
                    if slide_index < 0:
                        slide_index = 0 # Stay on first slide

        if slide_index < len(story_slides):
            # Load the current slide
            text, image_file = story_slides[slide_index]
            image = pygame.image.load(image_file)
            image = pygame.transform.scale(image, (width, height))  # Scale to fit the screen

            # Display the image
            screen.blit(image, (0, 0))

            # Render the text with a typewriter effect
            if "displayed_text" not in locals() or slide_index != previous_slide_index:
                displayed_text = typewriter_effect(screen, text, font, (255, 255, 255), (50, height - 100), speed=30)
                previous_slide_index = slide_index  # Track the current slide index
            else:
                rendered_text = font.render(displayed_text, True, (255, 255, 255))
                text_rect = rendered_text.get_rect(center=(width // 2, height - 100))
                screen.blit(rendered_text, text_rect)

            # Add "Next" or "Play" button with hover effect
            mouse_pos = pygame.mouse.get_pos()
            if slide_index == len(story_slides) - 1:  # Last slide
                # Change "Next" button to "Play"
                button_text = "Play"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 820 <= mouse_pos[0] <= 920 and 540 <= mouse_pos[1] <= 580:
                        pygame.mixer.music.stop()  # Stop background music
                        running = False  # Exit story loop and start the game
            else:
                # Regular "Next" button
                button_text = "Next >"
            button_color = (200, 200, 200) if 820 <= mouse_pos[0] <= 920 and 540 <= mouse_pos[1] <= 580 else (
            150, 150, 150)
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

        pygame.display.flip()

    # Stop background music
    pygame.mixer.music.stop()


def start_game_with_story():
    """
    Main function to start the game with a backstory, images, and transitions.
    """
    screen = pygame.display.set_mode(resolution)
    display_story_with_buttons(screen)
    game_loop()  # Directly call the game loop after the story
