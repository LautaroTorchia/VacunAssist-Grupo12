from django import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from ..views.administrator_view import *
from ..views.vaccinator_list_view import *

urlpatterns = [
    path("", administrator_home_view, name="admin-home-view"),
    path("create_vaccinator/",
         validating_dni_for_vaccinator_view,
         name="creating-vaccinator-view"),
    path("create_vaccinator/step2",
         creating_vaccinator_view,
         name="create_vaccinator_step2"),
    path("vaccinators_list/", vaccinators_list_view, name="vaccinators_list"),
    path("stock/", stock_view, name="stock_view"),
    path('cambiarNombre/', NameUpdate.as_view(), name="cambiarNombre"),
    path('vaccinator/<int:id>/',
         edit_vaccinator_profile_view,
         name="edit_vaccinator_profile"),
    path('vaccinator/<int:id>/delete',
         vaccinator_delete_view,
         name="vaccinator_delete"),
]
