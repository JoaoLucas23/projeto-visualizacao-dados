import streamlit as st 
import pandas as pd
import plotly.express as px
import pycountry
import pycountry_convert as pc


def draw_tab3(df):
    st.title("Temperatura Média Global")