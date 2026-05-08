from django.shortcuts import render, redirect
from django.http import Http404
from catalog.models import GPPractices, GPDetails, GPPopulations

# Create your views here.


class AgeGroup:
    # Small data holder for one age band in the practice detail chart.
    def __init__(self):
        self.range = None
        self.female = None
        self.male = None
        self.total = None


def get_age_data(practice):
    # Fetch the female and male population rows for the selected practice.
    females = GPPopulations.objects.get(practice=practice, sex="Female")
    males = GPPopulations.objects.get(practice=practice, sex="Male")
    age_groups = []
    # Age labels shown on the chart.
    age_range = [
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
    counter = 0
    # Build one AgeGroup object per age band using the female counts first.
    for value in [
        females.ages00to04,
        females.ages05to09,
        females.ages10to14,
        females.ages15to19,
        females.ages20to24,
        females.ages25to29,
        females.ages30to34,
        females.ages35to39,
        females.ages40to44,
        females.ages45to49,
        females.ages50to54,
        females.ages55to59,
        females.ages60to64,
        females.ages65to69,
        females.ages70to74,
        females.ages75to79,
        females.ages80to84,
        females.ages85plus,
    ]:
        ag = AgeGroup()
        ag.range = age_range[counter]
        ag.female = value
        counter += 1
        age_groups.append(ag)
    counter = 0
    # Fill in the male counts and compute the total for each age band.
    for value in [
        males.ages00to04,
        males.ages05to09,
        males.ages10to14,
        males.ages15to19,
        males.ages20to24,
        males.ages25to29,
        males.ages30to34,
        males.ages35to39,
        males.ages40to44,
        males.ages45to49,
        males.ages50to54,
        males.ages55to59,
        males.ages60to64,
        males.ages65to69,
        males.ages70to74,
        males.ages75to79,
        males.ages80to84,
        males.ages85plus,
    ]:
        age_groups[counter].male = value
        age_groups[counter].total = (
            age_groups[counter].male + age_groups[counter].female
        )
        counter += 1

    return age_groups


def get_Practices(request):
    # Keep the old route working by redirecting to the main practices table.
    return redirect("/tables/practices")


def get_Practice(request, id):
    # Look up the practice by its practice code and return 404 if it does not exist.
    try:
        practice = GPPractices.objects.get(practice_code=id)
    except GPPractices.DoesNotExist:
        raise Http404("GPPractice does not exist")

    # Collect GP codes for display on the detail page.
    doctors = []
    details = GPDetails.objects.filter(practice=practice)
    for detail in details:
        doctors.append(detail.gp_code)
    patients = practice.list_size
    try:
        # Guard against division by zero when no doctors are linked to the practice.
        pat_doc_ratio = patients / len(doctors)
        pat_doc_ratio = round(pat_doc_ratio, 1)
    except:
        pat_doc_ratio = "N/A"

    # Pair GP codes with their designations so the template can render both together.
    designations = []
    for detail in details:
        designations.append(detail.designation)

    # Assemble all data needed by the detail template.
    context = {
        "practice": practice,
        "doctor_num": len(doctors),
        "pat_doc_ratio": pat_doc_ratio,
        "doctors": zip(doctors, designations),
        "age_data": get_age_data(practice),
    }

    return render(request, "core/practice_detail.html", context)
