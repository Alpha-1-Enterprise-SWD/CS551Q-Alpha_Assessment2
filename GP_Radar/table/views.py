from django.shortcuts import render
from catalog.models import GPDetails, GPPractices, GPPopulations
import math
from django.shortcuts import redirect


# Create your views here.


class TableFilterParam:
    def __init__(self, page, address, postcode, keyword, pagesize):
        self.page = page
        self.postcode = postcode
        self.address = address
        self.keyword = keyword
        self.pagesize = pagesize


class PracticeData:
    def __init__(self, practice):
        self.practice = practice
        self.doctors = []
        self.doctor_num = 0
        self.patient_gp_ratio = 0
        self.female_patient_num = 0
        self.male_patient_num = 0


def get_Practices(request):
    # Get parameters in URL
    page = int(request.GET.get("page", 1))
    keyword = request.GET.get("keyword", None)
    address = request.GET.get("address", None)
    postcode = request.GET.get("postcode", None)
    pagesize = int(request.GET.get("page-size", 5))

    # Query all practices
    practices = GPPractices.objects.all()
    total_practice_num = len(practices)

    # filter practice list according to parameters
    if keyword != None:
        practices = practices.filter(name__icontains=keyword)
    if address != None:
        practices = practices.filter(address__icontains=address)
    if postcode != None:
        practices = practices.filter(postcode__icontains=address)
    total_page_num = math.ceil(total_practice_num / pagesize)
    print("total_page_num: " + str(total_practice_num) + str(total_page_num))
    if total_page_num < page:
        return redirect(
            f"/tables/practices?page={1}&keyword={keyword}&address={address}&postcode={postcode}&page-size={pagesize}"
        )
    else:
        begin = (page - 1) * pagesize
        end = None
        if len(practices[begin:]) < pagesize:
            practices = practices[begin:]
        else:
            end = begin + pagesize - 1
            practices = practices[begin:end]

    doctors = GPDetails.objects.all()
    total_doctor_num = len(doctors)
    populations = GPPopulations.objects.all()
    context = {
        "practices": [],
        "total_practice_num": total_practice_num,
        "total_doc_num": total_doctor_num,
        "total_patient_num": None,
        "avg_pat_doc_ratio": None,
        "filter_params": None,
        "total_page_num": total_page_num,
        "page_range": range(1, (total_page_num + 1)),
    }
    total_patient_num = 0
    avg_pat_doc_ratio = 0
    for p in practices:
        Practice = PracticeData(p)
        doctors_list = doctors.filter(practice=p.practice_code)
        Practice.doctors = doctors_list
        Practice.doctor_num = len(doctors_list)

        female = populations.get(practice=p.practice_code, sex="Female")
        male = populations.get(practice=p.practice_code, sex="Male")
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
        Practice.male_patient_num = male_population
        Practice.female_patient_num = female_population
        total = p.list_size
        total_patient_num += total

        if Practice.doctor_num == 0:
            Practice.patient_gp_ratio = "no doctors found."
            avg_pat_doc_ratio += 0
        else:
            ratio = total / Practice.doctor_num
            Practice.patient_gp_ratio = ratio
            avg_pat_doc_ratio += ratio

        context["practices"].append(Practice)

    context["total_patient_num"] = total_patient_num
    context["avg_pat_doc_ratio"] = avg_pat_doc_ratio / context["total_practice_num"]
    context["filter_params"] = TableFilterParam(
        page=page,
        address=address,
        postcode=postcode,
        keyword=keyword,
        pagesize=pagesize,
    )

    return render(request, "table/dashboard.html", context)
