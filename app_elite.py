import streamlit as st
import numpy as np
import random
import math
import time

# This is the size of the board
ROWS = 6
COLS = 7

if 'board' not in st.session_state:
    st.session_state.board = np.zeros((ROWS, COLS), dtype=int)
    st.session_state.turn = 1

st.title("Connect Four - Elite AI (Minimax Depth 5)")
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
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def is_valid_location(board, col):
    return board[0][col] == 0

def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]

def get_next_open_row(board, col):
    for r in reversed(range(ROWS)):
        if board[r][col] == 0:
            return r
    return -1

# This function helps us score a board based on how favorable it is
def score_position(board, piece):
    center = [int(i) for i in list(board[:, COLS // 2])]
    center_count = center.count(piece)
    return center_count * 3

# This is our Minimax with Alpha-Beta Pruning AI logic
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
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
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
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

# Here we created a clickable column buttons so we can drop the pieces.
cols = st.columns(COLS)
for i in range(COLS):
    if cols[i].button("⬇️", key=f"col_{i}"):
        if st.session_state.turn == 1:
            success = drop_piece(st.session_state.board, i, 1)
            if success:
                if check_winner(st.session_state.board, 1):
                    st.success("🎉 Player (🔴) Wins!")
                    st.session_state.turn = 0  # Freeze game
                else:
                    st.session_state.turn = 2

# This section uses AI to play with Minimax and Alpha-Beta Pruning (depth 5)
if st.session_state.turn == 2:
    valid_cols = get_valid_locations(st.session_state.board)
    if valid_cols:
        start_time = time.time()
        col, _ = minimax(st.session_state.board, 5, -math.inf, math.inf, True)
        end_time = time.time()
        st.write(f"AI move took {end_time - start_time:.4f} seconds")
        drop_piece(st.session_state.board, col, 2)
        if check_winner(st.session_state.board, 2):
            st.success("🟡 AI Wins!")
            st.session_state.turn = 0
        else:
            st.session_state.turn = 1

draw_board(st.session_state.board)
