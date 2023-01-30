from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from settings import app_logger

from libs.handler.postgres_handler import PostgresHandler


class Index(APIView):
    def get(self, request):
        return Response({
            'available endpoints': 'config'
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