import streamlit as st 
import pandas as pd
import plotly.express as px
import pycountry
import pycountry_convert as pc

# Função para obter o continente pelo nome do país
def get_continent(country_name):
    try:
        country_alpha2 = pycountry.countries.lookup(country_name).alpha_2
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except LookupError:
        return None
    

def draw_tab2(df):
    df['Continent'] = df['Area'].apply(get_continent)

    continentes = df['Continent'].unique()
    continente_selecionado_temperatura = st.multiselect("Selecione os Continentes: ", continentes, default=continentes)

    anos = df['Year'].unique()
    ano_selecionado_temperatura = st.slider("Selecione o Ano Temperatura: ", min_value=int(anos.min()), max_value=int(anos.max()), value=int(anos.max()))

    df = df[df['Continent'].isin(continente_selecionado_temperatura)]
    df = df[df['Year'] <= ano_selecionado_temperatura]

    fig = px.line(df, x='Year', y='Average Temperature °C', color='Area', title='Average Temperature (°C) by Year')
    st.plotly_chart(fig)