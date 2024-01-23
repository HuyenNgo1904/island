from django.urls import path, re_path

from islands import views

urlpatterns = [
    path('', views.retrieve_island_list, name='view island'),
]