'''
Deduplicates HSDS3 formatted addresses using exact matching on name, address_1, address_2, city, state_province, and postal_code
'''

import pandas as pd
import pandas_dedupe


addr2_types = [
    'rm',
    'bldg',
    'apt',
    'unit'
]


def split_addresses(addr1: str, addr2: str=""):
    addr1 = addr1.lower()
    addr2 = addr2.lower()

    comma_index = addr1.find(',')
    if comma_index > -1 and addr2 != "":
        addr1, addr2 = addr1.split(',', 1)

    parts = addr1.split(' ')
    numerical, street_name, street_type = parts[0], " ".join(parts[1: len(parts)-2]), parts[len(parts)-1]
    return numerical, street_name, street_type, addr2



def deduplicate_exact_match_address(df: pd.DataFrame):
    df.fillna("",inplace=True)
    df['key'] = df.apply(lambda row: str(row['name']).lower().replace(' ', '') + str(row['address_1']).lower().replace(' ', '') + str(row['address_2']).lower().replace(' ', '') + str(row['city']).lower().replace(' ', '') + str(row['state_province']).lower().replace(' ', '') + str(row['address_2']).lower()[:5], axis = 1)
    duplicates = pd.DataFrame(columns=[*df.columns, "original_organization_id", "original_name", "original_address_1", "original_address_2", "original_city", "original_city", "original_state_province", "original_postal_code"])    
    uniques = pd.DataFrame(columns=df.columns)
    
    for index, row in df.iterrows():
        unique_flag = True

        unique_row = uniques.loc[(uniques['key'] == str(row['name']).lower().replace(' ', '') + str(row['address_1']).lower().replace(' ', '') + str(row['address_2']).lower().replace(' ', '') + str(row['city']).lower().replace(' ', '') + str(row['state_province']).lower().replace(' ', '') + str(row['address_2']).lower()[:5])]
        if not unique_row.empty:
            row['original_organization_id'] = unique_row.iloc[0]['organization_id']
            row['original_name'] = unique_row.iloc[0]['name']
            row['original_address_1'] = unique_row.iloc[0]['address_1']
            row['original_address_2'] = unique_row.iloc[0]['address_2']
            row['original_city'] = unique_row.iloc[0]['city']
            row['state_province'] = unique_row.iloc[0]['state_province']
            row['postal_code'] = unique_row.iloc[0]['postal_code']
            duplicates.loc[len(duplicates.index)] = row
            unique_flag = False

        if unique_flag:
            uniques.loc[len(uniques.index)] = row

    
    uniques.drop(columns=['key',], inplace=True)
    uniques.fillna("",inplace=True)
    duplicates.fillna('', inplace=True)

    return {
        'results': uniques,
        'duplicates': duplicates,
        'original': df
    }


