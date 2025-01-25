import transform


if __name__ == "__main__":
    df_people = transform.transform_swapi_planets()
    print(f"Всего строк: {len(df_people)}")
