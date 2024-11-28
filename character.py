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
        self.image = pygame.image.load("dragon.png")  # Load player sprite
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.original_color = self.image.copy()  # Save original appearance

        # Set initial position
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Gameplay variables
        self.speed = 2
        self.max_health = 100
        self.health = self.max_health
        self.invincible = False # Start not invincible
        self.bullet_cooldown = 0
        self.damage_cooldown = 0

    def update(self):
        """
        Update the position of the player based on keyboard input
        """

        if not pygame.get_init():  # Safeguard: Check if Pygame is initialized
            print("[ERROR] Pygame video system not initialized.")

        # Detecting key presses for character movement
        keys = pygame.key.get_pressed()
        # Move the character based on key presses, ensuring the character doesn't move out of bounds
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.x > 0:  # Prevent moving past the left edge
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.x < resolution[0] - self.rect.width:  # Prevent moving past the right edge
                self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.y > 0:  # Prevent moving past the top edge
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.y < resolution[1] - self.rect.height:  # Prevent moving past the bottom edge
                self.rect.y += self.speed
        # Reduz o cooldown de dano
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

    def shoot(self, bullets: pygame.sprite.Group):
        """
        Shoot bullet in 4 direction depending on the cooldown.

        ARGS
        ---
        bullet (pygame.sprite.Group):
            The bullet group that we will add the news ones to
        """
        if self.bullet_cooldown <= 0:
            for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
                bullet= Bullet(
                    self.rect.center[0], self.rect.center[1], angle
                )
                bullets.add(bullet)
            self.bullet_cooldown = fps #Frames until the next shot
        #If you're not
        self.bullet_cooldown -=1

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
        Reduce health, considering cooldown, unless invincible
        """
        if self.invincible:
            return  # Ignore damage if invincible

        if self.damage_cooldown <= 0:  # Only take damage if cooldown has expired
            self.health -= damage
            self.damage_cooldown = fps  # Cooldown for 1 second

    def draw(self, screen):
        # Desenhar o inimigo
        screen.blit(self.image, self.rect)

        # Desenhar barra de vida
        health_bar_width = self.rect.width
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, deep_black, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))




