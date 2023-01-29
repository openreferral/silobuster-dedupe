import sys
import os

import json
import csv

import pandas as pd 
import pandas_dedupe


def dedupe_names_orgs(data: pd.DataFrame):
    df_final = pandas_dedupe.dedupe_dataframe(data, [
        ('o_name', 'String'),
        ('address_1', 'String'), 
        ('address_2','Text', 'has missing'), 
        ('city','Text','has missing'), 
        ('state_province','Text','has missing'), 
        ('postal_code','Text','has missing'), 
        ('o_url','Text','has missing'), 
        #('l_description','Text','has missing')
    ])

    return data, df_final, 'dedupe_results'