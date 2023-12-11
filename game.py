import pygame
import sys
from player import GameBot
from objects import Object

class Game:
    # Constants
    START_X, START_Y = 723, 208
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
        self.brush = Object(self, self.brush_img, 200, 150)
        self.objects.add(self.brush)
        self.player = GameBot(self, self.START_X, self.START_Y)

        # Last clicked coordinates
        self.last_clickedx = 0
        self.last_clickedy = 0

        # Create the game window
        self.screen = pygame.display.set_mode((960, 540))
        pygame.display.set_caption("Get Ready Game")

    def run(self):
        # Main game loop
        running = True

        # Font for countdown
        font = pygame.font.Font(None, 36)

        # Set countdown time (in seconds)
        countdown_time = 10
        current_time = countdown_time

        # Draw the initial screen
        self.screen.blit(self.background, (0, 0)) 
        self.objects.draw(self.screen)
        self.player.draw(self.screen)
        

        while running:
            # If the time runs up, the game is over
            if current_time == 0:
                running = False
                self.player.update("time's up")

            
            # Set fps to 120
            self.dt += self.clock.tick(120)

            # Handle closing the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # If object gets clicked, alter the FSM * modified from ChatGPT * - check for mouse click event
                # Check if the mouse click is inside the sprite
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
 
                    if self.brush.rect.collidepoint(mouse_x, mouse_y):
                        self.last_clickedx = mouse_x
                        self.last_clickedy = mouse_y
                        self.player.update("item clicked")
            
            # If the player is in action and collides with brush, state should change and timer should be set to zero
            collided_objs = pygame.sprite.spritecollide(self.player, self.objects, False)
            print(collided_objs)
            if self.player.get_state() == "ia" and len(collided_objs) > 0:
                self.dt = 0
                self.player.update("reached item")
            
            elif self.player.get_state() == "bh" and self.dt > 8000:
                self.player.update("action complete")

            self.player.update()
            
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