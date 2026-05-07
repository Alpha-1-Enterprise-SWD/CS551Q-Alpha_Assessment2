from django.template.loader import render_to_string

# Create your views here.


def getPracticeMarkers(context):

    map_practices = []

    for p in context["practices"]:
        # Use coordinates already stored in database
        latitude = p.practice.latitude
        longitude = p.practice.longitude

        # Only add markers with valid coordinates
        if longitude and latitude:
            practiceName = p.practice.name
            address = p.practice.address
            patientCount = p.practice.list_size
            gpCount = p.doctor_num
            ratio = p.patient_gp_ratio

            popup_html = render_to_string(
                "map/_practice_popup.html",
                {
                    "practiceName": practiceName,
                    "address": address,
                    "patientCount": patientCount,
                    "gpCount": gpCount,
                    "ratio": ratio,
                },
            )
            map_practices.append(
                {"latitude": latitude, "longitude": longitude, "popup_html": popup_html}
            )

    return map_practices
