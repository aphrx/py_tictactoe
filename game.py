import pygame
import sys
import time
import math
import numpy as np
import random

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
board = ["", "", "", 
         "", "", "", 
         "", "", ""]

# Each square's center coordinate
squares =  [(150, 150), (450, 150), (750, 150), 
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
    if player is winner:
        return 1
    else:
        return -1

# Determine winner and end game
def reset(winner):
    global isGameRunning
    if(winner != ""):
        print(winner + " wins!")
    else:
        print("Tie game!")
    isGameRunning = False

# Create new game
def new_game():
    global board, isGameRunning
    time.sleep(1)
    isGameRunning = True
    board = []
    for i in range(9):
        board.append("")
    screen.fill(background_color)
    lines()

# Draw lines
def lines():
    for i in range(1, 3):
        pygame.draw.line(screen, line_color, (line_padding, (width/3)*i), (width - line_padding,(width/3)*i), line_stroke)
        pygame.draw.line(screen, line_color, ((width/3)*i, line_padding), ((width/3)*i,   width - line_padding), line_stroke)

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

# Ordered Opponent
def ordered_click(player):
    for i in range(9):
        if board[i] == "":
            board[i] = player
            marker(board)            
            break

# Count empty tiles
def count_empty():
    counter = 0
    for i in board:
        if i == "":
            counter += 1
    return counter

# Minimax Opponent
def minimax_click(player):
    if count_empty() == 9:
        pos = random.choice([0, 2, 6, 8])
    else:
        pos, _ = minimax(board, player)
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
def minimax(board, turn):
    candidate = [None, None]

    score, _ = score_board(board, opponent, False)

    if abs(score) == 1: 
        return None, score
    elif count_empty() == 0: 
        return None, 0

    if turn == player:
        candidate = [None, math.inf]
    else:
        candidate = [None, -math.inf] 

    for move in possible_moves(board):
        board[move] = turn
        if turn == player:
            position, score = minimax(board, opponent)
        else:
            position, score = minimax(board, player)

        board[move] = ""

        if turn == player and candidate[1] > score:
            candidate = [move, score]
        elif turn == opponent and candidate[1] < score:
            candidate = [move, score]

    return candidate


def score_board(board, turn, IsNotAI):
    score = 0
    suspect = None

    for m in matches:
        if board[m[0]] == board[m[1]] == board[m[2]] != "":
            suspect = board[m[0]]
            if IsNotAI:
                pygame.draw.line(screen, highlight_color, squares[m[0]], squares[m[2]], 30)
            score = get_score(suspect, turn)

    return score, suspect

def check_board():
    free_squares = 0
    for i in range(9):
        if board[i] == "":
            free_squares += 1
         
    result, suspect = score_board(board, opponent, True)
    
    if result == 0:
        if(free_squares == 0):
            reset("")
    elif suspect != None:
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