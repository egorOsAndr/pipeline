from typing import Literal
import pandas as pd
from sqlalchemy import create_engine


def get_engine(
    user: str = 'egor',
    password: str = '',
    host: str = 'localhost',
    port: str = '5432',
    dbname: str = 'egor'
):
    db_url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    engine = create_engine(db_url, echo=False)
    return engine


def load_df_to_db(
    df: pd.DataFrame,
    table_name: str,
    engine,
    if_exists: Literal['fail', 'replace', 'append'] = 'replace'
):
    df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
