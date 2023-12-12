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
        self.door_img = pygame.image.load("images/door.png")
        self.purpshirt_img = pygame.image.load("images/purple.png")
        self.pinkshirt_img = pygame.image.load("images/pink.png")

        # Sprites
        self.objects = pygame.sprite.Group()
        self.brush = Object(self, self.brush_img, 275, 25, 65, 65, "brush")
        self.objects.add(self.brush)
        self.door = Object(self, self.door_img, 920, 350, 50, 175, "door")
        self.objects.add(self.door)
        self.purpshirt = Object(self, self.purpshirt_img, 50, 275, 75, 90, "purple shirt")
        self.objects.add(self.purpshirt)
        self.pinkshirt = Object(self, self.pinkshirt_img, 50, 400, 75, 90, "pink shirt")
        self.objects.add(self.pinkshirt)
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
        countdown_time = 15000

        # Draw the initial screen
        self.screen.blit(self.background, (0, 0)) 
        self.objects.draw(self.screen)
        self.player.draw(self.screen)

        while running:
            # If the time runs up, the game is over
            if countdown_time <= 0:
                self.player.update("time's up")

            # Set fps to 120
            self.dt += self.clock.tick(120)
            countdown_time -= self.clock.tick(120)

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
                    
                    elif self.door.rect.collidepoint(mouse_x, mouse_y):
                        self.last_clickedx = mouse_x
                        self.last_clickedy = mouse_y
                        self.player.update("item clicked")

                    elif self.purpshirt.rect.collidepoint(mouse_x, mouse_y):
                        self.last_clickedx = mouse_x
                        self.last_clickedy = mouse_y
                        self.player.update("item clicked")

                    elif self.pinkshirt.rect.collidepoint(mouse_x, mouse_y):
                        self.last_clickedx = mouse_x
                        self.last_clickedy = mouse_y
                        self.player.update("item clicked")
            
            # If the player is in action and collides with objects, state should change and timer should be set to zero
            collided_objs = pygame.sprite.spritecollide(self.player, self.objects, False)
            print(collided_objs)
            if self.player.get_state() == "ia" and len(collided_objs) > 0:
                if self.door in collided_objs:
                    print(self.door)
                    self.player.update("at door")
                elif self.brush in collided_objs:
                    self.dt = 0
                    self.player.update("reached brush")
                elif self.pinkshirt in collided_objs or self.purpshirt in collided_objs:
                    self.dt = 0
                    self.player.update("reached shirts")
            
            elif self.player.get_state() == "bh" and self.dt > 2000:
                self.player.update("action complete")

            elif self.player.get_state() == "ch" and self.dt > 1500:
                self.player.update("action complete")

            self.player.update()

            # Draw to the screen
            self.screen.blit(self.background, (0, 0)) 
            self.objects.draw(self.screen)
            self.player.draw(self.screen)

            # Display the countdown
            if self.player.game_over == False:
                countdown_text = font.render(f"Time: {countdown_time / 1000}", True, (0, 0, 0))
                self.screen.blit(countdown_text, (400, 50))
            
            # Display action
            if self.player.get_state() == "bh":
                text = font.render(f"brushing hair...", True, (0, 0, 0))
                self.screen.blit(text, (300, 500))
            elif self.player.get_state() == "ch":
                text = font.render(f"changing...", True, (0, 0, 0))
                self.screen.blit(text, (350, 500))

            # Game over
            if self.player.game_over == True:
                countdown_time = 3000
                font = pygame.font.Font(None, 100)
            
                if self.player.winner == True:
                    end_text = font.render(f"YOU WON!!!", True, (0, 0, 0))
                    if self.player.indx < 3:
                        font = pygame.font.Font(None, 30)
                        other_end_text = font.render(f"you look a little messy though...", True, (0, 0, 0))
                        self.screen.blit(other_end_text, (350, 300))
                else:
                    end_text = font.render(f"YOU LOST :(", True, (0, 0, 0))
            
                self.screen.blit(end_text, (300, 200))

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

# implementing timer and see how to check if they are at the door