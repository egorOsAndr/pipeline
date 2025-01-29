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
        }, inplace=True
    )

    planet_resid_df.rename(
        columns={
            'url': 'url_planet',
            'residents': 'url_resident'
        }, inplace=True
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


def transform_swapi_species(
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sw_species = requester_sw_ram.SWAPIRequester()
    df = pd.DataFrame(sw_species.get_all_species())

    needed_columns: list[str] = [
        'url',
        'name',
        'classification',
        'average_height',
        'average_lifespan',
        'homeworld',
        'language',
        'people',
        'films'
    ]

    df = df[needed_columns]
    species_main_df = df.drop(columns=['people', 'films'])
    species_people_df = df[['url', 'people']].explode('people')
    species_film_df = df[['url', 'films']].explode('films')

    species_main_df.rename(
        columns={
            'url': 'species_url'
        }, inplace=True
    )

    species_people_df.rename(
        columns={
            'url': 'url_species',
            'people': 'url_people'
        }, inplace=True
    )

    species_film_df.rename(
        columns={
            'url': 'url_species',
            'films': 'url_film'
        }, inplace=True
    )

    species_main_df['average_height'] = pd.to_numeric(
        species_main_df['average_height'], errors='coerce'
    )
    species_main_df['average_lifespan'] = pd.to_numeric(
        species_main_df['average_lifespan'], errors='coerce'
    )
    return species_main_df, species_people_df, species_film_df


def transform_swapi_vehicles(
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    obj_sw = requester_sw_ram.SWAPIRequester()
    df = pd.DataFrame(obj_sw.get_all_vehicles())

    needed_columns: list[str] = [
        'url',
        'model',
        'manufacturer',
        'cost_in_credits',
        'length',
        'max_atmosphering_speed',
        'crew',
        'passengers',
        'cargo_capacity',
        'vehicle_class',
        'pilots',
        'films'
    ]

    df = df[needed_columns]
    vehicles_main_df = df.drop(columns=['pilots', 'films'])
    vehicles_pilots_df = df[['url', 'pilots']].explode('pilots')
    vehicles_films_df = df[['url', 'films']].explode('films')

    columns_numer: list[str] = [
        'cost_in_credits',
        'length',
        'max_atmosphering_speed',
        'crew',
        'passengers',
        'cargo_capacity'
    ]

    for col in columns_numer:
        vehicles_main_df[col] = pd.to_numeric(
            vehicles_main_df[col], errors='coerce'
            )

    vehicles_main_df.rename(
        columns={
            'url': 'url_vehicles'
        }, inplace=True
    )

    vehicles_films_df.rename(
        columns={
            'url': 'url_vehicles',
            'films': 'url_films'
        }, inplace=True
    )

    vehicles_pilots_df.rename(
        columns={
            'url': 'url_vehicles',
            'pilots': 'url_pilots'
        }, inplace=True
    )
    return vehicles_main_df, vehicles_pilots_df, vehicles_films_df


def transform_ram_characters(
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    obj_ram = requester_sw_ram.RickAndMortyRequester()
    df = pd.DataFrame(obj_ram.get_all_characters())

    needed_columns: list[str] = [
        'id',
        'name',
        'status',
        'species',
        'gender',
        'location',
        'episode',
        'url'
    ]

    df = df[needed_columns]

    charactes_main_df = df.drop(columns=['location', 'episode'])
    charactes_locat_df = df[['id', 'location']].explode('location')
    charactes_epis_df = df[['id', 'episode']].explode('episode')

    charactes_main_df.rename(
        columns={
            'url': 'url_charactes'
        }, inplace=True
    )

    charactes_locat_df.rename(
        columns={
            'id': 'id_charactes',
            'location': 'url_location'
        }, inplace=True
    )

    charactes_epis_df.rename(
        columns={
            'id': 'id_charactes',
            'episode': 'url_episode'
        }, inplace=True
    )
    return charactes_main_df, charactes_locat_df, charactes_epis_df


def transform_ram_locations() -> Tuple[pd.DataFrame, pd.DataFrame]:
    obj_locat = requester_sw_ram.RickAndMortyRequester()
    df = pd.DataFrame(obj_locat.get_all_locations())

    locat_main_df = df.drop(columns=['created', 'residents'])
    locat_resid_df = df[['id', 'residents']].explode('residents')

    locat_main_df.rename(
        columns={
            'url': 'url_location'
        }, inplace=True
    )

    locat_resid_df.rename(
        columns={
            'residents': 'url_residents',
            'id': 'id_location'
        }, inplace=True
    )
    return locat_main_df, locat_resid_df


def transform_ram_episodes() -> Tuple[pd.DataFrame, pd.DataFrame]:
    obj_ep = requester_sw_ram.RickAndMortyRequester()
    df = pd.DataFrame(obj_ep.get_all_episodes())

    epis_main_df = df.drop(columns=['episode', 'characters', 'created'])
    epis_charac_df = df[['id', 'characters']].explode('characters')

    epis_charac_df.rename(
        columns={
            'id': 'id_episod',
            'characters': 'url_characters'
        }, inplace=True
    )
    epis_main_df['air_date'] = pd.to_datetime(
        epis_main_df['air_date'], errors='coerce'
        )
    return epis_main_df, epis_charac_df
