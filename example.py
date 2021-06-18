import pygame
import sys

# GAME LOOP #
# Get player input
# position elements
# Draw graphics


pygame.init()
# Set Display using a tuple for width and height
width = 600
height = 500
# Display surface, only one of which can exist. Displayed by default
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
fps = 60

# all surfaces except display must have code written in game loop to show them
test_surface = pygame.Surface((200,150))
test_surface.fill((0,80,200))
# rectangles can be manipulated more, pass in x, y, width, height
#test_rect = pygame.Rect(100,200,100,100)

test_rect = test_surface.get_rect(center = (300,250))

x_pos = 50
y_pos = 50

while True:
    # Checks all possible events before launching game
    for event in pygame.event.get():
        # quits game and exits all code upon closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # screen with color using RGB Tuple
    screen.fill((0, 200, 200))

    pygame.draw.rect(screen, pygame.Color('gray'), test_rect)

    # block image transfer to display previously created surface with its x, y position
    test_rect.left += 1
    screen.blit(test_surface, test_rect)

    # Drawing and updating all our elements here
    pygame.display.update()
    # Making sure game runs consistently at 60 fps to account for faster/slower machines exectuing oop at different speeds
    clock.tick(fps)