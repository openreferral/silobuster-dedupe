import pandas as pd


def to_list_of_dicts(df: pd.DataFrame):

    row_count, col_count = df.shape
    keys = df.columns
    results = list()
    for i in range(row_count):
        results.append( {key: df.at[i,key] for key in keys} )
        
    return results