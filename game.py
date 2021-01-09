import pygame
import sys
import time
import math
import numpy as np

pygame.init()
width = 900
screen = pygame.display.set_mode([width, width])
clock = pygame.time.Clock()

# Colors
background_color = (40, 44, 52)
line_color = (33,36,43)
opponent_color  = (224,107,116)
player_color = (152,195,121)
highlight_color = (171,178,191)

# Line Attributes
line_padding = 30
line_stroke = 20

# Player Markers
player = "O"
opponent = "X"

# Tic Tac Tie Board
board = [
    "", "", "", 
    "", "", "", 
    "", "", ""]

# Each square's center coordinate
squares = [
        (150, 150), (450, 150), (750, 150), 
        (150, 450), (450, 450), (750, 450), 
        (150, 750), (450, 750), (750, 750)]

# Squares which can match
matches =  [[0, 1, 2],
            [3, 4, 5], 
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]]

# Other Global Vars
isGameRunning = True
game_font = pygame.font.Font('font.ttf',250)
pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(background_color)

# End of game & determine winner
def get_score(winner, player):
    if(winner == player):
        score = 1
    else:
        score = -1
    return score

def reset(winner):
    global isGameRunning, board
    if(winner != ""):
        print(winner + " wins!")
    else:
        print("Tie game!")
    isGameRunning = False

# Create new game
def new_game():
    global isGameRunning, board
    time.sleep(1)
    isGameRunning = True
    board = [
        "", "", "", 
        "", "", "", 
        "", "", ""]
    screen.fill(background_color)
    lines()

# Draw lines
def lines():
    pygame.draw.line(screen, line_color, (line_padding, (width/3)), (width - line_padding,(width/3)), line_stroke)
    pygame.draw.line(screen, line_color, (line_padding, (width/3)*2), (width - line_padding,(width/3)*2), line_stroke)
    pygame.draw.line(screen, line_color, ((width/3), line_padding), ((width/3),   width - line_padding), line_stroke)
    pygame.draw.line(screen, line_color, ((width/3)*2, line_padding), ((width/3)*2, width - line_padding), line_stroke)

# Draw opponent & player markers
def marker(board):
    for i in range(9):
        if(board[i] == player):
            color = player_color
        else:
            color = opponent_color
        score_surface = game_font.render(board[i], 1, color)
        score_rect = score_surface.get_rect(center= squares[i])
        screen.blit(score_surface, score_rect)

# When player clicks
def click(pos, player):
    for i in range(9):
        if  ((squares[i][0] - 150) < pos[0] and (squares[i][0] + 150) >= pos[0]) and ((squares[i][1] - 150) < pos[1] and (squares[i][1] + 150) >= pos[1]):
            if board[i] == "":
                board[i] = player
                marker(board)
                return 1
    return 0

def get_states():
    discrete_board = []
    for i in board:
        if i == "":
            discrete_board.append(0)
        if i == "X":
            discrete_board.append(1)
        if i == "O":
            discrete_board.append(2)
    return discrete_board

# Ordered Opponent
def random_click(player):
    for i in range(9):
        if board[i] == "":
            board[i] = player
            marker(board)            
            break

def count_empty():
    counter = 0
    for i in board:
        if i == "":
            counter += 1
    return counter

# Minimax Opponent
def minimax_click(player):
    global board
    pos, score = 0, 0
    if count_empty() == 9:
        i = np.random.randint(0, 9)
        board[i] = player
        marker(board)
    else:
        pos, score = minimax(board, player, player)
        board[pos] = player
        marker(board)

# Possible Moves on board
def possible_moves(board):
    moves = []
    for i in range(len(board)):
        if board[i] == "":
            moves.append(i)
    return moves

# Recursive Minimax Function
def minimax(board, turn, current):
    global player, opponent
    candidate = [None, None]

    score, _ = score_board(board, current, False)

    if abs(score) == 1 :
        return None, score

    if count_empty() == 0:
        return None, 0

    if turn == player:
        candidate = [None, math.inf]
    else:
        candidate = [None, -math.inf] 

    for move in possible_moves(board):
        board[move] = turn
        next_turn = None
        if turn == player:
            next_turn = opponent
        else:
            next_turn = player

        position, score = minimax(board, next_turn, current)

        board[move] = ""

        if turn == player:
            if candidate[1] > score:
                candidate = [move, score]
        if turn == opponent: 
            if candidate[1] < score:
                candidate = [move, score]

    return candidate


def score_board(board, player, IsNotAI):
    score = 0
    suspect = None

    for m in matches:
        if board[m[0]] == board[m[1]] == board[m[2]] != "":
            suspect = board[m[0]]
            if IsNotAI:
                pygame.draw.line(screen, highlight_color, squares[m[0]], squares[m[2]], 30)
            score = get_score(suspect, player)

    return score, suspect
    

def check_board():
    global player
    free_squares = 0
    for i in range(9):
        if board[i] == "":
            free_squares += 1
    result, suspect = score_board(board, opponent, True)
    
    if result == 0:
        if(free_squares == 0):
            print(result)
            reset("")
    elif suspect != None:
        print(result)
        reset(suspect)

def game():
    isPlayerTurn = False
    lines()

    while True:
        pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                    
        if isGameRunning:
            if isPlayerTurn:

                if pos is not None and click(pos, player) == 1:
                    isPlayerTurn = False
            else:
                minimax_click(opponent)
                isPlayerTurn = True
            check_board()

        else:
            new_game()

        pygame.display.update()
        clock.tick(30)

game()