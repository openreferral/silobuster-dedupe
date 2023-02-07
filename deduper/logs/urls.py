from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.Index.as_view()),
    path('json', views.JSONView.as_view()),
    path('config', views.LogConfig.as_view()),
]