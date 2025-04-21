import streamlit as st
import numpy as np
import random 
# This is the size of the board
ROWS = 6
COLS = 7

if 'board' not in st.session_state:
    st.session_state.board = np.zeros((ROWS, COLS), dtype=int)  
    st.session_state.turn = 1 

st.title("Connect Four AI Project")
st.write("Click a column to drop your piece!")

# The board will be drawn using Red and Yellow like the actual game.
 #Player would red 🔴 and the AI will be yellow 🟡
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

# Here we created a clickable column buttons so we can drop the pieces. 
cols = st.columns(COLS)
for i in range(COLS):
    if cols[i].button("⬇️", key=f"col_{i}"):
        if st.session_state.turn == 1:
            success = drop_piece(st.session_state.board, i, 1)
            if success:
                st.session_state.turn = 2  # This will be the next turn for the AI

#This section is the AI just playing the game without the implemented minimax and Alpha beta pruning.
def is_valid_location(board, col): #This function is to tell whether or not a space is full and a piece could be placed.
    return board[0][col] == 0

def get_valid_locations(board): #This return all the open columns
    return [col for col in range(COLS) if is_valid_location(board, col)]
if st.session_state.turn == 2:
    valid_cols = get_valid_locations(st.session_state.board)
    if valid_cols:
        col = random.choice(valid_cols)
        drop_piece(st.session_state.board, col, 2)
        st.session_state.turn = 1  

draw_board(st.session_state.board)
# This displays the board

