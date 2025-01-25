import requester_SW_RAM
import pandas as pd


def transform_swapi_people() -> pd.DataFrame:
    sw_people = requester_SW_RAM.SWAPIRequester()
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
            'homeworld': 'homeworld_url',
            'url': 'person_url'
            },
        inplace=True
        )
    df['height'] = pd.to_numeric(df['height'], errors='coerce')
    df['mass'] = pd.to_numeric(df['mass'], errors='coerce')
    return df


def transform_swapi_planets() -> pd.DataFrame:
    sw_planets = requester_SW_RAM.SWAPIRequester()
    df = pd.DataFrame(sw_planets.get_all_planets())
    needed_columns: list[str] = [
        'name',
        'diameter',
        'climate',
        'population',
        'residents'
        'url'
    ]
    df = df[needed_columns]
    print(df.dtypes)
    print(df.head(10))
    return df
