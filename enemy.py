from utils import*
from config import*
import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize an enemy instance
        """
        super().__init__()
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(red)
        self.rect = self.image.get_rect()

        #Positioning
        # Set the position
        self.rect.x = random.randint(0, width - enemy_size)
        self.rect.y = random.randint(0, height - enemy_size)

        #Random speed
        self.speed = random.uniform(1, 1.5)

        # Health
        self.max_health = 10  # Define maximum health
        self.health = self.max_health  # Current health is equal to maximum health

    def update(self, player):
        """
        Update the enemy position according to the player's Args
        ---
        player (Player)
            The player to move towards
        """
        # Calculates the direction in which the player is(angle)
        direction = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)

        # Coordinate update
        self.rect.x += self.speed * math.cos(direction)
        self.rect.y += self.speed * math.sin(direction)

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)

    def draw(self, screen):
        # Draw the enemy
        screen.blit(self.image, self.rect)

        # Draw the health bar
        health_bar_width = self.rect.width
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, deep_black, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))