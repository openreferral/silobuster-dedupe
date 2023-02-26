'''
Deduplicates addresses using the dedupe.io (Pandas version) using name, address_1, address_2, city, state_province, and postal_code
'''
import pandas as pd
import pandas_dedupe

from inspect import getsourcefile
from os.path import abspath
from libs.uuid import random_uuid
import datetime


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



def dedupe_io_names_addresses(df: pd.DataFrame, **kwargs):
    '''
    Requires:
    keyword arguments:
    
    Run dedupe.io and match addresses. Use that data to dedupe within itself and return an organization and an address dataframe that is formatted for a node.
    '''
    lower_threshold = .6
    upper_threshold = .999

    formatted_df =  pd.DataFrame()
    formatted_df = df.copy(deep=True)
    
    formatted_df[['numerical', 'street_name', 'street_type', 'unit']] = formatted_df.apply(lambda row: pd.Series(split_addresses(str(row["address_1"]), str(row["address_2"]))), axis=1)
    formatted_df['postal_code'].map(lambda x: x.replace('-', '').replace(' ', ''))
    # formatted_df.fillna('', inplace=True)

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

    addr_results = pd.DataFrame(columns=['id', 'hsds', 'coordinates', 'aliases'])
    org_results = pd.DataFrame(columns=['id', 'hsds', 'locations', 'attributes', 'aliases'])
    deduper_df = deduper_df.sort_values(by=["cluster id",])
    processed = set()
    current_id = 0
    addr_row = list()

    
    addr_row = list()
    addr_id = random_uuid()
    addr_hsds = dict()
    addr_coordinates = list()
    addr_aliases = list()
    
    org_row = list()
    org_id = random_uuid()
    org_hsds = dict()
    org_locations = set()
    org_attributes = dict()
    org_aliases = list()

    for index, row in deduper_df.iterrows():    

        if row['confidence'] < lower_threshold or row['confidence'] > upper_threshold:
            continue


        
        if current_id != row['cluster id']: # create the new row
            #if index > 0: # skip the first row
            addr_row.append(addr_id)
            addr_row.append(addr_hsds)
            addr_row.append(addr_coordinates)
            addr_row.append(addr_aliases)
            addr_results.loc[len(addr_results)] = addr_row

            org_row.append(org_id)
            org_row.append(org_hsds)
            org_row.append(list(org_locations))
            org_row.append(org_attributes)
            org_row.append(org_aliases)
            org_results.loc[len(org_results)] = org_row

            # Reset the attributes    
            addr_row = list()
            addr_id = random_uuid()
            addr_hsds = dict()
            addr_coordinates = list()
            addr_aliases = list()

            org_row = list()
            org_id = random_uuid()
            org_hsds = dict()
            org_locations = set()
            org_attributes = dict()
            org_aliases = list()
            

        
        org_locations.add(addr_id)

        processed.add(row['address_id']) # Keeps track of processed rows.
        current_id = row['cluster id'] # Controls when the collection is reset... Cluster changes
        
        # Create the 
        #if isinstance(row['latitude'], float) and isinstance(row['longitude'], float):
        addr_coordinates.append({
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'source': row['source']
        })

        addr_aliases.append({
            # 'address_1': row['address_1'],
            # 'address_2': row['address_2'],
            # 'city': row['city'],
            # 'state_province': row['state_province'],
            # 'postal_code': row['postal_code'],
            # 'source': row['source'],
            **row,
            'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s")
        })
        
        org_aliases.append({
            **row,
            'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s")
        })
        


    # Iterate all of the rows from the original dataframe and add any that wasnt duplicated
    for index, row in df.iterrows():
        if row['address_id'] in processed:
            continue

        addr_id = random_uuid()
        addr_results.loc[len(addr_results)] = [
            addr_id,
            {},
            [{
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'source': row['source']
            }],
            [{
                # 'address_1': row['address_1'],
                # 'address_2': row['address_2'],
                # 'city': row['city'],
                # 'state_province': row['state_province'],
                # 'postal_code': row['postal_code'],
                # 'source': row['source'],
                'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s"),
                **row,
            }],
        ]

        org_results.loc[len(org_results)] = [
            random_uuid(),
            {},
            [addr_id,],
            {},
            [{
                'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s"),
                **row,
            }]

        ]

    return {
        'address_results': addr_results,
        'org_results': org_results,
        'dedupe_io_results': deduper_df,
        'original': df
    }

