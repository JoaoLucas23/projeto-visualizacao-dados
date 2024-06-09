import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import pycountry_convert as pc

def draw_intro():
    st.title("Introdução")
    st.write("""
    Este é um projeto de visualização de dados que tem como objetivo analisar os impactos ambientais da produção agroalimentar, com foco específico na emissão de dióxido de carbono (CO2) e sua relação com o aumento da temperatura.
    """)
    st.markdown("""
    Os dados utilizados neste projeto estão disponíveis em: [Agri-food CO2 emission dataset - Forecasting ML](https://www.kaggle.com/datasets/alessandrolobello/agri-food-co2-emission-dataset-forecasting-ml), um conjunto de dados que compila informações sobre as emissões de CO2 associadas à produção agroalimentar. Ele inclui uma variedade de variáveis, como as emissões provenientes da aplicação de fertilizantes, do transporte de produtos agrícolas, do processamento de alimentos e do desmatamento, entre outros.
    """)

    st.write("""
    O projeto é dividido em três abas principais:
    - **Produção Agricola**: Análise da produção agrícola global ao longo do tempo.
    - **Emissão C02**: Foco na distribuição das emissões de CO2 por país ao longo do período.
    - **Temperatura**: Análise da temperatura média global ao longo do tempo.
    """)

    st.write("""
    Projeto desenvolvido por 
    - João Lucas Lage Gonçalves
    - João Marcos Ribeiro Tolentino
    - Kléber Junior
    """)
             
             
    
             