from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_Practices, name="get_Practices"),
    path("<int:id>/", views.get_Practice, name="get_Practice"),
]
