from django.urls import path
from . import views

urlpatterns = [
    path("practices", views.get_Practices, name="dashboard"),
]
