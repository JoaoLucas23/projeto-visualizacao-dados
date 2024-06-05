import streamlit as st 
import pandas as pd

def draw_tab1(raw_df):
    st.write(raw_df.head(10))