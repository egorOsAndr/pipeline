from transform import (
    transform_swapi_people,
    transform_swapi_films
)
from loader import (
    get_engine,
    load_df_to_db
)


def load_swapi_data():
    engine = get_engine(
        user='egor',
        password='',
        host='localhost',
        port='5432',
        dbname='egor'
    )

    df_people = transform_swapi_people()
    load_df_to_db(df_people, 'people', engine, if_exists='replace')

    films_main_df, film_characters_df = transform_swapi_films()
    load_df_to_db(films_main_df, 'films', engine, 'replace')
    load_df_to_db(film_characters_df, 'film_characters', engine, 'replace')


if __name__ == '__main__':
    load_swapi_data()
