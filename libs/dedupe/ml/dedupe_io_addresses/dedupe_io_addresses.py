import pandas as pd
import pandas_dedupe

from inspect import getsourcefile
from os.path import abspath

# Make sure we are getting the absolute path to the training file!
path_arr = abspath(getsourcefile(lambda:0)).split('/')
path_arr.pop()
curpath = '/'.join(path_arr)


addr2_types = [
    'rm',
    'bldg',
    'apt',
    'unit'
]


def split_addresses(addr1: str, addr2: str=""):
    addr1 = addr1.lower()
    unit = addr2.lower() if addr2.lower() else ""

    comma_index = addr1.find(',')
    if comma_index > -1 and addr2 != "":
        addr1, unit = addr1.split(',', 1)

    parts = addr1.split(' ')
    numerical, street_name, street_type = parts[0], " ".join(parts[1: len(parts)-2]), parts[len(parts)-1]
    numerical = numerical if numerical else ""
    street_name = street_name if street_name else ""
    street_type = street_type if street_type else ""
    unit = unit if unit else ""
    return numerical, street_name, street_type, unit



def dedupe_io_addresses(df: pd.DataFrame):
    formatted_df =  pd.DataFrame()
    formatted_df = df.copy(deep=True)
    
    formatted_df[['numerical', 'street_name', 'street_type', 'unit']] = formatted_df.apply(lambda row: pd.Series(split_addresses(str(row["address_1"]), str(row["address_2"]))), axis=1)
    formatted_df['postal_code'].map(lambda x: x.replace('-', '').replace(' ', ''))
    formatted_df.fillna('', inplace=True)

    formatted_df.mask(formatted_df == "", inplace=True)
    deduper_df = pandas_dedupe.dedupe_dataframe(df=formatted_df, field_properties=[
            ('name', 'String'),
            ('numerical', 'Exact'), 
            ('street_name', 'String'), 
            ('street_type', 'String', 'has missing'), 
            ('unit','String', 'has missing'), 
            ('city','String'), 
            ('state_province','String'), 
            ('postal_code','Exact'), 
            
            #('l_description','Text','has missing')
        ],
        config_name=curpath + '/dedupe_io_addresses',
    )

    return {
        'results': df,
        'duplicates': deduper_df,
        'original': df
    }

