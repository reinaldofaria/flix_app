import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
from genres.service import GenreService


def show_genres():
    genre_service = GenreService()
    genres = genre_service.get_genres()

    if genres:
        st.write('Lista de Gêneros:')
        genres_df = pd.json_normalize(genres)
        AgGrid(
            data=genres_df,
            reload_data=True,
            key='genres_grid',
        )
    else:
        st.warning('Nenhum gênero encontrado.')

    st.title('Cadastrar novo Gênero')
    name = st.text_input('Nome do Gênero')
    if st.button('Cadastrar'):
        new_genres = genre_service.create_genre(
            name=name
        )
        if new_genres:
            st.rerun()
        else:
            st.error('Erro ao cadastrar novo gênero. Verifique os campos')
