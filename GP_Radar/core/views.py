from django.shortcuts import render, HttpResponseRedirect

# Create your views here.


def map(request):
    pass


def table(request):
    pass


def get_Practice(request, id):
    print(id)
    return render(request, "core/practice_detail.html")
