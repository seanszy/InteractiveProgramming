import pygame

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
jump = 0


### Model
class Rectangle():
    """Used when initializing block objects. These block objects are later put into the field matrix.
    has atributes for:
    x and y position   -  the upper-left pixel of each block
    width and height of the block
    color of block as an RGB value
    """
    def __init__(self, x=10, y=10, width=20, height=10, color=BLUE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    #draws the rectangles that are dropped
    def draw_rectangle(self):
        """Uses pygame to draw the rectangle on the screen
        -filled solid with color
        """
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

    def draw_with_outline(self):
        """Uses pygame to draw the rectangle on the screen
        -as a colored outline
        """
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 1)


class Field():
    """ Used when creating and storing the blocks in the field.
    Contains following atributes:
    blocks - a list of block objects
    matrix - a matrix with each value equal to the block type in that position
           - This is helpful because you don't need to iterate through every
             block on the map to look for collisions
             """
    def __init__(self, num_rows=4, color=0):
        """ initializing field using an algorithm"""
        self.blocks = []
        self.matrix = []
        inner = []
        for i in range(size[1]//40+1):
            inner = []
            self.matrix.append(inner)
            for j in range(size[0]//40+1):
                inner.append(0)
        for row in range(num_rows):
            for column in range(int(size[0]/block_size)):
                if row == 3:
                    self.matrix[row+19][column] = 9
                else:
                    self.matrix[row+19][column] = row+1
                    # setting up the trmpoline
        self. matrix[18][15] = 4

    def matrix_update(self, block_type):
        """Uses the block objects in the list of blocks to update the matrix
        used to detect collisions"""
        for block in self.blocks:
            self.matrix[int(block.y//block_size)][int(block.x//block_size)] = block_type
            self.blocks.remove(block)

    def matrix_print(self):
        """Prints the matrix in a format that is easy to read"""
        print("Matrix")
        for rows in self.matrix:
            print(rows, ",")

class Player():
    """Contains Atributes and Methods regarding the player's position,
    appearance, and motion.
        """

    def __init__(self, x=40, y=700, width=40, height=80, color=0, velocity=0,
                 fall='on', left='off', right='off', jump=0):
        """The first 5 atributes are the same as the Rectangle class above.
        velocity - change in y position for each time step.
        acceleration_constant - change in velocity if falling
        fall - whether the player should be falling
        jump - whether the player is allowed to jump or not
            """
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
        self.jump = jump

    def bottom_collision(self, field, next_y):
        """ stops the player's downward movement if his vertical position is
        colliding with a block."""
        """Also makes the player bounce if this block is a trmpoline"""
        self.jump = 0
        block_below = field.matrix[int(self.ygrid+2)][int(self.xgrid)]
        block_below_right = field.matrix[int(self.ygrid+2)][int(self.xgrid+1)]
        if self.x % 40 == 0:
            if block_below != 0:
                self.fall = "off"
                self.velocity = 0
                self.y = (self.ygrid)*40
                self.jump = 1
                if block_below == 4:
                    self.super_jump()
        elif block_below != 0 or block_below_right != 0:
            self.fall = "off"
            self.velocity = 0
            self.y = (self.ygrid)*40
            self.jump = 1
            if block_below == 4 or block_below_right == 4:
                self.super_jump()

    def left_collision(self, field):
        """Prohibits leftward movement if it would bring the player inside a
        block or outside the screen."""
        if self.x%40 == 0:
            if self.y%40 == 0:
                if field.matrix[int(self.ygrid)][int(self.xgrid-1)] != 0 or field.matrix[int(self.ygrid+1)][int(self.xgrid-1)] != 0:
                    return False
                else:
                    return True
            elif field.matrix[int(self.ygrid)][int(self.xgrid-1)] != 0 or field.matrix[int(self.ygrid+1)][int(self.xgrid-1)] != 0 or field.matrix[int(self.ygrid+2)][int(self.xgrid-1)] != 0:
                return False
            else:
                return True
        else:
            return True

    def right_collision(self, field):
        """Prohibits leftward movement if it would bring the player inside a
        block or outside the screen."""
        if self.x%40 == 0:
            if self.y%40 == 0:
                if field.matrix[int(self.ygrid)][int(self.xgrid+1)] != 0 or field.matrix[int(self.ygrid+1)][int(self.xgrid+1)] != 0:
                    return False
                else:
                    return True
            elif field.matrix[int(self.ygrid)][int(self.xgrid+1)] != 0 or field.matrix[int(self.ygrid+1)][int(self.xgrid+1)] != 0 or field.matrix[int(self.ygrid+2)][int(self.xgrid+1)] != 0:
                return False
            else:
                return True
        else:
            return True

    def top_collision(self, field):
        if self.x % 40 == 0:
            if field.matrix[int(self.ygrid)][int(self.xgrid)] != 0:
                self.y = (self.ygrid+1)*40
                self.velocity = self.velocity * -.5
        elif field.matrix[int(self.ygrid)][int(self.xgrid)] != 0 or field.matrix[int(self.ygrid)][int(self.xgrid+1)] != 0:
            self.velocity = self.velocity * -.5
            self.y = (self.ygrid+ 1)*40

    def player_in_grid(self):
        self.xgrid = self.x//block_size
        self.ygrid = self.y//block_size

    def draw(self, amon_picture, sean, colvin):
        if self.fall == 'on':
            self.velocity += self.acceleration_constant

        if self.left == 'on':
            self.x += -4

        if self.right == 'on':
            self.x += 4

        self.y = self.y + self.velocity
        #pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
        print(self.color)
        if self.color == 0:
            screen.blit(amon_picture,(self.x,self.y))
        if self.color == 1:
            screen.blit(sean,(self.x,self.y))
        if self.color == 2:
            screen.blit(colvin,(self.x,self.y))

    def jumps(self):
        self.velocity = -9
        self.fall = 'on'

    def super_jump(self):
        self.velocity = -13
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

def menu(previous_level_select):
    level_select = "Menu"
    done = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # If user hit q or closed")
                done = True
            if previous_level_select is "unknown":
                if event.key == pygame.K_8:
                    level_select = "Level_One"
                if event.key == pygame.K_9:
                    level_select = "Level_Two"
                if event.key == pygame.K_p:
                    level_select = "Level_One"
            else:
                print("going previous", previous_level_select)
                if event.key == pygame.K_p:
                    level_select = previous_level_select
            #if event.key == pygame.K_r:
            #    player = Player()
    screen.fill(WHITE)
    text_list = []
    text1 = Text("Bounce Bounce Play Time", 150, 50, 100, RED)
    text2 = Text("Instructions:", 50, 200, 60, BLUE)
    text3 = Text("-This is a rudimentary version of Minecraft. Use w, a, s, d to move.", 100, 300, 30, BLACK)
    text4 = Text("-You can move around the world and change the blocks within it.", 100, 350, 30, BLACK)
    text5 = Text("-Your inventory is in the upper left. Cycle through which item to drop with 1, 2, 3, and 4", 100, 400, 30, BLACK)
    text6 = Text("-Use left click to pick up items and right click to drop them", 100, 450, 30, BLACK)
    text7 = Text("-Which block you will drop is shown by the \"Current Block\" space in your inventory", 100, 500, 30, BLACK)
    text8 = Text("-There are multiple worlds to choose from. Press 8 or 9 to enter a different world.",  100, 550, 30, BLACK)
    text9 = Text("-Pause with P, and return to your previous world by pressing P again.", 100, 600, 30, BLACK)
    text10 = Text("-Press Q to quit the program", 100, 650, 30, BLACK)
    text11 = Text("-You can also change your character by pressing C",  100, 700, 30, BLACK)
    text12 = Text("-Trampolines will make you jump extra high when you land on them",  100, 750, 30, BLACK)
    text_add_list = [text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12]
    for texts in text_add_list:
        text_list.append(texts)
    for texts in text_list:
        texts.print_text()
    return [level_select, done]

class Inventory():
    def __init__(self, init_quantity, x_pos, y_pos, bin_height, bin_width):#, init_quantity, x_pos = 20, y_pos, bin_height, bin_width):
        bin_list = [0, 0, 0, 0]
        bin_list_item = [BLACK, RED, BLACK, GREEN, BLUE]
        self.init_quantity = init_quantity
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.bin_list = bin_list
        self.bin_list_item = bin_list_item

    def update_bin_width(self, block_type):
        if self.bin_list[block_type-1] > 9:
            self.bin_width = 1.5*block_size
        else:
            self.bin_width = block_size

    def add_to_inventory(self, mouse, field, player_x, player_y):
        mouse_x_grid = mouse[0] // 40
        mouse_y_grid = mouse[1] // 40
        player_x_grid = player_x//40
        player_y_grid = player_y//40
        block_type = field.matrix[mouse_y_grid][mouse_x_grid]
        if block_type != 9:
            if ((mouse_x_grid - player_x_grid)**2 + (mouse_y_grid - player_y_grid)**2)**.5 < 5:
                if self.bin_list[block_type-1] < 64:
                    if field.matrix[mouse[1]//40][mouse[0]//40] != 0:
                        self.bin_list[block_type-1] += 1
                        field.matrix[mouse[1]//40][mouse[0]//40] = 0
                        self.update_bin_width(block_type)

    def remove_from_inventory(self, field, block_type, player_x, player_y, current_block_index, mouse):
        mouse_x_grid = mouse[0] // 40
        mouse_y_grid = mouse [1] // 40
        player_x_grid = player_x//40
        player_y_grid = player_y //40
        if player_x%40 == 0:
            check_top_player = (mouse_x_grid == player_x_grid and mouse_y_grid == player_y_grid)
            check_bottom_player = (mouse_x_grid == player_x_grid and mouse_y_grid == player_y_grid+1)
            if (check_top_player== False) and (check_bottom_player== False):
                if field.matrix[mouse[1]//40][mouse[0]//40] == 0:
                    if self.bin_list[block_type-1] > 0:
                        if ((mouse_x_grid - player_x_grid)**2 + (mouse_y_grid - player_y_grid)**2)**.5 < 5:
                                self.bin_list[block_type-1] -= 1
                                mouse_x_to_grid = (mouse[0]//40)*40
                                mouse_y_to_grid = (mouse[1]//40)*40
                                drop_block = Rectangle(mouse_x_to_grid, mouse_y_to_grid, 40, 40, self.bin_list_item[current_block_index])
                                field.blocks.append(drop_block)
        else:
            check_top_left_player = (mouse_x_grid == player_x_grid and mouse_y_grid == player_y_grid)
            check_top_right_player =((mouse_x_grid == player_x_grid and mouse_y_grid == player_y_grid+1))
            check_bottom_left_player = (mouse_x_grid == player_x_grid+1 and mouse_y_grid == player_y_grid)
            check_bottom_right_player = (mouse_x_grid == player_x_grid+1 and mouse_y_grid == player_y_grid+1)
            if (check_top_left_player == False) and (check_top_right_player == False):
                if (check_bottom_left_player== False) and (check_bottom_right_player== False):
                    if field.matrix[mouse[1]//40][mouse[0]//40] == 0:
                        if self.bin_list[block_type-1] > 0:
                            if abs(mouse_x_grid - player_x_grid) < 5 and abs(mouse_y_grid - player_y_grid - 1) < 5:
                                    self.bin_list[block_type-1] -= 1
                                    mouse_x_to_grid = (mouse[0]//40)*40
                                    mouse_y_to_grid = (mouse[1]//40)*40
                                    drop_block = Rectangle(mouse_x_to_grid, mouse_y_to_grid, 40, 40, self.bin_list_item[current_block_index])
                                    field.blocks.append(drop_block)
        self.update_bin_width(block_type)

    def draw_inventory(self, field,  current_block_index, grass, stone, dirt, bedrock, spring):
        text = Text("Inventory:", self.x_pos, self.y_pos-20, 20, RED)
        text.print_text()
        image_list = [grass, dirt, stone, spring]
        for bin in range(len(self.bin_list)):
            #rectangle = Rectangle(self.x_pos, self.y_pos + bin*self.bin_height, self.bin_width, self.bin_height, self.bin_list_item[bin+1])
            #rectangle.draw_rectangle()
            if bin+1 == 1:
                screen.blit(grass,(self.x_pos, self.y_pos + bin*self.bin_height))
            if bin+1 == 2:
                screen.blit(dirt,(self.x_pos, self.y_pos + bin*self.bin_height))
            if bin+1 == 3:
                screen.blit(stone,(self.x_pos, self.y_pos + bin*self.bin_height))
            if bin+1 == 4:
                screen.blit(spring,(self.x_pos, self.y_pos + bin*self.bin_height))
            text = Text(str(self.bin_list[bin]), self.x_pos+ 5, self.y_pos + bin*self.bin_height, 40, WHITE)
            text.print_text()
        text2 = Text("Current Block:", self.x_pos, self.y_pos + bin*self.bin_height+60, 20, RED)
        text2.print_text()
        #current_block = Rectangle(self.x_pos, self.y_pos + bin*self.bin_height + 80, self.bin_width, self.bin_height, self.bin_list_item[current_block_index])
        #current_block.draw_rectangle()
        screen.blit(image_list[current_block_index-1],(self.x_pos, self.y_pos + bin*self.bin_height + 80))

def level_two_map():
    """Stores the map for the second level"""
    matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 4, 0, 9, 9, 9, 9, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 0, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [0, 0, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 9, 1, 2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    [1, 1, 2, 1, 9, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 9, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0] ,
    [2, 2, 2, 2, 9, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0] ,
    [2, 2, 2, 2, 9, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 9, 3, 3, 3, 3, 2, 2, 2, 2, 2, 0] ,
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0] ,
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]
    return matrix


def main_movement(player, field, clock, mouse, mouse2, grass, dirt, stone,
                  bedrock, amon_picture, inventory, inventory_block_index,
                  level_select, level, previous_level_select, spring,
                  player_color, done, sean, colvin):
    """This is the main function of the program. It contains the controller for the program
    user keystrokes and other actions are turned into actions in the game
    by referencing other funtions and classes."""
    player.fall = 'on'
    field.matrix_update(inventory_block_index)
    next_y = player.velocity #how far the player will move on the next iteration
    #finds where in the matrix the player is
    player.player_in_grid()
    #top/bottom collisions
    player.top_collision(field)
    player.bottom_collision(field, next_y)
    previous_level_select = str(level)
    clock.tick(40)

    #move left/right
    keys = pygame.key.get_pressed()
    player.left = 'off'
    player.right = 'off'
    #move left. Allows for holding the key down. Left collisions
    if keys[pygame.K_a]:
        player_left_move = player.left_collision(field)
        if player_left_move is True:
            player.left = 'on'
        else:
            player.left = 'off'
    #move right. Allows for holding the key down. Right collisions
    if keys[pygame.K_d]:
        player_right_move = player.right_collision(field)
        if player_right_move is True:
            player.right = 'on'

    #stops plyaer from moving out of screen to left, right, or bottom
    if player.x <= 0:
        player.x = 0
    if player.x >= 1800:
        player.x = 1800
    if player.y >= 840:
        player.y = 840
        player.velocity = 0
        player.jump = 1
        player.fall = 'off'

    #pick up block
    if mouse2[0] == 1:
        inventory.add_to_inventory(mouse, field, player.x, player.y)
    #place block
    if mouse2[2] == 1:
        inventory.remove_from_inventory(field, inventory_block_index, player.x, player.y, inventory_block_index, mouse)
    #possible actions start here
    for event in pygame.event.get():
        #press teh x in the top left to quit
        if event.type == pygame.QUIT:
            done = True

        #Here begins all the possible actions dependent on keystrokes
        if event.type == pygame.KEYDOWN:
            #jump function
            if event.key == pygame.K_w:
                if player.jump == 1:
                    player.jumps()
                player.jump = 0
            #pause
            if event.key == pygame.K_p:
                level_select = "Menu"
            #chance player character
            if event.key == pygame.K_c:
                player_color += 1
                if player_color == 3:
                    player_color = 0
                player.color = player_color

            # inventory
            #cycles which block to place by pressing 1,2,3, and 4
            if event.key == pygame.K_1:
                inventory_block_index = 1
            if event.key == pygame.K_2:
                inventory_block_index = 2
            if event.key == pygame.K_3:
                inventory_block_index = 3
            if event.key == pygame.K_4:
                inventory_block_index = 4

            #Switches between levels
            if event.key == pygame.K_8:
                level_select = "Level_One"
            if event.key == pygame.K_9:
                level_select = "Level_Two"

            #quit game
            if event.key == pygame.K_q:
                pygame.quit()
                return

    # View-------------------------------------------------------------
    #prints the background
    screen.fill(WHITE)

    #This prints all of the blocks on the screen
    #row and column counts are used to keep track of matrix row and column
    #there is a for loop to run through each row and column
    row_count = -1
    for row in field.matrix:
        column_count = -1
        row_count += 1
        for column in row:
            column_count+=1
            if field.matrix[row_count][column_count] != 0:
                if field.matrix[row_count][column_count] == 4:
                    #based on the number entry in the matrix, it prints a different block
                    screen.blit(spring, (column_count*40, row_count*40))
                if field.matrix[row_count][column_count] == 1:
                    screen.blit(grass, (column_count*40, row_count*40))
                if field.matrix[row_count][column_count] == 2:
                    screen.blit(dirt, (column_count*40, row_count*40))
                if field.matrix[row_count][column_count] == 3:
                    screen.blit(stone, (column_count*40, row_count*40))
                if field.matrix[row_count][column_count] == 9:
                    screen.blit(bedrock, (column_count*40, row_count*40))
    inventory.draw_inventory(field, inventory_block_index, grass, stone, dirt, bedrock, spring)
    player.draw(amon_picture, sean, colvin)
    return [level_select, inventory_block_index, previous_level_select, player_color, done]

#Control
def main():
    #how long between each cycle of the while loop
    clock = pygame.time.Clock()

    #initializes player, field, and other variables for level one and two
    player_color = 0
    player_color2 = 0
    previous_level_select = "unknown"
    level_select = "Menu"
    done = False
    player = Player()
    field = Field()
    field2 = Field()
    field2.matrix = level_two_map()
    player2 = Player()
    player2.x = 0
    inventory = Inventory(0, 0, 20, 40, 40)
    inventory2 = Inventory(0, 0, 20, 40, 40)
    inventory_block_index = 1
    inventory_block_index2 = 1

    #loads all the pictures
    amon_picture = pygame.image.load('amon.png')
    grass = pygame.image.load("grass.png")
    stone = pygame.image.load("stone.png")
    dirt = pygame.image.load("dirt.png")
    soulsand = pygame.image.load("soulsand.png")
    netherack = pygame.image.load("netherack.png")
    netherquartz = pygame.image.load("netherquartz.png")
    bedrock = pygame.image.load("bedrock.png")
    spring = pygame.image.load("spring.png")
    sean = pygame.image.load("sean.png")
    colvin = pygame.image.load("colvin.png")
### CONTROL
    while not done:
        #sets the caption to the name of the level
        pygame.display.set_caption(level_select)
        mouse = pygame.mouse.get_pos()
        mouse2 = pygame.mouse.get_pressed()
        mouse_y = mouse[1]
        #setting up the menu
        if level_select is "Menu":
            returned = menu(previous_level_select)
            level_select = returned[0]
            done = returned[1]
        #setting up level one
        if level_select is "Level_One":
            level_one = main_movement(player, field, clock, mouse, mouse2, grass, dirt, stone, bedrock, amon_picture, inventory, inventory_block_index, level_select, "Level_One", previous_level_select, spring, player_color, done, sean, colvin)
            #the variables in the main function can't be accessed from the main_movement function. They are
            level_select = level_one[0]
            inventory_block_index = level_one[1]
            previous_level_select = level_one[2]
            player_color = level_one[3]
            done = level_one[4]
        #setting up level two
        if level_select is "Level_Two":
            level_two = main_movement(player2, field2, clock, mouse, mouse2, soulsand, netherack, netherquartz, bedrock, amon_picture, inventory2, inventory_block_index2, level_select, "Level_Two", previous_level_select, spring, player_color2, done, sean, colvin)
            level_select = level_two[0]
            inventory_block_index2 = level_two[1]
            previous_level_select = level_two[2]
            player_color2 = level_two[3]
            done = level_two[4]
        #prints the game on each iteration of the loop
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
