from django.contrib import admin
from django.urls import path
from django.urls import include
from.views import *
urlpatterns = [

    path('', menu),
    path('/menu', menu),
    path('/kontur_get_link', kontur_get_link),
    path('/kontur_auth', kontur_auth),
    path('/sbis_auth', sbis_auth),
]