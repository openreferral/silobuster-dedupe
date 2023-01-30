import pandas as pd 



def create_map_from_dedupe_definition(definition: list, df: pd.DataFrame):

    old_names = [item[0] for item in definition]
    new_names = df.columns
