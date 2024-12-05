from utils import*
from config import*
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: float):
        """
        Initialize a bullet instance:

        Args
        ---
        x:position of the bullet in the x-axis
        y:Position of the bullet in the y-axis
        direction: direction in which it is fired, in radians
        """
        super().__init__()
        self.speed = 2
        self.direction = direction

        # Carregar a imagem (fire)
        self.image = pygame.image.load('characters images/fire.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """
        Update the bullet's position and check if it goes offscreen.
        :return:
        """
        # Update only the horizontal coordinate
        self.rect.x += int(self.speed * math.copysign(1, math.cos(self.direction)))

        # Remove the bullet if it goes offscreen
        if self.rect.x < 0 or self.rect.x > width:
            self.kill()

    def draw(self, screen: pygame.Surface):
        """
        Draw the bullet on the screen
        """
        screen.blit(self.image, self.rect)

