import pygame
from math import pi

pygame.init()
size = [400, 300]
screen = pygame.display.set_mode(size)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)


### Model

class Rectangle():
    def __init__(self, x = 10, y = 10, width = 20, height = 10, color = BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    #draws the rectangles that are dropped
    def draw_rectangle(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])


    def draw_shot(self):
        self.x = self.x + 10
        self.y = self.y
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])


def menu():
    pygame.display.set_caption("Menu")


    def jump(self):
        pass


#Control
def main():
    color_matrix = [BLACK, BLUE, GREEN, RED]
    pygame.display.set_caption("Game!")
    shoot_object_list = []
    done = False
    clock = pygame.time.Clock()
    text_x = 150
    text_y = 20
    rectangles_x = 100
    rectangles_y = 100
    rectangle_list = []
    which_object = "Rectangle"
    color = 0


### CONTROL

    while not done:
        clock.tick(40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            rectangles_y += -3
        if keys[pygame.K_DOWN]:
            rectangles_y += 3
        if keys[pygame.K_LEFT]:
            rectangles_x += -3
        if keys[pygame.K_RIGHT]:
            rectangles_x += 3

        for event in pygame.event.get():  # User did something

            if event.type == pygame.QUIT:  # If user hit q or closed
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    color += 1
                    if color == 3:
                        color = 0
                if event.key == pygame.K_t:
                    which_object = "Text"
                if event.key == pygame.K_r:
                    which_object = "Rectangle"

            #control text
            if which_object == "Text":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_a:
                        text_x += -10
                    if event.key == pygame.K_d:
                        text_x += 10
                    if event.key == pygame.K_w:
                        text_y += -10
                    if event.key == pygame.K_s:
                        rectangle.jump()

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

                        #make shoot object
                        if event.key == pygame.K_f:
                            draw_rectangle_x = rectangles_x
                            draw_rectangle_y = rectangles_y
                            rectangle_color = color_matrix[color]
                            rectangle = Rectangle(draw_rectangle_x, draw_rectangle_y+5, 10, 10, rectangle_color)
                            shoot_object_list.append(rectangle)

                        #make rectangle object
                        if event.key == pygame.K_g:
                                draw_rectangle_x = rectangles_x
                                draw_rectangle_y = rectangles_y
                                rectangle_color = color_matrix[color]
                                rectangle = Rectangle(draw_rectangle_x, draw_rectangle_y+5, 10, 10, rectangle_color)
                                rectangle_list.append(rectangle)

                        #clear objects
                        if event.key == pygame.K_z:
                                rectangle_list = []

### View
        screen.fill(WHITE)
        #draw text
        myfont = pygame.font.SysFont("monospace", 15)
        text_color = (0, 0, 0)
        text_position = (text_x, text_y)
        label = myfont.render("Sean and Colvin's Game", 100, text_color)
        screen.blit(label, (text_position))

        #draw rectangle objects
        for rectangles in rectangle_list:
            rectangles.draw_rectangle()

        #draw shooter objects
        for shooters in shoot_object_list:
            shooters.draw_shot()

        #draw color matric and main rectangle
        pygame.draw.rect(screen, color_matrix[color], [rectangles_x, rectangles_y, 50, 20])
        pygame.draw.rect(screen, color_matrix[color], [0, 0, 40, 40])

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
