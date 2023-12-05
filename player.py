import pygame
from fsm import FSM

class GameBot(pygame.sprite.Sprite):
    # States
    NEUTRAL, IN_ACTION, WALKING, WON, LOST, BRUSHING_HAIR = "n", "ia", "wa", "wo", "l" "bh"

    def __init__(self, game, x=50, y=50):
        super().__init__()

        self.game = game

        # Load initial image
        self.image = pygame.image.load("images/neutral_girl.png")
        self.rect = self.image.get_rect()

        # Set rectangle
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.centerx = x
        self.rect.centery = y

        # Creates the Bot's finite state machine (self.fsm) with initial state
        self.fsm = FSM(self.NEUTRAL)
        self.init_fsm()
    
    def init_fsm(self):
        # Add more here for the other states with actions
        self.fsm.add_transition("action complete", self.BRUSHING_HAIR, self.reset, self.NEUTRAL)
        
        #TODO: implement lose + win (in game function), and brushing hair (tbd)
        self.fsm.add_transition("time's up", self.NEUTRAL, self.lose, self.LOST)
        self.fsm.add_transition("time's up", self.IN_ACTION, self.lose, self.LOST)
        self.fsm.add_transition("time's up", self.BRUSHING_HAIR, self.lose, self.LOST)
        self.fsm.add_transition("at door", self.IN_ACTION, self.win, self.WON)

        self.fsm.add_transition("item clicked", self.NEUTRAL, self.move, self.IN_ACTION)

        self.fsm.add_transition("reached item", self.IN_ACTION, self.brush_hair, self.BRUSHING_HAIR)
        
    def get_state(self):
        return self.fsm.current_state
    
    def move (self, x=0, y=0):
        if self.rect.centerx <= x:
            self.rect.centerx += 5
        elif self.rect.centerx >= x:
            self.rect.centerx -= 5

        if self.rect.centery <= y:
            self.rect.centery += 5
        elif self.rect.centery >= y:
            self.rect.centery -= 5
     
    def update(self, input = None):
        # TODO: Use the finite state machine to process input
        self.fsm.process(input)
        # make sure to change image based on different conditions
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y))