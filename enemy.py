from utils import *
from config import *
import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, platform):
        """
        Initialize an enemy instance restricted to a specific platform.

        Parameters
        ----------
        platform: pygame.Rect
                The platform the enemy will be restricted to.
        """
        super().__init__()
        # Load the enemy image
        self.original_image = pygame.image.load("characters images/Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image,(80, 80))
        self.rect = self.image.get_rect()

        # Platform association
        self.platform = platform

        # Initial position on the platform
        self.rect.x = random.randint(platform.left, platform.right - self.rect.width)
        self.rect.y = platform.top - self.rect.height

        # Random horizontal speed
        self.speed = random.choice([-1, 1]) * random.uniform(1, 1.5)

        # Health
        self.max_health = 20
        self.health = self.max_health

    def update(self, character=None):
        """
        Update the enemy's horizontal position, restricting it to its assigned platform.

        Parameters
        ----------
        character : Character
            The player character, used for potential future interactions (default is None).
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

        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the enemy and health bar on.
        """
        # Draw enemy
        screen.blit(self.image, self.rect)

        # Draw health bar background
        health_bar_width = self.rect.width
        pygame.draw.rect(screen, deep_black, (self.rect.x, self.rect.y - 10, health_bar_width, 5))

        # Draw health bar foreground (proportional to current health)
        health_ratio = max(0, self.health / self.max_health)  # Avoid negative health values
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))

    def decrease_health(self, amount):
        """
        Decrease the enemy's health by a certain amount.

        Parameters
        ----------
        amount : int
            The amount of health to subtract.
        """
        self.health -= amount
        self.health = max(0, self.health)  # Ensure health doesn't go below zero