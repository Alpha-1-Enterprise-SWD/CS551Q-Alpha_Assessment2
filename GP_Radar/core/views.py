from django.shortcuts import render
from django.http import HttpResponse, Http404
from catalog.models import GPPractices, GPDetails, GPPopulations

# Create your views here.


def map(request):
    pass


def table(request):
    pass


class AgeGroupData:
    def __init__(self):
        self.age_group = [
            "0~4",
            "5~9",
            "10~14",
            "15~19",
            "20~24",
            "25~29",
            "30~34",
            "35~39",
            "40~44",
            "45~49",
            "50~54",
            "55~59",
            "60~64",
            "65~69",
            "70~74",
            "75~79",
            "80~84",
            "85+",
        ]
        self.females = []
        self.males = []


def get_Practice(request, id):
    try:
        practice = GPPractices.objects.get(practice_code=id)
    except GPPractices.DoesNotExist:
        raise Http404("Poll does not exist")

    donctors = GPDetails.objects.filter(practice=practice)
    patients = practice.list_size
    age_group_data = GPPopulations
    context = {
        "practice": practice,
        "doctor_num": donctors.count(),
        "pat_doc_ratio": round(practice.list_size / donctors.count(), 1),
        "doctors": donctors,
        "age_group_data": age_group_data,
    }

    return render(request, "core/practice_detail.html", context)
