# importing libraries
import pygame
import time
import random
import json


snake_speed = 15

# Window size
window_x = 720
window_y = 480
res = (720,720)
# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Minigame: Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]
# fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10, 
				random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0
# opens up a window 
screen = pygame.display.set_mode(res)
# white color 
color = (255,255,255) 

# light shade of the button 
color_light = (170,170,170) 

# dark shade of the button 
color_dark = (100,100,100) 

# stores the width of the 
# screen into a variable 
width = screen.get_width() 

# stores the height of the 
# screen into a variable 
height = screen.get_height() 

# defining a font 
smallfont = pygame.font.SysFont('Corbel',35) 

# rendering a text written in 
# this font 
text = smallfont.render('quit' , True , color)

def return_to_main():
        with open("./data/saved.json", "r") as file:
                data = json.load(file)
        with open("./data/saved.json", "w") as outfile:
                json.dump(data, outfile)
        import collisionA

# displaying Score function
def show_score(choice, color, font, size):

	# creating font object score_font
	score_font = pygame.font.SysFont(font, size)
	
	# create the display surface object 
	# score_surface
	score_surface = score_font.render('Score : ' + str(score), True, color)
	
	# create a rectangular object for the text
	# surface object
	score_rect = score_surface.get_rect()
	
	# displaying text
	game_window.blit(score_surface, score_rect)

# game over function
def game_over():

	# creating font object my_font
	my_font = pygame.font.SysFont('times new roman', 50)
	
	# creating a text surface on which text 
	# will be drawn
	game_over_surface = my_font.render(
		'Your Score is : ' + str(score), True, red)
	
	# create a rectangular object for the text 
	# surface object
	game_over_rect = game_over_surface.get_rect()
	
	# setting position of the text
	game_over_rect.midtop = (window_x/2, window_y/4)
	
	# blit will draw the text on screen
	game_window.blit(game_over_surface, game_over_rect)
	pygame.display.flip()
	
	
	# deactivating pygame library
	while True: 
	
		for ev in pygame.event.get(): 
		
			if ev.type == pygame.QUIT: 
                                return_to_main()
                                pygame.quit()
			
                        #checks if a mouse is clicked 
			if ev.type == pygame.MOUSEBUTTONDOWN: 
                                #if the mouse is clicked on the 
                                # button the game is terminated 
				if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                                        return_to_main()
                                        pygame.quit()

 
	
                # stores the (x,y) coordinates into 
                # the variable as a tuple 
		mouse = pygame.mouse.get_pos() 
	
                # if mouse is hovered on a button it 
                # changes to lighter shade 
		if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
			pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
		
		else: 
			pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
	
                # superimposing the text onto our button 
		screen.blit(text , (width/2+50,height/2)) 
	
                # updates the frames of the game 
		pygame.display.update() 

                 
#Main game
while True:
	# handling key events
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                                change_to = 'UP'
                        if event.key == pygame.K_DOWN:
                                change_to = 'DOWN'
                        if event.key == pygame.K_LEFT:
                                change_to = 'LEFT'
                        if event.key == pygame.K_RIGHT:
                               change_to = 'RIGHT'
                if event.type == pygame.QUIT:
                        return_to_main()
                        pygame.quit()
        # If two keys pressed simultaneously
        # we don't want snake to move into two 
        # directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
                snake_position[1] -= 10
        if direction == 'DOWN':
                snake_position[1] += 10
        if direction == 'LEFT':
                snake_position[0] -= 10
        if direction == 'RIGHT':
                snake_position[0] += 10

        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                score += 10
                fruit_spawn = False
        else:
                snake_body.pop()
		
        if not fruit_spawn:
                fruit_position = [random.randrange(1, (window_x//10)) * 10, 
						random.randrange(1, (window_y//10)) * 10]
		
        fruit_spawn = True
        game_window.fill(black)
	
        for pos in snake_body:
                pygame.draw.rect(game_window, green,
                        pygame.Rect(pos[0], pos[1], 10, 10))
                pygame.draw.rect(game_window, white, pygame.Rect(
                        fruit_position[0], fruit_position[1], 10, 10))

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x-10:
                  game_over()
                        
        if snake_position[1] < 0 or snake_position[1] > window_y-10:
                        game_over()
                        
        # Touching the snake body
        for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                        game_over()
                      

        # displaying score continuously
        show_score(1, white, 'times new roman', 20)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(snake_speed)

game_run=True

