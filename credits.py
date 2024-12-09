import pygame
from config import resolution, white, deep_black, dark_red, grey, light_grey

def credits_(screen):
    # fonts
    comicsans_font = pygame.font.SysFont("Comic Sans MS", 40)
    corbel_font = pygame.font.SysFont("Corbel", 50, bold=True)

    background_image = pygame.image.load("backstory images/credits image.png")
    background_image = pygame.transform.scale(background_image, resolution)  # Scale the image to match the screen resolution

    # text
    leonor = comicsans_font.render("Leonor Aires", True, deep_black)
    constanca = comicsans_font.render("Constança Fernandes", True, deep_black)
    marta = comicsans_font.render("Marta Soares", True, deep_black)
    #leonor:20231654@novaims.unl.pt / constanca: 20231685@novaims.unl.pt / marta:20231640@novaims.unl.pt


    running = True
    # main game loop
    while running:
        # mouse information
        mouse = pygame.mouse.get_pos()

        # check for events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Clear the screen before exiting
                pygame.display.update()
                if 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80:
                    running = False

        # background
        screen.blit(background_image, (0, 0))

        # display text
        screen.blit(constanca, (335, 25))
        screen.blit(leonor, (335, 75))
        screen.blit(marta,(335, 125))

        back_hover = 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 80
        button_color = light_grey if back_hover else grey  # Change color on hover

        pygame.draw.rect(screen, button_color, pygame.Rect(20, 20, 140, 60), border_radius=10)  # Rectangle for the button
        # pygame.draw.rect(screen,deep_black,pygame.Rect(20,20,140,60),width=2,border_radius=10)#Border

        # draw a back button [x, y, width, height]
        back_text = corbel_font.render("    back", True, deep_black)
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 20 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Update the screen
        pygame.display.update()
