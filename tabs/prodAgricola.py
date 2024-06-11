import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import pycountry

def select_columns(df):
    selected_columns = ['Area', 'total_emission', 'Agrifood Systems Waste Disposal', 'Food Household Consumption',
                        'Forest fires', 'Fires in humid tropical forests', 'Savanna fires',
                        'IPPU', 'Food Processing', 'Food Transport', 'Food Packaging', 'Pesticides Manufacturing',
                        'Fertilizers Manufacturing', 'Food Retail',
                        'Rice Cultivation', 'Manure left on Pasture', 'Drained organic soils (CO2)',
                        'Crop Residues', 'Manure Management', 'Manure applied to Soils', 'Average Temperature °C', 'Year']
    return df[selected_columns].copy()

def calculate_total_emissions(df):
    emission_sources = ['Forest fires', 'Fires in humid tropical forests', 'Savanna fires',
                        'IPPU', 'Food Processing', 'Food Transport', 'Food Packaging', 'Pesticides Manufacturing',
                        'Fertilizers Manufacturing', 'Food Retail',
                        'Rice Cultivation', 'Manure left on Pasture', 'Drained organic soils (CO2)',
                        'Crop Residues', 'Manure Management', 'Manure applied to Soils']

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

def graf1(df):
    temp = select_columns(df)
    temp = df.iloc[:, 2:-7].copy()
    delete_list = ['Forestland', 'Net Forest conversion', 'On-farm Electricity Use']
    temp = temp.drop(delete_list, axis=1)

    means = temp.mean()
    means.sort_values(ascending=True, inplace=True)
    cols = means.index

    fig = px.bar(x=means, y=cols, orientation='h', color=means, 
                 color_continuous_scale='Reds', 
                 labels={'x': 'Média de emissões de CO2 (em toneladas)', 'y': ''})
    
    fig.update_layout(title='Média de emissões de CO2 (em toneladas) por atividade agroalimentar',
                      title_font_size=18,
                      xaxis_title_font_size=14,
                      yaxis_title_font_size=14,
                      xaxis_tickfont_size=12,
                      yaxis_tickfont_size=12)
    
    st.plotly_chart(fig, use_container_width=True)

def graf2(df):
    selected_columns = ['Area', 'total_emission', 'Agrifood Systems Waste Disposal', 'Food Household Consumption',
                        'Forest fires', 'Fires in humid tropical forests', 'Savanna fires',
                        'IPPU', 'Food Processing', 'Food Transport', 'Food Packaging', 'Pesticides Manufacturing',
                        'Fertilizers Manufacturing', 'Food Retail',
                        'Rice Cultivation', 'Manure left on Pasture', 'Drained organic soils (CO2)',
                        'Crop Residues', 'Manure Management', 'Manure applied to Soils', 'Average Temperature °C', 'Year']

    temp = df[selected_columns].copy()

    emission_sources = ['Forest fires', 'Fires in humid tropical forests', 'Savanna fires',
                        'IPPU', 'Food Processing', 'Food Transport', 'Food Packaging', 'Pesticides Manufacturing',
                        'Fertilizers Manufacturing', 'Food Retail',
                        'Rice Cultivation', 'Manure left on Pasture', 'Drained organic soils (CO2)',
                        'Crop Residues', 'Manure Management', 'Manure applied to Soils']

    temp['total_fire_emissions'] = temp[emission_sources[:3]].sum(axis=1)
    temp['total_industrial_emissions'] = temp[emission_sources[3:12]].sum(axis=1)
    temp['total_cultivation_emissions'] = temp[emission_sources[12:]].sum(axis=1)

    means = temp[['total_fire_emissions', 'total_industrial_emissions', 'total_cultivation_emissions',
                   'Agrifood Systems Waste Disposal', 'Food Household Consumption']].mean()

    means.rename({'total_fire_emissions' : 'mean_fire_emissions', 'total_industrial_emissions' : 'mean_industrial_emissions', 
                  'total_cultivation_emissions' : 'mean_cultivation_emissions', 
                  'Agrifood Systems Waste Disposal' :  'mean Agrifood Systems Waste Disposal', 
                  'Food Household Consumption' : 'mean Food Household Consumption'}, inplace=True)

    means.sort_values(ascending=True, inplace=True)

    fig = px.bar(x=means, y=means.index, orientation='h', color=means, 
                 color_continuous_scale='Reds', 
                 labels={'x': 'Mean CO2 emissions (in tons)', 'y': ''})

    fig.update_layout(title='Mean CO2 emissions (in tons) by Agri-food activity',
                      title_font_size=18,
                      xaxis_title_font_size=14,
                      yaxis_title_font_size=14,
                      xaxis_tickfont_size=12,
                      yaxis_tickfont_size=12)

    st.plotly_chart(fig, use_container_width=True)

def graf3(df):
    df_copia = df.copy()
    CO2_df = df[['Area', 'total_emission', 'Average Temperature °C']]
    mean_CO2_df = CO2_df.groupby('Area').mean()

    scaler = MinMaxScaler()
    mean_CO2 = scaler.fit_transform(mean_CO2_df)
    normalized_emission = pd.DataFrame(mean_CO2, columns=['mean_CO2_emission', 'Average Temperature °C'], index=mean_CO2_df.index)
    normalized_emission['Area'] = normalized_emission.index
    normalized_emission['iso_alpha'] = normalized_emission['Area'].apply(get_iso_alpha)

    fig = px.choropleth(
        normalized_emission,
        locations="iso_alpha",
        color="mean_CO2_emission",
        hover_name="Area",
        color_continuous_scale="RdYlBu_r"
    )

    fig2 = px.scatter_geo(
        normalized_emission,
        locations="iso_alpha",
        size="mean_CO2_emission"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout(
        title={'text': "Mean Agrifood CO2 emissions and mean temperature increase by country", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig)

def graf4(df):
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

    fig = px.choropleth(
        normalized_emission,
        locations="iso_alpha",
        color="mean_CO2_emission",
        hover_name="Area",
        color_continuous_scale=["blue", "green", "yellow", "orange", "red"]
    )

    fig2 = px.scatter_geo(
        normalized_emission,
        locations="iso_alpha",
        size="mean_industrial_emissions"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout(
        title={'text': "Mean Agrifood CO2 emissions and mean industrial emissions by country", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig)

def graf5(df):
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

    fig = px.choropleth(
        normalized_emission,
        locations="iso_alpha",
        color="mean_CO2_emission",
        hover_name="Area",
        color_continuous_scale=["blue", "green", "yellow", "orange", "red"]
    )

    fig2 = px.scatter_geo(
        normalized_emission,
        locations="iso_alpha",
        size="mean_waste_emission"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout(
        title={'text': "Mean Agrifood CO2 emissions and agrifood waste disposal emissions by country", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig)

def graf6(df):
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

    fig = px.choropleth(
        normalized_emission,
        locations="iso_alpha",
        color="mean_CO2_emission",
        hover_name="Area",
        color_continuous_scale=["blue", "green", "yellow", "orange", "red"]
    )

    fig2 = px.scatter_geo(
        normalized_emission,
        locations="iso_alpha",
        size="mean_cultivation_emissions"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout(
        title={'text': "Mean Agrifood CO2 emissions and mean cultivation emissions by country", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig)

def graf7(df):
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

    fig = px.choropleth(
        normalized_emission,
        locations="iso_alpha",
        color="mean_CO2_emission",
        hover_name="Area",
        color_continuous_scale=["blue", "green", "yellow", "orange", "red"]
    )

    fig2 = px.scatter_geo(
        normalized_emission,
        locations="iso_alpha",
        size="mean_fire_emissions"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout(
        title={'text': "Mean Agrifood CO2 emissions and mean fire emissions by country", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig)

def graf8(df):
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

    fig = px.choropleth(
        normalized_emission,
        locations="iso_alpha",
        color="mean_CO2_emission",
        hover_name="Area",
        color_continuous_scale=["blue", "green", "yellow", "orange", "red"]
    )

    fig2 = px.scatter_geo(
        normalized_emission,
        locations="iso_alpha",
        size="mean_household_emission"
    )

    fig.add_trace(fig2.data[0])

    fig.update_layout(
        title={'text': "Mean Agrifood CO2 emissions and household consumption emissions by country", 'x': 0.5, 'xanchor': 'center'},
        autosize=False,
        height=600,
        width=1200
    )

    st.plotly_chart(fig)

def draw_tab1(df):
    graf1(df)
    graf2(df)
    graf3(df)
    graf4(df)
    graf5(df)
    graf6(df)
    graf7(df)
    graf8(df)
