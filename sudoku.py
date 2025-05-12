import numpy as np
import random
from flask import Flask, render_template, request, session, redirect, url_for
import uuid

sudoku = Flask(__name__)
sudoku.secret_key = "sudoku_secret_key"  # Replace with a proper secret key in production

def solve_board(board):
    """Backtracking Sudoku solver to generate a full valid board"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_board():
    """Generate a complete Sudoku board"""
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_board(board)
    return board

# Game state will be stored in session
def random_board(number_of_filled_cells):
    """Generate a valid Sudoku board with exactly `number_of_filled_cells` pre-filled"""
    board = generate_full_board()
    
    # Create a list of all cell positions
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    
    # Number of cells to remove
    to_remove = 81 - number_of_filled_cells
    
    for _ in range(to_remove):
        row, col = cells.pop()
        board[row][col] = 0
    
    return board

def is_valid(board, row, col, num):
    """Check if placing num at position (row, col) is valid"""
    # Check row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
             
    return True

def is_complete(board):
    """Check if the board is complete (no empty cells)"""
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True

@sudoku.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        level = request.form.get('level', 'easy')
        
        # Initialize a new game with selected difficulty
        if level == 'easy':
            board = random_board(35)
        elif level == 'hard':
            board = random_board(20)
        else:  # extreme
            board = random_board(15)
        
        # Store game state in session
        session['board'] = board
        session['original_board'] = [row[:] for row in board]  # Deep copy of the board
        session['wrong_moves'] = 0
        session['game_over'] = False
        session['message'] = ''
        
        return redirect(url_for('game'))
    
    return render_template('index.html')

@sudoku.route('/game', methods=['GET', 'POST'])
def game():
    # Initialize session data if not exists
    if 'board' not in session:
        return redirect(url_for('index'))
    
    board = session['board']
    original_board = session['original_board']
    wrong_moves = session['wrong_moves']
    game_over = session['game_over']
    message = session['message']
    
    if request.method == 'POST':
        if game_over:
            message = "Game is already over. Start a new game."
        else:
            # Process each cell in the grid
            for i in range(9):
                for j in range(9):
                    cell_name = f"cell_{i}_{j}"
                    
                    # Skip cells that are already filled in the original board
                    if original_board[i][j] != 0:
                        continue
                    
                    # Process user input for this cell
                    if cell_name in request.form and request.form[cell_name]:
                        try:
                            value = int(request.form[cell_name])
                            
                            if value < 1 or value > 9:
                                message = "Please enter a number between 1 and 9."
                                continue
                                
                            # If cell was already filled by user, clear it first
                            if board[i][j] != 0:
                                board[i][j] = 0
                                
                            # Check if move is valid
                            if is_valid(board, i, j, value):
                                board[i][j] = value
                                message = "Valid move!"
                            else:
                                wrong_moves += 1
                                message = f"Invalid move! Wrong moves: {wrong_moves}/3"
                                if wrong_moves >= 3:
                                    game_over = True
                                    message = "Game over! You've made 3 wrong moves."
                        except ValueError:
                            message = "Please enter a valid number."
            
            # Check if the game is complete
            if is_complete(board) and not game_over:
                game_over = True
                message = "Congratulations! You've completed the Sudoku puzzle!"
        
        # Update session data
        session['board'] = board
        session['wrong_moves'] = wrong_moves
        session['game_over'] = game_over
        session['message'] = message
    
    return render_template('sudoku.html', 
                          board=board, 
                          original_board=original_board,
                          message=message,
                          wrong_moves=wrong_moves,
                          game_over=game_over)

@sudoku.route('/new_game', methods=['GET'])
def new_game():
    # Clear game data from session
    session.pop('board', None)
    session.pop('original_board', None)
    session.pop('wrong_moves', None)
    session.pop('game_over', None)
    session.pop('message', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    sudoku.run(debug=True)