from abc import ABC, abstractmethod
from character import *
import random

class PowerUp(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y):
        """
        Set the initial state and position for the objects

        Parameters:
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
            The player that is affected.
        """
        pass

    @abstractmethod
    def affect_game(self, game_state):
        """
        Abstract method to apply the power-ups effect on the game.

        Parameters
        ----------
        game_state : dict
            The current state of the game.
        """
        pass

    def update(self):
        """
        Update the power-ups timer and deactivate if expired.
        """
        if self.collected:
            self.timer -= 1
            if self.timer <= 0:
                self.expire()

    def expire(self):
        """
        Deactivate when the power-ups effect ends.
        """
        self.kill()  # Remove the power-up sprite

class InvincibilityPowerUp(PowerUp):
    requires_game_state = False  # This power-up does not need game_state
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("characters images/Shield 1.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y-15))

        self.player = None # Store a reference to the player
        self.invincible_image = pygame.image.load("characters images/Invincible tomatio .png")
        self.invincible_image = pygame.transform.scale(self.invincible_image, (120, 120))

    def affect_player(self, player):
        """
        Make the player invincible and change its appearance.

        Parameters
        ----------
        player : Character
            The player that is affected.
        """
        self.player = player  # Save reference
        self.timer = self.duration
        player.invincible = True
        player.invincibility_timer = self.duration

        # Save original player appearance and replace with the invincible image
        player.original_image = player.image
        player.original_y = player.rect.y
        player.image = self.invincible_image

        player.rect.y -= 15  # Move the rect up by 15 pixels

    def affect_game(self, game_state):
        """
        No direct effect on the game state.
        """
        pass


    def expire(self):
        """
        Deactivate when invincibility ends.
        Resets the player back to their original state.
        """
        if self.player:
            self.player.invincible = False
            self.player.image = self.player.original_image

            # Reset the rect.y to the original stored position
            self.player.rect.y = self.player.original_y
        super().expire()

class TomatoCoinPowerUp(PowerUp):
    requires_game_state = False  # This power-up does not need game_state
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("characters images/Tomato coin.png")
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
            The player that is affected.
        """
        self.timer = self.duration
        player.coin_powerup_active = True
        player.coin_powerup_timer = self.duration
        self.player = player

        player.original_image = player.image
        player.original_y = player.rect.y
        player.image = self.golden_image
        player.coin_reward = 10
        player.rect.y -= 15

    def affect_game(self, game_state):
        """
        No direct effect on the game state.
        """
        pass

    def expire(self):
        """
        Reset the coin reward back to 5.
        """
        if self.player:
            self.player.coin_powerup_active = False
            self.player.image = self.player.original_image
            self.player.coin_reward = 5

            # Reset the rect.y to the original stored position
            self.player.rect.y = self.player.original_y
        super().expire()

class RapidBlasterPowerUp(PowerUp):
    requires_game_state = False  # This power-up does not need game_state
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("characters images/rapid_blaster1.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=(x, y - 10))
        self.player = None
        self.collected = False
        self.duration = 5 * fps  # Effect lasts for 5 seconds
        self.timer = 0

    def affect_player(self, player):
        """
        Temporarily shoot constant automatic bullets.

        Parameters
        ----------
        player : Character
            The player that is affected.
        """
        if not self.collected:
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
        Updates the Rapid Blaster power-up timer and fires bullets constantly.
        """
        if self.collected and self.timer < self.duration:
            self.timer += 1
            if self.timer >= self.duration:
                self.expire()

    def expire(self):
        """
        Deactivate when the rapid shooting effect ends.
        """
        if self.player:
            self.player.rapid_blaster_active = False
            self.player.rapid_blaster_timer = 0
        super().expire()


class DespawnerPowerUp(PowerUp):
    """
    Power-up that removes a random number of enemies, ensuring at least one enemy
    is removed and not all enemies are removed.
    """
    requires_game_state = True  # This power-up needs game_state
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("characters images/despawner.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y - 10))
        self.collected = False
    def affect_player(self, player, game_state):
        """
        Notify that the despawner power-up was activated.

        Parameters
        ----------
        player : Character
            The player that is affected.
        game_state : dict
            The current state of the game containing enemies.
        """
        self.affect_game(game_state)  # Apply the game effect directly

    def affect_game(self, game_state):
        """
        Remove a random number of enemies from the game.

        Parameters
        ----------
        game_state : dict
            The current state of the game containing enemies.
        """
        if self.collected:
            return

        enemies_group = game_state.get('enemies', None)

        if enemies_group:
            total_enemies = len(enemies_group)

            if total_enemies == 1:
                # If only one enemy exists, remove it
                enemies_to_remove = 1
            else:
                # Otherwise, pick a random number between 1 and total_enemies - 1
                enemies_to_remove = random.randint(1, total_enemies - 1)

            enemies_removed = 0

            # Remove enemies
            for enemy in list(enemies_group):
                if enemies_removed < enemies_to_remove:
                    enemy.kill()
                    enemies_removed += 1

            self.collected = True

