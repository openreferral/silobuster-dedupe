
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class HomeView(APIView):

    def post(self, request):

        data = request.data 
        return Response({
            'status': 'success',
            'message': 'Welcome to SiloBuster! You made a POST request to root. But, there is nothing here for you to post. Please use the get method to get more details'
        })

    def delete(self, request):

        data = request.data 
        return Response({
            'status': 'success',
            'message': 'Welcome to SiloBuster! You made a DELETE request to root. But, there is nothing here for you to delete. Please use the get method to get more details'
        })

    def put(self, request):

        data = request.data 
        return Response({
            'status': 'success',
            'message': 'Welcome to SiloBuster! You made a PUT request to home. But, there is nothing here for you to update. Please use the get method to get more details'
        })

    def get(self, request):

        data = request.data 
        return Response({
            'status': 'success',
            'message': 'Welcome to SiloBuster! Documentation is coming soon...'
        })