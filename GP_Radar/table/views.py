from django.shortcuts import render
from catalog.models import GPDetails, GPPractices, GPPopulations, GPPractitioners
import math
from django.shortcuts import redirect
from map.views import getPracticeMarkers

# Create your views here.


class TableFilterParam:
    # Store the current filter state so the template can keep form values in sync.
    def __init__(self, page, address, postcode, keyword, pagesize):
        self.page = page
        self.postcode = postcode
        self.address = address
        self.keyword = keyword
        self.pagesize = pagesize


class PracticeData:
    # Lightweight container for computed values that are not stored directly in the model.
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
    try:
        avg_pat_doc_ratio = round(avg_pat_doc_ratio / valid_practice, 1)
    except:
        avg_pat_doc_ratio = None

    return avg_pat_doc_ratio


def safe_int(value, default, minimum=1):
    try:
        result = int(value)
        return max(result, minimum)
    except:
        return default


def get_Populations(populations, practice_code, sex):
    try:
        record = populations.get(practice=practice_code, sex=sex)
        return (
            record.ages00to04
            + record.ages05to09
            + record.ages10to14
            + record.ages15to19
            + record.ages20to24
            + record.ages25to29
            + record.ages30to34
            + record.ages35to39
            + record.ages40to44
            + record.ages45to49
            + record.ages50to54
            + record.ages55to59
            + record.ages60to64
            + record.ages65to69
            + record.ages70to74
            + record.ages75to79
            + record.ages80to84
            + record.ages85plus
        )
    except:
        return 0


# need to be revised
def get_Practices(request):
    # Get parameters in URL
    page = safe_int(request.GET.get("page"), 1)
    keyword = request.GET.get("keyword", "")
    address = request.GET.get("address", "")
    postcode = request.GET.get("postcode", "")
    pagesize = safe_int(request.GET.get("pagesize"), 5)

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

    doctors = GPPractitioners.objects.all()
    total_doctor_num = doctors.count()
    populations = GPPopulations.objects.all()

    # Build the context passed to the dashboard template.
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
        "map_practices": None,
        "health_board_data": None,
    }

    for p in practices:
        Practice = PracticeData(p)

        # Collect all doctors linked to the current practice.
        doctors_list = []
        details = GPDetails.objects.filter(practice=p)
        for detail in details:
            doctors_list.append(detail.gp_code)

        Practice.doctors = doctors_list
        Practice.doctor_num = len(doctors_list)

        Practice.male_patient_num = get_Populations(
            populations, p.practice_code, sex="Male"
        )
        Practice.female_patient_num = get_Populations(
            populations, p.practice_code, sex="Female"
        )
        try:
            # Guard against division by zero when a practice has no assigned doctors.
            Practice.patient_gp_ratio = round(p.list_size / Practice.doctor_num, 1)
        except:
            Practice.patient_gp_ratio = None

        context["practices"].append(Practice)

    context["filter_params"] = TableFilterParam(
        page=page,
        address=address,
        postcode=postcode,
        keyword=keyword,
        pagesize=pagesize,
    )

    # Reuse the shared map helper so the template receives marker data in the same format as the map app.
    map_practices = getPracticeMarkers(context)
    context["map_practices"] = map_practices
    context["health_board_data"] = getHealthBoardData(practices)

    return render(request, "table/dashboard.html", context)


def getHealthBoardData(practices):
    # Count how many practices belong to each health board.
    health_board = {}

    for p in practices:
        if p.health_board in health_board:
            health_board[p.health_board] += 1
        else:
            health_board[p.health_board] = 1

    # Sort by frequency and keep only the top eight for the chart.
    sorted_health_board = sorted(
        health_board.items(), key=lambda item: item[1], reverse=True
    )[:8]

    # Return the exact structure expected by the dashboard JavaScript.
    return {
        "labels": [item[0] for item in sorted_health_board],
        "data": [item[1] for item in sorted_health_board],
    }


def to_practices_table(request):
    return redirect("/tables/practices")
