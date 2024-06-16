import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import pycountry

def select_columns(df):
    selected_columns = ['Area', 'total_emission', 'Agrifood Systems Waste Disposal', 'Food Household Consumption', 'Forest fires', 'Fires in humid tropical forests', 'Savanna fires', 'IPPU', 'Food Processing', 'Food Transport', 'Food Packaging', 'Pesticides Manufacturing', 'Fertilizers Manufacturing', 'Food Retail', 'Rice Cultivation', 'Manure left on Pasture', 'Drained organic soils (CO2)', 'Crop Residues', 'Manure Management', 'Manure applied to Soils', 'Average Temperature °C', 'Year']
    return df[selected_columns].copy()

def calculate_total_emissions(df):
    emission_sources = ['Forest fires', 'Fires in humid tropical forests', 'Savanna fires', 'IPPU', 'Food Processing', 'Food Transport', 'Food Packaging', 'Pesticides Manufacturing', 'Fertilizers Manufacturing', 'Food Retail', 'Rice Cultivation', 'Manure left on Pasture', 'Drained organic soils (CO2)', 'Crop Residues', 'Manure Management', 'Manure applied to Soils']

    df['total_fire_emissions'] = df[emission_sources[:3]].sum(axis=1)
    df['total_industrial_emissions'] = df[emission_sources[3:12]].sum(axis=1)
    df['total_cultivation_emissions'] = df[emission_sources[12:]].sum(axis=1)
    return df

def get_iso_alpha(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        iso_alpha = country.alpha_3
        return iso_alpha
    except:
        return None

def chart1(df):
    df_copia = df.copy()
    CO2_df = df[['Area', 'total_emission', 'Average Temperature °C']]
    mean_CO2_df = CO2_df.groupby('Area').mean()

    scaler = MinMaxScaler()
    mean_CO2 = scaler.fit_transform(mean_CO2_df)
    normalized_emission = pd.DataFrame(mean_CO2, columns=['mean_CO2_emission', 'Average Temperature °C'], index=mean_CO2_df.index)
    normalized_emission['Area'] = normalized_emission.index
    normalized_emission['iso_alpha'] = normalized_emission['Area'].apply(get_iso_alpha)

    normalized_emission.rename(columns={'mean_CO2_emission': 'Emissão Média de CO2'}, inplace=True)

    fig = px.choropleth \
    (
        normalized_emission,
        locations="iso_alpha",
        color="Emissão Média de CO2",
        hover_name="Area",
        color_continuous_scale=["#FA8072", "#FF0000"] 
    )

    fig2 = px.scatter_geo \
    (
        normalized_emission,
        locations="iso_alpha",
        size="Average Temperature °C"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout(
        title={'text': "Aumento médio da temperatura por país", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig, use_container_width=True)

def chart2(df):
    temp = select_columns(df)
    temp = select_columns(df)
    temp = calculate_total_emissions(temp)

    CO2_df = temp[['Area', 'total_emission', 'total_industrial_emissions']]
    mean_CO2_df = CO2_df.groupby('Area').mean()

    scaler = MinMaxScaler()
    mean_CO2 = scaler.fit_transform(mean_CO2_df)
    normalized_emission = pd.DataFrame(mean_CO2, columns=['mean_CO2_emission', 'mean_industrial_emissions'], index=mean_CO2_df.index)
    normalized_emission['Area'] = normalized_emission.index
    normalized_emission['iso_alpha'] = normalized_emission['Area'].apply(get_iso_alpha)
    normalized_emission['mean_industrial_emissions'] = normalized_emission['mean_industrial_emissions'].fillna(0)

    normalized_emission.rename(columns={'mean_CO2_emission': 'Emissão Média de CO2'}, inplace=True)

    fig = px.choropleth \
    (
        normalized_emission,
        locations="iso_alpha",
        color="Emissão Média de CO2",
        hover_name="Area",
        color_continuous_scale=["#FA8072", "#FF0000"] 
    )

    fig2 = px.scatter_geo \
    (
        normalized_emission,
        locations="iso_alpha",
        size="mean_industrial_emissions"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout(
        title={'text': "Emissões industriais médias por país", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig, use_container_width=True)

def chart3(df):
    temp = select_columns(df)
    temp = calculate_total_emissions(temp)

    CO2_df = temp[['Area', 'total_emission', 'Agrifood Systems Waste Disposal']]
    mean_CO2_df = CO2_df.groupby('Area').mean()

    scaler = MinMaxScaler()
    mean_CO2 = scaler.fit_transform(mean_CO2_df)
    normalized_emission = pd.DataFrame(mean_CO2, columns=['mean_CO2_emission', 'mean_waste_emission'], index=mean_CO2_df.index)
    normalized_emission['Area'] = normalized_emission.index
    normalized_emission['iso_alpha'] = normalized_emission['Area'].apply(get_iso_alpha)
    normalized_emission['mean_waste_emission'] = normalized_emission['mean_waste_emission'].fillna(0)

    normalized_emission.rename(columns={'mean_CO2_emission': 'Emissão Média de CO2'}, inplace=True)

    fig = px.choropleth \
    (
        normalized_emission,
        locations="iso_alpha",
        color="Emissão Média de CO2",
        hover_name="Area",
        color_continuous_scale=["#FA8072", "#FF0000"] 
    )

    fig2 = px.scatter_geo \
    (
        normalized_emission,
        locations="iso_alpha",
        size="mean_waste_emission"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout \
    (
        title={'text': "Emissões de eliminação de resíduos agroalimentares por país", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig, use_container_width=True)

def chart4(df):
    temp = select_columns(df)
    temp = calculate_total_emissions(temp)

    CO2_df = temp[['Area', 'total_emission', 'total_cultivation_emissions']]
    mean_CO2_df = CO2_df.groupby('Area').mean()

    scaler = MinMaxScaler()
    mean_CO2 = scaler.fit_transform(mean_CO2_df)
    normalized_emission = pd.DataFrame(mean_CO2, columns=['mean_CO2_emission', 'mean_cultivation_emissions'], index=mean_CO2_df.index)
    normalized_emission['Area'] = normalized_emission.index
    normalized_emission['iso_alpha'] = normalized_emission['Area'].apply(get_iso_alpha)
    normalized_emission['mean_cultivation_emissions'] = normalized_emission['mean_cultivation_emissions'].fillna(0)

    normalized_emission.rename(columns={'mean_CO2_emission': 'Emissão Média de CO2'}, inplace=True)

    fig = px.choropleth \
    (
        normalized_emission,
        locations="iso_alpha",
        color="Emissão Média de CO2",
        hover_name="Area",
        color_continuous_scale=["#FA8072", "#FF0000"] 
    )

    fig2 = px.scatter_geo \
    (
        normalized_emission,
        locations="iso_alpha",
        size="mean_cultivation_emissions"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout \
    (
        title={'text': "Emissões médias de cultivo por país", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig, use_container_width=True)

def chart5(df):
    temp = select_columns(df)
    temp = calculate_total_emissions(temp)

    CO2_df = temp[['Area', 'total_emission', 'total_fire_emissions']]
    mean_CO2_df = CO2_df.groupby('Area').mean()

    scaler = MinMaxScaler()
    mean_CO2 = scaler.fit_transform(mean_CO2_df)
    normalized_emission = pd.DataFrame(mean_CO2, columns=['mean_CO2_emission', 'mean_fire_emissions'], index=mean_CO2_df.index)
    normalized_emission['Area'] = normalized_emission.index
    normalized_emission['iso_alpha'] = normalized_emission['Area'].apply(get_iso_alpha)
    normalized_emission['mean_fire_emissions'] = normalized_emission['mean_fire_emissions'].fillna(0)

    normalized_emission.rename(columns={'mean_CO2_emission': 'Emissão Média de CO2'}, inplace=True)

    fig = px.choropleth \
    (
        normalized_emission,
        locations="iso_alpha",
        color="Emissão Média de CO2",
        hover_name="Area",
        color_continuous_scale=["#FA8072", "#FF0000"] 
    )

    fig2 = px.scatter_geo \
    (
        normalized_emission,
        locations="iso_alpha",
        size="mean_fire_emissions"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout \
    (
        title={'text': "Emissões de incêndios por país", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig, use_container_width=True)

def chart6(df):
    temp = select_columns(df)
    temp = calculate_total_emissions(temp)

    CO2_df = temp[['Area', 'total_emission', 'Food Household Consumption']]
    mean_CO2_df = CO2_df.groupby('Area').mean()

    scaler = MinMaxScaler()
    mean_CO2 = scaler.fit_transform(mean_CO2_df)
    normalized_emission = pd.DataFrame(mean_CO2, columns=['mean_CO2_emission', 'mean_household_emission'], index=mean_CO2_df.index)
    normalized_emission['Area'] = normalized_emission.index
    normalized_emission['iso_alpha'] = normalized_emission['Area'].apply(get_iso_alpha)
    normalized_emission['mean_household_emission'] = normalized_emission['mean_household_emission'].fillna(0)

    normalized_emission.rename(columns={'mean_CO2_emission': 'Emissão Média de CO2'}, inplace=True)

    fig = px.choropleth \
    (
        normalized_emission,
        locations="iso_alpha",
        color="Emissão Média de CO2",
        hover_name="Area",
        color_continuous_scale=["#FA8072", "#FF0000"] 
    )

    fig2 = px.scatter_geo \
    (
        normalized_emission,
        locations="iso_alpha",
        size="mean_household_emission"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout \
    (
        title={'text': "Emissões de consumo doméstico por país", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig, use_container_width=True)

def draw_tab1(df):
    chart1(df)
    chart2(df)
    chart3(df)
    chart4(df)
    chart5(df)
    chart6(df)
