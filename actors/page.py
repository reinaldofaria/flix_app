import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid
from actors.services import ActorService


def show_actors():
    actor_service = ActorService()
    actors = actor_service.get_actors()

    if actors:
        st.write('Lista de Atores:')
        actors_df = pd.json_normalize(actors)
        AgGrid(
            data=actors_df,
            reload_data=True,
            key='actors_grid',
        )
    else:
        st.warning('Nenhum ator encontrado.')

    st.title('Cadastrar novo Ator')
    name = st.text_input('Nome do Ator')
    birthday = st.date_input(
        label='Data de Nascimento',
        value=datetime.today(),
        min_value=datetime(1600, 1, 1).date(),
        max_value=datetime.today(),
        format='DD/MM/YYYY',
    )
    nationality_dropdown = ['BR', 'USA']
    nationality = st.selectbox(
        label='Nacionalidades',
        options=nationality_dropdown,
    )
    if st.button('Cadastrar'):
        new_actors = actor_service.create_actor(
            name=name,
            birthday=birthday,
            nationality=nationality,
        )
        if new_actors:
            st.rerun()
        else:
            st.error('Erro ao cadastrar novo ator. Verifique os campos')
