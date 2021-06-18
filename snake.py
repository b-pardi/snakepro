import pygame
import sys
import random
from pygame.math import Vector2

# GAME LOOP #
# Get player input
# position elements
# Draw graphics

# IDEAS #
# snake can't turn opposite direction (it would crash into itself)
# Difficulty increases speed and grid density as well as fruit spawns far away
# Walls commit the murder
# fruit shouldn't appear where snake currently is

class Fruit:
    # initialize Fruit object using position as a 2D vector
    def __init__(self):
        self.randomize()

    # create and draw rectangle for fruit
    def draw_fruit(self):
        # fruit rectangle needs x pos, y pos, width, and height
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size), cell_size, cell_size)
        #screen.blit(fruit_img, fruit_rect)
        pygame.draw.rect(screen,(0, 200, 80),fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        # pygame.math. >
        self.pos = Vector2(self.x,self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(1,0)
        self.add_block = False

    def draw_snake(self):
        for block in self.body:
            # create a rect and draw for each iteration of loop
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos,cell_size,cell_size)
            pygame.draw.rect(screen, (0,200,200), block_rect)

    # to move snake, move head to desired direction, then make each block follow previous blocks location
    def move_snake(self):
        if self.add_block == True:
            body_cur = self.body[:]
            body_cur.insert(0, body_cur[0] + self.direction)
            self.body = body_cur[:]
            self.add_block = False
        else:
            # [:] copies whole self.body list, [:-1] copies all but 1 element from the end
            body_cur = self.body[:-1]
            body_cur.insert(0, body_cur[0] + self.direction)
            self.body = body_cur[:]

    def grow_snake(self):
        self.add_block = True

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.fruit_munch()
        self.check_snake_death()

    def draw(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def fruit_munch(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.grow_snake()

    def check_snake_death(self):
        # case 1: snake hits walls
        if not (0 <= self.snake.body[0].x <= cell_number - 1) or not (0 <= self.snake.body[0].y <= cell_number - 1):
            print("game over loser")

        # case 2: snake suicidal
        # [1:] is all elems in vector after first one
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                print("Snake aliven't")
        

pygame.init()
# Set Display using a tuple for width and height
cell_size = 30
cell_number = 20
# Display surface, only one of which can exist. Displayed by default
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

clock = pygame.time.Clock()
fps = 60

# load fruit image and convert it to format pygame can use more efficiently
fruit_img = pygame.image.load("images/fruit.png").convert_alpha()

# create event for timer
SCREEN_UPDATE = pygame.USEREVENT
# timer set for 150 ms
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while True:
    # Checks all possible events before launching game
    for event in pygame.event.get():
        # quits game and exits all code upon closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == SCREEN_UPDATE:
            main_game.update()
        
        # checks for any keypresses
        if event.type == pygame.KEYDOWN:
            # checks for specific key presses
            if event.key == pygame.K_UP:
                # makes sure snake isn't going opp. dir. so it doesn't 180 into itself
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            

    # screen with color using RGB Tuple
    screen.fill((0, 80, 80))

    main_game.draw()

    # Drawing and updating all our elements here
    pygame.display.update()
    # Making sure game runs consistently at 60 fps to account for faster/slower machines exectuing oop at different speeds
    clock.tick(fps)