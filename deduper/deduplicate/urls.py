from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('options', views.Options.as_view()),
    path('', views.Instructions.as_view()),
    path('database/database', views.DatabaseToDatabase.as_view()),
    path('database/json', views.DatabaseToJSON.as_view()),
    path('database/excel', views.DatabaseToExcel.as_view()),
]