import pygame
from config import resolution, white, deep_black, dark_red

def credits_(screen):
    #screen = pygame.display.set_mode(resolution)
    # fonts
    comicsans_font = pygame.font.SysFont("Comic Sans MS", 25)
    corbel_font = pygame.font.SysFont("Corbel", 50)

    # text
    leonor = comicsans_font.render("Leonor Aires, 20231654@novaims.unl.pt", True, white)
    constanca = comicsans_font.render("Constança Fernandes, 20231685@novaims.unl.pt", True, white)
    marta = comicsans_font.render("Marta Soares, 20231640@novaims.unl.pt", True, white)

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
        screen.fill(deep_black)

        # display text
        screen.blit(constanca, (250, 200))
        screen.blit(leonor, (250, 225))
        screen.blit(marta, (250, 250))

        # draw a back button [x, y, width, height]
        back_text = corbel_font.render("    back", True, white)
        back_rect = back_text.get_rect(center=(20 + 140 // 2, 20 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Update the screen
        pygame.display.update()
