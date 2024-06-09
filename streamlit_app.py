import streamlit as st 
import pandas as pd

from tabs.emissaoCO2 import draw_tab1
from tabs.tab2 import draw_tab2
from tabs.intro import draw_intro

st.title('Projeto de Visualização de Dados')

raw_df = pd.read_csv('./data/Agrofood_co2_emission.csv')


intro, tab1, tab2= st.tabs(["Emissões de CO2", "Tab2"])
with intro:
    draw_intro(raw_df)

with tab1:
    draw_tab1(raw_df)

with tab2:
    st.title("Overview 2")
    draw_tab2(raw_df)
