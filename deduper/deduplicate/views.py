import json

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from settings import DEDUPLICATION_STEPS, app_logger

from libs.handler.postgres_handler import PostgresHandler
from libs.connector.postgres_connector import PostgresToPostgresConnector
from libs.dataframes.to_types import to_list_of_dicts

from . import ProcessDbToDb



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
            'schema': 'Optionally, (source_schema destination_schema) can be set',
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
        
        data = request.data

        return Response(ProcessDbToDb(data))


class DatabaseToExcel(APIView):
    pass