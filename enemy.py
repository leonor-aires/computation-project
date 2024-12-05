from utils import *
from config import *
import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, platform):
        """
        Initialize an enemy instance restricted to a specific platform.

        Args:
            platform (pygame.Rect): The platform the enemy will be restricted to.
        """
        super().__init__()
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(red)
        self.rect = self.image.get_rect()

        # Platform association
        self.platform = platform

        # Initial position on the platform
        self.rect.x = random.randint(platform.left, platform.right - self.rect.width)
        self.rect.y = platform.top - self.rect.height

        # Random horizontal speed
        self.speed = random.choice([-1, 1]) * random.uniform(1, 1.5)

        # Health
        self.max_health = 10
        self.health = self.max_health

    def update(self):
        """
        Update the enemy's horizontal position, restricting it to its assigned platform.
        """
        # Move horizontally
        self.rect.x += self.speed

        # Reverse direction when reaching platform edges
        if self.rect.left < self.platform.left or self.rect.right > self.platform.right:
            self.speed = -self.speed  # Reverse direction
            self.rect.x += self.speed  # Correct position to stay within bounds

        # Keep enemy fixed on the platform
        self.rect.bottom = self.platform.top

    def draw(self, screen):
        """
        Draw the enemy and its health bar on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        # Draw enemy
        screen.blit(self.image, self.rect)

        # Draw health bar
        health_bar_width = self.rect.width
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, deep_black, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))
