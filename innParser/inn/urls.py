from django.urls import path
from.views import *
urlpatterns = [
    path("", parser),
    path("/search_result", getInn),
    path("/upload_file", upload_file),
    path("/results", results),
    path("/download", download)
]
