import transform


if __name__ == "__main__":
    planet_main_df = transform.transform_swapi_species()
    print("=== films_main_df ===")
    print(planet_main_df.head())
    print(planet_main_df.columns)
    #print(planet_resid_df.head())
    #print(planet_resid_df.columns)
