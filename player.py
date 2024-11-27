from config import *
import pygame
import math
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize a Player instance
        """
        super().__init__()
        # Drawing variables
        self.image = pygame.image.load("character.png")  # Load player sprite
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize image if necessary
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # Gameplay variables
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0

    def update(self):
        """
        Update the position of the player based on keyboard input
        """
        keys = pygame.key.get_pressed()
        # Moving upwards
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        # Moving downwards
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
        # Moving left
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        # Moving right
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed

    def shoot(self, bullets):
        """
        Shoots bullets in multiple directions
        bullets --> pygame group where I will add bullets
        """
        # cooldown ==> how many frames I need to wait until I can shoot again
        if self.bullet_cooldown <= 0:
            # === defining the directions in which the bullets will fly ===
            # these 4 directions are, in order, right, left, up, down
            for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                # === creating a bullet for each angle ===

                # I will use self.rect.centerx to make the x position of the bullet the same as the
                # x position of the player, thus making the bullet come out of them.
                # finally, the direction of the bullet is the angle
                bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                # adding the bullet to the bullets pygame group.
                bullets.add(bullet)

            # resetting the cooldown
            self.bullet_cooldown = fps

        self.bullet_cooldown -= 1

    def draw(self, screen):
        """
        Draw the player on the screen.
        """
        screen.blit(self.image, self.rect)


