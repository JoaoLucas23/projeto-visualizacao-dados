import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import pycountry_convert as pc

st.set_page_config(layout="wide")

# Função para obter o continente pelo nome do país
def get_continent(country_name):
    try:
        country_alpha2 = pycountry.countries.lookup(country_name).alpha_2
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except LookupError:
        return None

# Função para desenhar o mapa de calor
def draw_tab1(df):
    st.title("Emissões de CO2 no período por País")
    # Adicionar coluna de continente
    df['Continent'] = df['Area'].apply(get_continent)

    col1, col2 = st.columns([1, 1])
    with col1:
        # Seleção de continentes
        continentes = df[df['Continent'].notna()]['Continent'].unique()
        continente_selecionado = st.multiselect("Selecione os Continentes", continentes, default=continentes, key="continent_select")

    with col2:
        # Seleção de ano
        anos = df['Year'].unique()
        ano_min, ano_max = st.slider("Selecione o Intervalo de Anos", 
                                min_value=int(anos.min()), 
                                max_value=int(anos.max()), 
                                value=(int(anos.min()), int(anos.max())), 
                                key="year_range_select")

    # Filtrar os dados com base na seleção do usuário
    df = df[df['Continent'].isin(continente_selecionado)]
    

    if ano_min != ano_max:
        df = df[df['Year'].between(ano_min,ano_max)]
        df = df.groupby(['Area', 'Continent'])['total_emission'].sum().reset_index()
    else:
        df = df[df['Year'] == ano_min]

    # Determinar o escopo do mapa
    continente = 'world' if len(continente_selecionado) > 1 else continente_selecionado[0].lower()

    # Criar o mapa coroplético

    fig = px.choropleth(df,
                        locations="Area",
                        locationmode='country names',
                        color="total_emission",
                        projection="natural earth",
                        color_continuous_scale='YlOrBr',
                        hover_name="Area",
                        labels={'total_emission': 'Emissões Totais de CO2 (kt)'},
                        scope=continente,
                        fitbounds="locations",
                        # width=1000,
                        # height=800,
                    )

    fig.update_layout(
        margin={"r":100,"t":0,"l":100,"b":0},
        autosize=True,
        annotations=[
        {
            'xref': 'paper',
            'yref': 'paper',
            'x': 0.5,
            'y': -0.1,
            'xanchor': 'center',
            'yanchor': 'top',
            'text': 'Os países em cinza não contêm dados.',
            'showarrow': False
        }
    ]
    )

    fig.update_layout(width=None, height=None)

    # Exibir o gráfico centralizado usando o argumento use_container_width=True
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("*Os países em cinza não contêm dados.")