import streamlit as st 
import pandas as pd

from tabs.emissaoCO2 import draw_tab2
from tabs.temperatura import draw_tab3
from tabs.anoArea import draw_tab4
from tabs.prodAgricola import draw_tab1
from tabs.intro import draw_intro

st.title('Projeto de Visualização de Dados')

raw_df = pd.read_csv('./data/Agrofood_co2_emission.csv')


intro, tab1, tab2, tab3, tab4= st.tabs(["Intro","Produção Agrícola","Emissões de CO2", "Temperatura", "Ano x Area"])
with intro:
    draw_intro()

with tab1:
    draw_tab1(raw_df)

with tab2:
    draw_tab2(raw_df)

with tab3:
    draw_tab3(raw_df)

with tab4:
    draw_tab4(raw_df)
