import streamlit as st
import numpy as np

st.title("Connect Four AI Project")
st.write("Building a Connect Four game with AI!")

# Creating the Game Board 
ROWS = 6
COLS = 7
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((ROWS, COLS), dtype=int)
    st.session_state.turn = 1

