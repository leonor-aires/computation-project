import pygame
from config import*
import math
from music import shooting, is_sound_enabled

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: float, weapon_type="default"):
        """
        Initialize a bullet instance:

        Parameters
        ----------
        x : int
            Position of the bullet in the x-axis
        y : int
            Position of the bullet in the y-axis
        direction: float
            Direction in which it is fired, in radians
        weapon_type : str
            The type of weapon firing the bullet, by default "default".
        """
        super().__init__()
        self.speed = 2
        self.direction = direction
        self.weapon_type = weapon_type
        self.start_x = x
        self.start_y = y


        if is_sound_enabled():
            shooting(("Music/Shooting sfx.mp3"), volume=0.5)

        # Load different bullet images based on weapon type
        if self.weapon_type == "Ketchup Kannon":
            self.image = pygame.image.load('characters images/bomb.png')
        elif self.weapon_type == "Knife of Justice":
            self.image = pygame.image.load('characters images/Knife_of_justice.png')
        elif self.weapon_type == "Tomato Slice":
            self.image = pygame.image.load('characters images/Tomato_slice.png')
        else:
            self.image = pygame.image.load('characters images/fire.png')
        if self.weapon_type == "egg":
            self.image = pygame.image.load('characters images/egg.png')

        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """
        Update the bullet's position and check if it goes off-screen.
        """
        # Update only the horizontal coordinate
        self.rect.x += int(self.speed * math.copysign(1, math.cos(self.direction)))

        # Remove the bullet if it goes off-screen or exceeds a certain range
        if self.rect.x < 0 or self.rect.x > width or self.exceeds_range():
            self.kill()

    def exceeds_range(self):
        """
        Check if the bullet exceeds a certain range based on its starting position.

        Returns: boolean
            True if the bullet exceeds the predefined range, False otherwise.
        """
        # Calculate the distance from the starting position
        distance = math.sqrt((self.rect.x - self.start_x) ** 2 + (self.rect.y - self.start_y) ** 2)
        return distance > 150

    def draw(self, screen: pygame.Surface):
        """
        Draw the bullet on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The Pygame surface on which the bullet will be drawn.
        """
        screen.blit(self.image, self.rect)

