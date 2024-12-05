from config import *
import pygame
import math
from bullet import Bullet


class Character(pygame.sprite.Sprite):
    def __init__(self, image, x = 100, y = 100):
        """
        Initialize a Player instance
        """
        super().__init__()
        # Load and scale the image
        self.image = pygame.image.load("characters images/Tomátio.png")  # Load player sprite
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Set initial position
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Gameplay variables
        self.speed = 2
        self.max_health = 100
        self.health = self.max_health
        self.bullet_cooldown = 0
        self.damage_cooldown = 0
        self.invincible = False  # Default invincibility status

        # Jumping variables
        self.is_jumping = False
        self.y_velocity = 0
        self.gravity = 0.5  # Gravity strength
        self.jump_height = -12  # Jump height (negative to make the character move up)

    def update(self):
        """
        Update the position of the character based on keyboard input and physics (gravity).
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

    def shoot(self, bullets_group):
        """
        Create a bullet in the direction of the mouse
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.atan2(dy, dx)  # Direction in radians

        new_bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
        bullets_group.add(new_bullet)

    def take_damage(self, damage):
        """
        Reduce the player's health, considering invincibility and cooldown.
        """
        if self.invincible:  # Do not apply damage if invincible
            return
        if self.damage_cooldown <= 0:  # Only take damage if cooldown has ended
            self.health -= damage
            self.damage_cooldown = fps  # Cooldown of 1 second

    def draw(self, screen):
        # Desenhar o inimigo
        screen.blit(self.image, self.rect)

        # Desenhar barra de vida
        health_bar_width = self.rect.width
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, deep_black, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))




