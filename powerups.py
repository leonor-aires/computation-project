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
        Abstract method to apply the power-ups effect on the player.

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
                print(f"[DEBUG] {self.__class__.__name__} timer expired.")
                self.expire()

    def expire(self):
        """
        Cleanup when the power-up's effect ends.
        """
        self.kill()  # Remove the power-up sprite

class InvincibilityPowerUp(PowerUp):
    requires_game_state = False  # This power-up does not need game_state
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
        self.player = player  # Save reference
        self.timer = self.duration  # Set the timer
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
    requires_game_state = False  # This power-up does not need game_state
    def __init__(self, x, y):
        super().__init__(x, y)
        # Load the Tomato Coin image
        self.image = pygame.image.load("characters images/Tomato coin.png")  # Visual representation
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y - 10))
        self.player = None
        self.golden_image = pygame.image.load("characters images/golden_tomatio1.png")
        self.golden_image = pygame.transform.scale(self.golden_image, (120, 120))

    def affect_player(self, player):
        """
        Temporarily set the coin reward to 10.

        Parameters
        ----------
        player : Character
            The player character to affect.
        """
        self.timer = self.duration
        player.coin_powerup_active = True
        player.coin_powerup_timer = self.duration
        self.player = player

        player.original_image = player.image
        player.image = self.golden_image
        player.coin_reward = 10
        player.original_y = player.rect.y  # Store the original position
        player.rect.y -= 15
        # Set coin reward to 10 coins
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
            self.player.coin_powerup_active = False
            self.player.image = self.player.original_image
            self.player.coin_reward = 5
            self.player.image_offset_y = 0

            # Reset the rect.y to the original stored position
            self.player.rect.y = self.player.original_y  # Restore the original position

            print("[DEBUG] Tomato Coin Power-Up expired.")
        super().expire()

class RapidBlasterPowerUp(PowerUp):
    requires_game_state = False  # This power-up does not need game_state
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
    """
    Power-up that removes a random number of enemies, ensuring at least one enemy
    is removed and not all enemies are removed.
    """
    requires_game_state = True  # This power-up needs game_state
    def __init__(self, x, y):
        """
        Initialize the despawner power-up
        """
        super().__init__(x, y)
        self.image = pygame.image.load("characters images/despawner.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y - 10))

    def affect_player(self, player, game_state):
        """
        Remove a random number of enemies (at least 1 and less than total enemies).

        Parameters
        ----------
        player : Character
            The player object.
        game_state : dict
            The current state of the game containing enemies.
        """
        enemies_group = game_state.get('enemies', None)

        if enemies_group:
            total_enemies = len(enemies_group)

            if total_enemies == 1:
                # If only one enemy exists, remove it
                enemies_to_remove = 1
            else:
                # Otherwise, pick a random number between 1 and total_enemies - 1
                enemies_to_remove = random.randint(1, total_enemies - 1)

            print(f"[DEBUG] Removing {enemies_to_remove} enemies out of {total_enemies}.")
            enemies_removed = 0

            # Remove enemies
            for enemy in list(enemies_group):
                if enemies_removed < enemies_to_remove:
                    enemy.kill()
                    enemies_removed += 1

            print(f"[DEBUG] {enemies_removed} enemies removed.")
        else:
            print("[DEBUG] No enemies to remove.")

    def affect_game(self, game_state):
        """
        Reduce enemy count and slow down spawns.
        """
        pass

    def update(self):
        """
        Update the timer and expire when done.
        """
        pass

    def expire(self):
        """
        Expire the power-up.
        """
        pass

