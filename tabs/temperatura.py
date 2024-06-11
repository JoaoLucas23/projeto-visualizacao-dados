# BOX PLOT

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

# Função para desenhar a aba de Temperaturas com gráfico de box plot
def draw_tab3BoxPlot(df_temperaturas):
    st.title("Variação da temperatura ao Longo do Tempo")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # Seleção de continentes
        continentes_temperatura = df_temperaturas['Continent'].unique()
        continente_selecionado_temperatura = st.multiselect(
            "Selecione os Continentes", continentes_temperatura, default=continentes_temperatura, key="continent_select_temperatura_box")

    with col2:
        # Seleção de países
        paises_temperatura = df_temperaturas[df_temperaturas['Continent'].isin(continente_selecionado_temperatura)]['Area'].unique()
        paises_selecionados_temperatura = st.multiselect(
            "Selecione os Países", paises_temperatura, default=paises_temperatura[:5], key="country_select_temperatura_box")

    with col3:
        # Seleção de intervalo de anos
        anos_disponiveis = sorted(df_temperaturas['Year'].unique())
        intervalo_anos = st.slider("Selecione o Intervalo de Anos", min_value=min(anos_disponiveis), max_value=max(anos_disponiveis), value=(min(anos_disponiveis), max(anos_disponiveis)), key="year_select_box")

    # Filtrar os dados com base na seleção do usuário
    df_filtrado_temperatura = df_temperaturas[df_temperaturas['Area'].isin(paises_selecionados_temperatura) & df_temperaturas['Year'].between(intervalo_anos[0], intervalo_anos[1])]

    # Preparar os dados para o box plot
    data = []
    for pais in paises_selecionados_temperatura:
        df_pais = df_filtrado_temperatura[df_filtrado_temperatura['Area'] == pais]
        data.append(go.Box(y=df_pais['Average Temperature °C'], name=pais, boxpoints='all', whiskerwidth=0.2, marker=dict(size=4), line=dict(width=1)))

    # Layout do gráfico
    layout = go.Layout(
        title="Variação média da temperatura ao Longo do Tempo por País",
        xaxis=dict(title="Ano"),
        yaxis=dict(title="Temperatura Média (°C)"),
        boxmode='group',  # Mostrar os boxes em grupo
        autosize=False,
        width=1000,  # Ajuste da largura do gráfico
        height=600  # Ajuste da altura do gráfico
    )

    # Criar a figura do box plot
    fig_temperatura = go.Figure(data=data, layout=layout)

    # Exibir o gráfico
    st.plotly_chart(fig_temperatura)

    st.markdown("*Os box plots representam a distribuição da temperatura média anual dos países selecionados ao longo do tempo.")




# Apresentacao da variacao acumulada
    

# Função para desenhar a aba de Temperaturas com gráfico de variação acumulada ao longo do tempo.
def draw_tab3(df_temperaturas):
    st.title("Variação Acumulada da Temperatura ao Longo do Tempo")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # Seleção de continentes
        continentes_temperatura = df_temperaturas['Continent'].unique()
        continente_selecionado_temperatura = st.multiselect(
            "Selecione os Continentes", continentes_temperatura, default=continentes_temperatura, key="continent_select_temperatura_cumulative")

    with col2:
        # Seleção de países
        paises_temperatura = df_temperaturas[df_temperaturas['Continent'].isin(continente_selecionado_temperatura)]['Area'].unique()
        paises_selecionados_temperatura = st.multiselect(
            "Selecione os Países", paises_temperatura, default=paises_temperatura[:5], key="country_select_temperatura_cumulative")

    with col3:
        # Seleção de intervalo de anos
        anos_disponiveis = sorted(df_temperaturas['Year'].unique())
        intervalo_anos = st.slider("Selecione o Intervalo de Anos", min_value=min(anos_disponiveis), max_value=max(anos_disponiveis), value=(min(anos_disponiveis), max(anos_disponiveis)), key="year_select_cumulative")

    # Filtrar os dados com base na seleção do usuário
    df_filtrado_temperatura = df_temperaturas[df_temperaturas['Area'].isin(paises_selecionados_temperatura) & df_temperaturas['Year'].between(intervalo_anos[0], intervalo_anos[1])]

    # Calcular a variação acumulada da temperatura
    df_filtrado_temperatura['Average Temperature °C'] = df_filtrado_temperatura.groupby('Area')['Average Temperature °C'].cumsum()

    # Preparar os dados para o gráfico de linha
    data = []
    for pais in paises_selecionados_temperatura:
        df_pais = df_filtrado_temperatura[df_filtrado_temperatura['Area'] == pais]
        data.append(go.Scatter(x=df_pais['Year'], y=df_pais['Average Temperature °C'], mode='lines', name=pais))

    # Layout do gráfico
    layout = go.Layout(
        title="Variação Acumulada da Temperatura ao Longo do Tempo por País",
        xaxis=dict(title="Ano"),
        yaxis=dict(title="Temperatura Média Acumulada (°C)"),
        autosize=False,
        width=1000,  # Ajuste da largura do gráfico
        height=600  # Ajuste da altura do gráfico
    )

    # Criar a figura do gráfico de linha
    fig_temperatura = go.Figure(data=data, layout=layout)

    # Exibir o gráfico
    st.plotly_chart(fig_temperatura)

    st.markdown("*Os gráficos de linha representam a variação acumulada da temperatura média anual dos países selecionados ao longo do tempo.")

    draw_tab3BoxPlot(df_temperaturas)

# Simulação da chamada da função
# Carregar os dados de temperatura de um arquivo CSV em um DataFrame
# df_temperaturas = pd.read_csv("./data/Agrofood_co2_emission.csv")
# Adicionar coluna de continente
# df_temperaturas['Continent'] = df_temperaturas['Area'].apply(get_continent)

# # Chamar a função para desenhar a aba de Temperaturas
# draw_tab3(df_temperaturas)
