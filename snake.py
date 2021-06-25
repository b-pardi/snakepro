import pygame
import sys
import random
import time
from pygame.math import Vector2

# GAME LOOP #
# Get player input
# position elements
# Draw graphics

# IDEAS #
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
        screen.blit(fruit_img_scaled, fruit_rect)
        #pygame.draw.rect(screen,(0, 200, 80),fruit_rect)

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

        # load and scale all snake graphics
        self.bodyVERT = pygame.image.load("images/snake parts/body_vertical.png").convert_alpha()
        self.bodyVERT = pygame.transform.scale(self.bodyVERT, (cell_size, cell_size))
        self.bodyHOR = pygame.image.load("images/snake parts/body_horizontal.png").convert_alpha()
        self.bodyHOR = pygame.transform.scale(self.bodyHOR, (cell_size, cell_size))
        self.bodyBL = pygame.image.load("images/snake parts/body_bottomleft.png").convert_alpha()
        self.bodyBL = pygame.transform.scale(self.bodyBL, (cell_size, cell_size))
        self.bodyBR = pygame.image.load("images/snake parts/body_bottomright.png").convert_alpha()
        self.bodyBR = pygame.transform.scale(self.bodyBR, (cell_size, cell_size))
        self.bodyTL = pygame.image.load("images/snake parts/body_topleft.png").convert_alpha()
        self.bodyTL = pygame.transform.scale(self.bodyTL, (cell_size, cell_size))
        self.bodyTR = pygame.image.load("images/snake parts/body_topright.png").convert_alpha()
        self.bodyTR = pygame.transform.scale(self.bodyTR, (cell_size, cell_size))

        self.headDOWN = pygame.image.load("images/snake parts/head_down.png").convert_alpha()
        self.headDOWN = pygame.transform.scale(self.headDOWN, (cell_size, cell_size))
        self.headLEFT = pygame.image.load("images/snake parts/head_left.png").convert_alpha()
        self.headLEFT = pygame.transform.scale(self.headLEFT, (cell_size, cell_size))
        self.headRIGHT = pygame.image.load("images/snake parts/head_right.png").convert_alpha()
        self.headRIGHT = pygame.transform.scale(self.headRIGHT, (cell_size, cell_size))
        self.headUP = pygame.image.load("images/snake parts/head_up.png").convert_alpha()
        self.headUP = pygame.transform.scale(self.headUP, (cell_size, cell_size))

        self.tailDOWN = pygame.image.load("images/snake parts/tail_down.png").convert_alpha()
        self.tailDOWN = pygame.transform.scale(self.tailDOWN, (cell_size, cell_size))
        self.tailLEFT = pygame.image.load("images/snake parts/tail_left.png").convert_alpha()
        self.tailLEFT = pygame.transform.scale(self.tailLEFT, (cell_size, cell_size))
        self.tailRIGHT = pygame.image.load("images/snake parts/tail_right.png").convert_alpha()
        self.tailRIGHT = pygame.transform.scale(self.tailRIGHT, (cell_size, cell_size))
        self.tailUP = pygame.image.load("images/snake parts/tail_up.png").convert_alpha()
        self.tailUP = pygame.transform.scale(self.tailUP, (cell_size, cell_size))

        self.crunch_sfx = pygame.mixer.Sound("sfx/Bite.mp3")

    def draw_snake(self):
        self.update_head_img()
        self.update_tail_img()

        # enumerate gives each block an index so we can reference next and prev boxes
        for index, block in enumerate(self.body):
            # still need rect for position
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos,cell_size,cell_size)

            # find direction snake is heading
            # index 0 is the head of the body
            if index == 0:
                screen.blit(self.head, block_rect)
            # length - -1 is the tail
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            # last case is body
            else:
                body_prev = self.body[index - 1] - self.body[index]
                body_next = self.body[index + 1] - self.body[index]

                if body_next.x == body_prev.x:
                    screen.blit(self.bodyVERT, block_rect)
                elif body_next.y == body_prev.y:
                    screen.blit(self.bodyHOR, block_rect)
                else:
                    if (body_next.x == -1 and body_prev.y == -1) or (body_next.y == -1 and body_prev.x == -1):
                        screen.blit(self.bodyTL, block_rect)
                    elif (body_next.x == 1 and body_prev.y == -1) or (body_next.y == -1 and body_prev.x == 1):
                        screen.blit(self.bodyTR, block_rect)
                    elif (body_next.x == 1 and body_prev.y == 1) or (body_next.y == 1 and body_prev.x == 1):
                        screen.blit(self.bodyBR, block_rect)
                    elif (body_next.x == -1 and body_prev.y == 1) or (body_next.y == 1 and body_prev.x == -1):
                        screen.blit(self.bodyBL, block_rect)
            
        #for block in self.body:
            # create a rect and draw for each iteration of loop
            #x_pos = int(block.x * cell_size)
            #y_pos = int(block.y * cell_size)
            #block_rect = pygame.Rect(x_pos, y_pos,cell_size,cell_size)
            #pygame.draw.rect(screen, (0,200,200), block_rect)

    def update_head_img(self):
        # subtract first body piece pos from head piece pos to get direction facing
        head_relative = self.body[1] - self.body[0]
        # head is to left of body
        if head_relative == Vector2(1,0): self.head = self.headLEFT
        # head is to right of body
        elif head_relative == Vector2(-1, 0): self.head = self.headRIGHT
        # head is above body
        elif head_relative == Vector2(0, 1): self.head = self.headUP
        # head is below body
        elif head_relative == Vector2(0, -1): self.head = self.headDOWN

    def update_tail_img(self):
        # subtract first body piece pos from head piece pos to get direction facing
        tail_relative = self.body[len(self.body) - 2] - self.body[len(self.body) - 1]
        # head is to left of body
        if tail_relative == Vector2(1,0): self.tail = self.tailLEFT
        # head is to right of body
        elif tail_relative == Vector2(-1, 0): self.tail = self.tailRIGHT
        # head is above body
        elif tail_relative == Vector2(0, 1): self.tail = self.tailUP
        # head is below body
        elif tail_relative == Vector2(0, -1): self.tail = self.tailDOWN

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

    def play_crunch_sound(self):
        self.crunch_sfx.play()

    def reset(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(0,0)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.fruit_munch()
        self.check_snake_death()

    def draw(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def fruit_munch(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.grow_snake()
            self.snake.play_crunch_sound()
        
        for i in range(1, len(self.snake.body)):
            if self.fruit.pos == self.snake.body[i]:
                self.fruit.randomize()

    def check_snake_death(self):
        # case 1: snake hits walls
        if not (0 <= self.snake.body[0].x <= cell_number - 1) or not (0 <= self.snake.body[0].y <= cell_number - 1):
            print("game over idiot")
            self.game_over()

        # case 2: snake suicidal
        # [1:] is all elems in vector after first one
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                print("Snake aliven't")
                self.game_over()

    def draw_grass(self):
        grass_color1 = (98,160,50)
        grass_color2 = (105,170,50)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_color = grass_color1
                    else:
                        grass_color = grass_color2

                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

            else:
                for col in range(cell_number):
                    if col % 2 == 1:
                        grass_color = grass_color1
                    else:
                        grass_color = grass_color2
                        
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score = len(self.snake.body) - 3
        score_text = "Score: " + str(score)
        # text surfaces pass in str to display, anti alias or not, and color
        score_color = (10, 50, 40)
        score_surface = snake_font.render(score_text, True, score_color)

        # blit the text surface and position with bg surface
        score_xpos = int(cell_size * cell_number + 120)
        score_ypos = 25
        score_rect = score_surface.get_rect(center = (score_xpos, score_ypos))

        score_bg_rect = pygame.Rect(score_rect.left-2, score_rect.top-2, score_rect.width+4, score_rect.height+4)
        score_bg_color = (90,145,40)
        pygame.draw.rect(screen, score_bg_color, score_bg_rect)
        pygame.draw.rect(screen, score_color, score_bg_rect, 2)
        screen.blit(score_surface,score_rect)
    
    def game_over(self):
        time.sleep(0.25)
        print("You Lost!")
        self.snake.reset()


# this prepares sound so there's no delay
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
# Set Display using a tuple for width and height
cell_size = 30
cell_number = 18
# Display surface, only one of which can exist. Displayed by default
screen = pygame.display.set_mode((cell_number * cell_size + 240, cell_number * cell_size))

clock = pygame.time.Clock()
fps = 60

# load fruit image and convert it to format pygame can use more efficiently
fruit_img = pygame.image.load("images/fruit.png").convert_alpha()
fruit_img_scaled = pygame.transform.scale(fruit_img, (cell_size, cell_size))

# fonts!
font_size = 35
snake_font = pygame.font.Font("fonts/Snake Chan.ttf", font_size)

# create event for timer
SCREEN_UPDATE = pygame.USEREVENT
# timer set for 150 ms
pygame.time.set_timer(SCREEN_UPDATE, 150)
# Fixes bug that snake would be able to turn two directions before next tick
did_screen_update = False

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
            did_screen_update = True
        
        # checks for any keypresses
        if event.type == pygame.KEYDOWN:
            # checks for specific key presses
            if event.key == pygame.K_UP:
                # makes sure snake isn't going opp. dir. so it doesn't 180 into itself
                if main_game.snake.direction.y != 1 and did_screen_update == True:
                    main_game.snake.direction = Vector2(0,-1)
                    did_screen_update = False
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1 and did_screen_update == True:
                    main_game.snake.direction = Vector2(0,1)
                    did_screen_update = False
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1 and did_screen_update == True:
                    main_game.snake.direction = Vector2(1,0)
                    did_screen_update = False
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1 and did_screen_update == True:
                    main_game.snake.direction = Vector2(-1,0)
                    did_screen_update = False
            

    # screen with color using RGB Tuple
    BG_color = (90,145,40)
    screen.fill(BG_color)

    main_game.draw()

    # Drawing and updating all our elements here
    pygame.display.update()
    # Making sure game runs consistently at 60 fps to account for faster/slower machines exectuing oop at different speeds
    clock.tick(fps)