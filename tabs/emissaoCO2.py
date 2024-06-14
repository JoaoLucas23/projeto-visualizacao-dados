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
def draw_tab2(df):
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
        grouped_df = df.groupby(['Area', 'Continent'])['total_emission'].sum().reset_index()
    else:
        grouped_df = df[df['Year'] == ano_min]

    # Determinar o escopo do mapa
    continente = 'world' if len(continente_selecionado) > 1 else continente_selecionado[0].lower()

    # Criar o mapa coroplético

    fig = px.choropleth(grouped_df,
                        locations="Area",
                        locationmode='country names',
                        color="total_emission",
                        projection="natural earth",
                        color_continuous_scale='YlOrBr',
                        hover_name="Area",
                        labels={'total_emission': 'Emissões Totais de CO2 (kt)'},
                        scope=continente,
                        fitbounds="locations",
                        hover_data=['Continent', 'total_emission'],
                        # width=1000,
                        # height=800,
                    )

    fig.update_layout(
        margin={"r":100,"t":0,"l":100,"b":0},
        autosize=True
    )

    fig.update_layout(width=None, height=None)

    # Exibir o gráfico centralizado usando o argumento use_container_width=True
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Os países em cinza não contêm dados*")

    st.markdown("## Emissões de CO2 por País e Fonte de Emissão no período selecionado")

    emission_sources = [
        'Savanna fires', 'Forest fires', 'Crop Residues', 'Rice Cultivation',
        'Drained organic soils (CO2)', 'Pesticides Manufacturing', 'Food Transport',
        'Forestland', 'Net Forest conversion', 'Food Household Consumption',
        'Food Retail', 'On-farm Electricity Use', 'Food Packaging',
        'Agrifood Systems Waste Disposal', 'Food Processing',
        'Fertilizers Manufacturing', 'IPPU', 'Manure applied to Soils',
        'Manure left on Pasture', 'Manure Management', 'Fires in organic soils',
        'Fires in humid tropical forests', 'On-farm energy use'
    ]

    col1, col2 = st.columns([1, 1])
    with col1:
        n_pais = st.number_input("Número de Países a serem exibidos", min_value=1, max_value=10, value=5, step=1, key="num_countries")
    with col2:
        n_emissors = st.number_input("Número de Emissores a serem exibidos", min_value=1, max_value=10, value=5, step=1, key="num_emissors")

    for column in df.columns:
        if column in emission_sources:
            df[column] = df[column].apply(pd.to_numeric, errors='coerce')
    
    total_emissions_by_country = df.groupby('Area')[emission_sources].sum().sum(axis=1)
    top_5_countries = total_emissions_by_country.nlargest(n_pais).index.tolist()

    data_filtered = df[df['Area'].isin(top_5_countries)].sort_values(by='total_emission',ascending=False)

    total_emissions_by_source = data_filtered[emission_sources].sum()
    top_n_sources = total_emissions_by_source.nlargest(n_emissors).index.tolist()

    emissions_long = data_filtered.melt(id_vars=['Area','Year'], value_vars=top_n_sources, 
                                    var_name='Emission Source', value_name='Emission Value')
    
    df_grouped = emissions_long.groupby(['Area','Emission Source'])['Emission Value'].sum()
    df_grouped = df_grouped.sort_values(ascending=False)

    fig = px.bar(
          df_grouped.reset_index(),
          x='Area',
          y='Emission Value',
          color='Emission Source',
          barmode='group',
          labels={'Emission Value': 'Emissões Totais de CO2 (kt)'},
          title='Emissões de CO2 por País e Fonte de Emissão',
          color_discrete_sequence=px.colors.qualitative.G10
    )

    st.plotly_chart(fig, use_container_width=True)
