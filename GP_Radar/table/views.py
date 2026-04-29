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


def get_total_patient():
    practices = GPPractices.objects.all()
    total_patient_num = 0
    for p in practices:
        total_patient_num += p.list_size

    return total_patient_num


def get_total_practice():
    total_practice_num = GPPractices.objects.all().count()
    return total_practice_num


def get_avg_pat_doc_ratio():
    practices = GPPractices.objects.all()
    doctors = GPDetails.objects.all()
    avg_pat_doc_ratio = 0
    valid_practice = practices.count()
    for p in practices:
        doctor_num_by_practice = doctors.filter(practice=p).count()
        if doctor_num_by_practice != 0:
            avg_pat_doc_ratio += p.list_size / doctor_num_by_practice
        else:
            valid_practice -= 1
    avg_pat_doc_ratio = round(avg_pat_doc_ratio / valid_practice, 1)

    return avg_pat_doc_ratio


def get_Practices(request):
    # Get parameters in URL
    page = int(request.GET.get("page", 1))
    keyword = request.GET.get("keyword", "")
    address = request.GET.get("address", "")
    postcode = request.GET.get("postcode", "")
    pagesize = int(request.GET.get("pagesize", 5))

    # Query all practices
    practices = GPPractices.objects.all()

    # filter practice list according to parameters
    if keyword != None:
        practices = practices.filter(name__icontains=keyword)
    if address != None:
        practices = practices.filter(address__icontains=address)
    if postcode != None:
        practices = practices.filter(postcode__icontains=postcode)
    total_practice_num = len(practices)
    total_page_num = math.ceil(total_practice_num / pagesize)

    begin = 0
    end = 0

    if total_page_num < page and page > 1:
        return redirect(
            f"/tables/practices?page={1}&keyword={keyword}&address={address}&postcode={postcode}&pagesize={pagesize}"
        )
    else:
        begin = (page - 1) * pagesize
        end = None
        if len(practices[begin:]) < pagesize:
            practices = practices[begin:]
        else:
            end = begin + pagesize
            practices = practices[begin:end]

    doctors = GPDetails.objects.all()
    total_doctor_num = len(doctors)
    populations = GPPopulations.objects.all()

    context = {
        "practices": [],
        "total_practice_num": get_total_practice(),
        "total_doc_num": total_doctor_num,
        "total_patient_num": get_total_patient(),
        "avg_pat_doc_ratio": get_avg_pat_doc_ratio(),
        "filter_params": None,
        "total_page_num": total_page_num,
        "page_range": range(1, (total_page_num + 1)),
        "begin_index": begin + 1,
        "end_index": end,
    }

    for p in practices:
        Practice = PracticeData(p)
        doctors_list = doctors.filter(practice=p.practice_code)
        Practice.doctors = doctors_list
        Practice.doctor_num = doctors_list.count()

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
        try:
            Practice.patient_gp_ratio = round(p.list_size / Practice.doctor_num, 1)
        except:
            Practice.patient_gp_ratio = None
        total = p.list_size

        context["practices"].append(Practice)

    context["filter_params"] = TableFilterParam(
        page=page,
        address=address,
        postcode=postcode,
        keyword=keyword,
        pagesize=pagesize,
    )

    return render(request, "table/dashboard.html", context)
