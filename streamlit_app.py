import streamlit as st 
import pandas as pd

from tabs.tab1 import draw_tab1
from tabs.tab2 import draw_tab2

st.title('Projeto de Visualização de Dados')

raw_df = pd.read_csv('./data/Agrofood_co2_emission.csv')


tab1, tab2= st.tabs(["Tab1", "Tab2"])
with tab1:
    st.subheader("Overview")
    draw_tab1(raw_df)

with tab2:
    st.subheader("Overview 2")
    draw_tab2(raw_df)
