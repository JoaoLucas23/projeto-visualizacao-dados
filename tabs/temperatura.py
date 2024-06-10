import streamlit as st 
import pandas as pd
import plotly.express as px
import pycountry
import pycountry_convert as pc
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

def draw_tab3(df):
    # Carregar os dados
    df = pd.read_csv('./data/Agrofood_co2_emission.csv')

    # Agregar dados por ano
    temp = df.groupby('Year').agg({'Average Temperature °C':'mean', 'total_emission':'sum'})

    # Função para formatar em milhões
    def millions_formatter(x, pos):
        return '{:,.0f}M'.format(x / 1000000) 

    # Configurações do gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    g = sns.scatterplot(data=temp, x='total_emission', y='Average Temperature °C', ax=ax, hue='Year', palette='mako', s=100) 

    # Aplicar formatação aos ticks do eixo x
    ax.xaxis.set_major_formatter(FuncFormatter(millions_formatter))

    # Títulos e rótulos
    fig.suptitle('Gráfico de dispersão entre a temperatura média anual global e as emissões totais anuais de CO2')
    ax.set_xlabel('Emissões anuais totais de CO2 em milhões de toneladas')
    ax.set_ylabel('Temperatura média anual (°C)')

    # Exibir gráfico
    st.pyplot(fig)
