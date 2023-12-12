import pygame
from fsm import FSM

class GameBot(pygame.sprite.Sprite):
    # States
    NEUTRAL, IN_ACTION, WALKING, WON, LOST, BRUSHING_HAIR, CHANGING = "n", "ia", "wa", "wo", "l", "bh", "ch"

    def __init__(self, game, x=50, y=50):
        super().__init__()

        self.game = game

        # Load initial image
        self.images = [pygame.image.load("images/messyneutral.png"), pygame.image.load("images/messypink.png"), pygame.image.load("images/messypurple.png"), pygame.image.load("images/neutral_girl.png"), pygame.image.load("images/girlhotpink.png"), pygame.image.load("images/girlpurple.png")]
        for i in range (6):
            self.images[i] = pygame.transform.scale(self.images[i], (110, 180))
            self.rect = self.images[i].get_rect()

        # Clothing index
        self.indx = 0

        self.winner = False
        self.game_over = False

        # Set rectangle
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.rect.centerx = x
        self.rect.centery = y

        # Creates the Bot's finite state machine (self.fsm) with initial state
        self.fsm = FSM(self.NEUTRAL)
        self.init_fsm()
    
    def init_fsm(self):
        # Add more here for the other states with actions
        self.fsm.add_transition("action complete", self.BRUSHING_HAIR, None, self.NEUTRAL)
        self.fsm.add_transition("action complete", self.CHANGING, None, self.NEUTRAL)

        #TODO: implement lose + win (in game function), and brushing hair (tbd)
        self.fsm.add_transition("time's up", self.NEUTRAL, self.lose, self.LOST)
        self.fsm.add_transition("time's up", self.IN_ACTION, self.lose, self.LOST)
        self.fsm.add_transition("time's up", self.BRUSHING_HAIR, self.lose, self.LOST)
        self.fsm.add_transition("time's up", self.CHANGING, self.lose, self.LOST)
        self.fsm.add_transition("at door", self.IN_ACTION, self.win, self.WON)

        self.fsm.add_transition(None, self.IN_ACTION, self.move, self.IN_ACTION)
        self.fsm.add_transition(None, self.NEUTRAL, None, self.NEUTRAL)
        self.fsm.add_transition(None, self.BRUSHING_HAIR, None, self.BRUSHING_HAIR)
        self.fsm.add_transition(None, self.CHANGING, None, self.CHANGING)
        self.fsm.add_transition(None, self.WON, self.win, self.WON)
        self.fsm.add_transition(None, self.LOST, self.lose, self.LOST)


        self.fsm.add_transition("item clicked", self.NEUTRAL, self.move, self.IN_ACTION)
        self.fsm.add_transition("item clicked", self.BRUSHING_HAIR, None, self.BRUSHING_HAIR)
        self.fsm.add_transition("item clicked", self.CHANGING, None, self.CHANGING)

        self.fsm.add_transition("reached brush", self.IN_ACTION, self.brush_hair, self.BRUSHING_HAIR)
        self.fsm.add_transition("reached shirts", self.IN_ACTION, self.change, self.CHANGING)
        
    def get_state(self):
        return self.fsm.current_state
    
    def move(self):
        x = self.game.last_clickedx
        y = self.game.last_clickedy
        if self.rect.x < x:
            self.rect.x += 3
        elif self.rect.x > x:
            self.rect.x -= 3

        if self.rect.y < y and self.rect.y + self.height < 540:
            self.rect.y += 3
        elif self.rect.y > y:
            self.rect.y -= 3

    def brush_hair(self):
        if self.indx < 3:
            self.indx += 3
    
    def change(self):
        if self.indx < 2:
            self.indx += 1
        elif self.indx == 2:
            self.indx = 0
        elif self.indx < 5:
            self.indx += 1
        elif self.indx == 5:
            self.indx = 3

    def lose(self):
        self.game_over = True

    def win(self):
        self.game_over = True
        self.winner = True
     
    def update(self, input = None):
        print(input, self.fsm.current_state)
        self.fsm.process(input)
    
    def draw(self, screen):
        screen.blit(self.images[self.indx], (self.rect.x , self.rect.y))
