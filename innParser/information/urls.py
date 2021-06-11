from django.urls import path
from.views import *
urlpatterns = [
    path("", parser),
    path("/upload_file", upload_file),
    path("/results", results),
    path("/download", download)
]
