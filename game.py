import pygame
import sys
import time

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

# Other Global Vars
isPlayerTurn = False
isGameRunning = True
game_font = pygame.font.Font('font.ttf',250)
pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(background_color)

# End of game & determine winner
def reset(winner):
    global isGameRunning, player
    score = 0
    if(winner != ""):
        print(winner + " wins!")
        if(winner == player):
            score = 1
        else:
            score = -1
    else:
        print("Tie game!")
    isGameRunning = False
    return score

# Create new game
def new_game():
    time.sleep(1)
    global isGameRunning, board
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



# Minimax Opponent
def minimaxClick(turn):
    
    for i in range(9):
        board_cp = board.copy()
        if board_cp[i] == "":
            board_cp[i] = turn
            print(board_cp)
            print(score(board_cp, turn))


# Ordered Opponent
def random_click(player):
    minimaxClick(player)
    '''for i in range(9):
        if board[i] == "":
            board[i] = player
            marker(board)            
            break
'''
# Score board
def score(board, turn):
    if board[0] == board[1] == board[2] != "": 
        return score_point(board[0], turn)
    elif board[3] == board[4] == board[5] != "": 
        return score_point(board[3], turn)
    elif board[6] == board[7] == board[8] != "":
        return score_point(board[6], turn)
    elif board[0] == board[3] == board[6] != "":
        return score_point(board[0], turn)
    elif board[1] == board[4] == board[7] != "": 
        return score_point(board[1], turn)
    elif board[2] == board[5] == board[8] != "": 
        return score_point(board[2], turn)
    elif board[0] == board[4] == board[8] != "": 
        return score_point(board[0], turn)
    elif board[2] == board[4] == board[6] != "": 
        return score_point(board[2], turn)
    else:
        return 0

# Determine winner
def score_point(winner, player):
    if(winner == player):
        return 1
    else:
        return -1

def score_board(board):
    if board[0] == board[1] == board[2] != "": 
            pygame.draw.line(screen, highlight_color, squares[0], squares[2], 30)
            return reset(board[0])
    elif board[3] == board[4] == board[5] != "": 
            pygame.draw.line(screen, highlight_color, squares[3], squares[5], 30)
            return reset(board[3])
    elif board[6] == board[7] == board[8] != "":
            pygame.draw.line(screen, highlight_color, squares[6], squares[8], 30)
            return reset(board[6])
    elif board[0] == board[3] == board[6] != "":
            pygame.draw.line(screen, highlight_color, squares[0], squares[6], 30)
            return reset(board[0])
    elif board[1] == board[4] == board[7] != "": 
            pygame.draw.line(screen, highlight_color, squares[1], squares[7], 30)
            return reset(board[1])
    elif board[2] == board[5] == board[8] != "": 
            pygame.draw.line(screen, highlight_color, squares[2], squares[8], 30)
            return reset(board[2])
    elif board[0] == board[4] == board[8] != "": 
            pygame.draw.line(screen, highlight_color, squares[0], squares[8], 30)
            return reset(board[0])
    elif board[2] == board[4] == board[6] != "": 
            pygame.draw.line(screen, highlight_color, squares[2], squares[6], 30)
            return reset(board[2])
    else:
        return 0
    

def check_board():
    free_squares = 0
    for i in range(9):
        if board[i] == "":
            free_squares += 1
    if score_board(board) == 0:
        if(free_squares == 0):
            reset("")
    
    

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
            random_click(opponent)
            isPlayerTurn = True
        check_board()

    else:
        new_game()

    pygame.display.update()
    clock.tick(30)