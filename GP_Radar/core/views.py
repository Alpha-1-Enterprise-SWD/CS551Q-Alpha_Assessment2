from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import GPPractices

# Create your views here.


def map(request):
    pass


def table(request):
    pass


def get_Practice(request, id):
    practices = GPPractices.objects.get(practice_code=id)

    return render()
