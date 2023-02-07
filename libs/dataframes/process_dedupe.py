import pandas as pd


def deduplicate(df: pd.DataFrame, lower_threshold: float=.5, upper_threshold: float=.999):

    df.fillna("",inplace=True)
    duplicates = pd.DataFrame(columns=[*df.columns, "original_id", "original_name", "original_website"])
    uniques = pd.DataFrame(columns=df.columns)
    
    for index, row in df.iterrows():
    
        if not unique_row.empty:
            row['original_id'] = unique_row.iloc[0]['id']
            row['original_name'] = unique_row.iloc[0]['name']
            row['original_website'] = unique_row.iloc[0]['website']
            duplicates.loc[len(duplicates.index)] = row
            unique_flag = False
    
        if unique_flag:
            uniques.loc[len(uniques.index)] = row
    
    uniques.drop(columns=['key',], inplace=True)
    duplicates.drop(columns=['key',], inplace=True)
    df.drop(columns=['key',], inplace=True)
    return {
        'results': uniques,
        'duplicates': duplicates,
        'original': df
    }
