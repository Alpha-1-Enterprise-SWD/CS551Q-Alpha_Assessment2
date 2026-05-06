from django.shortcuts import render
from django.template.loader import render_to_string
import random

# Create your views here.


def getPracticeMarkers(context):

    map_practices = []

    for p in context["practices"]:
        practiceName = p.practice.name
        address = p.practice.address
        patientCount = p.practice.list_size
        gpCount = p.doctor_num
        ratio = p.patient_gp_ratio
        # longitude = p.practice.longitude
        # latitude = p.practice.latitude
        longitude = 56.4907 + (random.random() - 0.5) * 2
        latitude = -4.2026 + (random.random() - 0.5) * 4

        if longitude and latitude:
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
