import streamlit as st
import numpy as np
import random 
import math

# This is the size of the board
ROWS = 6
COLS = 7

if 'board' not in st.session_state:
    st.session_state.board = np.zeros((ROWS, COLS), dtype=int)  
    st.session_state.turn = 1 

st.title("Connect Four AI Project")
st.write("Click a column to drop your piece!")

# This button allows the game to be restarted from scratch
if st.button("New Game 🔄"):
    st.session_state.board = np.zeros((ROWS, COLS), dtype=int)
    st.session_state.turn = 1

# The board will be drawn using Red and Yellow like the actual game.
# Player would be red 🔴 and the AI will be yellow 🟡
def draw_board(board):
    display = np.where(
        board == 0, "⬜", 
        np.where(board == 1, "🔴", "🟡")  
    )
    board_str = ""
    for row in display:
        board_str += " ".join(row) + "\n"
    st.markdown(f"```\n{board_str}\n```")

# Here we created a function to drop a piece in a column
def drop_piece(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == 0:
            board[row][col] = player
            return True
    return False  # If the column is full

# This function checks if either player has won
def check_winner(board, piece):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Diagonal check (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Diagonal check (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

# This function tells the next open row in a column
def get_next_open_row(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col] == 0:
            return row
    return -1

# This function checks if a column is a valid move
def is_valid_location(board, col): 
    return board[0][col] == 0

# This returns all the open columns
def get_valid_locations(board): 
    return [col for col in range(COLS) if is_valid_location(board, col)]

# This function scores the board (center pieces are better)
def score_position(board, piece):
    center_array = [int(i) for i in list(board[:, COLS // 2])]
    center_score = center_array.count(piece)
    return center_score * 3

# Here we created the Minimax Algorithm with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = check_winner(board, 1) or check_winner(board, 2) or len(valid_locations) == 0

    if depth == 0 or is_terminal:
        if check_winner(board, 2):
            return (None, 100000)
        elif check_winner(board, 1):
            return (None, -100000)
        else:
            return (None, score_position(board, 2))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            temp_board[row][col] = 2
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            temp_board[row][col] = 1
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# Here we created clickable column buttons so we can drop the pieces
cols = st.columns(COLS)
for i in range(COLS):
    if cols[i].button("⬇️", key=f"col_{i}"):
        if st.session_state.turn == 1:
            success = drop_piece(st.session_state.board, i, 1)
            if success:
                if check_winner(st.session_state.board, 1):
                    st.success("🎉 Player (🔴) Wins!")
                    st.session_state.turn = 0  # Checks if player wins and freezes the game
                else:
                    st.session_state.turn = 2  # This will be the next turn for the AI

# This section is the AI move using Minimax with Alpha-Beta pruning
if st.session_state.turn == 2:
    valid_cols = get_valid_locations(st.session_state.board)
    if valid_cols:
        col, _ = minimax(st.session_state.board, 3, -math.inf, math.inf, True)
        if col is not None:
            drop_piece(st.session_state.board, col, 2)
            if check_winner(st.session_state.board, 2):
                st.success("🟡 AI Wins!")
                st.session_state.turn = 0  # Checks if AI wins and freezes the game
            else:
                st.session_state.turn = 1  # Player's turn

# This displays the board
draw_board(st.session_state.board)
