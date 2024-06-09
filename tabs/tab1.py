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
    

def draw_tab1(df):
    
    ################################################# MAPA DE CALOR #################################################
    df['Continent'] = df['Area'].apply(get_continent)

    data_country = df.groupby(['Year','Area', 'Continent'])['total_emission'].sum().reset_index()

    continentes = data_country['Continent'].unique()
    continente_selecionado = st.multiselect("Selecione os Continentes", continentes, default=continentes)

    anos = df['Year'].unique()
    ano_selecionado = st.slider("Selecione o Ano", min_value=int(anos.min()), max_value=int(anos.max()), value=int(anos.max()))

    df = df[df['Continent'].isin(continente_selecionado)]
    df = df[df['Year'] <= ano_selecionado]


    fig = px.choropleth(df,
                        locations="Area",
                        locationmode='country names',
                        color="total_emission",
                        hover_name="Area",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        labels={'total_emission': 'Emissões Totais de CO2 (kt)'},
                        title="Mapa de Calor Global de Emissões de CO2")

    # Exibir o mapa no Streamlit
    st.plotly_chart(fig)

    ################################################# GRÁFICO DE LINHA #################################################
    fig = px.line(df, x='Year', y='total_emission', color='Area', title='Emissões de CO2 por Ano')
    st.plotly_chart(fig)


    ################################################# CO2 POR POPULACAO #################################################
    df['Population'] = df['Total Population - Male'] + df['Total Population - Female']
    df['total_emission_per_capita'] = df['total_emission'] / df['Population']
    df['total_emission_per_urban_capita'] = df['total_emission'] / df['Urban population']
    df['urban_population_percentage'] = df['Urban population'] / df['Population']

    # ranking dos países com maiores emissões per capita
    top10 = df.groupby('Area')['total_emission_per_capita'].mean().sort_values(ascending=False).head(10).index
    df_top10 = df[df['Area'].isin(top10)]
    st.write('Top 10 países com maiores emissões de CO2 per capita')
    st.write(df_top10[['Area','Year', 'total_emission_per_capita']].sort_values('total_emission_per_capita', ascending=False))