from config import *
import pygame
import math
from bullet import Bullet
import json

class Character(pygame.sprite.Sprite):
    def __init__(self, image, x = 100, y = 100):
        """
       Initialize the Character instance.

       Parameters
       ----------
       image : str
           Image file to be used as the character sprite.
       x : int
           Initial x-coordinate for the character's position (default is 100).
       y : int
           Initial y-coordinate for the character's position (default is 100).

       """
        super().__init__()
        # Load and scale the image
        self.image = pygame.image.load("characters images/Tomátio.png")  # Load player sprite
        self.original_image = self.image
        self.original_y = y
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.original_color = self.image.copy()  # Save original appearance

        # Set initial position
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.original_size = (80, 80)  # Store original image size for scaling

        # Gameplay variables
        self.speed = 2
        self.max_health = 100
        self.health = self.max_health
        self.bullet_cooldown = 0
        self.damage_cooldown = 0 # Cooldown timer for taking damage
        self.invincible = False  # Default invincibility status
        self.invincibility_timer = 0 # Initialize the invincibility timer
        self.coins = 0
        self.coin_reward = 5
        self.coin_powerup_active = False# Default reward per enemy
        self.coin_powerup_timer = 0  # Initialize the Tomato Coin timer
        self.rapid_blaster_active = False
        self.rapid_blaster_timer = 0
        self.weapon = "default"  # Default weapon type
        self.current_level = 1  # Initialize level
        self.diamond_count = 0
        self.bullet_damage = 3
        self.bullets = None

        # Jumping variables
        self.is_jumping = False
        self.y_velocity = 0
        self.gravity = 0.5  # Gravity strength
        self.jump_height = -12  # Jump height (negative to make the character move up)

    def update(self):
        """
        Update the character's state, including movement, gravity, and power-up effects.

        This method handles:
        - Character movement (left, right, and jumping).
        - Gravity effects and ensuring the character stays on the screen.
        - Handling cooldowns for damage and invincibility power-up.
        - Managing power-up timers.

        Notes:
        - Horizontal movement is controlled by left/right arrow keys or 'A'/'D'.
        - Jumping is controlled by the up arrow key or 'W'. The player can only jump when on the ground.
        - The player's position is adjusted to prevent them from leaving the screen boundaries.
        """
        # Detecting key presses for character movement
        keys = pygame.key.get_pressed()

        # Horizontal movement (left and right)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Jumping mechanism
        if keys[pygame.K_UP] or keys[pygame.K_w]:  # Check if the spacebar is pressed
            if not self.is_jumping:  # Only jump if not already jumping
                self.is_jumping = True
                self.y_velocity = self.jump_height  # Set the jump velocity

        # Apply gravity
        if self.is_jumping:
            self.rect.y += self.y_velocity
            self.y_velocity += self.gravity  # Gradually increase downward velocity

            # If the character hits the ground, stop jumping
            if self.rect.bottom >= height:  # Check if the character hits the ground
                self.rect.bottom = height  # Keep the character on the ground
                self.is_jumping = False  # Stop jumping
                self.y_velocity = 0  # Reset vertical velocity

        # Prevent the character from going off the left edge
        if self.rect.left < 0:
            self.rect.left = 0

        # Prevent the character from going off the right edge
        if self.rect.right > width:
            self.rect.right = width

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # Handle invincibility
        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False
                self.image = self.original_image  # Reset the image
                # self.image = self.original_color  # Restore original sprite
                print("[DEBUG] Invincibility expired!")

        # Handle Tomato Coin power-up timer
        if self.coin_powerup_active:
            self.coin_powerup_timer -= 1
            if self.coin_powerup_timer <= 0:
                self.coin_powerup_active = False
                self.image = self.original_image  # Reset the image
                self.coin_reward = 5  # Reset to default reward
                print("[DEBUG] Tomato Coin Power-Up expired.")

        # Handle Rapid Blaster timer
        if self.rapid_blaster_active:
            self.rapid_blaster_timer -= 1
            if self.rapid_blaster_timer <= 0:
                self.rapid_blaster_active = False
                print("[DEBUG] Rapid Blaster effect ended.")


    def shoot_automatic(self):
        """
        Automatically shoot bullets forward and backward.

        This method fires two bullets: one moving forward and the other backward.
        It is triggered when the Rapid Blaster power-up is active
        """
        if self.rapid_blaster_active:
            if self.rapid_blaster_cooldown <= 0:
                forward_bullet = Bullet(self.rect.centerx, self.rect.centery, 0)  # Right
                backward_bullet = Bullet(self.rect.centerx, self.rect.centery, math.pi)  # Left
                self.bullets.add(forward_bullet, backward_bullet)
                print("[DEBUG] Bullets fired automatically: forward and backward")
                self.rapid_blaster_cooldown = 10  # Reset cooldown (10 frames)
            else:
                self.rapid_blaster_cooldown -= 1

    def shoot(self, bullets_group):
        """
        Create a bullet in the direction of the mouse
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
            The amount of damage to inflict.
        """
        if self.invincible:  # Skip damage if invincible
            return

        if self.damage_cooldown <= 0:  # Only take damage if cooldown is inactive
            self.health -= damage
            self.damage_cooldown = 60  # Set cooldown (1 second at 60 FPS)
            print(f"[DEBUG] Character took damage: {damage}. Health: {self.health}")

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
        print(f"[DEBUG] Coins Earned: {earned_amount}. Total Coins: {self.coins}")

    def draw(self, screen):
        """
        Draw the character and its health bar on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen on which the character will be drawn.
        """
        # Apply an optional image offset for invincibility
        offset_y = getattr(self, "image_offset_y", 0)  # Default to 0 if not set

        # Draw the character with the offset applied
        screen.blit(self.image, (self.rect.x, self.rect.y + offset_y))

        # Draw the health bar above the character
        health_bar_width = self.rect.width
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, deep_black, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))

        # Function to update bullet damage
    def update_bullet_damage(self, new_damage):
        """
        Update the character's bullet damage value.

        Parameters
        ----------
        new_damage : int
            The new damage value for bullets.
        """
        self.bullet_damage = new_damage

    def save_player_data(self, save_file):
        player_data = {
            'weapon_power': self.weapon,
            'coins': self.coins,
            'diamonds': self.diamond_count,
            'level': self.current_level,
        }
        with open(save_file, 'w') as file:
            json.dump(player_data, file)

    def load_player_data(self, save_file):
        with open(save_file, 'r') as file:
            player_data = json.load(file)
            self.weapon = player_data['weapon_power']
            self.coins = player_data.get('coins', 0)
            self.diamond_count = player_data['diamonds']
            self.current_level = player_data['level']

    def reset_player_data(self, save_file):
        """
        Reset the player's progress to the initial state and save it.

        Parameters
        ----------
        save_file : str
            The path to the save file.
        """
        self.weapon = "default"
        self.coins = 0
        self.diamond_count = 0
        self.current_level = 1
        self.health = self.max_health
        with open(save_file, 'w') as file:
            json.dump({
                'weapon_power': self.weapon,
                'coins': self.coins,
                'diamonds': self.diamond_count,
                'level': self.current_level,
            }, file)


