import pygame
import random
import json
import sys

# Initialize Pygame
pygame.init()

# Display Dimensions
dis_width, dis_height = 800, 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Snake and Food Sizes
block_size = 20

# Font Style
font_style = pygame.font.SysFont(None, 50)

# Game Speed
snake_speed = 15
clock = pygame.time.Clock()

SA = pygame.mixer.Sound("./Media/music/Sneaky Adventure.mp3")
chipi=pygame.mixer.Sound("./Media/music/Chipi.mp3")

global_score = 0

def return_to_main():
    global global_score
    with open("./data/saved.json", "r") as file:
        data = json.load(file)
    data["score"] += global_score
    data["played_count"] += 1
    data["minigames_played"].append('snake_game')
    with open("./data/saved.json", "w") as outfile:
        json.dump(data, outfile)
    import main_game
    sys.exit()

# Score Display
def your_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])


# Draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])


# Display Message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


# Game Loop
def gameLoop():
    game_over = False
    game_close = False
    game_win = False

    x1, y1 = dis_width / 2, dis_height / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - block_size) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - block_size) / 20.0) * 20.0

    pygame.mixer.music.load('./Media/music/PewPew.mp3')
    pygame.mixer.music.play(-1)

    while not game_over:
        pygame.mixer.Sound.stop(SA)
        while game_close:

            pygame.mixer.Sound.play(SA)
            pygame.mixer.music.stop()
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            your_score(length_of_snake - 1)
            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        while game_win:
            pygame.mixer.Sound.play(chipi)
            pygame.mixer.music.stop()
            dis.fill(blue)
            message("You WIN! Press Q-Quit or C-Play Again", green)
            your_score(length_of_snake-1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return_to_main()
                        quit()
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True


        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, white, [foodx, foody, block_size, block_size])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        if length_of_snake==11:
            game_win=True

        our_snake(block_size, snake_list)
        your_score(length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            global global_score
            foodx = round(random.randrange(0, dis_width - block_size) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - block_size) / 20.0) * 20.0
            length_of_snake += 1
            global_score+=10

        clock.tick(snake_speed)




    pygame.quit()
    return_to_main()
    quit()


# Start the game
gameLoop()
