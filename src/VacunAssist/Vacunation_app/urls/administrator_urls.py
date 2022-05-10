from django import views
from django.contrib import admin
from django.urls import path

from ..views.administrator_view import administrator_home_view, creating_vaccinator_view, vaccinators_list_view

urlpatterns = [
    path("", administrator_home_view, name="admin-home-view"),
    path("create_vaccinator/",
         creating_vaccinator_view,
         name="creating-vaccinator-view"),
    path("vaccinators_list/", vaccinators_list_view, name="vaccinators_list"),
]
