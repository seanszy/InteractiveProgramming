import pygame

import pygame
from math import pi

######################
#Model
######################

pygame.init()
size = [400, 300]
screen = pygame.display.set_mode(size)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

class Rectangle():
    def __init__(self, x = 10, y = 10, width = 20, height = 10, color = BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    def draw_rectangle(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
    def draw_shot(self):
        self.x = self.x + 10
        self.y = self.y
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

def main():
    # Initialize the game engine
    pygame.init()

    # Define the colors we will use in RGB format
    color_matrix = [BLACK, BLUE, GREEN, RED]
    # Set the height and width of the screen
    size = [400, 300]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Example code for the draw module")
    shoot_object_list = []
    #Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()
    text_x = 150
    text_y = 20
    rectangles_x = 100
    rectangles_y = 100
    rectangle_list = []
    which_object = "Rectangle"
    color = 0
    draw_rectangle = 0
    while not done:
        clock.tick(10)
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    color+=1
                    if color == 3:
                        color = 0
                if event.key == pygame.K_t:
                    which_object = "Text"
                if event.key == pygame.K_r:
                    which_object = "Rectangle"
            if which_object == "Text":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_a:
                        text_x +=-10
                    if event.key == pygame.K_d:
                        text_x+=10
                    if event.key == pygame.K_w:
                        text_y += -10
                    if event.key == pygame.K_s:
                        text_y += 10
            if which_object == "Rectangle":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            done = True
                        if event.key == pygame.K_a:
                            rectangles_x +=-10
                        if event.key == pygame.K_d:
                            rectangles_x+=10
                        if event.key == pygame.K_w:
                            rectangles_y += -10
                        if event.key == pygame.K_s:
                            rectangles_y += 10
                        if event.key == pygame.K_f:
                            draw_rectangle_x = rectangles_x
                            draw_rectangle_y = rectangles_y
                            rectangle_color = color_matrix[color]
                            rectangle = Rectangle(draw_rectangle_x, draw_rectangle_y+5, 10, 10, rectangle_color)
                            shoot_object_list.append(rectangle)
                        if event.key == pygame.K_g:
                                draw_rectangle_x = rectangles_x
                                draw_rectangle_y = rectangles_y
                                rectangle_color = color_matrix[color]
                                rectangle = Rectangle(draw_rectangle_x, draw_rectangle_y+5, 10, 10, rectangle_color)
                                rectangle_list.append(rectangle)
                        if event.key == pygame.K_z:
                                rectangle_list = []


        ##########################
        #VIEW
        ##########################
        screen.fill(WHITE)
        myfont = pygame.font.SysFont("monospace", 15)
        keys=pygame.key.get_pressed()
        text_color = (0, 0, 0)
        text_position = (text_x, text_y)
        label = myfont.render("Sean and Colvin's Game", 100, text_color)
        screen.blit(label, (text_position))
        for rectangles in rectangle_list:
            rectangles.draw_rectangle()
        for shooters in shoot_object_list:
            shooters.draw_shot()
        pygame.draw.rect(screen, BLACK, [rectangles_x, rectangles_y, 50, 20])
        pygame.draw.rect(screen, color_matrix[color], [0, 0, 20, 40])

        pygame.display.flip()

    # Be IDLE friendly
    pygame.quit()


if __name__ == '__main__':
    main()
