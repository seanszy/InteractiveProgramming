import pygame
from math import pi

pygame.init()
size = [1840, 920]
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
        self.x = self.x + 1
        self.y = self.y
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])


class Player():
    def __init__(self, x=40, y=10, width=40, height=80, color=GREEN, velocity=0, fall='on', left='off', right='off'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = velocity
        self.fall = fall
        self.left = left
        self.right = right
        self.acceleration_constant = .6


    # draws the rectangles that are dropped
    def draw(self):
        if self.fall == 'on':
            self.velocity += self.acceleration_constant

        if self.left == 'on':
            self.x += -4

        if self.right == 'on':
            self.x += 4

        self.y = self.y + self.velocity
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])


    def draw_shot(self):
        self.x = self.x + 10
        self.y = self.y
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])


    def jump(self):
        self.velocity = -8
        self.fall = 'on'


def menu():
    pygame.display.set_caption("Menu")


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
    color = 0

    player = Player()

### CONTROL

    while not done:
        clock.tick(40)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.jump()
        if keys[pygame.K_DOWN]:
            rectangles_y += 3
        if keys[pygame.K_LEFT]:
            player.left = 'on'
        else:
            player.left = 'off'

        if keys[pygame.K_RIGHT]:
            player.right = 'on'
        else:
            player.right = 'off'

        if player.y >= 740:
            player.y = 740
            player.fall = 'off'

        for event in pygame.event.get():  # User did something

            if event.type == pygame.QUIT:  # If user hit q or closed
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    color += 1
                    if color == 3:
                        color = 0
                    player.color = color_matrix[color]

                # make shoot object
                if event.key == pygame.K_f:
                    draw_rectangle_x = player.x
                    draw_rectangle_y = player.y
                    rectangle_color = color_matrix[color]
                    rectangle = Rectangle(draw_rectangle_x, draw_rectangle_y+5, 10, 10, rectangle_color)
                    shoot_object_list.append(rectangle)

                # make rectangle object
                if event.key == pygame.K_g:
                        draw_rectangle_x = player.x
                        draw_rectangle_y = player.y
                        rectangle_color = color_matrix[color]
                        rectangle = Rectangle(draw_rectangle_x, draw_rectangle_y+5, 10, 10, rectangle_color)
                        rectangle_list.append(rectangle)

                # clear objects
                if event.key == pygame.K_z:
                        rectangle_list = []
                        shoot_object_list = []

                if event.key == pygame.K_q:
                    pygame.quit()
                    return

        # View-------------------------------------------------------------
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
        pygame.draw.rect(screen, color_matrix[color], [0, 0, 40, 40])
        player.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
