import pygame

import pygame
from math import pi

def main():
    # Initialize the game engine
    pygame.init()

    # Define the colors we will use in RGB format
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    RED =   (255,   0,   0)

    # Set the height and width of the screen
    size = [400, 300]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Example code for the draw module")

    #Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()
    text_x = 150
    text_y = 20
    rectangle_x = 100
    rectangle_y = 100
    which_object = "Text"
    while not done:
        clock.tick(10)

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    which_object = "Text"
                if event.key == pygame.K_r:
                    which_object = "Rectangle"
            if which_object == "Text":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_LEFT:
                        text_x +=-10
                    if event.key == pygame.K_RIGHT:
                        text_x+=10
                    if event.key == pygame.K_UP:
                        text_y += -10
                    if event.key == pygame.K_DOWN:
                        text_y += 10
            if which_object == "Rectangle":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            done = True
                        if event.key == pygame.K_LEFT:
                            rectangle_x +=-10
                        if event.key == pygame.K_RIGHT:
                            rectangle_x+=10
                        if event.key == pygame.K_UP:
                            rectangle_y += -10
                        if event.key == pygame.K_DOWN:
                            rectangle_y += 10
        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.

        # Clear the screen and set the screen background
        screen.fill(WHITE)

        # Draw on the screen a GREEN line from (0,0) to (50.75)
        # 5 pixels wide.
        myfont = pygame.font.SysFont("monospace", 15)
        keys=pygame.key.get_pressed()

        text_color = (0, 0, 0)
        text_position = (text_x, text_y)
        label = myfont.render("Sean and Colvin's Game", 100, text_color)
        screen.blit(label, (text_position))
        #pygame.draw.lines(screen, BLACK, False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)
        #pygame.draw.aaline(screen, GREEN, [0, 50],[50, 80])

        #pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)
        #pygame.draw.arc(screen, RED,  [210, 75, 150, 125], 3*pi/2, 2*pi, 2)
        #pygame.draw.circle(screen, BLUE, [60, 250], 40)
        pygame.draw.rect(screen, BLACK, [rectangle_x, rectangle_y, 50, 20])

        pygame.display.flip()

    # Be IDLE friendly
    pygame.quit()


if __name__ == '__main__':
    main()
