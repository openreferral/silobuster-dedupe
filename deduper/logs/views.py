import json

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from settings import app_logger

from libs.handler.postgres_handler import PostgresHandler


class Index(APIView):
    def get(self, request):
        return Response({
            'available endpoints': 'config, json',
            'instructions': 'Logs can be retrieved one of two ways. 1. pass an "id" of the log. 2. pass a "job_id" and a "step_name"',
            'config': 'Change the settings for the log configuration',
            'json': 'retrieve a json view of the log',
        })

class LogConfig(APIView):

    def get(self, request):
        return Response({
            'default_destination': app_logger.default_destination,
            'db_host': app_logger.db_handler.host,
            'db': app_logger.db_handler.db,
            'database_instructions': 'Configure database logs by providing parameters (host, port, db, username, password)',
        })


    def post(self, request):
        data = request.data

        if data.get('host') and data.get('port') and data.get('db') and data.get('username') and data.get('password'):
            log_handler = PostgresHandler(host=data['host'], port=data['port'], db=data['db'], username=data['username'], password=data['password'])
            app_logger.db_handler = log_handler
            app_logger.default_destination = 'db'

            return Response({
                'status': 'success',
                'message': 'App logger configured to use database',
                'payload': data
            })

        return Response({
            'status': 'no_action'
        })
    

class JSONView(APIView):
    def get(self, request):
        data = request.data
        kwargs = {k:v for k,v in data.items()} # Not sure if this is needed. But converting to regular dict anyways.
        logs = app_logger.get(**kwargs)

        return Response({
            'status': 'success',
            'payload': logs
        })
        