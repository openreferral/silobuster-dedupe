import json

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from settings import DEDUPLICATION_STEPS, app_logger

from libs.handler.postgres_handler import PostgresHandler
from libs.connector.postgres_connector import PostgresToPostgresConnector
from libs.dataframes.to_types import to_list_of_dicts


class Options(APIView):
    
    def get(self, request):
        
        return Response({
            'available_steps': DEDUPLICATION_STEPS.keys()
        })

    

class DatabaseToDatabase(APIView):

    def get(self, request):
        data = dict()
        instructions = {
            'supports': 'Postgres',
            'source_query': 'Query to select the fields for deduplication. This should be a SELECT query',
            'destination_query': 'Query to write the fields for deduplication. This should be an INSERT query. Please use %s for the value placeholders without quotes. i.e. INSERT INTO transformed (first_name, last_name) VALUES (%s, %s). This is the transformed data, not the logs. For logs, please refer to /logs',
            'write_logs': 'Specifies whether each step is logged',
            'source': 'Pass all source parameters to pull data from your database. Paramaters are (source_host, source_db, source_port, source_username, source_password, source_query)',
            'destination': 'Pass all destination parameters to write final results to your database. Paramaters are (destination_host, destination_db, destination_port, destination_username, destination_password, destination_query)',
            'env_source_prefix': 'The server will attempt to retrieve the source settings from the environment using the specified prefix',
            'env_destination_prefix': 'The server will attempt to retrieve the destination settings from the environment using the specified prefix',
            'steps': 'The server will transform the data using the steps provided in the order they are received. If this parameter is not supplied, all steps will be performed. The format for steps should be a list of function names. See available steps',
            'available_steps': DEDUPLICATION_STEPS.keys()
        }
        data['instructions'] = instructions

        return Response({
            'status': 'success',
            'instructions': instructions,
        })


    def post(self, request):
        print ('Recieved transform request...')
        data = request.data
        print (data)
        
        # We dont need to check if the parameters are passed because that is handled on the Connector class. Just in case...
        # if data.get('source_db') and data.get('source_host') and data.get('source_username') and data.get('source_passsword') and data.get('source_query'):
        #    pass
        write_logs = data.get('write_logs') if data.get('write_logs') else True
        if not data.get('source_query') or not data.get('destination_query'):
            return Response({
                'status': 'error',
                'message': 'Please provide a source and a destination query in your request (source_query, destination_query). For more information on how to use this endpoint, make a get request.'
            })

        input_handler = PostgresHandler(
            host=data.get('source_host'), 
            port=data.get('source_port'), 
            db=data.get('source_db'), 
            username=data.get('source_username'), 
            password=data.get('source_password'),
            query=data.get('source_query'), 
            env_prefix=data.get('env_source_prefix')
        )
        
        output_handler = PostgresHandler(
            host=data.get('destination_host'), 
            port=data.get('destination_port'), 
            db=data.get('destination_db'), 
            username=data.get('destination_username'), 
            password=data.get('destination_password'), 
            query=data.get('destination_query'),
            env_prefix=data.get('env_destination_prefix')
        )

        connector = PostgresToPostgresConnector(
            input_handler=input_handler, 
            output_handler=output_handler, 
            log_handler=app_logger, 
            write_logs=write_logs
        )
        
        steps = DEDUPLICATION_STEPS
        
        if data.get('steps'):
            for step in data.get('steps'):
                if DEDUPLICATION_STEPS.get(step):
                    steps[step] = DEDUPLICATION_STEPS[step]

            steps = data.get('steps')
        
        
        try:
            results = connector.transform(connector.parse_steps(steps))
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Error in transforming data'
            })

        return Response({
            'status': 'success',
            'payload': results
        })