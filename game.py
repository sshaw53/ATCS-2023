import pygame
import sys
from player import GameBot
from objects import Object

class Game:
    # Constants
    START_X, START_Y = 823, 178
    BACKGROUND_COLOR = (0, 0, 0)

    def __init__(self):
        self.DEBUG = True

        # Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dt = 0

        # Initializing images
        self.background = pygame.image.load("images/background.png")
        self.brush_img = pygame.image.load("images/brush.png")

        # Sprites
        self.objects = pygame.sprite.Group()
        self.brush = Object(self, self.brush_img, 50, 50)
        self.objects.add(self.brush)
        self.player = GameBot(self)

        # Create the game window
        self.screen = pygame.display.set_mode((960, 540))
        pygame.display.set_caption("Get Ready Game")

    def run(self):
        # Main game loop
        running = True

        # Draw the initial screen
        self.screen.blit(self.background, (0, 0)) 
        self.objects.draw(self.screen)
        self.player.draw(self.screen)
        
        while running:
            # Set fps to 120
            self.dt += self.clock.tick(120)

            # Handle closing the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # clicking should go here
            
            # If the player is in action and collides with brush, state should change and timer should be set to zero
            if self.player.game.get_state() == "ia" and self.player.colliderect(self.brush):
                self.dt = 0
                self.player.update("reached item")
            
            elif self.player.game.get_state() == "bh" and self.dt > 8000:
                self.player.update("action complete")

            # Draw to the screen
            self.screen.blit(self.background, (0, 0)) 
            self.objects.draw(self.screen)
            self.player.draw(self.screen)

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

# look at clicking and how to know if a sprite has been clicked in pygame