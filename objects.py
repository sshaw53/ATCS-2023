# object class 
import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, game, image, x=50, y=50):
            super().__init__()

            self.game = game
            self.image = image

            # Load initial image
            self.rect = self.image.get_rect()

            # Set rectangle
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.rect.centerx = x
            self.rect.centery = y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y))