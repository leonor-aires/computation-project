import pygame
from config import resolution, white, deep_black, grey, light_grey

def credits_(screen):
    """
    Display the credits screen.

    Parameters
    ----------
    screen : pygame.Surface
        The Pygame surface on which the credits will be displayed.

    """

    comicsans_font = pygame.font.SysFont("Comic Sans MS", 40)
    corbel_font = pygame.font.SysFont("Corbel", 40, bold=True)

    # Load and scale background image
    background_image = pygame.image.load("backstory images/credits image.png")
    background_image = pygame.transform.scale(background_image, resolution)

    leonor = comicsans_font.render("Leonor Aires 20231654", True, deep_black)
    constanca = comicsans_font.render("Constança Fernandes 20231685", True, deep_black)
    marta = comicsans_font.render("Marta Soares 20231640", True, deep_black)

    running = True
    while running:
        # Get mouse position
        mouse = pygame.mouse.get_pos()
        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Clear the screen before exiting
                pygame.display.update()
                if 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80:
                    running = False

        # Draw the background
        screen.blit(background_image, (0, 0))

        # Display contributor names
        screen.blit(constanca, (335, 25))
        screen.blit(leonor, (335, 75))
        screen.blit(marta,(335, 125))

        # Back button
        back_hover = 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80
        button_color = light_grey if back_hover else grey
        pygame.draw.rect(screen, button_color, pygame.Rect(20, 20, 140, 60), border_radius=10)

        # Draw a back button [x, y, width, height]
        back_text = corbel_font.render("back", True, white)
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 20 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Update the screen
        pygame.display.update()
