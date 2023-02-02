import pandas as pd 
import pandas_dedupe

from inspect import getsourcefile
from os.path import abspath


# Make sure we are getting the absolute path to the training file!
path_arr = abspath(getsourcefile(lambda:0)).split('/')
path_arr.pop()
curpath = '/'.join(path_arr)


def dedupe_names_orgs(data: pd.DataFrame):

    col_map = dict()
    for column in list(data.columns):
        if 'organization_name' in column.lower() or 'name' in column.lower():
            col_map[column] = 'o_name'
        elif column.lower() in 'address_1' or column.lower() in 'address1':
            col_map[column] = 'address_1'
        elif column.lower() in 'address_2' or column.lower() in 'address2':
            col_map[column] = 'address_2'
        elif column.lower() in 'city':
            col_map[column] = 'city'
        elif column.lower() in 'state_province' or column.lower() in 'state':
            col_map[column] = 'state_province'
        elif column.lower() in 'postal_code' or column.lower() in 'postalcode' or column.lower() in 'zip' or column.lower() in 'zip_code':
            col_map[column] = 'postal_code'
        elif column.lower() in 'url' or column.lower() in 'o_url' or column.lower() in 'site' or column.lower() in 'website':
            col_map[column] = 'o_url'

    reverse_map = {v: k for k,v in col_map.items()}
    data.rename(columns=col_map, inplace=True)
    

    df_final = pandas_dedupe.dedupe_dataframe(df=data, field_properties=[
            ('o_name', 'String'),
            ('address_1', 'String'), 
            ('address_2','Text', 'has missing'), 
            ('city','Text','has missing'), 
            ('state_province','Text','has missing'), 
            ('postal_code','Text','has missing'), 
            ('o_url','Text','has missing'), 
            #('l_description','Text','has missing')
        ],
        config_name=curpath + '/names_orgs',

    )


    data.rename(columns=reverse_map, inplace=True)

    final_obj = dict()
    final_obj['original'] = data
    final_obj['dedupe_results'] = df_final
    final_obj['results'] = {}
    return final_obj
    # return data, df_final, 'dedupe_results'



