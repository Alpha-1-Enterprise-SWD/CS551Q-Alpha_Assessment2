from django.shortcuts import render
from catalog.models import GPDetails, GPPractices, GPPopulations
import math
from django.shortcuts import redirect

RECORDS_PER_PAGE = 50

# Create your views here.


def get_Practices(request):
    page = int(request.GET.get("page", 1))
    name = request.GET.get("name", None)
    location = request.GET.get("location", None)
    # print("page: " + str(page))
    # print("name: " + str(name))
    # print("location:" + str(location))

    practices = GPPractices.objects.all()

    if name != None:
        practices = practices.filter(name__icontains=name)
    if location != None:
        practices = practices.filter(address__icontains=location)
    if math.ceil(len(practices) / 50) < page:
        return redirect(f"/tables/practices?page={1}&name={name}&location={location}")
    else:
        begin = (page - 1) * RECORDS_PER_PAGE
        end = None
        if len(practices[begin:]) < 50:
            practices = practices[begin:]
        else:
            end = begin + RECORDS_PER_PAGE - 1
            practices = practices[begin:end]
        print("begin:" + str(begin) + " end: " + str(end))

    doctors = GPDetails.objects.all()
    populations = GPPopulations.objects.all()
    dict = {
        "practices": [],
        "doctors": [],
        "doc_num": [],
        "patient_gp_ratio": [],
        "total_patient": [],
        "male_population": [],
        "female_population": [],
    }
    for i in range(len(practices)):
        dict["practices"].append(practices[i])
        doctors_list = doctors.filter(practice=practices[i].practice_code)
        dict["doctors"].append(doctors_list)
        doctor_number = len(doctors_list)
        dict["doc_num"].append(doctor_number)
        female = populations.get(practice=practices[i].practice_code, sex="Female")
        male = populations.get(practice=practices[i].practice_code, sex="Male")
        female_population = (
            female.ages00to04
            + female.ages05to09
            + female.ages10to14
            + female.ages15to19
            + female.ages20to24
            + female.ages25to29
            + female.ages30to34
            + female.ages35to39
            + female.ages40to44
            + female.ages45to49
            + female.ages50to54
            + female.ages55to59
            + female.ages60to64
            + female.ages65to69
            + female.ages70to74
            + female.ages75to79
            + female.ages80to84
            + female.ages85plus
        )
        male_population = (
            male.ages00to04
            + male.ages05to09
            + male.ages10to14
            + male.ages15to19
            + male.ages20to24
            + male.ages25to29
            + male.ages30to34
            + male.ages35to39
            + male.ages40to44
            + male.ages45to49
            + male.ages50to54
            + male.ages55to59
            + male.ages60to64
            + male.ages65to69
            + male.ages70to74
            + male.ages75to79
            + male.ages80to84
            + male.ages85plus
        )

        dict["male_population"].append(male_population)
        dict["female_population"].append(female_population)
        total = practices[i].list_size
        dict["total_patient"].append(total)
        if doctor_number == 0:
            dict["patient_gp_ratio"].append("no doctors found.")
        else:
            dict["patient_gp_ratio"].append(total / doctor_number)

    # print(dict["practices"][0])
    # print(dict["practices"][0].practice_code)
    # print(dict["doctors"][0])
    # print(dict["doc_num"][0])
    # print(dict["patient_gp_ratio"][0])
    # print(dict["total_patient"][0])
    # print(dict["male_population"][0])
    # print(dict["female_population"][0])

    return render(request, "index.html", dict)
