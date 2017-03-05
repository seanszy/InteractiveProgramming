import pygame
from math import pi

pygame.init()
size = [1840, 920]
screen = pygame.display.set_mode(size)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  20, 255,   20)
RED =   (255,   0,   0)
block_size = 40
color_matrix = [BLACK, BLUE, GREEN, RED]
text_x = 20
text_y = 200
### Model

class Rectangle():
    def __init__(self, x=10, y=10, width=20, height=10, color=BLUE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    #draws the rectangles that are dropped
    def draw_rectangle(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
    def draw_with_outline(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 1)


    def draw_shot(self):
        self.x = self.x + 1
        self.y = self.y
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

class Field():
    def __init__(self, num_rows=3, color=0):
        self.blocks = []

        for row in range(num_rows):
            for column in range(int(size[0]/block_size)):
                rectangle_color = color_matrix[color]
                block = Rectangle(column*block_size, size[1]-block_size*row - block_size,
                              block_size, block_size, rectangle_color)
                self.blocks.append(block)

class Player():
    def __init__(self, x=40, y=0, width=40, height=80, color=GREEN, velocity=0, fall='on', left='off', right='off'):
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

class Text():
    def __init__(self, text, x_pos, y_pos, size, color):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = size
        self.color = color
    def print_text(self):
        font = pygame.font.SysFont("monospace", self.size)
        label = font.render(self.text, 40, self.color)
        screen.blit(label, (self.x_pos, self.y_pos))

def menu():
    menu_screen = True
    done = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # If user hit q or closed")
                done = True
            if event.key == pygame.K_p:
                menu_screen = False
            #if event.key == pygame.K_r:
            #    player = Player()
    screen.fill(WHITE)
    text_list = []
    text1 = Text("Sean and Colvin's Game", 150, 50, 100, RED)
    text2 = Text("Instructions:", 50, 250, 60, BLUE)
    text3 = Text("-Press Left or Right to Move", 100, 350, 60, BLACK)
    text4 = Text("-Press J to Jump", 100, 450, 60, BLACK)
    text5 = Text("-Press Q to Quit", 100, 550, 60, BLACK)
    text7 = Text("-Your Inventory is in the upper left. Cycle through which item to drop by pressing 1, 2, and 3", 100, 700, 30, BLACK)
    text8 = Text("-Add items to that slot by pressing E, and drop them into the world by pressing R", 100, 800, 30, BLACK)
    text9 = Text("-Which Block you will drop is shown by the \"Current Block\" space in your inventory", 100, 750, 30, BLACK)
    #text6 = Text("Press R to Restart the Game", 100, 650, 60, RED)
    text6 = Text("While In Game Press P to Return to Game", 100, 850, 60, RED)
    text_add_list = [text1, text2, text3, text4, text4, text5, text6, text7, text8, text9]
    for texts in text_add_list:
        text_list.append(texts)
    for texts in text_list:
        texts.print_text()
    return [menu_screen, done]

class Inventory():
    def __init__(self, init_quantity, x_pos, y_pos, bin_height, bin_width):#, init_quantity, x_pos = 20, y_pos, bin_height, bin_width):
        bin_list = [0, 0, 0]
        bin_list_item = [RED, BLACK, GREEN]
        self.init_quantity = init_quantity
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.bin_list = bin_list
        self.bin_list_item = bin_list_item
    def add_to_inventory(self, block_type):
        self.bin_list[block_type] += 1

    def remove_from_inventory(self, field, block_type, player_x, player_y, current_block_index):
        if self.bin_list[block_type] > 0:
            self.bin_list[block_type] -= 1
            drop_block = Rectangle(player_x, player_y, 40, 40, self.bin_list_item[current_block_index])
            field.blocks.append(drop_block)

    def draw_inventory(self, field,  current_block_index):
        text = Text("Inventory:", self.x_pos, self.y_pos-20, 20, RED)
        text.print_text()
        for bin in range(len(self.bin_list)):
            rectangle = Rectangle(self.x_pos, self.y_pos + bin*self.bin_width, self.bin_width, self.bin_height, self.bin_list_item[bin])
            rectangle.draw_rectangle()
            text = Text(str(self.bin_list[bin]), self.x_pos+ 5, self.y_pos + bin*self.bin_width, 40, WHITE)
            text.print_text()
        text2 = Text("Current Block:", self.x_pos, self.y_pos + bin*self.bin_width+60, 20, RED)
        text2.print_text()
        current_block = Rectangle(self.x_pos, self.y_pos + bin*self.bin_width + 80, self.bin_width, self.bin_height, self.bin_list_item[current_block_index])
        current_block.draw_rectangle()


#Control
def main():
    #color_matrix = [BLACK, BLUE, GREEN, RED]
    pygame.display.set_caption("Game!")
    shoot_object_list = []
    clock = pygame.time.Clock()
    rectangles_x = 100
    rectangles_y = 100
    rectangle_list = []
    player_color = 0
    menu_screen = True
    done = False
    player = Player()
    field = Field()
    inventory = Inventory(0, 0, 20, 40, 40)
    inventory_block_index = 0
### CONTROL
    while not done:
        player.fall = 'on'
        if menu_screen is True:
            returned = menu()
            menu_screen = returned[0]
            done = returned[1]
        if menu_screen is False:
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

            if player.y >= 720:
                player.y = 720
                player.fall = 'off'


            for event in pygame.event.get():  # User did something

                if event.type == pygame.QUIT:  # If user hit q or closed
                    done = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        menu_screen = True
                    if event.key == pygame.K_c:
                        player_color += 1
                        if player_color == 3:
                            player_color = 0
                        player.color = color_matrix[player_color]

                    # inventory
                    if event.key == pygame.K_e:
                        inventory.add_to_inventory(inventory_block_index)
                    if event.key == pygame.K_r:
                        inventory.remove_from_inventory(field, inventory_block_index, player.x, player.y, inventory_block_index)
                    if event.key == pygame.K_1:
                        inventory_block_index = 0
                    if event.key == pygame.K_2:
                        inventory_block_index = 1
                    if event.key == pygame.K_3:
                        inventory_block_index = 2

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

            # draw text

            # draw rectangle objects
            for rectangles in rectangle_list:
                rectangles.draw_with_outline()

            # draw shooter objects
            for shooters in shoot_object_list:
                shooters.draw_shot()

            # draw color matric and main rectangle
            for block in field.blocks:
                block.draw_with_outline()

            inventory.draw_inventory(field, inventory_block_index)
            player.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
