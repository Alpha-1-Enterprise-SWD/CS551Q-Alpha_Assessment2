from django.urls import path
from . import views

urlpatterns = [
    path("", views.to_practices_table, name="temp_root"),
    path("practices", views.get_Practices, name="table_practices"),
    path("practices/filters", views.apply_filters_api, name="apply_filters_api"),
]
