import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

def draw_tab2(raw_df):
    fig, ax = plt.subplots()
    ax.hist(raw_df['Savanna fires'], bins=30, edgecolor='black')
    ax.set_title('Distribution of Savanna Fires')
    ax.set_xlabel('Number of Fires')
    ax.set_ylabel('Frequency')

    # Display the plot using Streamlit
    st.pyplot(fig)  