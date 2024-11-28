import pygame

def show_rules(screen, font, images):
    """
    Display the rules of the game
    Args:
        screen: The game screen to put the rules on
        font: The font used for the text
        images: A dictionary containing images for the power-ups and for the chests
    :param screen:
    :param font:
    :param images:
    :return:
    """
    # Clear the screen
    screen.fill((255, 255, 255)) #White background

    # Title
    title_text = font.render("Rules", True, (0, 0, 255))
    screen.blit(title_text, (400, 50))

    # Description
    powerup_desc = font.render("(Collect power-ups to gain abilities)", True, (0, 0, 0))
    screen.blit(powerup_desc, (50, 200))

    # Render each power-up image and its description
    y_offset = 250
    for i, (key, image) in enumerate(images.items()):
        if "powerup" in key:
            screen.blit(image, (50, y_offset))
            desc_text = font.render(f"Power-Up {i + 1} description here", True, (0, 0, 0))
            screen.blit(desc_text, (150, y_offset + 25))
            y_offset += 100

    # Chests Section
    chest_title = font.render("Chests:", True, (0, 128, 0))  # Green title
    screen.blit(chest_title, (50, y_offset))

    # Description
    chest_desc = font.render("(Choose different weapons/skills from chests)", True, (0, 0, 0))
    screen.blit(chest_desc, (50, y_offset + 50))

    # Render each chest image and its label
    chest_y_offset = y_offset + 100
    for i in range(1, 4):  # Assuming there are 3 chests
        chest_key = f"chest{i}"
        if chest_key in images:
            screen.blit(images[chest_key], (50, chest_y_offset))
            chest_label = font.render(f"Chest {i}", True, (0, 0, 0))
            screen.blit(chest_label, (150, chest_y_offset + 25))
            chest_y_offset += 100

    # Controls Section
    controls_title = font.render("Controls:", True, (0, 0, 0))  # Black title
    screen.blit(controls_title, (50, chest_y_offset + 50))

    # Render control buttons
    controls = [
        ("Left", "</A"),
        ("Right", ">/D"),
        ("Shoot", "Space"),
        ("Up", "^/W"),
        ("Down", "v/S")
    ]
    control_y_offset = chest_y_offset + 100
    for control in controls:
        text = font.render(f"{control[0]}: {control[1]}", True, (0, 0, 0))
        screen.blit(text, (50, control_y_offset))
        control_y_offset += 50

    # Update the display
    pygame.display.flip()


# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Rules")
    font = pygame.font.Font(None, 36)

    # Load images (replace with actual image paths)
    images = {
        "powerup1": pygame.Surface((50, 50)),  # Placeholder for power-up 1
        "powerup2": pygame.Surface((50, 50)),  # Placeholder for power-up 2
        "chest1": pygame.Surface((50, 50)),  # Placeholder for chest 1
        "chest2": pygame.Surface((50, 50)),  # Placeholder for chest 2
        "chest3": pygame.Surface((50, 50))  # Placeholder for chest 3
    }
    for image in images.values():
        image.fill(((255, 0, 0), (0, 255, 0), (255, 255, 0)))  # Random colors

    # Call the show_rules function
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        show_rules(screen, font, images)

    pygame.quit()

