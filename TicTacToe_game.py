import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 10

# Colors
BACKGROUND_COLOR = (49, 51, 56)
GRID_COLOR = (255, 255, 255)
PLAYER_X_COLOR = (255, 100, 100)
PLAYER_O_COLOR = (100, 100, 255)
TEXT_COLOR = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# Function to draw the grid
def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
        pygame.draw.line(screen, GRID_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

# Function to draw X or O
def draw_symbol(index, symbol):
    row, col = divmod(index, GRID_SIZE)
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2

    if symbol == 'X':
        pygame.draw.line(screen, PLAYER_X_COLOR, (x - 30, y - 30), (x + 30, y + 30), 5)
        pygame.draw.line(screen, PLAYER_X_COLOR, (x + 30, y - 30), (x - 30, y + 30), 5)
    elif symbol == 'O':
        pygame.draw.circle(screen, PLAYER_O_COLOR, (x, y), 30, 5)

# Function to check for a win
def check_win(board, symbol):
    # Check rows and columns
    for i in range(GRID_SIZE):
        row_start = i * GRID_SIZE
        if set(board[row_start: row_start + GRID_SIZE]) == set(symbol) or set([board[0 + i], board[3 + i], board[6 + i]]) == set(symbol):
            return True

    # Check diagonals
    if all(board[i * GRID_SIZE + i] == symbol for i in range(GRID_SIZE)) or all(
            board[i * GRID_SIZE + GRID_SIZE - i - 1] == symbol for i in range(GRID_SIZE)):
        return True

    return False

# Function to check if the board is full
def is_board_full(board):
    return all(cell != ' ' for cell in board)

# Function to display text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function for bot's turn
def bot_turn(board):
    # Simulate "thinking" by adding a delay
    time.sleep(1)

    defend_moves = []
    for i in range(3):
        this_row = board[i * 3: i * 3 + 3]
        if len(set(this_row)) == 2 and this_row.count(' ') == 1:
            if 'X' in this_row:
                return this_row.index(' ') + 3 * i
            else:
                defend_moves.append(this_row.index(' ') + 3 * i)

        this_col = [board[0 + i], board[3 + i], board[6 + i]]
        if len(set(this_col)) == 2 and this_col.count(' ') == 1:
            if 'X' in this_col:
                return this_col.index(' ') * 3 + i
            else:
                defend_moves.append(this_col.index(' ') * 3 + i)

    lr_diag = [board[0], board[4], board[8]]
    if len(set(lr_diag)) == 2 and lr_diag.count(' ') == 1:
        if 'X' in lr_diag:
            return lr_diag.index(' ') * 4
        else:
            defend_moves.append(lr_diag.index(' ') * 4)

    rl_diag = [board[2], board[4], board[6]]
    if len(set(rl_diag)) == 2 and rl_diag.count(' ') == 1:
        if 'X' in rl_diag:
            return 2 + rl_diag.index(' ') * 2
        else:
            defend_moves.append(2 + rl_diag.index(' ') * 2)

    if not defend_moves:
        # Find an empty spot and make a move
        empty_spots = [i for i in range(GRID_SIZE * GRID_SIZE) if board[i] == ' ']
        if empty_spots:
            return random.choice(empty_spots)
    elif len(defend_moves) == 1:
        return defend_moves[0]
    else:
        print('I withdraw... You win!')
        print('Game end!')
        quit()



# Main game loop
board = [' ' for _ in range(GRID_SIZE * GRID_SIZE)]
player_turn = 'X'

# Fonts
font = pygame.font.Font(None, 36)

running = True
while running:
    mouse_event = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and player_turn == 'X':
            mouse_event = event.dict

    # Human player's turn
    if player_turn == 'X':
        if mouse_event:
            clicked_index = (mouse_event['pos'][1] // CELL_SIZE) * GRID_SIZE + mouse_event['pos'][0] // CELL_SIZE

            if board[clicked_index] == ' ':
                board[clicked_index] = 'X'
                if check_win(board, 'X'):
                    print("Player X wins!")
                    running = False
                elif is_board_full(board):
                    print("It's a draw!")
                    running = False

                player_turn = 'O'

    # Bot's turn
    else:
        board[bot_turn(board)] = 'O'
        if check_win(board, 'O'):
            print("Player O wins!")
            running = False

        elif is_board_full(board):
            print("It's a draw!")
            running = False

        player_turn = 'X'

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    draw_grid()

    for index in range(GRID_SIZE * GRID_SIZE):
        if board[index] == 'X':
            draw_symbol(index, 'X')
        elif board[index] == 'O':
            draw_symbol(index, 'O')

    draw_text(f"Turn: {player_turn}", font, TEXT_COLOR, WIDTH // 2, HEIGHT - 20)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
quit()
