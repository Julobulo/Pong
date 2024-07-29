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

running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1400, 800))
background = pygame.image.load(os.path.join('images', 'background.jpg'))
background = pygame.transform.scale(background, (1400, 800))

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

while running:
    update()
    display()
    
    clock.tick(30) # make game slow until it reaches 30 fps
    
    pygame.display.set_caption(str(round(clock.get_fps()))) # set the name of the pygame window to the number of fps
    pygame.display.flip() # Flip the display SUPER IMPORTANT, renders the screen

pygame.quit()