from utils import *  # no need to import pygame because the import is in utils
from character import * # import player
from game import execute_game, game_loop
from utils import under_construction
from story import start_game_with_story


def interface():
    # initiating pygame
    pygame.init()
    pygame.mixer.music.load('Music/music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # creating the screen at the set resolution
    screen = pygame.display.set_mode(resolution)

    # fonts
    corbel_font = pygame.font.SysFont("Corbel", 50)
    comicsans_font = pygame.font.SysFont("Comic Sans MS", 50)

    # text
    # first parameter is the text
    # second parameter is anti-analising, always True
    # third parameter is the color
    #wilderness_text = corbel_font.render("Wilderness Explorer", True, white)
    wilderness_text = corbel_font.render("Play", True, white)
    rules_text = corbel_font.render("Rules", True, white)
    options_text = corbel_font.render("Options", True, white)
    credits_text = corbel_font.render("Credits", True, white)
    quit_text = corbel_font.render("Quit", True, white)
    #title_text = comicsans_font.render("Computation III - Project", True, glowing_light_red)
    title_text = comicsans_font.render("Wilderness Explorer", True, glowing_light_red)

    # Load and scale the background image once
    image = pygame.image.load("backstory images/jump_scare.jpg")
    image_width, image_height = 1000, 600
    image = pygame.transform.scale(image, (image_width, image_height))

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # main game loop
    while True:
        # event handling
        for ev in pygame.event.get():
            # quitting the game with the close button on the window (X)
            if ev.type == pygame.QUIT:
                pygame.quit()

            # detecting if the user clicked on the quit button (750, 500 para 890, 560)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 750 <= mouse[0] <= 890 and 500 <= mouse[1] <= 560:
                    pygame.quit()

            # detecting if the user clicked on options button (100, 500 para 240, 560):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= mouse[0] <= 240 and 500 <= mouse[1] <= 560:
                    under_construction()

            # detecting if the user clicked on the rules button (100, 380 para 240, 440):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= mouse[0] <= 240 and 380 <= mouse[1] <= 440:
                    under_construction()

            # detecting if the user clicked on the wilderness explorer button (100, 150 para 700, 210):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 200 <= mouse[0] <= 1000 and 150 <= mouse[1] <= 210:
                    start_game_with_story() # Call the story first


            # detecting if the user clicked on the credits button (750, 380 para 890, 440):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 750 <= mouse[0] <= 890 and 380 <= mouse[1] <= 440:
                    credits_()

        # Draw the background image
        screen.blit(image, (0, 0))


        # Bunch of things

        # get the mouse infomration
        mouse = pygame.mouse.get_pos()  # locates where the mouse is

        # drawing the buttons

        # wilderness explorer button - apperance
        pygame.draw.rect(screen, dark_red, [200, 150, 600, 60])
        wilderness_rect = wilderness_text.get_rect(center=(200 + 600 // 2, 150 + 60 // 2))
        screen.blit(wilderness_text, wilderness_rect)

        # Rules button
        pygame.draw.rect(screen, grey, [100, 380, 140, 60])
        rules_rect = rules_text.get_rect(center=(100 + 140 // 2, 380 + 60 // 2))
        screen.blit(rules_text, rules_rect)

        # Options button
        pygame.draw.rect(screen, grey, [100, 500, 140, 60])
        options_rect = options_text.get_rect(center=(100 + 140 // 2, 500 + 60 // 2))
        screen.blit(options_text, options_rect)

        # Credits button
        pygame.draw.rect(screen, grey, [750, 380, 140, 60])
        credits_rect = credits_text.get_rect(center=(750 + 140 // 2, 380 + 60 // 2))
        screen.blit(credits_text, credits_rect)

        # Quit button
        pygame.draw.rect(screen, grey, [750, 500, 140, 60])
        quit_rect = quit_text.get_rect(center=(750 + 140 // 2, 500 + 60 // 2))
        screen.blit(quit_text, quit_rect)

        # Title
        screen.blit(title_text, (250, 20))

        # at the end
        pygame.display.update()

        # Limit the frame rate to 60 FPS
        clock.tick(60)

    pass


# Under construction screen


def credits_():

    screen = pygame.display.set_mode(resolution)

    # fonts
    comicsans_font = pygame.font.SysFont("Comic Sans MS", 25)
    corbel_font = pygame.font.SysFont("Corbel", 50)

    # text
    leonor = comicsans_font.render("Leonor Aires, 20231654@novaims.unl.pt", True, white)
    constanca = comicsans_font.render("Constança Fernandes, 20231685@novaims.unl.pt", True, white)
    marta = comicsans_font.render("Marta Soares, 20231640@novaims.unl.pt", True, white)

    # main game loop
    while True:
        # mouse information
        mouse = pygame.mouse.get_pos()

        # check for events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 430 <= mouse[0] <= 570 and 540 <= mouse[1] <= 600:
                    interface()

        # background
        screen.fill(deep_black)

        # display text
        screen.blit(constanca, (250, 200))
        screen.blit(leonor, (250, 225))
        screen.blit(marta, (250, 250))

        # draw a back button [x, y, width, height]
        pygame.draw.rect(screen, dark_red, [430, 540, 140, 60])
        back_text = corbel_font.render("    back", True, white)
        back_rect = back_text.get_rect(center=(430 + 140 // 2, 540 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Update the screen
        pygame.display.update()


def rules_():
    print("Displaying rules...")


def wilderness_explorer():
    execute_game()
    interface()




