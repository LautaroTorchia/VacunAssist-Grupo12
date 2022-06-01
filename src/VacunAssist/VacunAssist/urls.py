"""VacunAssist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from Vacunation_app.views.accounts.login_view import CustomLogin, CustomLoginClave
from Vacunation_app.views.accounts.registration_view import registration_view
from Vacunation_app.views.homes.vaccinator_home_view import  contact_view, logout_view, notification_view, zona_view
from Vacunation_app.views.redirect_view import HomeRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLogin.as_view(), name="login"),
    path('accounts/loginClave/', CustomLoginClave.as_view(),name="loginClave"),
    path("logout",logout_view,name="logout"),
    path('', HomeRedirectView.as_view(), name='redirectHome'),
    path("zona",zona_view,name="zona"),
    path("notifications",notification_view,name="notifications"),
    path("contact",contact_view,name="contact_us"),
    path("registration",registration_view,name="registrate"),
    path("administrator/",include("Vacunation_app.urls.administrator_urls"),name="admin_views"),
    path("vaccinator/",include("Vacunation_app.urls.vaccinator_urls"),name="vaccinator_views"),
    path("patient/",include("Vacunation_app.urls.patient_urls"),name="patient_views"),
    path('accounts/', include('django.contrib.auth.urls')),#!Revisar recuperar contraseña
]