import json

from settings import DEDUPLICATION_STEPS, app_logger

from libs.handler.postgres_handler import PostgresHandler
from libs.handler.json_handler import JsonHandler
from libs.handler.excel_handler import ExcelHandler
from libs.connector.postgres_connector import PostgresToPostgresConnector, PostgresToJsonConnector, PostgresToExcelConnector
from libs.dataframes.to_types import to_list_of_dicts



def ProcessDbToDb(data: dict):
    # We dont need to check if the parameters are passed because that is handled on the Connector class. Just in case...
    # if data.get('source_db') and data.get('source_host') and data.get('source_username') and data.get('source_passsword') and data.get('source_query'):
    #    pass
    write_logs = data.get('write_logs') if data.get('write_logs') else True
    if not data.get('source_query') or not data.get('destination_query'):
        return {
            'status': 'error',
            'message': 'Please provide a source and a destination query in your request (source_query, destination_query). For more information on how to use this endpoint, make a get request.'
        }

    source_schema = 'public'
    if data.get('source_schema'):
        source_schema = data.get('source_schema')

    destination_schema = 'public'
    if data.get('destination_schema'):
        destination_schema = data.get('destination_schema')

    input_handler = PostgresHandler(
        host=data.get('source_host'), 
        port=data.get('source_port'), 
        db=data.get('source_db'), 
        username=data.get('source_username'), 
        password=data.get('source_password'),
        query=data.get('source_query'),
        schema=source_schema,
        env_prefix=data.get('env_source_prefix')
    )
    
    output_handler = PostgresHandler(
        host=data.get('destination_host'), 
        port=data.get('destination_port'), 
        db=data.get('destination_db'), 
        username=data.get('destination_username'), 
        password=data.get('destination_password'), 
        query=data.get('destination_query'),
        schema=destination_schema,
        env_prefix=data.get('env_destination_prefix')
    )

    connector = PostgresToPostgresConnector(
        input_handler=input_handler, 
        output_handler=output_handler, 
        log_handler=app_logger, 
        write_logs=write_logs
    )
    
    # steps = DEDUPLICATION_STEPS
    steps = dict()
    
    if data.get('steps'):
        for step in data.getlist('steps'):
            if DEDUPLICATION_STEPS.get(step):
                steps[step] = DEDUPLICATION_STEPS[step]

    # steps = data.get('steps')
    #try:
    job_id = connector.mutate(connector.parse_steps(steps))
    if not data.get('dry_run'):
        connector.write()

    #except Exception as e:
    #    return {
    #        'status': 'error',
    #        'message': f'Error in transforming data {e}'
    #    }

    return {
        'status': 'success',
        'message': 'Results delivered to db',
        'payload': {
            'job_id': job_id
        }
    }


def ProcessDbToJSON(data: dict):
    # We dont need to check if the parameters are passed because that is handled on the Connector class. Just in case...
    # if data.get('source_db') and data.get('source_host') and data.get('source_username') and data.get('source_passsword') and data.get('source_query'):
    #    pass
    write_logs = data.get('write_logs') if data.get('write_logs') else True
    if not data.get('source_query') or not data.get('destination_query'):
        return {
            'status': 'error',
            'message': 'Please provide a source and a destination query in your request (source_query, destination_query). For more information on how to use this endpoint, make a get request.'
        }

    source_schema = 'public'
    if data.get('source_schema'):
        source_schema = data.get('source_schema')


    input_handler = PostgresHandler(
        host=data.get('source_host'), 
        port=data.get('source_port'), 
        db=data.get('source_db'), 
        username=data.get('source_username'), 
        password=data.get('source_password'),
        query=data.get('source_query'),
        schema=source_schema,
        env_prefix=data.get('env_source_prefix')
    )
    
    output_handler = JsonHandler()
    connector = PostgresToJsonConnector(
        input_handler=input_handler, 
        output_handler=output_handler, 
        log_handler=app_logger, 
        write_logs=write_logs
    )
    
    # steps = DEDUPLICATION_STEPS
    steps = dict()
    
    if data.get('steps'):
        for step in data.getlist('steps'):
            if DEDUPLICATION_STEPS.get(step):
                steps[step] = DEDUPLICATION_STEPS[step]

    # steps = data.get('steps')
    #try:
    job_id = connector.mutate(connector.parse_steps(steps))
    results = connector.write()

    #except Exception as e:
    #    return {
    #        'status': 'error',
    #        'message': f'Error in transforming data {e}'
    #    }

    return {
        'status': 'success',
        'payload': {
            'job_id': job_id,
            'results': results
        }
    }


def ProcessDbToExcel(data: dict):
    # We dont need to check if the parameters are passed because that is handled on the Connector class. Just in case...
    # if data.get('source_db') and data.get('source_host') and data.get('source_username') and data.get('source_passsword') and data.get('source_query'):
    #    pass
    write_logs = data.get('write_logs') if data.get('write_logs') else True
    if not data.get('source_query') or not data.get('destination_query'):
        return {
            'status': 'error',
            'message': 'Please provide a source and a destination query in your request (source_query, destination_query). For more information on how to use this endpoint, make a get request.'
        }

    source_schema = 'public'
    if data.get('source_schema'):
        source_schema = data.get('source_schema')


    input_handler = PostgresHandler(
        host=data.get('source_host'), 
        port=data.get('source_port'), 
        db=data.get('source_db'), 
        username=data.get('source_username'), 
        password=data.get('source_password'),
        query=data.get('source_query'),
        schema=source_schema,
        env_prefix=data.get('env_source_prefix')
    )
    
    output_handler = ExcelHandler()
    connector = PostgresToExcelConnector(
        input_handler=input_handler, 
        output_handler=output_handler, 
        log_handler=app_logger, 
        write_logs=write_logs
    )
    
    # steps = DEDUPLICATION_STEPS
    steps = dict()
    
    if data.get('steps'):
        for step in data.getlist('steps'):
            if DEDUPLICATION_STEPS.get(step):
                steps[step] = DEDUPLICATION_STEPS[step]

    job_id = connector.mutate(connector.parse_steps(steps))
    results = connector.write()

    return job_id, results
