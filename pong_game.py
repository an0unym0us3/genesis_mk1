import pygame
import sys
import json
import importlib

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle and Ball
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 15

# Paddle Speed
PADDLE_SPEED = 10  # Increased paddle speed for more excitement
AI_SPEED = 4  # AI speed for Player 2

# Initialize paddles
left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Initialize ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed = [5, 5]  # Initial speed of the ball

# Player scores
left_score = 0
right_score = 0

# Font for scoring
font = pygame.font.Font(None, 36)

# Victory and Defeat screens
victory_screen = font.render("Player ONE Wins!", True, WHITE)
defeat_screen = font.render("Player TWO Wins!", True, WHITE)

def return_to_main():
    with open("./data/saved.json", "r") as file:
        data = json.load(file)
    data["score"] += score
    data["played_count"] += 1
    data["minigames_played"].append('pong_game')
    with open("./data/saved.json", "w") as outfile:
        json.dump(data, outfile)
    if not data["played_count"]:
        import collisionA
    else:
        import collisionA
        # importlib.reload(collisionA)
    sys.exit()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            score=0
            return_to_main()
            sys.exit()

    # Handle player input for Player 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    # Simple AI for Player 2
    if ball.centery < right_paddle.centery and right_paddle.top > 0:
        right_paddle.y -= AI_SPEED
    elif ball.centery > right_paddle.centery and right_paddle.bottom < HEIGHT:
        right_paddle.y += AI_SPEED

    # Move the ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]  # Reflect the ball vertically

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0]  # Reflect the ball horizontally

    # Ball out of bounds (scoring)
    if ball.left <= 0:
        right_score += 1
        ball_speed[0] = -ball_speed[0]  # Reflect the ball horizontally
        ball.x = WIDTH // 2 - BALL_RADIUS // 2
        ball.y = HEIGHT // 2 - BALL_RADIUS // 2

    if ball.right >= WIDTH:
        left_score += 1
        ball_speed[0] = -ball_speed[0]  # Reflect the ball horizontally
        ball.x = WIDTH // 2 - BALL_RADIUS // 2
        ball.y = HEIGHT // 2 - BALL_RADIUS // 2

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw scores
    left_score_text = font.render("Player 1: {}".format(left_score), True, WHITE)
    right_score_text = font.render("Player 2: {}".format(right_score), True, WHITE)
    screen.blit(left_score_text, (50, 20))
    screen.blit(right_score_text, (WIDTH - right_score_text.get_width() - 50, 20))

    # Check for victory or defeat
    if left_score == 5:
        screen.blit(victory_screen, (WIDTH // 2 - victory_screen.get_width() // 2, HEIGHT // 2 - victory_screen.get_height() // 2))
        score=50
        pygame.display.flip()
        pygame.time.delay(2000)  # Delay for 2 seconds before exiting
        return_to_main()

    elif right_score == 5:
        screen.blit(defeat_screen, (WIDTH // 2 - defeat_screen.get_width() // 2, HEIGHT // 2 - defeat_screen.get_height() // 2))
        score=-50
        pygame.display.flip()
        pygame.time.delay(2000)  # Delay for 2 seconds before exiting
        return_to_main()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
