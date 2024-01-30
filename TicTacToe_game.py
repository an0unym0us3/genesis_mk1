import pygame
import random
import time
import json
import sys

pygame.init()

# make the screen
screen_w, screen_h = 600, 600
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Tic Tac Toe")

# Constants
side_cell = 3
cell_size = screen_w // side_cell

bg_color = (49, 51, 56)
l_color = (255, 255, 255)
x_color = (255, 100, 100)
o_color = (100, 100, 255)

font_color = (255, 255, 255)
font = pygame.font.Font(None, 36)


def return_to_main():
    
    with open("./data/saved.json", "r") as file:
        data = json.load(file)
    data["score"] += score
    data["played_count"] += 1
    data["minigames_played"].append('TicTacToe_game')
    with open("./data/saved.json", "w") as outfile:
        json.dump(data, outfile)
    import main_game
    sys.exit()
    quit()

# draw the grid
def draw_grid():
    for i in range(1, side_cell):
        pygame.draw.line(screen, l_color, (i * cell_size, 0), (i * cell_size, screen_h))
        pygame.draw.line(screen, l_color, (0, i * cell_size), (screen_w, i * cell_size))

# draw x or o
def draw_player(index, symbol):
    row, col = divmod(index, side_cell)
    x = col * cell_size + cell_size // 2
    y = row * cell_size + cell_size // 2

    if symbol == 'X':
        pygame.draw.line(screen, x_color, (x - 30, y - 30), (x + 30, y + 30), 5)
        pygame.draw.line(screen, x_color, (x + 30, y - 30), (x - 30, y + 30), 5)
    elif symbol == 'O':
        pygame.draw.circle(screen, o_color, (x, y), 30, 5)

# check if there is a streak of non blank character
def check_win(board, symbol):
    # Check rows and columns
    for i in range(side_cell):
        row_start = i * side_cell
        if set(board[row_start: row_start + side_cell]) == set(symbol) or {board[0 + i], board[3 + i], board[6 + i]} == set(symbol):
            return True

    # Check diagonals
    if set(board[::side_cell+1]) == set(symbol) or set(board[side_cell-1:side_cell**2 -1:side_cell-1]) == set(symbol):
        return True

    return False

# check if the board is full
def check_full(board):
    return all(board)

# show text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function for bot's turn
def do_play(board):
    # bot supposedly thinks
    time.sleep(1)

    if board[4] == '':
        return 4
    
    defend_moves = []
    for i in range(3):
        this_row = board[i * 3: i * 3 + 3]
        if len(set(this_row)) == 2 and this_row.count('') == 1:
            if 'X' in this_row:
                return this_row.index('') + 3 * i
            else:
                defend_moves.append(this_row.index('') + 3 * i)

        this_col = [board[0 + i], board[3 + i], board[6 + i]]
        if len(set(this_col)) == 2 and this_col.count('') == 1:
            if 'X' in this_col:
                return this_col.index('') * 3 + i
            else:
                defend_moves.append(this_col.index('') * 3 + i)

    lr_diag = [board[0], board[4], board[8]]
    if len(set(lr_diag)) == 2 and lr_diag.count('') == 1:
        if 'X' in lr_diag:
            return lr_diag.index('') * 4
        else:
            defend_moves.append(lr_diag.index('') * 4)

    rl_diag = [board[2], board[4], board[6]]
    if len(set(rl_diag)) == 2 and rl_diag.count('') == 1:
        if 'X' in rl_diag:
            return 2 + rl_diag.index('') * 2
        else:
            defend_moves.append(2 + rl_diag.index('') * 2)

    if not defend_moves:
        # Find an empty spot and make a move
        empty_spots = [i for i in range(side_cell * side_cell) if board[i] == '']
        if empty_spots:
            return random.choice(empty_spots)
    elif len(defend_moves) == 1:
        return defend_moves[0]
    else:
        print('I withdraw... You win!')
        print('Game end!')
        return_to_main()



# Main game loop
def run_game(score, this_game, total_games):
    board = ['' for _ in range(side_cell * side_cell)]
    player_turn = 'X'

    clock = pygame.time.Clock()
    running = True
    while running:
        mouse_event = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # running = False
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN and player_turn == 'X':
                mouse_event = event.dict

        # Human plays
        if player_turn == 'X':
            if mouse_event:
                clicked_index = (mouse_event['pos'][1] // cell_size) * side_cell + mouse_event['pos'][0] // cell_size

                if board[clicked_index] == '':
                    board[clicked_index] = 'X'
                    if check_win(board, 'X'):
                        print("Player X wins!")
                        return 10
                        #running = False
                    elif check_full(board):
                        print("It's a draw!")
                        return 0
                        #running = False

                    player_turn = 'O'

        # Bot plays
        else:
            board[do_play(board)] = 'O'
            if check_win(board, 'O'):
                print("Player O wins!")
                return -10
                #running = False

            elif check_full(board):
                print("It's a draw!")
                return 0
                #running = False

            player_turn = 'X'

        # Draw the UI
        screen.fill(bg_color)
        draw_grid()

        for index in range(side_cell **2):
            if board[index] == 'X':
                draw_player(index, 'X')
            elif board[index] == 'O':
                draw_player(index, 'O')

        draw_text(f"Turn: {player_turn}", font, font_color, screen_w // 2, screen_h - 20)
        draw_text(f"Score: {score}", font, font_color, screen_w // 2, 20)
        draw_text(f"Game: {this_game}/{total_games}", font, font_color, 100, 20)


        pygame.display.flip()
        clock.tick(10)

score = 0
games = 3
for i in range(games):
    score += run_game(score, i, games)
    print(score)

return_to_main()
