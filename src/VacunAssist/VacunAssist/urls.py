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
from Vacunation_app.views.login_view import CustomLogin, CustomLoginClave
from Vacunation_app.views.home_view import HomeView, contact_view, logout_view, notification_view, zona_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLogin.as_view(), name="login"),
    path('accounts/loginClave/', CustomLoginClave.as_view(),name="loginClave"),
    path("logout",logout_view,name="logout"),
    path("administrator/",include("Vacunation_app.urls.administrator_urls"),name="admin-home-view"),
    path("vaccinator/",include("Vacunation_app.urls.vaccinator_urls"),name="vaccinator-home-view"),
    path("patient/",include("Vacunation_app.urls.patient_urls"),name="patient-home-view"),
    path('', HomeView.as_view(), name='homepage'),
    path("zona",zona_view,name="zona"),
    path("notifications",notification_view,name="notifications"),
    path("contact",contact_view,name="contact_us"),
    path('accounts/', include('django.contrib.auth.urls')),#!Revisar recuperar contraseña
]
