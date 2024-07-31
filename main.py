import pygame, os

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
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screensize)
background = pygame.image.load(os.path.join('images', 'background.jpg'))
background = pygame.transform.scale(background, screensize)

def update():
        global running
        events = pygame.event.get()
        # Look at every event in the queue
        for event in events:
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

def display():
        screen.blit(background, (0, 0))

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, dir: int):
        self.x = x
        self.y = y
        self.dir = dir
        self.size = (x, y)
        self.color = "black"
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.dir = dir
    def update(self):
        if self.rect.y + self.dir[1] + self.size[1] > screensize[1] or self.rect.y + self.dir[1] < 0:
            self.dir = (self.dir[0], self.dir[1])
        dx, dy = self.dir
        self.rect.x += dx
        self.rect.y += dy
    def draw (self):
        pygame.draw.rect(screen, self.color, self.rect)

player1 = Player(10, 150, (0, 8))
# all_sprites = pygame.sprite.Group()
# all_sprites.add(player1)

while running:
    update()
    display()
    player1.update()
    player1.draw()
    # all_sprites.update()
    # all_sprites.draw(screen)
    
    clock.tick(30) # make game slow until it reaches 30 fps
    
    
    pygame.display.set_caption(str(round(clock.get_fps()))) # set the name of the pygame window to the number of fps
    pygame.display.flip() # Flip the display SUPER IMPORTANT, renders the screen

pygame.quit()