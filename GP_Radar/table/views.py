from django.shortcuts import render
from catalog.models import GPDetails, GPPractices, GPPopulations, GPPractitioners
import math
from django.shortcuts import redirect
from map.views import getPracticeMarkers
from django.http import JsonResponse
import json

# Create your views here.


class TableFilterParam:
    # Store the current filter state so the template can keep form values in sync.
    def __init__(
        self,
        page,
        address,
        postcode,
        keyword,
        pagesize,
        patient_size=None,
        health_board=None,
        patient_ratio=None,
    ):
        self.page = page
        self.postcode = postcode
        self.address = address
        self.keyword = keyword
        self.pagesize = pagesize
        self.patient_size = patient_size
        self.health_board = health_board
        self.patient_ratio = patient_ratio


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

    # New filter parameters
    patient_size = request.GET.get("patient_size", "")
    health_board = request.GET.get("health_board", "")
    patient_ratio = request.GET.get("patient_ratio", "")

    # Query all practices
    practices = GPPractices.objects.all()

    # filter practice list according to parameters
    if keyword != None and keyword != "":
        practices = practices.filter(name__icontains=keyword)
    if address != None and address != "":
        practices = practices.filter(address__icontains=address)
    if postcode != None and postcode != "":
        practices = practices.filter(postcode__icontains=postcode)

    # Apply new filters
    if patient_size != "":
        # Parse patient size range (e.g., "0-1000", "1001-2500", "10000+")
        if "-" in patient_size:
            min_size, max_size = patient_size.split("-")
            practices = practices.filter(
                list_size__gte=min_size, list_size__lte=max_size
            )
        elif "+" in patient_size:
            min_size = patient_size.replace("+", "")
            practices = practices.filter(list_size__gte=min_size)

    if health_board != "":
        practices = practices.filter(health_board__icontains=health_board)

    if patient_ratio != "":
        # Parse patient ratio range (e.g., "0-1000", "1001-2500", "5001+")
        if "-" in patient_ratio:
            min_ratio, max_ratio = patient_ratio.split("-")
            # Convert to float for comparison
            try:
                min_ratio = float(min_ratio)
                max_ratio = float(max_ratio)
                valid_ratio = True
            except ValueError:
                print(f"Invalid ratio values: {min_ratio}, {max_ratio}")
                valid_ratio = False

            if valid_ratio:
                # Filter practices where calculated patient/GP ratio is in range
                filtered_practices = []
                for practice in practices:
                    doctors_count = GPDetails.objects.filter(practice=practice).count()
                    if doctors_count > 0:
                        ratio = practice.list_size / doctors_count
                        if min_ratio <= ratio <= max_ratio:
                            filtered_practices.append(practice)
                practices = filtered_practices
        elif "+" in patient_ratio:
            min_ratio = patient_ratio.replace("+", "")
            # Convert to float for comparison
            try:
                min_ratio = float(min_ratio)
                valid_ratio = True
            except ValueError:
                print(f"Invalid ratio value: {min_ratio}")
                valid_ratio = False

            if valid_ratio:
                filtered_practices = []
                for practice in practices:
                    doctors_count = GPDetails.objects.filter(practice=practice).count()
                    if doctors_count > 0:
                        ratio = practice.list_size / doctors_count
                        if ratio >= min_ratio:
                            filtered_practices.append(practice)
                practices = filtered_practices
    total_practice_num = len(practices)
    total_page_num = math.ceil(total_practice_num / pagesize)

    # Handle pagination
    if total_practice_num == 0:
        # No results found
        practices = []
        begin = 0
        end = 0
    elif total_page_num < page and page > 1:
        # Page out of range, redirect to first page
        return redirect(
            f"/tables/practices?page={1}&keyword={keyword}&address={address}&postcode={postcode}&pagesize={pagesize}&patient_size={patient_size}&health_board={health_board}&patient_ratio={patient_ratio}"
        )
    else:
        # Normal pagination
        begin = (page - 1) * pagesize
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

    # Use predefined health board list from import data command
    all_health_boards = [
        "NHS Ayrshire and Arran",
        "NHS Borders",
        "NHS Dumfries and Galloway",
        "NHS Forth Valley",
        "NHS Grampian",
        "NHS Highland",
        "NHS Lothian",
        "NHS Orkney",
        "NHS Shetland",
        "NHS Western Isles",
        "NHS Fife",
        "NHS Tayside",
        "NHS Greater Glasgow and Clyde",
        "NHS Lanarkshire",
    ]

    context["filter_params"] = TableFilterParam(
        page=page,
        address=address,
        postcode=postcode,
        keyword=keyword,
        pagesize=pagesize,
        patient_size=patient_size,
        health_board=health_board,
        patient_ratio=patient_ratio,
    )

    context["end_index"] = end if end else total_practice_num

    context["all_health_boards"] = all_health_boards

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


def apply_filters_api(request):
    """
    Filter endpoint to apply filters and render filtered practices page
    URL: /practices/filters?patient_size={}&health_board={}&patient_ratio={}
    """
    if request.method == "GET":
        try:
            # Get filter parameters - use same names as main view
            page = int(request.GET.get("page", 1))
            keyword = request.GET.get("keyword", "")
            address = request.GET.get("address", "")
            postcode = request.GET.get("postcode", "")
            pagesize = int(request.GET.get("pagesize", 5))
            patient_size = request.GET.get("patient_size", "")
            health_board = request.GET.get("health_board", "")
            patient_ratio = request.GET.get("patient_ratio", "")

            print(
                f"Filter Parameters - page: {page}, patient_size: {patient_size}, health_board: {health_board}, patient_ratio: {patient_ratio}"
            )

            # Query all practices with optimization
            practices = GPPractices.objects.all()
            print(f"Total practices before filtering: {practices.count()}")

            # Apply filters
            if keyword != None and keyword != "":
                practices = practices.filter(name__icontains=keyword)
            if address != None and address != "":
                practices = practices.filter(address__icontains=address)
            if postcode != None and postcode != "":
                practices = practices.filter(postcode__icontains=postcode)

            if patient_size != "":
                print(f"Applying patient size filter: {patient_size}")
                if "-" in patient_size:
                    min_size, max_size = patient_size.split("-")
                    practices = practices.filter(
                        list_size__gte=min_size, list_size__lte=max_size
                    )
                elif "+" in patient_size:
                    min_size = patient_size.replace("+", "")
                    practices = practices.filter(list_size__gte=min_size)
                print(f"After patient size filter: {practices.count()}")

            if health_board != "":
                print(f"Applying health board filter: {health_board}")
                practices = practices.filter(health_board__icontains=health_board)
                print(f"After health board filter: {practices.count()}")

            if patient_ratio != "":
                print(f"Applying patient ratio filter: {patient_ratio}")
                if "-" in patient_ratio:
                    min_ratio, max_ratio = patient_ratio.split("-")
                    # Convert to float for comparison
                    try:
                        min_ratio = float(min_ratio)
                        max_ratio = float(max_ratio)
                        valid_ratio = True
                    except ValueError:
                        print(f"Invalid ratio values: {min_ratio}, {max_ratio}")
                        valid_ratio = False

                    if valid_ratio:
                        filtered_practices = []
                        for practice in practices:
                            doctors_count = GPDetails.objects.filter(
                                practice=practice
                            ).count()
                            if doctors_count > 0:
                                ratio = practice.list_size / doctors_count
                                if min_ratio <= ratio <= max_ratio:
                                    filtered_practices.append(practice)
                        practices = filtered_practices
                elif "+" in patient_ratio:
                    min_ratio = patient_ratio.replace("+", "")
                    # Convert to float for comparison
                    try:
                        min_ratio = float(min_ratio)
                        valid_ratio = True
                    except ValueError:
                        print(f"Invalid ratio value: {min_ratio}")
                        valid_ratio = False

                    if valid_ratio:
                        filtered_practices = []
                        for practice in practices:
                            doctors_count = GPDetails.objects.filter(
                                practice=practice
                            ).count()
                            if doctors_count > 0:
                                ratio = practice.list_size / doctors_count
                                if ratio >= min_ratio:
                                    filtered_practices.append(practice)
                        practices = filtered_practices
                print(f"After patient ratio filter: {len(practices)}")

            # Apply pagination
            total_practice_num = len(practices)
            total_page_num = math.ceil(total_practice_num / pagesize)

            if total_practice_num == 0:
                practices = []
                begin = 0
                end = 0
            elif total_page_num < page and page > 1:
                return redirect(
                    f"/practices/filters?page=1&keyword={keyword}&address={address}&postcode={postcode}&pagesize={pagesize}&patient_size={patient_size}&health_board={health_board}&patient_ratio={patient_ratio}"
                )
            else:
                begin = (page - 1) * pagesize
                end = begin + pagesize
                practices = practices[begin:end]

            # Get all health boards for dropdown
            all_health_boards = [
                "NHS Ayrshire and Arran",
                "NHS Borders",
                "NHS Dumfries and Galloway",
                "NHS Forth Valley",
                "NHS Grampian",
                "NHS Highland",
                "NHS Lothian",
                "NHS Orkney",
                "NHS Shetland",
                "NHS Western Isles",
                "NHS Fife",
                "NHS Tayside",
                "NHS Greater Glasgow and Clyde",
                "NHS Lanarkshire",
            ]

            # Build context for template rendering
            context = {
                "practices": [],
                "total_practice_num": get_total_practice(),
                "total_doc_num": GPPractitioners.objects.all().count(),
                "total_patient_num": get_total_patient(),
                "avg_pat_doc_ratio": get_avg_pat_doc_ratio(),
                "filter_params": TableFilterParam(
                    page=page,
                    address=address,
                    postcode=postcode,
                    keyword=keyword,
                    pagesize=pagesize,
                    patient_size=patient_size,
                    health_board=health_board,
                    patient_ratio=patient_ratio,
                ),
                "total_page_num": total_page_num,
                "page_range": range(1, (total_page_num + 1)),
                "begin_index": begin + 1,
                "end_index": end if end else total_practice_num,
                "all_health_boards": all_health_boards,
            }

            # Build practice data for template
            for p in practices:
                Practice = PracticeData(p)

                doctors_list = []
                details = GPDetails.objects.filter(practice=p)
                for detail in details:
                    doctors_list.append(detail.gp_code)

                Practice.doctors = doctors_list
                Practice.doctor_num = len(doctors_list)

                female = GPPopulations.objects.get(
                    practice=p.practice_code, sex="Female"
                )
                male = GPPopulations.objects.get(practice=p.practice_code, sex="Male")
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
                    Practice.patient_gp_ratio = round(
                        p.list_size / Practice.doctor_num, 1
                    )
                except:
                    Practice.patient_gp_ratio = None

                context["practices"].append(Practice)

            print(f"Rendering filtered page with {len(context['practices'])} practices")
            return render(request, "table/dashboard.html", context)

        except Exception as e:
            print(f"Filter Error: {str(e)}")
            import traceback

            traceback.print_exc()
            # Return error context for user feedback
            return render(
                request,
                "table/dashboard.html",
                {
                    "practices": [],
                    "total_practice_num": 0,
                    "total_doc_num": 0,
                    "total_patient_num": 0,
                    "avg_pat_doc_ratio": 0,
                    "filter_params": TableFilterParam(
                        page=1,
                        address="",
                        postcode="",
                        keyword="",
                        pagesize=5,
                        patient_size="",
                        health_board="",
                        patient_ratio="",
                    ),
                    "total_page_num": 0,
                    "page_range": [],
                    "begin_index": 0,
                    "end_index": 0,
                    "all_health_boards": [
                        "NHS Ayrshire and Arran",
                        "NHS Borders",
                        "NHS Dumfries and Galloway",
                        "NHS Forth Valley",
                        "NHS Grampian",
                        "NHS Highland",
                        "NHS Lothian",
                        "NHS Orkney",
                        "NHS Shetland",
                        "NHS Western Isles",
                        "NHS Fife",
                        "NHS Tayside",
                        "NHS Greater Glasgow and Clyde",
                        "NHS Lanarkshire",
                    ],
                    "error_message": (
                        f"Error applying filters: {str(e)}"
                        if str(e)
                        else "An unknown error occurred"
                    ),
                },
            )

    return render(
        request,
        "table/dashboard.html",
        {
            "practices": [],
            "total_practice_num": 0,
            "total_doc_num": 0,
            "total_patient_num": 0,
            "avg_pat_doc_ratio": 0,
            "filter_params": TableFilterParam(
                page=1,
                address="",
                postcode="",
                keyword="",
                pagesize=5,
                patient_size="",
                health_board="",
                patient_ratio="",
            ),
            "total_page_num": 0,
            "page_range": [],
            "begin_index": 0,
            "end_index": 0,
            "all_health_boards": [
                "NHS Ayrshire and Arran",
                "NHS Borders",
                "NHS Dumfries and Galloway",
                "NHS Forth Valley",
                "NHS Grampian",
                "NHS Highland",
                "NHS Lothian",
                "NHS Orkney",
                "NHS Shetland",
                "NHS Western Isles",
                "NHS Fife",
                "NHS Tayside",
                "NHS Greater Glasgow and Clyde",
                "NHS Lanarkshire",
            ],
        },
    )


def to_practices_table(request):
    return redirect("/tables/practices")
