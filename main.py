import pygame, os, math
from random import randint, choice, uniform

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_a,
    K_p,
    K_w,
    K_DOWN,
)

pygame.init()

global screensize
screensize = (1400, 800)
global playersize
playersize = (10, 150)
global ballsize
ballsize = (10, 10)
ball_coef = 1.1
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screensize)
background = pygame.image.load(os.path.join('images', 'background.jpg'))
background = pygame.transform.scale(background, screensize)

pygame.font.init()
scoreFont = pygame.font.SysFont('Comic Sans MS', math.floor(screensize[1]/8))

def update():
        global running
        # Look at every event in the queue
        for event in events:
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_w:
                    ball.reset()
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

def display():
        screen.blit(background, (0, 0))

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, dir: int, key):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.dir = dir
        self.size = playersize
        self.color = "black"
        self.scoreTextList = [scoreFont.render(str(score), False, (0, 0, 0)) for score in range(0, 10)]
        self.key = key
        self.score = 0
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dir = dir
    def update(self):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == self.key:
                    self.dir = (self.dir[0], -self.dir[1])
        if self.rect.y + self.dir[1] + self.size[1] > screensize[1] or self.rect.y + self.dir[1] < 0:
            self.dir = (self.dir[0], -self.dir[1])
        dx, dy = self.dir
        self.rect.x += dx
        self.rect.y += dy
    def display(self):
        if self.x < screensize[0] / 2: # player1
            screen.blit(self.scoreTextList[self.score], (screensize[0]/4, screensize[1]/16))
        else: # player2
            screen.blit(self.scoreTextList[self.score], (screensize[0]/4 + screensize[0]/2, screensize[1]/16))
        pygame.draw.rect(screen, self.color, self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int):
        pygame.sprite.Sprite.__init__(self)
        self.color = "white"
        self.size = ballsize
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.initial_speed = speed
        self.reset()
    def reset(self):
        # reset pos
        self.rect.x = screensize[0]/2
        self.rect.y = screensize[1]/2
        # reset dir
        angle = uniform(0.3, 1.3)
        self.dir = (self.initial_speed * math.cos(angle), self.initial_speed * math.sin(angle))
        self.dir = (self.dir[0] * choice([1, -1]), self.dir[1] * choice([1, -1]))
        print(f'scores: Player1: {player1.score}, Player2: {player2.score}')
    def update(self):
        if self.rect.y + self.dir[1] + self.size[1] > screensize[1] or self.rect.y + self.dir[1] < 0:
            self.dir = (ball_coef*self.dir[0], -ball_coef*self.dir[1])
        if self.rect.x + self.dir[0] + self.size[0] + ballsize[0] > screensize[0] or self.rect.x + self.dir[0] - ballsize[0] < 0:
            if self.rect.x < screensize[0]/2: # left player is concerned
                if self.rect.y - self.size[1] > player1.rect.y and self.rect.y < player1.rect.y + player1.size[1]:
                    print('player1 got the ball!')
                else:
                    print('player1 didn\'t get the ball...')
                    player2.score += 1
                    self.reset()
            else: # right player is concerned
                if self.rect.y - self.size[1] > player2.rect.y and self.rect.y < player2.rect.y + player2.size[1]:
                    print('player2 got the ball!')
                else:
                    print('player2 didn\'t get the ball...')
                    player1.score += 1
                    self.reset()
            self.dir = (-ball_coef*self.dir[0], ball_coef*self.dir[1])
        dx, dy = self.dir
        self.rect.x += dx
        self.rect.y += dy
    def display(self):
        pygame.draw.rect(screen, self.color, self.rect)

player1 = Player(0, 0, (0, 4), K_a)
player2 = Player(screensize[0]-playersize[0], 0, (0, 4), K_p)
ball = Ball(screensize[0]/2, screensize[1]/2, 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

while running:
    events = pygame.event.get()
    update()
    display()
    all_sprites.update()
    for sprite in all_sprites:
        sprite.display()
    
    clock.tick(60) # make game slow until it reaches 30 fps
    
    
    pygame.display.set_caption(str(round(clock.get_fps()))) # set the name of the pygame window to the number of fps
    pygame.display.flip() # Flip the display SUPER IMPORTANT, renders the screen

pygame.quit()