from config import *
import pygame
import math
from bullet import Bullet
import json

class Character(pygame.sprite.Sprite):
    def __init__(self, image, x=100, y=100):
        """
       Initialize the Character instance.

       Parameters:
       ----------
       image : str
           Image file to be used as the character sprite.
       x : int
           Initial x-coordinate for the character's position.
       y : int
           Initial y-coordinate for the character's position.

       """
        super().__init__()
        self.image = pygame.image.load("characters images/Tomátio.png")
        self.original_image = self.image
        self.original_y = y
        self.image = pygame.transform.scale(self.image, (80, 80))

        # Set initial position
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Gameplay variables
        self.speed = 2
        self.max_health = 100
        self.health = self.max_health
        self.damage_cooldown = 0
        self.invincible = False
        self.invincibility_timer = 0
        self.coins = 0
        self.coin_reward = 5
        self.coin_powerup_active = False
        self.coin_powerup_timer = 0
        self.rapid_blaster_active = False
        self.rapid_blaster_timer = 0
        self.weapon = "default"
        self.current_level = 1
        self.diamond_count = 0
        self.bullet_damage = 3
        self.bullets = None

        # Jumping variables
        self.is_jumping = False
        self.y_velocity = 0
        self.gravity = 0.5  # Gravity strength
        self.jump_height = -12

    def update(self):
        """
        Update the character's state, including movement, gravity, and power-up effects.
        """
        # Detecting key presses for character movement
        keys = pygame.key.get_pressed()

        # Horizontal movement (left and right)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Jumping mechanism
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if not self.is_jumping:
                self.is_jumping = True
                self.y_velocity = self.jump_height

        # Apply gravity
        if self.is_jumping:
            self.rect.y += self.y_velocity
            self.y_velocity += self.gravity

        # Prevent the character from going off the left edge
        if self.rect.left < 0:
            self.rect.left = 0

        # Prevent the character from going off the right edge
        if self.rect.right > width:
            self.rect.right = width

        # Cooldown timer for when the character can take damage again after being hit
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # Handle invincibility timer
        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False
                self.image = self.original_image

        # Handle Tomato Coin power-up timer
        if self.coin_powerup_active:
            self.coin_powerup_timer -= 1
            if self.coin_powerup_timer <= 0:
                self.coin_powerup_active = False
                self.image = self.original_image
                self.coin_reward = 5

        # Handle Rapid Blaster timer
        if self.rapid_blaster_active:
            self.rapid_blaster_timer -= 1
            if self.rapid_blaster_timer <= 0:
                self.rapid_blaster_active = False


    def shoot_automatic(self):
        """
        Automatically shoot bullets forward and backward.
        It is triggered when the Rapid Blaster power-up is active.
        """
        if self.rapid_blaster_active:
            if self.rapid_blaster_cooldown <= 0:
                forward_bullet = Bullet(self.rect.centerx, self.rect.centery, 0)  # Forward
                backward_bullet = Bullet(self.rect.centerx, self.rect.centery, math.pi)  # Backward
                self.bullets.add(forward_bullet, backward_bullet)
                self.rapid_blaster_cooldown = 10  # Reset cooldown (10 frames)
            else:
                self.rapid_blaster_cooldown -= 1

    def shoot(self, bullets_group):
        """
        Shoot a bullet from the character's current position.

        Parameters
        ----------
        bullets_group : pygame.sprite.Group
            The group to which the new bullet will be added.
        """
        angle = math.radians(0)

        # Create a new bullet with the current weapon type
        new_bullet = Bullet(self.rect.centerx, self.rect.centery, angle, weapon_type=self.weapon)
        bullets_group.add(new_bullet)

    def take_damage(self, damage):
        """
        Reduce the player's health, considering invincibility and cooldown.

        Parameters
        ----------
        damage : int
            The amount of damage that is inflicted.
        """
        if self.invincible:  # Skip damage if invincible
            return

        if self.damage_cooldown <= 0:  # Only take damage if cooldown is inactive
            self.health -= damage
            self.damage_cooldown = 60  # Set cooldown (1 second at 60 FPS)

    def earn_coins(self, amount):
        """
        Add coins to the player's total

         Parameters
        ----------
        amount : int
            The number of coins to add.
        """
        earned_amount = amount
        self.coins += earned_amount
        self.save_player_data("save_file.json")

    def draw(self, screen):
        """
        Draw the character and its health bar on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen on which the character will be drawn.
        """
        # Draw the character with the offset applied
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Draw the health bar above the character
        health_bar_width = self.rect.width
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, deep_black, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))


    def save_player_data(self, save_file):
        """
        Save the player's current state to a file.

        Parameters:
        ----------
        save_file : str
            The path to the file where the player data will be saved.
        """
        player_data = {
            'weapon_power': self.weapon,
            'coins': self.coins,
            'diamonds': self.diamond_count,
            'level': self.current_level,
        }
        with open(save_file, 'w') as file:
            json.dump(player_data, file)

    def load_player_data(self, save_file):
        """
        Load the player's state from a file.

        Parameters:
        ----------
        save_file : str
            The path to the file from which the player data will be loaded.
        """
        with open(save_file, 'r') as file:
            player_data = json.load(file)
            self.weapon = player_data['weapon_power']
            self.coins = player_data.get('coins', 0)
            self.diamond_count = player_data['diamonds']
            self.current_level = player_data['level']

    def reset_player_data(self, save_file):
        """
        Reset the player's progress to the initial state and save it.

        Parameters:
        ----------
        save_file : str
            The path to the save file that will be reset.
        """
        self.weapon = "default"
        self.coins = 0
        self.diamond_count = 0
        self.current_level = 1
        self.health = self.max_health
        self.rect.x = 0
        self.rect.y = height - self.rect.height
        with open(save_file, 'w') as file:
            json.dump({
                'weapon_power': self.weapon,
                'coins': self.coins,
                'diamonds': self.diamond_count,
                'level': self.current_level,
            }, file)

