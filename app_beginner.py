import streamlit as st
import numpy as np
import random
import time

# This is the size of the board
ROWS = 6
COLS = 7

if 'board' not in st.session_state:
    st.session_state.board = np.zeros((ROWS, COLS), dtype=int)  
    st.session_state.turn = 1 
    st.session_state.game_over = False

st.title("Connect Four Beginner Bot 🤖")
st.write("Click a column to drop your piece!")

# This button allows the game to be restarted from scratch
if st.button("New Game 🔄"):
    st.session_state.board = np.zeros((ROWS, COLS), dtype=int)
    st.session_state.turn = 1
    st.session_state.game_over = False

# The board will be drawn using Red and Yellow like the actual game.
# Player is red 🔴 and the AI is yellow 🟡
def draw_board(board):
    display = np.where(
        board == 0, "⬜", 
        np.where(board == 1, "🔴", "🟡")  
    )
    board_str = ""
    for row in display:
        board_str += " ".join(row) + "\n"
    st.markdown(f"```\n{board_str}\n```")

# Drop a piece in a column
def drop_piece(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == 0:
            board[row][col] = player
            return True
    return False

# Check for a winner (4 in a row)
def check_winner(board, piece):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False

def is_valid_location(board, col):
    return board[0][col] == 0

def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]

# Beginner AI just picks a random valid move
def beginner_bot_move(board):
    valid_cols = get_valid_locations(board)
    return random.choice(valid_cols)

# These are the button controls for player
cols = st.columns(COLS)
for i in range(COLS):
    if cols[i].button("⬇️", key=f"col_{i}") and not st.session_state.game_over:
        if st.session_state.turn == 1:
            success = drop_piece(st.session_state.board, i, 1)
            if success:
                if check_winner(st.session_state.board, 1):
                    st.success("🎉 Player (🔴) Wins!")
                    st.session_state.game_over = True
                else:
                    st.session_state.turn = 2

# This is the AI's turn (Beginner)
if st.session_state.turn == 2 and not st.session_state.game_over:
    time.sleep(0.5)  
    start_time = time.time()  
    col = beginner_bot_move(st.session_state.board)
    end_time = time.time()  
    drop_piece(st.session_state.board, col, 2)
    st.write(f"🕒 AI move took {end_time - start_time:.4f} seconds")
    if check_winner(st.session_state.board, 2):
        st.success("🟡 Beginner AI Wins!")
        st.session_state.game_over = True
    else:
        st.session_state.turn = 1

# Show the board
draw_board(st.session_state.board)
