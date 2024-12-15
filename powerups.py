import pygame
from abc import ABC, abstractmethod
from config import *
from character import *
import random

class PowerUp(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y):
        """
        Abstract class for power-ups in the game.

        Parameters
        ----------
        x : int
            X-coordinate of the power-up.
        y : int
            Y-coordinate of the power-up.
        """
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

        Parameters
        ----------
        player : Character
            The player character to affect.
        """
        pass

    @abstractmethod
    def affect_game(self, game_state):
        """
        Abstract method to apply the power-up's effect on the game.

        Parameters
        ----------
        game_state : dict
            The current state of the game.
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
        self.image = pygame.image.load("characters images/Shield 1.png") # Visual representation
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y-15))

        self.player = None # Store a reference to the player
        self.invincible_image = pygame.image.load("characters images/Invincible tomatio .png")  # Load the invincible player image
        self.invincible_image = pygame.transform.scale(self.invincible_image, (120, 120))  # Scale the player image

    def affect_player(self, player):
        """
        Make the player invincible and change its appearance.

        Parameters
        ----------
        player : Character
            The player character to affect.
        """
        self.player = player # Save reference
        self.timer = self.duration # Set the timer
        player.invincible = True
        player.invincibility_timer = self.duration

        # Save original player appearance and replace with the invincible image
        player.original_image = player.image  # Save the original image
        player.image = self.invincible_image  # Replace with invincible image

        # Save the original y-position of the rect and move the player higher
        player.original_y = player.rect.y  # Store the original position
        player.rect.y -= 15  # Move the rect up by 15 pixels

    def affect_game(self, game_state):
        """
        No direct effect on the game state.
        """
        pass


    def expire(self):
        """
        Cleanup when invincibility ends.
        Resets the player back to their original state.
        """
        if self.player:
            self.player.invincible = False
            self.player.image = self.player.original_image
            self.player.image_offset_y = 0

            # Reset the rect.y to the original stored position
            self.player.rect.y = self.player.original_y  # Restore the original position

        super().expire()  # Call the base class expire logic


class TomatoCoinPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Load the Tomato Coin image
        self.image = pygame.image.load("characters images/Tomato coin.png")  # Visual representation
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y - 10))
        self.player = None
        self.duration = 5 * fps

    def affect_player(self, player):
        """
        Temporarily set the coin reward to 10.

        Parameters
        ----------
        player : Character
            The player character to affect.
        """
        self.player = player
        self.timer = self.duration
        player.coin_powerup_active = True # Track activation
        player.coin_powerup_timer = self.duration
        player.coin_reward = 10  # Set coin reward to 10 coins
        print(f"[DEBUG] Tomato Coin Power-Up activated! Duration: {self.timer / fps} seconds")

    def affect_game(self, game_state):
        """
        No direct effect on the game state.
        """
        pass  # Required to satisfy the abstract class requirement

    def expire(self):
        """
        Reset the coin multiplier effect.
        """
        if self.player:
            self.player.coin_reward = False # Mark as expired
        super().expire()

class RapidBlasterPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Load the visual representation for the power-up
        self.image = pygame.image.load("characters images/rapid_blaster1.png")  # Replace with the actual image
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=(x, y - 10))
        self.player = None
        self.collected = False
        self.duration = 5 * fps  # Effect lasts for 5 seconds
        self.timer = 0

    def affect_player(self, player):
        """
        Temporarily apply RapidBlasterPowerUp

        Parameters
        ----------
        player : Character
            The player character to affect.
        """
        if not self.collected:  # Only activate once
            self.collected = True
            player.rapid_blaster_active = True
            player.rapid_blaster_timer = self.duration
            player.rapid_blaster_cooldown = 10  # Cooldown for automatic shots

    def affect_game(self, game_state):
        """
        No direct effect on the game state.
        """
        pass

    def update(self):
        """
        Updates the Rapid Blaster power-up timer and fires bullets continuously.
        """
        if self.collected and self.timer < self.duration:
            self.timer += 1
            if self.timer >= self.duration:
                self.expire()

    def expire(self):
        """
        Cleanup when the rapid shooting effect ends.
        """
        if self.player:
            self.player.rapid_blaster_active = False
            self.player.rapid_blaster_timer = 0
            print("[DEBUG] Rapid Blaster expired!")
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


