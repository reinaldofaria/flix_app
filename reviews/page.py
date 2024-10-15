import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from reviews.service import ReviewsService
from movies.service import MovieService


def show_reviews():
    reviews_service = ReviewsService()
    reviews = reviews_service.get_reviews()

    if reviews:
        st.write('Lista de Avaliações:')

        reviews_df = pd.json_normalize(reviews)

        AgGrid(
            data=reviews_df,
            reload_data=True,
            key='reviews_grid',
        )
    else:
        st.warning('Nenhuma avaliação encontrada.')

    st.title('Cadastrar Nova Avaliação')

    movie_service = MovieService()
    movies = movie_service.get_movies()
    movies_titles = {movie['title']: movie['id'] for movie in movies}
    selected_movie_title = st.selectbox('Filme', list(movies_titles.keys()))

    stars = st.number_input(
        label='Estrelas',
        min_value=0,
        max_value=5,
        step=1,
    )
    comment = st.text_area('Comentário')

    if st.button('Cadastrar'):
        new_reviews = reviews_service.create_review(
            movie=movies_titles[selected_movie_title],
            stars=stars,
            comment=comment,
        )
        if new_reviews:
            st.rerun()
        else:
            st.error('Erro ao cadastrar a avaliação. Verifique os campos')
