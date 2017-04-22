import pygame

""" The following section of the script initializes a few global varables that
are helpful to reference at any point in the program."""

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


"""    Model ------------------------------------------------------------  """


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
                    # setting up the trampoline
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
        """ prohibits movement if the player is going upwards through a block.
        Incorprorates a 50% bounce back velocity"""
        if self.x % 40 == 0:
            if field.matrix[int(self.ygrid)][int(self.xgrid)] != 0:
                self.y = (self.ygrid+1)*40
                self.velocity = self.velocity * -.5
        elif field.matrix[int(self.ygrid)][int(self.xgrid)] != 0 or field.matrix[int(self.ygrid)][int(self.xgrid+1)] != 0:
            self.velocity = self.velocity * -.5
            self.y = (self.ygrid+1)*40

    def player_in_grid(self):
        """Finds the matrix value that the player's position corresponds to
        stores this in the new atributes self.xgrid and self.ygrid"""
        self.xgrid = self.x//block_size
        self.ygrid = self.y//block_size

    def draw(self, amon_picture, sean, colvin):
        """ The actual printing of the player on the screen
        This is where we excecute our movement if the player is supposed
        to be moving or falling."""
        if self.fall == 'on':
            self.velocity += self.acceleration_constant

        if self.left == 'on':
            self.x += -4

        if self.right == 'on':
            self.x += 4

            # update the y position
        self.y = self.y + self.velocity

           # change-able skins integrated here
        print(self.color)
        if self.color == 0:
            screen.blit(amon_picture,(self.x,self.y))
        if self.color == 1:
            screen.blit(sean,(self.x,self.y))
        if self.color == 2:
            screen.blit(colvin,(self.x,self.y))

    def jumps(self):
        """regular jump function
        triggered by the 'w' key """
        jump_strength = -9
        self.velocity = jump_strength
        self.fall = 'on'

    def super_jump(self):
        """Extra high jump triggered by a bottom collision with a trampoline"""
        jump_strength = -13
        self.velocity = jump_strength
        self.fall = 'on'


class Text():
    """ Used when forming all of our text boxes - especially in the menu"""
    def __init__(self, text, x_pos, y_pos, size, color):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = size
        self.color = color

    def print_text(self):
        """ A pygame pring function integrated into the Text class"""
        font = pygame.font.SysFont("monospace", self.size)
        label = font.render(self.text, 40, self.color)
        screen.blit(label, (self.x_pos, self.y_pos))


def menu(previous_level_select):
    """This is the menu screen that is shown when you first start playing the
    game. It gives brief instructions on what the game is. You can start
    playing the game by pressing 8, 9, or P"""
    level_select = "Menu"
    done = False
    # Looks for player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quits
            done = True
        # looks for a keystroke
        if event.type == pygame.KEYDOWN:
            # quits when q is pressed
            if event.key == pygame.K_q:  # If user hit q or closed")
                done = True
            # which level to go to is selected here.
            # p is used to go to the previous level.
            # on the first iteration, this is "unknown:, so p takes you to level one
            # 8 or 9 also take you to level one or two
            if previous_level_select is "unknown":
                if event.key == pygame.K_8:
                    level_select = "Level_One"
                if event.key == pygame.K_9:
                    level_select = "Level_Two"
                if event.key == pygame.K_p:
                    level_select = "Level_One"
            else:
                # After you have entered a level this takes you back to the previous
                # level when you press P
                print("going previous", previous_level_select)
                if event.key == pygame.K_p:
                    level_select = previous_level_select

    # Fill the screen white and print a bunch of text.
    screen.fill(WHITE)
    text_list = []
    text1 = Text("Bounce Bounce Play Time", 150, 50, 100, RED)
    text2 = Text("Instructions:", 50, 200, 60, BLUE)
    text3 = Text("-This is a rudimentary version of Minecraft. Use w, a, s, d to move.", 100, 300, 30, BLACK)
    text4 = Text("-You can move around the world and change the blocks within it.", 100, 350, 30, BLACK)
    text5 = Text("-Your inventory is in the upper left. Cycle through which item to drop with 1, 2, 3, and 4", 100, 400, 30, BLACK)
    text6 = Text("-Use left click to pick up items and right click to drop them. You have a limited range.", 100, 450, 30, BLACK)
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
    """The inventory is used to pick up, place, and store blocks. The inventory
    is shown in the upper left. The blocks you can place, and the number of
    those blocks that you have are shown in the inventory. Additionally, the block
    that you are currently placing is shown here."""
    def __init__(self, init_quantity, x_pos, y_pos, bin_height, bin_width):
        bin_list = [0, 0, 0, 0]  # initializes you with 0 blocks of any kind
        bin_list_item = [BLACK, RED, BLACK, GREEN, BLUE]
        self.init_quantity = init_quantity
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.bin_list = bin_list
        self.bin_list_item = bin_list_item


    def add_to_inventory(self, mouse, field, player_x, player_y):
        """This method picks up a block from the world when you left click. It
        then increments the count of that block in your inventory by one"""
        # finds where the mouse and player are in the field grid
        mouse_x_grid = mouse[0] // 40
        mouse_y_grid = mouse[1] // 40
        player_x_grid = player_x//40
        player_y_grid = player_y//40
        # finds what block type you picked up
        block_type = field.matrix[mouse_y_grid][mouse_x_grid]
        if block_type != 9:  # 9 is beckrock, which cannot be mined
            # implement a range in which you can pick up from
            if ((mouse_x_grid - player_x_grid)**2 + (mouse_y_grid - player_y_grid)**2)**.5 < 5:
                # you can only hold a maximum of 64 of a certain item
                if self.bin_list[block_type-1] < 64:
                    # only adds if there is a block in that space
                    if field.matrix[mouse[1]//40][mouse[0]//40] != 0:
                        self.bin_list[block_type-1] += 1
                        # sets that space on the field to empty
                        field.matrix[mouse[1]//40][mouse[0]//40] = 0

    def remove_from_inventory(self, field, block_type, player_x, player_y, current_block_index, mouse):
        """This function is used to place items in the word. The current block in the inventory
        then removed from the inventory and placed in the world in the position of the mouse"""
        # finds where the mouse is located in the field grid
        mouse_x_grid = mouse[0] // 40
        mouse_y_grid = mouse[1] // 40
        # finds where the player is located in the field grid
        player_x_grid = player_x//40
        player_y_grid = player_y//40
        # To prevent the player from dropping a block where he or she is standing
        # many if loops were used.
        # the first is based on if the player is directly over a block
        if player_x % 40 == 0:
            # in this case the block cannot be placed in either the top or bottom
            # block of the player
            check_top_player = (mouse_x_grid == player_x_grid and mouse_y_grid == player_y_grid)
            check_bottom_player = (mouse_x_grid == player_x_grid and mouse_y_grid == player_y_grid+1)
            if (check_top_player== False) and (check_bottom_player== False):
                if field.matrix[mouse[1]//40][mouse[0]//40] == 0: # A block cannot be placed if another block already is in that spot
                    if self.bin_list[block_type-1] > 0: #you must have at least one in your inventory to place
                        # T he range in which you can place a block is a circle with radius 5
                        if ((mouse_x_grid - player_x_grid)**2 + (mouse_y_grid - player_y_grid)**2)**.5 < 5:
                                self.bin_list[block_type-1] -= 1 # subtract one from inventory
                                # place the block where your mouse is
                                mouse_x_to_grid = (mouse[0]//40)*40
                                mouse_y_to_grid = (mouse[1]//40)*40
                                drop_block = Rectangle(mouse_x_to_grid, mouse_y_to_grid, 40, 40, self.bin_list_item[current_block_index])
                                field.blocks.append(drop_block)
        else:
            # In this case the player is halway over a block, which means
            # that the player spans 4 blocks, and you should not be able to
            # place a block in any of these places
            check_top_left_player = (mouse_x_grid == player_x_grid and mouse_y_grid == player_y_grid)
            check_top_right_player =((mouse_x_grid == player_x_grid and mouse_y_grid == player_y_grid+1))
            check_bottom_left_player = (mouse_x_grid == player_x_grid+1 and mouse_y_grid == player_y_grid)
            check_bottom_right_player = (mouse_x_grid == player_x_grid+1 and mouse_y_grid == player_y_grid+1)
            if (check_top_left_player == False) and (check_top_right_player == False):
                if (check_bottom_left_player== False) and (check_bottom_right_player== False):
                    # make sure a block isn't already in that position
                    if field.matrix[mouse[1]//40][mouse[0]//40] == 0:
                        # make sure you have at least one item in your inventor
                        if self.bin_list[block_type-1] > 0:
                            if abs(mouse_x_grid - player_x_grid) < 5 and abs(mouse_y_grid - player_y_grid - 1) < 5:
                                    self.bin_list[block_type-1] -= 1 #subtract one from inventory
                                    # place the block where your mouse is
                                    mouse_x_to_grid = (mouse[0]//40)*40
                                    mouse_y_to_grid = (mouse[1]//40)*40
                                    drop_block = Rectangle(mouse_x_to_grid, mouse_y_to_grid, 40, 40, self.bin_list_item[current_block_index])
                                    field.blocks.append(drop_block)

    def draw_inventory(self, field,  current_block_index, grass, stone, dirt, bedrock, spring):
        """Draws the inventory in the top left. Also prints the number of blocks in each slot of the inventory"""
        text = Text("Inventory:", self.x_pos, self.y_pos-20, 20, RED)
        text.print_text()
        # A list of all the images to print in the top left
        image_list = [grass, dirt, stone, spring]
        # For loop to print the inventory for every item in the inventoryy
        for bin in range(len(self.bin_list)):
            # checks what type of block and prints that type
            if bin+1 == 1:
                screen.blit(grass,(self.x_pos, self.y_pos + bin*self.bin_height))
            if bin+1 == 2:
                screen.blit(dirt,(self.x_pos, self.y_pos + bin*self.bin_height))
            if bin+1 == 3:
                screen.blit(stone,(self.x_pos, self.y_pos + bin*self.bin_height))
            if bin+1 == 4:
                screen.blit(spring,(self.x_pos, self.y_pos + bin*self.bin_height))
            # prints the number of items in the inventory in that slot
            text = Text(str(self.bin_list[bin]), self.x_pos+45, self.y_pos + bin*self.bin_height, 30, BLACK)
            text.print_text()
        # prints the current block and the text for it.
        text2 = Text("Current Block:", self.x_pos, self.y_pos + bin*self.bin_height+60, 20, RED)
        text2.print_text()
        screen.blit(image_list[current_block_index-1],(self.x_pos, self.y_pos + bin*self.bin_height + 80))

def level_two_map():
    """Stores the map for the second level"""
    matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 4, 0, 9, 9, 9, 9, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 9, 1, 2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 2, 1, 9, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 9, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 9, 3, 3, 3, 3, 2, 2, 2, 2, 2, 0],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
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
    # finds where in the matrix the player is
    player.player_in_grid()
    # top/bottom collisions
    player.top_collision(field)
    player.bottom_collision(field, next_y)
    previous_level_select = str(level)
    clock.tick(40)

    # move left/right
    keys = pygame.key.get_pressed()
    player.left = 'off'
    player.right = 'off'
    # move left. Allows for holding the key down. Left collisions
    if keys[pygame.K_a]:
        player_left_move = player.left_collision(field)
        if player_left_move is True:
            player.left = 'on'
        else:
            player.left = 'off'
    # move right. Allows for holding the key down. Right collisions
    if keys[pygame.K_d]:
        player_right_move = player.right_collision(field)
        if player_right_move is True:
            player.right = 'on'

    # stops plyaer from moving out of screen to left, right, or bottom
    if player.x <= 0:
        player.x = 0
    if player.x >= 1800:
        player.x = 1800
    if player.y >= 840:
        player.y = 840
        player.velocity = 0
        player.jump = 1
        player.fall = 'off'

    # pick up block
    if mouse2[0] == 1:
        inventory.add_to_inventory(mouse, field, player.x, player.y)
    # place block
    if mouse2[2] == 1:
        inventory.remove_from_inventory(field, inventory_block_index, player.x, player.y, inventory_block_index, mouse)
    # possible actions start here
    for event in pygame.event.get():
        # press teh x in the top left to quit
        if event.type == pygame.QUIT:
            done = True

        # Here begins all the possible actions dependent on keystrokes
        if event.type == pygame.KEYDOWN:
            # jump function
            if event.key == pygame.K_w:
                if player.jump == 1:
                    player.jumps()
                player.jump = 0
            # pause
            if event.key == pygame.K_p:
                level_select = "Menu"
            # chance player character
            if event.key == pygame.K_c:
                player_color += 1
                if player_color == 3:
                    player_color = 0
                player.color = player_color

            # inventory
            # cycles which block to place by pressing 1,2,3, and 4
            if event.key == pygame.K_1:
                inventory_block_index = 1
            if event.key == pygame.K_2:
                inventory_block_index = 2
            if event.key == pygame.K_3:
                inventory_block_index = 3
            if event.key == pygame.K_4:
                inventory_block_index = 4

            # Switches between levels
            if event.key == pygame.K_8:
                level_select = "Level_One"
            if event.key == pygame.K_9:
                level_select = "Level_Two"

            # quit game
            if event.key == pygame.K_q:
                pygame.quit()
                return

    # View-------------------------------------------------------------
    # prints the background
    screen.fill(WHITE)

    # This prints all of the blocks on the screen
    # row and column counts are used to keep track of matrix row and column
    # there is a for loop to run through each row and column
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
    """ The actual call of the start of the program.
    Main movement is referenced by this function.
    """
    # how long between each cycle of the while loop
    clock = pygame.time.Clock()

    # initializes player, field, and other variables for level one and two
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

    # loads all the pictures
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

    """CONTROL"""
    while not done:
        # sets the caption to the name of the level
        pygame.display.set_caption(level_select)
        mouse = pygame.mouse.get_pos()
        mouse2 = pygame.mouse.get_pressed()
        # setting up the menu
        if level_select is "Menu":
            returned = menu(previous_level_select)
            level_select = returned[0]
            done = returned[1]
        # setting up level one
        if level_select is "Level_One":
            level_one = main_movement(player, field, clock, mouse, mouse2, grass, dirt, stone, bedrock, amon_picture, inventory, inventory_block_index, level_select, "Level_One", previous_level_select, spring, player_color, done, sean, colvin)
            # the variables in the main function can't be accessed from the main_movement function. They are
            level_select = level_one[0]
            inventory_block_index = level_one[1]
            previous_level_select = level_one[2]
            player_color = level_one[3]
            done = level_one[4]
        # setting up level two
        if level_select is "Level_Two":
            level_two = main_movement(player2, field2, clock, mouse, mouse2, soulsand, netherack, netherquartz, bedrock, amon_picture, inventory2, inventory_block_index2, level_select, "Level_Two", previous_level_select, spring, player_color2, done, sean, colvin)
            level_select = level_two[0]
            inventory_block_index2 = level_two[1]
            previous_level_select = level_two[2]
            player_color2 = level_two[3]
            done = level_two[4]
        # prints the game on each iteration of the loop
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
