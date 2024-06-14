import streamlit as st 
import pandas as pd

from tabs.emissaoCO2 import draw_tab2
from tabs.temperatura import draw_tab3
from tabs.atividadesEmissoras import draw_tab1
from tabs.intro import draw_intro

st.title('Projeto de Visualização de Dados')

raw_df = pd.read_csv('./data/Agrofood_co2_emission.csv')


intro, tab1, tab2, tab3= st.tabs(["Intro","Atividades Emissoras","Emissões de CO2", "Temperatura"])
with intro:
    draw_intro()

with tab1:
    draw_tab1(raw_df)

with tab2:
    draw_tab2(raw_df)

with tab3:
    draw_tab3(raw_df)
