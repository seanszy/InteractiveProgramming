import pygame
import pickle

""" The following section of the script initializes a few global varables that
are helpful to reference at any point in the program."""

#A bunch of variables used throughout the game
pygame.init() #initialize pygame
size = [1840, 920] #size of screen
screen = pygame.display.set_mode(size)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  20, 255,   20)
RED =   (255,   0,   0)
LIGHT_BLUE = (0, 255, 255)
color_matrix = [BLACK, BLUE, GREEN, RED]
block_size = 40 #width/length of blocks in pixels
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
        #makes a matrix that is the shape of the field
        #adds an extra row to width and height to prevent out of bounds errors
        for i in range(size[1]//40+1):
            inner = []
            self.matrix.append(inner)
            for j in range(size[0]//40+1):
                inner.append(0)
        #adds blocks to the first 4 rows of the field
        for row in range(num_rows):
            for column in range(int(size[0]/block_size)):
                if row == 3:
                    self.matrix[row+19][column] = 9
                else:
                    self.matrix[row+19][column] = row+1
        self.matrix[18][15] = 4 #add trampoline

    def matrix_update(self, block_type):
        """Uses the block objects in the list of blocks to update the field matrix
        used to detect collisions. The block is then removed from the list"""
        for block in self.blocks:
            self.matrix[int(block.y//block_size)][int(block.x//block_size)] = block_type
            self.blocks.remove(block)

    def matrix_print(self):
        """Prints the field matrix in a format that is easy to read"""
        print("Matrix")
        for rows in self.matrix:
            print(rows, ",")

class Player():
    """Contains Atributes and Methods regarding the player's position,
    appearance, and motion.
        """

    def __init__(self, x=40, y=700, width=40, height=80, color=0, velocity=0,
                 fall='on', left='off', right='off', jump=0):
        """The first 5 attributes are the same as the Rectangle class above.
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
        colliding with a block and allows him to jump again."""
        """Also makes the player bounce if this block is a trampoline"""
        self.jump = 0
        block_below = field.matrix[int(self.ygrid+2)][int(self.xgrid)]
        block_below_right = field.matrix[int(self.ygrid+2)][int(self.xgrid+1)]
        #below is for if the player is directly over a block
        if self.x % 40 == 0:
            if block_below != 0:
                self.fall = "off"
                self.velocity = 0
                self.y = (self.ygrid)*40
                self.jump = 1
                if block_below == 4:
                    self.super_jump() #trampoline jump
        #below is for if the player is between two blocks
        elif block_below != 0 or block_below_right != 0:
            self.fall = "off"
            self.velocity = 0
            self.y = (self.ygrid)*40
            self.jump = 1
            if block_below == 4 or block_below_right == 4:
                self.super_jump() #trampoline jump

    def left_collision(self, field):
        """Prohibits leftward movement if it would bring the player inside a
        block or outside the screen."""
        #collisions occur when the block is directly over a block
        if self.x%40 == 0:
            #if the player is not jumping only two blocks are checked
            if self.y%40 == 0:
                if field.matrix[int(self.ygrid)][int(self.xgrid-1)] != 0 or field.matrix[int(self.ygrid+1)][int(self.xgrid-1)] != 0:
                    return False
                else:
                    return True
            #if the player is jumping more blocks must be checked for collisions
            elif field.matrix[int(self.ygrid)][int(self.xgrid-1)] != 0 or field.matrix[int(self.ygrid+1)][int(self.xgrid-1)] != 0 or field.matrix[int(self.ygrid+2)][int(self.xgrid-1)] != 0:
                return False
            else:
                return True
        else:
            return True

    def right_collision(self, field):
        """Prohibits rightward movement if it would bring the player inside a
        block or outside the screen. Essentally the same as left_collision"""
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
        if self.x % 40 == 0: #if directly over block
            if field.matrix[int(self.ygrid)][int(self.xgrid)] != 0:
                self.y = (self.ygrid+1)*40
                self.velocity = self.velocity * -.5
        #if between two blocks check more spots for collisions
        elif field.matrix[int(self.ygrid)][int(self.xgrid)] != 0 or field.matrix[int(self.ygrid)][int(self.xgrid+1)] != 0:
            self.velocity = self.velocity * -.5
            self.y = (self.ygrid+1)*40

    def player_in_grid(self):
        """Finds the field matrix value that the player's position corresponds to
        and stores this in the new atributes self.xgrid and self.ygrid"""
        self.xgrid = self.x//block_size
        self.ygrid = self.y//block_size

    def draw(self, amon_picture, sean, colvin):
        """ The actual printing of the player on the screen
        This is where we excecute our movement if the player is supposed
        to be moving or falling."""
        if self.fall == 'on':
            #the player has a velocity to allow vertical position to change
            #fluidly
            self.velocity += self.acceleration_constant
        if self.left == 'on':
            self.x += -4

        if self.right == 'on':
            self.x += 4

        # update the y position
        self.y = self.y + self.velocity

         # change-able skins integrated here
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


class Button(Rectangle):
    """This Class is a sub-class of the rectangle class. This class makes buttons
    which register activity when the mouse is over them or the mouse is clicked.
    I could have used the pygame button class but chose to write my own"""

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        #Rectangle.__init__(self, x, y, width, height, color)

    def is_hover(self, mouse_x, mouse_y):
            """This function detects if the mouse is over the box, but has
            not been clicked"""

            #checks to see if mouse is over box
            if mouse_x > self.x and mouse_x < self.x + self.width:
                if mouse_y > self.y and mouse_y < self.y+self.height:
                    return True

    def is_pushed(self, mouse_x, mouse_y, is_pushed, current_state = False):
            """This function checks to see if the button has been pushed.
            It checks that the mouse hovers over the button and the mouse
            is clicked down."""

            #is hover
            if mouse_x > self.x and mouse_x < self.x + self.width:
                if mouse_y > self.y and mouse_y < self.y+self.height:
                    #is clicked
                    if current_state == True:
                        return False
                    else:
                        return True
                else:
                    return False
            else:
                return False

class Text():
    """Used when forming all of our text boxes - especially in the menu"""
    def __init__(self, text, x_pos, y_pos, size, color):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = size
        self.color = color

    def print_text(self):
        """ A pygame print function integrated into the Text class"""
        font = pygame.font.SysFont("monospace", self.size)
        label = font.render(self.text, 40, self.color)
        screen.blit(label, (self.x_pos, self.y_pos))

def username_exists_function(username, user_information_list):
    """This function checks whether or not a user has already registered
    in the database. It returns true if they have, and false if they have not."""

    if user_information_list != None: #makes sure the profile box on the register screen has input
        for profile in user_information_list: #checks through user profiles
            username_current = profile[0] #username is a subset of the profile
            password = profile[1] #password is also subset of profile
            if username == username_current: #checks to see if they match
                return True
        return False
    else: return False

def invalid_password(password):
    """This function is used to make sure the password is of a reasonable
    size. The requirements could be increased or simplified to make more
    or fewer passwords valid."""

    if len(password) < 6:
        return True

def enter_new_user(enter_button_state_var, user_information_list, old_user_information_list):
    """This function is used to enter a new user into the database of information.
    If the file that the information is stored to is blank, an error occurs,
    so a try loop catches it."""

    #it first checks to see if the user profile already exists
    username_exists_result = username_exists_function(user_information_list[0], old_user_information_list)
    #it then changes the next screen it will show if the user does not exist
    level_select = "Menu"
    if username_exists_result == True:
        level_select = "register_screen"
    #makes sure that it wasn't the default user with no input
    elif user_information_list[0] != 1:
        #catches an error thrown when there is no text in the file
        try: #try loop makes sure file is not blank
            #loads the information
            files = open("user_information_list.txt", 'rb')
            old_user_information_list = pickle.load(files)
            files.close
            #adds current information to the old information
            #then it saves it
            old_user_information_list.append(user_information_list)
            user_information_list = old_user_information_list
            with open('user_information_list.txt', 'wb') as fp:
                pickle.dump(user_information_list, fp)
        except:
            #it just dumps it all if there is already data
            with open('user_information_list.txt', 'wb') as fp:
                pickle.dump([user_information_list], fp)
    enter_button_state_var = False
    #sort out 1 profile from them all
    user_information_list = user_information_list[len(user_information_list)-1]
    return [level_select, user_information_list, enter_button_state_var, username_exists_result]

def validate_user(username, password, old_user_information_list):
    """This function is used from the login screen to make sure that the
    user has entered the correct credentials with a username and password that
    are in the system"""

    #defaults to no error message
    error_messages="No_error"
    #tries to validate user
    for profile in old_user_information_list:
        if username == profile[0]:
            if password == profile[1]:
                return [True, error_message(error_messages)]
            else:
                error_messages="Incorrect_Password" #error message if incorrect password
            return [False, error_message(error_messages)]
        else:
            error_messages="Username_Not_Found" #error messagae if incorrect username
    return [False, error_message(error_messages)]

def error_message(message_type):
    """This function generates the error messages based on keys"""

    text2 = Text("", 5000, 5000, 60, BLUE) #default error message is off screen so it can't be seen

    #below are a bunch of the different possible messages
    if message_type == "Username_Taken":
        text2 = Text("Username Already Taken", 650, 650, 30, RED)
    elif message_type == "invalid_password":
        text2 = Text("Your Password Is Currently Too Short", 550, 650, 30, RED)
    elif message_type == "Username_Not_Found":
        text2= Text("Username Not Found", 685, 650, 30, RED)
    elif message_type == "Incorrect_Password":
        text2 = Text("Incorrect Password", 685, 650, 30, RED)
    else:
        text2 = Text("Incorrect Password", 5000, 5000, 60, BLUE)
    return text2

def save_world(field, user_information_list, level):
    """This function starts the process of saving the user's information by
    putting the field's current status in the user's profile"""

    #checks what level you are on so it can save the right one
    #updates user profile to reflect the current field
    if level == "Level_One":
        user_information_list[2] = field.matrix
    if level == "Level_Two":
        user_information_list[3] = field.matrix
    #runs the function that completes the saving process
    old_user_information_list = save_world_to_file(user_information_list)
    return [user_information_list, old_user_information_list]

def find_user_profile(username, old_user_information_list):
    """This function finds the user in a list of all the profiles and returns
    the user's information and the index of the profile list where the user's
    profile is"""

    username_index_var = False
    profile = []
    profile = []
    username_index = -1 #count variable

    #loops throught to find user profile
    while not username_index_var:
        username_index += 1
        profile = old_user_information_list[username_index] #loks at new profile
        current_username = profile[0] #checks current username
        if username == current_username:
            username_index_var = True
    return [profile, username_index]

def save_world_to_file(user_information_list):
    """Saves the user's information to the file"""

    username = user_information_list[0] #finds user's username
    #reads old data from the file
    files = open("user_information_list.txt", 'rb')
    old_user_information_list = pickle.load(files)
    files.close
    #finds the whole user's profile from the fund_user_profile function
    profile_with_index = find_user_profile(user_information_list[0], old_user_information_list)
    username_index = profile_with_index[1]
    #updates the user's old profile to be the new profile
    old_user_information_list[username_index] = user_information_list
    print("\nold_user_information in save_world_to_file", old_user_information_list, "\n")
    #write the new data to the file
    with open('user_information_list.txt', 'wb') as fp:
        print("\nold where python dumps", old_user_information_list, "\n")
        pickle.dump(old_user_information_list, fp)
    #returns the new list of data
    return old_user_information_list

def menu(previous_level_select, username, user_information_list):
    """This is the menu screen that is shown when you first start playing the
    game. It gives brief instructions on what the game is and how to proceed to
    playing the game"""

    level_select = "Menu" #the level key for this screen
    done = False #quits if done is True

    # Looks for player input
    for event in pygame.event.get():

        #allows the program to close if the x is pushed
        if event.type == pygame.QUIT:
            done = True

        #below is what to do with keyboard input
        if event.type == pygame.KEYDOWN:
            # quits when q is pressed
            if event.key == pygame.K_q:  # If user hit q or closed")
                done = True

            # which level to go to is selected here.
            # p is used to go to the previous level.
            # on the first iteration, this is "unknown:, so p takes you to level one
            # 8 or 9 also take you to level one or two
            if event.key == pygame.K_8:
                level_select = "Level_One"
            if event.key == pygame.K_9:
                level_select = "Level_Two"
            if event.key == pygame.K_p:
                level_select = "Level_One"
            if event.key == pygame.K_x:
                print("\n user information list in menu", user_information_list, "\n")

            #goes back to the previous level.
            #The first if statement prevents a bug when you press p on the
            #first time through and there is no previous level
            if previous_level_select != "unknown":
                if event.key == pygame.K_p:
                    level_select = previous_level_select

    # Fill the screen white and print a bunch of text.
    screen.fill(WHITE)
    text_list = []
    text1 = Text("Welcome, " + username, 250, 50, 100, RED)
    text2 = Text("Instructions:", 50, 200, 60, BLUE)
    text3 = Text("-This is a rudimentary version of Minecraft. Use w, a, s, d to move.", 100, 300, 30, BLACK)
    text4 = Text("-UPDATE: Press z to save your world when you are in it. When you log in again, it is the same", 100, 350, 30, BLACK)
    text5 = Text("-Your inventory is in the upper left. Cycle through which item to drop with 1, 2, 3, and 4", 100, 400, 30, BLACK)
    text6 = Text("-Use left click to pick up items and right click to drop them. You have a limited range.", 100, 450, 30, BLACK)
    text7 = Text("-Which block you will drop is shown by the \"Current Block\" space in your inventory", 100, 500, 30, BLACK)
    text8 = Text("-There are multiple worlds to choose from. Press 8 or 9 to enter a different world.",  100, 550, 30, BLACK)
    text9 = Text("-Pause with P, and return to your previous world by pressing P again.", 100, 600, 30, BLACK)
    text10 = Text("-Press Q to quit the program", 100, 650, 30, BLACK)
    text11 = Text("-You can also change your character by pressing C",  100, 700, 30, BLACK)
    text12 = Text("-Trampolines will make you jump extra high when you land on them",  100, 750, 30, BLACK)
    text_add_list = [text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12]

    #put the texts in a list and print the text
    for texts in text_add_list:
        text_list.append(texts)
    for texts in text_list:
        texts.print_text()
    return [level_select, done]


def menu2(previous_level_select, mouse, mouse2):
    """The first screen that appears. It allow the user to navigate to the
    login screen or the register screen."""

    level_select = "Menu2" #The level key for this funtion
    done = False

    #Mouse input is conerted to x and y direction
    x_mouse = mouse[0]
    y_mouse = mouse[1]

    #parameters for the login and register buttons
    register_block_left = 535
    register_block_top = 400
    register_block_length = 300
    register_block_height = 60

    login_block_left = 865
    login_block_top = 400
    login_block_length = 300
    login_block_height = 60

    #creates the register and login buttons and determines if the mouseu is
    #hovering over the button
    login_button = Button(login_block_left, login_block_top, login_block_length, login_block_height, RED)
    register_button = Button(register_block_left, register_block_top, register_block_length, register_block_height, RED)
    login_button_state = login_button.is_hover(x_mouse, y_mouse)
    register_button_state = register_button.is_hover(x_mouse, y_mouse)

    #Takes in user input
    for event in pygame.event.get():

        #if input is clicking down the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
                #checks to see if the register or login buttons are pushed
                register_button_state_var = register_button.is_pushed(x_mouse, y_mouse, mouse2[0])
                login_button_state_var = login_button.is_pushed(x_mouse, y_mouse, mouse2[0])
                #changes the menu to the right screen after button is pushed
                if register_button_state_var:
                    level_select = "register_screen"
                if login_button_state_var:
                    level_select = "login_menu"

        #quits
        if event.type == pygame.QUIT:
            done = True

        # looks for a keystroke
        if event.type == pygame.KEYDOWN:

            # quits when q is pressed
            if event.key == pygame.K_q:
                done = True

    # Fill the screen white and print a bunch of text.
    screen.fill(LIGHT_BLUE)

    #print the white box around the buttons
    white_box = Rectangle(500, 375, 710, 115, WHITE)
    white_box.draw_rectangle()

    #input text for the login and register buttons
    register_box_input = "Register"
    login_box_input = "Log in"

    #draws buttons based on if you are hovering over it or not
    if login_button_state: #are hovering over login button
            login_button.draw_rectangle()
    else:
        login_button = Button(login_block_left, login_block_top, login_block_length, login_block_height, LIGHT_BLUE)
        login_button.draw_rectangle()
        login_button = Button(login_block_left, login_block_top, login_block_length, login_block_height, RED)
    if register_button_state: #are hovering over register button
        register_button.draw_rectangle()
    else:
        register_button = Button(register_block_left, login_block_top, login_block_length, login_block_height, LIGHT_BLUE)
        register_button.draw_rectangle()
        register_button = Button(register_block_left, login_block_top, login_block_length, login_block_height, RED)

    #printing text
    text_list = []

    text1 = Text("Welcome to CraftMine", 300, 50, 100, RED)
    text2 = Text(register_box_input, register_block_left+7, register_block_top, 60, BLACK)
    text3 = Text(login_box_input, login_block_left+40, login_block_top, 60, BLACK)

    text_add_list = [text1, text2, text3]
    for texts in text_add_list:
        text_list.append(texts)
    for texts in text_list:
        texts.print_text()
    #returns what level you're on and if you should quit
    return [level_select, done]

def register_screen(previous_level_select, username_list, password_list, mouse, mouse2, password_button_state_var, username_button_state_var, most_recent, username, password, user_information_list, old_user_information_list, username_exists):
    """The screen you are taken to if you click the register button.
    On this screen you can register a new account."""

    level_select = "register_screen" #level key
    done = False

    #initializes a "username_list" which holds a users information
    username_list = username_list
    enter_button_state_var = False

    #Reads mouse input
    x_mouse = mouse[0]
    y_mouse = mouse[1]

    #Parameters for username, password, and enter buttons
    username_block_left = 650
    username_block_top = 300
    username_block_length = 400
    username_block_height = 60
    password_block_left = 650
    password_block_top = 400
    password_block_length = 400
    password_block_height = 60
    enter_block_left = 650
    enter_block_top = 500
    enter_block_length = 400
    enter_block_height = 60

    #initiializes the buttons and sees if the mouse is hovering over them
    password_button = Button(password_block_left, password_block_top, password_block_length, password_block_height, LIGHT_BLUE)
    username_button = Button(username_block_left, username_block_top, username_block_length, username_block_height, LIGHT_BLUE)
    enter_button = Button(enter_block_left, enter_block_top, enter_block_length, enter_block_height, RED)
    password_button_state = password_button.is_hover(x_mouse, y_mouse)
    username_button_state = username_button.is_hover(x_mouse, y_mouse)
    enter_button_state = enter_button.is_hover(x_mouse, y_mouse)

    #Checks user input
    for event in pygame.event.get():

        #What it does when clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            #checks to see if any of the buttons are clicked
            if username_button_state:
                username_button_state_var = username_button.is_pushed(x_mouse, y_mouse, mouse2[0], username_button_state_var)
                most_recent = "username"
            if password_button_state:
                password_button_state_var = password_button.is_pushed(x_mouse, y_mouse, mouse2[0], password_button_state_var)
                most_recent = "password"
            if enter_button_state:
                enter_button_state_var = enter_button.is_pushed(x_mouse, y_mouse, mouse2[0])
                if enter_button_state_var:
                    level_select = "Menu"

        #quits
        if event.type == pygame.QUIT:
            done = True

        # looks for a keystroke
        if event.type == pygame.KEYDOWN:
            #checks the most recent button state to see which you should be
            #able to type in to
            if most_recent == "password":
                if password_button_state_var == True:
                    if event.key != pygame.K_TAB and event.key != 13 and event.key < 300: #makes sure the input isn't a tab or shift or other input
                        password_list += (chr(event.key)) #adds a key to the password box
            elif username_button_state_var == True:
                if event.key != pygame.K_TAB and event.key != 13 and event.key < 300: #makes sure input is just regular keyboard input
                    username_list += (chr(event.key)) #adds key input to username
            else: #if neither of the buttons are true
                if event.key == pygame.K_q:  # If user hit q it quits
                    done = True
            if username_button_state_var: #moves from one box to another if you press tab
                if event.key == pygame.K_TAB:
                    password_button_state_var = True
                    most_recent = "password"
            if event.key == pygame.K_BACKSPACE: #delets key if you press backspace
                if most_recent == "username":
                    username_list = username_list[0:len(username_list)-2]
                if most_recent == "password":
                    password_list = password_list[0:len(password_list)-2]
            #changes menu if you have entered all the right information
            if username_button_state_var and password_button_state_var and (len(password_list)>4 and event.key == 13):
                level_select = "Menu"
                enter_button_state_var = True

    # Fill the screen Light Blue and print a bunch of text.
    screen.fill(LIGHT_BLUE)

    #print username and password in their boxes.
    username_box_input = "Username"
    password_box_input = "Password"

    #draws box around buttons
    white_box = Rectangle(600, 260, 500, 340, WHITE)
    white_box.draw_rectangle()

    #changes color if you are hovering over or clicked pasword button
    if password_button_state == True and password_button_state_var == False:
        password_button = Button(password_block_left, password_block_top, password_block_length, password_block_height, RED)
        password_button.draw_rectangle()
        password_button = Button(password_block_left, password_block_top, password_block_length, password_block_height, LIGHT_BLUE)
    elif password_button_state_var == True:#if you have clicked on it
        password_box_input = ""
        password_button.draw_with_outline()
    else: #if neither
        password_list = "Password"
        password_button.draw_rectangle()
        password_list = ""

    #changes register button if you have clicked it or are hovering over it
    if username_button_state == True and username_button_state_var == False: #hovering
        username_button = Button(username_block_left, username_block_top, username_block_length, username_block_height, RED)
        username_button.draw_rectangle()
        username_button = Button(username_block_left, username_block_top, username_block_length, username_block_height, LIGHT_BLUE)
    elif username_button_state_var == True: #clicked
            username_box_input = ""
            username_button.draw_with_outline()
    else: #neither
        username_list = "Username"
        username_button.draw_rectangle()
        username_list = ""

    #changes enter button if you hover over it
    if enter_button_state:
            enter_button.draw_rectangle()
    else: #if not hovering
        enter_button = Button(enter_block_left, enter_block_top, enter_block_length, enter_block_height, LIGHT_BLUE)
        enter_button.draw_rectangle()
        enter_button = Button(enter_block_left, enter_block_top, enter_block_length, enter_block_height, RED)

    #prints a bunch of text on the screen
    text_list = []
    text1 = Text("Register Here", 500, 50, 100, RED) #Title

    #if hovering and not clicking username button
    if username_button_state and not username_button_state_var:
        text2 = Text(str(username_box_input), username_block_left+60, username_block_top, 60, LIGHT_BLUE)
    elif username_button_state_var != True: #if not hovering
        text2 = Text(str(username_box_input), username_block_left+60, username_block_top, 60, RED)
    else: #if clicked
        text2 = Text(username_list, username_block_left+7, username_block_top, 60, RED)

    #if hovering and not clicking password button
    if password_button_state and not password_button_state_var:
        text3 = Text(password_box_input, password_block_left+60, password_block_top, 60, LIGHT_BLUE)
    elif password_button_state_var != True: #if not hovering
        text3 = Text(password_box_input, password_block_left+60, password_block_top, 60, RED)
    else: #if clicked
        text3 = Text(str(password_list), password_block_left+7, password_block_top, 60, RED)

    #if enter button is hovered
    if enter_button_state:
        text4 = Text("Enter", enter_block_left+110, enter_block_top, 60, LIGHT_BLUE)
    else: #otherwise
        text4 = Text("Enter", enter_block_left+110, enter_block_top, 60, RED)


    error_message_input = "No_Error" #default error message

    #checks to see if username already exists
    username_exists = username_exists_function(username, old_user_information_list)
    if username_exists == True: #outputs an error if username exists
        if username != "":
            error_message_input = "Username_Taken"
    elif invalid_password(password): #outputs error if invalid password password
        if password != "":
            error_message_input = "invalid_password"
    error_message_text = error_message(error_message_input) #makes text for the error_message

    #print out all of the texts to go on the screen
    text_add_list = [text1, text2, text3, text4, error_message_text]
    for texts in text_add_list:
        text_list.append(texts)
    for texts in text_list:
        texts.print_text()

    #sets username and password
    username = username_list
    password = password_list

    #sets the user_information_list to be used later
    user_information_list = [username, password, level_one_map(), level_two_map()]

    #checks to mak sure the password is of a reasonable length
    if enter_button_state_var:
        if invalid_password(password):
            enter_button_state_var = False
            level_select = "register_screen" #resets if it is not

    #if enter is clicked and pasword is reasonable, it enters the user
    if enter_button_state_var:
        #uses enter_user function to save user to file
        new_user_information = enter_new_user(enter_button_state_var, user_information_list, old_user_information_list)
        level_select = new_user_information[0] #changes level
        user_information_list = [username, password, level_one_map(), level_two_map()]
        enter_button_state_var = new_user_information[2]
        username_exists = new_user_information[3]

    if username == "": #makes sure the username isn't blank.
        level_select = "register_screen"
    return [level_select, done, username_list, password_button_state_var, username_button_state_var, password_list, most_recent, username, password, user_information_list, enter_button_state_var, username_exists]

def login_menu(previous_level_select, username_list, password_list, mouse, mouse2, password_button_state_var, username_button_state_var, most_recent, username, password, user_information_list, old_user_information_list, username_exists, error_message):
    """The login menu screen. This logs the user into their old profile, which
    is stored on a file in the computer"""

    level_select = "login_menu" #level key
    done = False
    enter_button_state_var = False

    # Looks for player input from mouse
    x_mouse = mouse[0]
    y_mouse = mouse[1]

    #parameters for username, password, and enter blocks
    username_block_left = 650
    username_block_top = 300
    username_block_length = 400
    username_block_height = 60
    password_block_left = 650
    password_block_top = 400
    password_block_length = 400
    password_block_height = 60
    enter_block_left = 650
    enter_block_top = 500
    enter_block_length = 400
    enter_block_height = 60

    #initializes password, username, and enter blocks, and checks if mouse is
    #hovering over them
    password_button = Button(password_block_left, password_block_top, password_block_length, password_block_height, LIGHT_BLUE)
    username_button = Button(username_block_left, username_block_top, username_block_length, username_block_height, LIGHT_BLUE)
    enter_button = Button(enter_block_left, enter_block_top, enter_block_length, enter_block_height, RED)
    password_button_state = password_button.is_hover(x_mouse, y_mouse)
    username_button_state = username_button.is_hover(x_mouse, y_mouse)
    enter_button_state = enter_button.is_hover(x_mouse, y_mouse)

    #checks for user input
    for event in pygame.event.get():

        #if input is the mouse being clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if username_button_state: #if hovering over the user
                #changes the button state to true and makes it the most recent
                username_button_state_var = username_button.is_pushed(x_mouse, y_mouse, mouse2[0], username_button_state_var)
                most_recent = "username"
            if password_button_state: #if hovering over the password button
                #checks if clicked and makes the most recent button the password button
                password_button_state_var = password_button.is_pushed(x_mouse, y_mouse, mouse2[0], password_button_state_var)
                most_recent = "password"
            if enter_button_state: #if enter button is clicked
                enter_button_state_var = enter_button.is_pushed(x_mouse, y_mouse, mouse2[0])
                if enter_button_state_var:
                    level_select = "Menu" #moves to next menu

        #quits
        if event.type == pygame.QUIT:  # quits
            done = True

        # looks for a keystroke
        if event.type == pygame.KEYDOWN:
            if most_recent == "password":
                if password_button_state_var == True:
                    if event.key != pygame.K_TAB and event.key != 13:
                        password_list += (chr(event.key))
            elif username_button_state_var == True:
                if event.key != pygame.K_TAB and event.key != 13 and event.key < 300:
                    username_list += (chr(event.key))
            else:
                if event.key == pygame.K_q:  # If user hit q or closed")
                    done = True
                if event.key == pygame.K_p:
                    level_select = "Menu"
            if username_button_state_var:
                if event.key == pygame.K_TAB:
                    password_button_state_var = True
                    most_recent = "password"
            if event.key == pygame.K_x:
                print(user_information_list)
                print(old_user_information_list)
            if event.key == pygame.K_BACKSPACE:
                if most_recent == "username":
                    username_list = username_list[0:len(username_list)-2]
                if most_recent == "password":
                    password_list = password_list[0:len(password_list)-2]
            if (username_button_state_var and password_button_state_var and event.key == 13):
                level_select = "Menu"
                enter_button_state_var = True
    # Fill the screen white and print a bunch of text.

    #fills the screen light blue
    screen.fill(LIGHT_BLUE)

    #changes text on boxes to username and password
    username_box_input = "Username"
    password_box_input = "Password"

    #draws white boxes around buttons
    white_box = Rectangle(600, 260, 500, 340, WHITE)
    white_box.draw_rectangle()

    #checks state of password button and prints accordingly
    if password_button_state == True and password_button_state_var == False: #hovering
        password_button = Button(password_block_left, password_block_top, password_block_length, password_block_height, RED)
        password_button.draw_rectangle()
        password_button = Button(password_block_left, password_block_top, password_block_length, password_block_height, LIGHT_BLUE)
    elif password_button_state_var == True: #clicked
        password_box_input = ""
        password_button.draw_with_outline()
    else: #neither
        password_list = "Password"
        password_button.draw_rectangle()
        password_list = ""

    #checks state of username button and prints accordingly
    if username_button_state == True and username_button_state_var == False: #hovering
        username_button = Button(username_block_left, username_block_top, username_block_length, username_block_height, RED)
        username_button.draw_rectangle()
        username_button = Button(username_block_left, username_block_top, username_block_length, username_block_height, LIGHT_BLUE)
    elif username_button_state_var == True: #clicked
            username_box_input = ""
            username_button.draw_with_outline()
    else: #neither
        username_list = "Username"
        username_button.draw_rectangle()
        username_list = ""

    #checks if hovering over enter button
    if enter_button_state: #if hovering
            enter_button.draw_rectangle()
    else: #If not hovering
        enter_button = Button(enter_block_left, enter_block_top, enter_block_length, enter_block_height,LIGHT_BLUE)
        enter_button.draw_rectangle()
        enter_button = Button(enter_block_left, enter_block_top, enter_block_length, enter_block_height, RED)

    #prints a bunch of text
    text_list = []
    text1 = Text("Welcome to CraftMine: Please Login", 150, 50, 100, RED) #title

    #prints username button depending on state
    if username_button_state and not username_button_state_var:#if hovering
        text2 = Text(str(username_box_input), username_block_left+60, username_block_top, 60, LIGHT_BLUE)
    elif username_button_state_var != True: #If nothing
        text2 = Text(str(username_box_input), username_block_left+60, username_block_top, 60, RED)
    else: #if clicked
        text2 = Text(username_list, username_block_left+7, username_block_top, 60, RED)

    #prints password button depending on state
    if password_button_state and not password_button_state_var: #if hovering
        text3 = Text(password_box_input, password_block_left+60, password_block_top, 60, LIGHT_BLUE)
    elif password_button_state_var != True: #if clicked
        text3 = Text(password_box_input, password_block_left+60, password_block_top, 60, RED)
    else: #if nothing
        text3 = Text(str(password_list), password_block_left+7, password_block_top, 60, RED)

    #Prints enter button depending on state
    if enter_button_state: #if hovering
        text4 = Text("Enter", enter_block_left+110, enter_block_top, 60, BLUE)
    else: #if not hovering
        text4 = Text("Enter", enter_block_left+110, enter_block_top, 60, RED)

    #checks to see if it is a valid username
    username_exists = username_exists_function(username, old_user_information_list)
    #if enter button is clicked checks validity of sign in
    if enter_button_state_var and level_select == "Menu":
        #checks valididity of username and password
        valid_user = validate_user(username, password, old_user_information_list)
        error_message = valid_user[1] #prints an error depending on result
        if valid_user[0]: #if it is valid move to next menu
            level_select = "Menu"
        else: level_select = "login_menu" #if not stay on login menu
    if username == "": #if username is blank don't move to next menu
        level_select = "login_menu"

    #print texts
    text_add_list = [text1, text2, text3, text4, error_message]
    for texts in text_add_list:
        text_list.append(texts)
    for texts in text_list:
        texts.print_text()

    #update username and password
    username = username_list
    password = password_list

    #finds the profile of the user from the file and reads it
    if level_select == "Menu":
        user_information_list_with_index = find_user_profile(username, old_user_information_list)
        user_information_list = user_information_list_with_index[0]
    return [level_select, done, username_list, password_button_state_var, username_button_state_var, password_list, most_recent, username, password, user_information_list, enter_button_state_var, username_exists, error_message]


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

def level_one_map():
    """Stores the map for the first level"""
    matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0] ,
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0] ,
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0] ,
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0] ,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ,
    ]
    return matrix

def main_movement(player, field, clock, mouse, mouse2, grass, dirt, stone,
                  bedrock, amon_picture, inventory, inventory_block_index,
                  level_select, level, previous_level_select, spring,
                  player_color, done, sean, colvin, user_information_list, old_user_information_list):
    """This is the main function of the program. It contains the controller for the program
    user keystrokes and other actions are turned into actions in the game
    by referencing other funtions and classes."""

    #updates the user's profile to reflect the current field
    if previous_level_select == "unknown" or previous_level_select != level_select:
        if user_information_list[2] != 1 and user_information_list[3] != 1: #if not default from the register screen. This would cause an error
            if level_select == "Level_One":
                field.matrix = user_information_list[2] #updates level one
            if level_select == "Level_Two":
                field.matrix = user_information_list[3] #updates level 2

    player.fall = 'on'
    field.matrix_update(inventory_block_index) #update field
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
                print(field.matrix_print(), "P Pressed")
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

            #saves if you press z
            if event.key == pygame.K_z:
                save_world_info = save_world(field, user_information_list, level_select)
                user_information_list = save_world_info[0]
                old_user_information_list = save_world_info[1]
            #quits if you press q
            if event.key == pygame.K_q:
                pygame.quit()
                done = True
                return [level_select, inventory_block_index, previous_level_select, player_color, done, user_information_list, old_user_information_list]

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
    inventory.draw_inventory(field, inventory_block_index, grass, stone, dirt, bedrock, spring) #draws the inventory
    player.draw(amon_picture, sean, colvin) #draws the player
    return [level_select, inventory_block_index, previous_level_select, player_color, done, user_information_list, old_user_information_list]

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
    level_select = "Menu2"
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
    password_button_state_var = False
    username_button_state_var = False
    most_recent = None
    username = ""
    password = ""
    user_information_list = [1]
    enter_button_state_var = False
    old_user_information_list = None
    username_exists = False
    error_message = Text("Incorrect_Password", 5000, 5000, 60, LIGHT_BLUE)

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
    username_list = ""
    password_list = ""

    #gets the old information from the files
    #it is in a try loop because it errors if there is no data in the file
    try: #if there is data
        files = open("user_information_list.txt", 'rb')
        old_user_information_list = pickle.load(files)
        files.close
    except: #if there is no data
        files = open("user_information_list.txt", 'wb')

    #this is the main while loop for the program
    while not done:
        # sets the caption to the name of the level
        pygame.display.set_caption(level_select)
        #find mouse position and whether or not it is clicked
        mouse = pygame.mouse.get_pos()
        mouse2 = pygame.mouse.get_pressed()

        #decides which screen to go to based on the "level_select" function
        # setting up the menu
        if level_select is "Menu":
            returned = menu(previous_level_select, username, user_information_list)
            level_select = returned[0]
            done = returned[1]
        # setting up level one
        if level_select is "Menu2":
            returned = menu2(previous_level_select, mouse, mouse2)
            level_select = returned[0]
            done = returned[1]
        #setting up the register screen
        if level_select is "register_screen":
            returned = register_screen(previous_level_select, username_list, password_list, mouse, mouse2, password_button_state_var, username_button_state_var, most_recent, username, password, user_information_list, old_user_information_list, username_exists)
            level_select = returned[0]
            done = returned[1]
            username_list = returned[2]
            password_button_state_var = returned[3]
            username_button_state_var = returned[4]
            password_list = returned[5]
            most_recent = returned[6]
            username = returned[7]
            password = returned[8]
            user_information_list = returned[9]
            enter_button_state_var = returned[10]
            username_exists = returned[11]
        # setting up the login screen
        if level_select is "login_menu":
            returned = login_menu(previous_level_select, username_list, password_list, mouse, mouse2, password_button_state_var, username_button_state_var, most_recent, username, password, user_information_list, old_user_information_list, username_exists, error_message)
            level_select = returned[0]
            done = returned[1]
            username_list = returned[2]
            password_button_state_var = returned[3]
            username_button_state_var = returned[4]
            password_list = returned[5]
            most_recent = returned[6]
            username = returned[7]
            password = returned[8]
            user_information_list = returned[9]
            enter_button_state_var = returned[10]
            username_exists = returned[11]
            error_message = returned[12]
        # setting up level one
        if level_select is "Level_One":
            level_one = main_movement(player, field, clock, mouse, mouse2, grass, dirt, stone, bedrock, amon_picture, inventory, inventory_block_index, level_select, "Level_One", previous_level_select, spring, player_color, done, sean, colvin, user_information_list, old_user_information_list)
            # the variables in the main function can't be accessed from the main_movement function. They are
            level_select = level_one[0]
            inventory_block_index = level_one[1]
            previous_level_select = level_one[2]
            player_color = level_one[3]
            done = level_one[4]
            user_information_list = level_one[5]
            old_user_information_list = level_one[6]
        # setting up level two
        if level_select is "Level_Two":
            level_two = main_movement(player2, field2, clock, mouse, mouse2, soulsand, netherack, netherquartz, bedrock, amon_picture, inventory2, inventory_block_index2, level_select, "Level_Two", previous_level_select, spring, player_color2, done, sean, colvin, user_information_list, old_user_information_list)
            level_select = level_two[0]
            inventory_block_index2 = level_two[1]
            previous_level_select = level_two[2]
            player_color2 = level_two[3]
            done = level_two[4]
            user_information_list = level_two[5]
            old_user_information_list = level_two[6]
        # prints the game on each iteration of the loop
        if not done:
            pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
