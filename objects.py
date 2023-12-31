# object class 
import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, game, image, x=50, y=50, w=100, h=100, name=None):
            super().__init__()

            self.game = game
            self.image = image
            self.name = name

            # Load initial image
            self.image = pygame.transform.scale(self.image, (w, h))
            self.rect = self.image.get_rect()

            # Set rectangle
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.rect.x = x
            self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def __repr__(self):
         return self.name