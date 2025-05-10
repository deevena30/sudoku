import numpy as np
import random
from flask import Flask, render_template, request

sudoku = Flask(__name__)
board = np.zeros((9, 9), dtype=int)

def random_board(numberof_filledcells):
    b = np.zeros((9, 9), dtype=int)
    filled_cells = 0
    while filled_cells < numberof_filledcells:
        rowrand = random.randint(0, 8)
        colrand = random.randint(0, 8)
        valuerand = random.randint(1, 9)
        if b[rowrand][colrand] == 0 and isvalid(b, rowrand, colrand, valuerand):
            b[rowrand][colrand] = valuerand
            filled_cells += 1
    return b
def printboard(b):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("----------------------")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if b[i][j] == 0:
                print("_", end=" ")
            else:
                print(b[i][j], end=" ")
        print()

def isvalid(b, r, c, n):
    for i in range(9):
        if b[r][i] == n:
            return False

    for i in range(9):
        if b[i][c] == n:
            return False
    
    rowstart=(r//3)*3
    columnstart=(c//3)*3 
    for i in range(rowstart, rowstart + 3):
        for j in range(columnstart, columnstart + 3):
            if b[i][j] == n:
                return False
         
    return True

# def play_game():
#     type= input("select difficulty level (easy or hard or extreme): ")
#     if(type=="easy"):
#         numberof_filledcells=35
#     elif(type=="hard"):
#         numberof_filledcells=20
#     elif(type=="extreme"):
#         numberof_filledcells=15    
#     board = random_board(numberof_filledcells)
#     print("NOTE: Allowed number of wrong moves are 3 only:)")
#     count = 0        
#     while True:
#         printboard(board)
#         r = int(input("Enter row (0 to 8): "))
#         c = int(input("Enter column (0 to 8): "))
#         n = int(input("Enter number (1 to 9): "))

#         if board[r][c] != 0:
#             print("filled.")
#         elif not isvalid(board, r, c, n):
#             print("Invalid move.")
#             count+=1
#         else:
#             board[r][c] = n
#         if(count>=3):
#             print("Number of wrong moves are 3,Game is over:(")
#             break
#         if all(all(cell != 0 for cell in row) for row in board):
#             printboard(board)
#             print("You completed the Sudoku!")
#             break

# play_game()
@sudoku.route('/',methods=['GET','POST'])
def index():
    global board
    if request.method == 'POST':
        level = request.form['level']
        if level == 'easy':
            board = random_board(35)
        elif level == 'hard':
            board = random_board(20)
        elif level == 'extreme':
            board = random_board(15)
        return render_template('sudoku.html', board=board)
    return render_template('index.html')

@sudoku.route('/game',methods=['GET','POST'])
def game():
    count = 0
    msg = "NOTE: Allowed number of wrong moves are 3 only:)"
    if request.method == 'POST':
        try:
            r = int(request.form['row'])
            c = int(request.form['col'])
            n = int(request.form['num'])
            if board[r][c] != 0:
                msg = "filled."
            elif not isvalid(board, r, c, n):
                msg = "Invalid move!"
                count+=1
            else:
                board[r][c] = n
            if(count>=3):
                msg = "Number of wrong moves are 3,Game is over:("
                return render_template('sudoku.html', board=board, message=msg)
            if all(all(cell != 0 for cell in row) for row in board):
                printboard(board)
                msg = "You completed the Sudoku!"
                return render_template('sudoku.html', board=board, message=msg)
        except:
            msg = "Invalid input!"
        return render_template('sudoku.html', board=board, message=msg)
                    
if __name__ == '__main__':
    sudoku.run(debug=True)    