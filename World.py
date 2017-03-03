import pygame
from math import pi

pygame.init()
screen_x = 1840
screen_y = 920
size = [1840, 920]
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

    #draws the rectangles that are dropped
    def draw_rectangle(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 1)

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
    draw_rectangle = 0

    #Main Loop
    while not done:
        clock.tick(10)

        #quit, change color, and change from controlling rect to text
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done=True
        num_rows = 3
        for z in range(num_rows):
            for i in range(int(screen_x/40)):
                pass
                draw_rectangle_x = rectangles_x
                draw_rectangle_y = rectangles_y
                rectangle_color = color_matrix[color]
                rectangle = Rectangle(i*40, screen_y-40*z - 40, 40, 40, rectangle_color)
                rectangle_list.append(rectangle)


        #VIEW-------------------------------------------------------------------
        screen.fill(WHITE)

        #draw rectangle objects
        for rectangles in rectangle_list:
            rectangles.draw_rectangle()

        #draw color matric and main rectangle
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
