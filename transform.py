import requester_sw_ram
from typing import Tuple
import pandas as pd


def transform_swapi_people() -> pd.DataFrame:
    sw_people = requester_sw_ram.SWAPIRequester()
    df = pd.DataFrame(sw_people.get_all_people())
    needed_columns: list[str] = [
        'name',
        'height',
        'mass',
        'gender',
        'homeworld',
        'url'
        ]

    df = df[needed_columns]

    df.rename(
        columns={
            'homeworld': 'url_homeworld',
            'url': 'url_person'
            },
        inplace=True
        )

    df['height'] = pd.to_numeric(df['height'], errors='coerce')
    df['mass'] = pd.to_numeric(df['mass'], errors='coerce')
    return df


def transform_swapi_planets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    sw_planets = requester_sw_ram.SWAPIRequester()
    df = pd.DataFrame(sw_planets.get_all_planets())
    needed_columns: list[str] = [
        'url',
        'name',
        'rotation_period',
        'orbital_period',
        'diameter',
        'climate',
        'population',
        'residents'
    ]

    df = df[needed_columns]
    planet_main_df = df.drop(columns=['residents'])
    planet_resid_df = df[['url', 'residents']].explode('residents')

    planet_main_df.rename(
        columns={
            'url': 'url_planet'
        }
    )

    planet_resid_df.rename(
        columns={
            'url': 'url_planet',
            'residents': 'url_resident'
        }
    )

    columns_numer: list[str] = [
        'rotation_period',
        'orbital_period',
        'diameter',
        'population'
    ]
    for col in columns_numer:
        planet_main_df[col] = pd.to_numeric(
            planet_main_df[col], errors='coerce'
        )
    return planet_main_df, planet_resid_df


def transform_swapi_films() -> Tuple[pd.DataFrame, pd.DataFrame]:
    sw_films = requester_sw_ram.SWAPIRequester()
    df = pd.DataFrame(sw_films.get_all_films())

    needed_columns: list[str] = [
        'url',
        'title',
        'episode_id',
        'director',
        'producer',
        'release_date',
        'characters'
    ]
    df = df[needed_columns]

    films_main_df = df.drop(columns=['characters'])
    film_characters_df = df[['url', 'characters']].explode('characters')

    films_main_df.rename(
        columns={
            'url': 'url_film'
        }, inplace=True
    )

    film_characters_df.rename(
        columns={
            'url': 'url_film',
            'characters': 'url_charact'
        }, inplace=True
    )
    films_main_df['release_date'] = pd.to_datetime(
        films_main_df['release_date'], errors='coerce'
        )
    return films_main_df, film_characters_df


def transform_swapi_species():
    sw_species = requester_sw_ram.SWAPIRequester()
    df = pd.DataFrame(sw_species.get_all_species())

    return df