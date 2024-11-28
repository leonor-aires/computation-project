import pygame
from abc import ABC, abstractmethod
from config import *
import random

class PowerUp(pygame.sprite.Sprite, ABC):
    """
    Abstract class for power-ups in the game.
    """

    def __init__(self, x, y):
        super().__init__()
        self.image = None  # To be defined in subclasses
        self.rect = None  # To be defined in subclasses
        self.duration = 5 * fps  # Default duration of 5 seconds
        self.timer = 0
        self.collected = False

    @abstractmethod
    def affect_player(self, player):
        """
        Abstract method to apply the power-up's effect on the player.
        """
        pass

    @abstractmethod
    def affect_game(self, game_state):
        """
        Abstract method to apply the power-up's effect on the game.
        """
        pass

    def update(self):
        """
        Update the power-up's timer and deactivate if expired.
        """
        if self.collected:
            self.timer -= 1
            if self.timer <= 0:
                self.expire()

    def expire(self):
        """
        Cleanup when the power-up's effect ends.
        """
        self.kill()  # Remove the power-up sprite

class InvincibilityPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((30, 30))  # Visual representation
        self.image.fill(blue)  # Blue color for invincibility
        self.rect = self.image.get_rect(center=(x, y))
        self.player = None # Store a reference to the player

    def affect_player(self, player):
        """
        Make the player invincible and change its appearance.
        """
        self.player = player # Save reference
        self.timer = self.duration # Set the timer
        player.invincible = True
        player.original_color = player.image.copy() # Save the original appearance
        player.image.fill((0, 255, 0)) # Change color to green
        print(f"[DEBUG] Invincibility activated. Timer: {self.timer}")

    def affect_game(self, game_state):
        """
        No direct effect on the game state.
        """
        pass

    def expire(self):
        """
        Cleanup when invincibility ends.
        """
        if self.player:
            self.player.invincible = False
            self.player.image = self.player.original_image  # Restore original appearance
            print("[DEBUG] Invincibility ended.")
        super().expire()


class DespawnerPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((30, 30))  # Visual representation
        self.image.fill(red)  # Red color for despawner
        self.rect = self.image.get_rect(center=(x, y))

    def affect_player(self, player):
        """
        No direct effect on the player.
        """
        pass

    def affect_game(self, game_state):
        """
        Reduce enemy count and slow down spawns.
        """
        for enemy in list(game_state['enemies'])[:3]:  # Remove 3 enemies
            enemy.kill()

        game_state['spawn_rate'] *= 2  # Slow spawn rate by half temporarily
