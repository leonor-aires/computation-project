from utils import*
from config import*
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: float):
        """
        Initialize a bullet instance:

        Args
        ---

        :param x:
            position of the bullet in the x-axis
        :param y:
            Position of the bullet in the y-axis
        :param direction:
            direction in which it is fired, in radians
        """
        super().__init__()
        self.radius = bullet_size
        #self.color = yellow
        self.rect = pygame.Rect(x-self.radius,
                                y-self.radius,
                                self.radius *2,
                                self.radius * 2)
        self.speed= 2
        self.direction = direction

        # Carregar a imagem do gift
        self.image = pygame.image.load('fire.png')
        self.image = pygame.transform.scale(self.image, (30, 30))  # Redimensione conforme necessário
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """
        Update the bullet's position and chect if it goes offscreen.
        :return:
        """
        #Coordinate update
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        #Coordinate update
        if (self.rect.x < 0 or self.rect.x > width or\
                self.rect.y < 0 or self.rect.y > height):
            self.kill()

    def draw(self, screen: pygame.Surface):
        """
        Draw the bullet on the screen

        The screen on which to draw the bullet

        """
        #Draw the bullet as a circle
        screen.blit(self.image, self.rect)
        #pygame.draw.circle(
            #screen, self.color, self.rect.center, self.radius
        #)
