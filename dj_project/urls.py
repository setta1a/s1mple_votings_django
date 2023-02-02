"""dj_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path

from first.views import voting_page, list_of_votings_page, index_page, add_voting, registration, redact_voting, profile, redact_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('voting/<int:voting_id>/', voting_page, name='voting_details'),
    path('list/', list_of_votings_page),
    path('login/', auth_views.LoginView.as_view(
        extra_context={
            "pagetitle": "Auth",
            "pageheader": "Авторизация"
        }
    )),
    # path('registration/', auth_views.LoginView.as_view(
    #     extra_context={
    #         "pagetitle": "Registration",
    #         "pageheader":"Регистрация"
    #     }
    # )),
    path('registration/', registration),
    path('logout/', auth_views.LogoutView.as_view()),
    path('add_voting/', add_voting),
    path('redact/<int:voting_id>/', redact_voting),
    path('profile', profile),
    path('redact_profile/', redact_profile)
]
