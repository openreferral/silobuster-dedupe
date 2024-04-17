import json

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from settings import DEDUPLICATION_STEPS, app_logger

from libs.handler.postgres_handler import PostgresHandler
from libs.connector.postgres_connector import PostgresToPostgresConnector
from libs.dataframes.to_types import to_list_of_dicts

from .process_requests import ProcessDbToDb, ProcessDbToJSON, ProcessDbToExcel



class Options(APIView):
    
    def get(self, request):
        
        return Response({
            'available_steps': DEDUPLICATION_STEPS.keys()
        })

    
class Instructions(APIView):
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
            'url_format': 'job/input/output.',
            'available_inputs': 'postgres',
            'available_outputs': 'postgres, json, excel',
            'available_jobs': 'dedupe_urls, dedupe_organization_identifiers, dedupe_addresses',
            'dry_run': 'Boolean value that specifies whether a write of the results will be performed. If it is set to True, then only a log will be written.'
        }

        data['instructions'] = instructions

        return Response({
            'status': 'success',
            'instructions': instructions,
        })


class DatabaseToDatabase(APIView):    
    
    #  job: dict={ 'exact_name_url': 'deduplicate_exact_match_name_url' }

    @staticmethod
    def post(request):
        data = request.data
        return Response(ProcessDbToDb(data))


class DatabaseToJSON(APIView):

    @staticmethod
    def post(request):
        data = request.data
        return Response(ProcessDbToJSON(data))


class DatabaseToExcel(APIView):
    
    @staticmethod
    def post(request):
        data = request.data
        job_id, content = ProcessDbToExcel(data)
        response = Response(
            headers={'Content-Disposition': f'attachment; filename={job_id}.xlsx'},
            content_type='application/excel'
        )
        response.content = content
        return response