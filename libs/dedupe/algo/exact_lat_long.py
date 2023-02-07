'''
Deduplicates HSDS3 formatted latitude and longitude using exact matches.
'''


import pandas as pd


def exact_lat_long(df: pd.DataFrame):

    df.fillna("", inplace=True)
    df['key'] = df.apply(lambda row: str(row['name']).replace(' ', '').lower().strip() + str(row['latitude']) + str(row['longitude']), axis = 1)
    duplicates = pd.DataFrame(columns=[*df.columns, "original_id", "original_name", "original_latitude", "original_longitude"])
    uniques = pd.DataFrame(columns=df.columns)
    

    for index, row in df.iterrows():
        # if row["latitude"] == "" or row["longitude"] == "" or row["address_1"] == "" or row["address_2"] == "":
        if row["latitude"] == "" or row["longitude"] == "":
            uniques.loc[len(uniques.index)] = row
            continue
            
        unique_flag = True
        
        unique_row = uniques.loc[(uniques['key'] == str(row['name']).replace(' ', '').lower().strip() + str(row['latitude']) + str(row['longitude']))]
        if not unique_row.empty:
            row['original_id'] = unique_row.iloc[0]['id']
            row['original_name'] = unique_row.iloc[0]['name']
            row['original_latitude'] = unique_row.iloc[0]['latitude']
            row['original_longitude'] = unique_row.iloc[0]['longitude']
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

