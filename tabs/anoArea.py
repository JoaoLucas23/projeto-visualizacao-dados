import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def draw_tab4(df):
    st.title("Análise de Emissões de CO2 por Ano e Área")
    # Ordenar o DataFrame
    df_sorted = df.sort_values(['Year', 'total_emission'], ascending=[True, False])
    df_sorted = df_sorted.groupby('Year')

    # Criar a figura
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False, figsize=(20, 10))
    titles = ['Maiores Emissões', 'Maiores Redutores de Carbono']

    for i, emissions_per_year in enumerate([df_sorted.head(3), df_sorted.tail(3)]):
        emissions_per_year = emissions_per_year.copy()
        # Remover categorias não utilizadas
        emissions_per_year['Area'] = emissions_per_year['Area'].astype('category').cat.remove_unused_categories()
        ax_i = ax[i]
        sns.barplot(data=emissions_per_year, x='Year', y='total_emission',
                    hue='Area', ax=ax_i)
        ax_i.set_xlabel('Ano')
        ax_i.set_ylabel('Emissão Total')
        ax_i.set_title(titles[i])
        ax_i.legend(title='Área')

    # Exibir o gráfico
    st.pyplot(fig)