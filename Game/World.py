import pygame
from math import pi

pygame.init()
screen_x = 1840
screen_y = 920
block_size = 40
size = [1840, 920]
screen = pygame.display.set_mode(size)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
color_matrix = [BLACK, BLUE, GREEN, RED]


class Block():
    def __init__(self, x=10, y=10, width=block_size, height=block_size, color=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    # draws the rectangles that are dropped
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width,
                                              self.height], 1)


class Field():
    def __init__(self, num_rows=3, color=0):
        self.blocks = []

        for z in range(num_rows):
            for i in range(int(screen_x/block_size)):
                rectangle_color = color_matrix[color]
                block = Block(i*block_size, screen_y-block_size*z - block_size,
                              block_size, block_size, rectangle_color)
                self.blocks.append(block)


# Control
def main():
    pygame.display.set_caption("Game!")
    done = False
    clock = pygame.time.Clock()
    field = Field()

    # Main Loop
    while not done:
        clock.tick(40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True


        # VIEW-------------------------------------------------------------------
        screen.fill((150, 190, 255))

        # draw rectangle objects
        for block in field.blocks:
            block.draw()

        # draw color matric and main rectangle
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
