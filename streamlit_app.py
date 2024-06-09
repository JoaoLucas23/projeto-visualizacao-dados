import streamlit as st 
import pandas as pd

from tabs.tab1 import draw_tab1
from tabs.tab2 import draw_tab2

st.title('Projeto de Visualização de Dados')

raw_df = pd.read_csv('./data/Agrofood_co2_emission.csv')


tab1, tab2= st.tabs(["Emissões de CO2", "Tab2"])
with tab1:
    st.title("Emissões de CO2")
    draw_tab1(raw_df)

with tab2:
    st.title("Overview 2")
    draw_tab2(raw_df)
