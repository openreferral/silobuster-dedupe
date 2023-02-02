import pandas as pd



def exact_identifier(df: pd.DataFrame):
    
    df.fillna("",inplace=True)
    duplicates = pd.DataFrame(columns=[*df.columns, "original_organization_id", "original_source_organization_id", "original_name", "original_identifier"])
    uniques = pd.DataFrame(columns=df.columns)
    
    for index, row in df.iterrows():
        if row["identifier"] == "":
            uniques.loc[len(uniques.index)] = row
            continue
            
        unique_flag = True
        unique_row = uniques.loc[(uniques['identifier']) == row['identifier']]
        if not unique_row.empty:
            row['original_organization_id'] = unique_row.iloc[0]['organization_id']
            row['original_source_organization_id'] = unique_row.iloc[0]['source_organization_id']
            row['original_name'] = unique_row.iloc[0]['name']
            row['original_identifier'] = unique_row.iloc[0]['identifier']
            duplicates.loc[len(duplicates.index)] = row
            
            unique_flag = False
    
        if unique_flag:
            uniques.loc[len(uniques.index)] = row
    
    uniques.fillna("",inplace=True)
    duplicates.fillna("",inplace=True)
    return {
        'results': uniques,
        'duplicates': duplicates,
        'original': df
    }

