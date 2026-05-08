from django.test import TestCase
from catalog.models import GPPractices, GPPractitioners, GPDetails, GPPopulations


# Create your tests here.
class DashboardFrontendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.practice = GPPractices.objects.create(
            practice_code="10001",
            name="Alpha Medical Practice",
            list_size=800,
            address="1 Test Street",
            postcode="DD2 5NH",
            telephone="01234567890",
            health_board="NHS Tayside",
            latitude=56.46,
            longitude=-2.97,
        )

        cls.doctor = GPPractitioners.objects.create(
            medical_council_number="GMC001",
            forename="Ada",
            surname="Lovelace",
            sex="Female",
        )

        GPDetails.objects.create(
            gp_code=cls.doctor,
            practice=cls.practice,
            designation="GP Partner",
        )

        GPPopulations.objects.create(
            practice=cls.practice,
            sex="Female",
            ages00to04=400,
        )

        GPPopulations.objects.create(
            practice=cls.practice,
            sex="Male",
            ages00to04=400,
        )

    def test_dashboard_page_loads(self):
        response = self.client.get("/tables/practices")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table/dashboard.html")
        self.assertContains(response, "GP Practice Dashboard")
        self.assertContains(response, "Alpha Medical Practice")

    def test_home_redirects_to_dashboard(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/tables/practices")

    def test_postcode_search_filters_results(self):
        response = self.client.get("/tables/practices", {"postcode": "DD2"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Medical Practice")
        self.assertContains(response, "DD2 5NH")

    def test_patient_size_filter_loads(self):
        response = self.client.get(
            "/tables/practices/filters",
            {"patient_size": "0-1000"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table/dashboard.html")
        self.assertContains(response, "Alpha Medical Practice")

    def test_practice_detail_page_loads(self):
        response = self.client.get("/practices/10001/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/practice_detail.html")
        self.assertContains(response, "Alpha Medical Practice")
        self.assertContains(response, "GP Doctors")
