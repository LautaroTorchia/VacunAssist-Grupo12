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
from Vacunation_app.views.vaccinator_list_view import vaccinator_delete_view
from Vacunation_app.views.home_view import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("administrator/",include("Vacunation_app.urls.administrator_urls"), name="admin-home-view"),
    path('accounts/login/',CustomLogin.as_view(template_name='registration/login.html'),name="login"),
    path('accounts/loginClave/',CustomLoginClave.as_view(template_name='registration/loginClave.html'),name="loginClave"),
    path('products/<int:id>/delete/',vaccinator_delete_view,name='vaccinator_delete'),
    path('',HomeView.as_view(),name='homepage'),
   
]
