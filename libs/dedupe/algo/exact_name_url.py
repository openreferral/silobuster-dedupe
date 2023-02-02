import pandas as pd



def extract_url(base_url: str):
    if not base_url:
        return ''
    
    if '//' in base_url.lower():
        base_url = base_url[base_url.find('//')+2:]
    if 'www.' in base_url.lower():
        base_url = base_url[base_url.find('www.')+4:]
    
    if base_url[-1:] == '/':
        base_url = base_url[:-1]
        
    return base_url


def create_index(url: str, name: str):
    url = extract_url(url).lower().strip()
    name = name.replace(' ', '').lower().strip()
    return url + name


def exact_name_url(df: pd.DataFrame):
    
    df.fillna("",inplace=True)
    df['key'] = df.apply(lambda row: create_index(row['website'], row['name']), axis = 1)
    duplicates = pd.DataFrame(columns=[*df.columns, "original_id", "original_name", "original_website"])
    uniques = pd.DataFrame(columns=df.columns)
    
    for index, row in df.iterrows():
        if row["website"] == "":
            uniques.loc[len(uniques.index)] = row
            continue
            
        unique_flag = True

        unique_row = uniques.loc[(uniques['key'] == create_index(row["website"], row["name"]))]
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

