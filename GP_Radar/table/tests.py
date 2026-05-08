from django.test import TestCase
from catalog.models import GPPractices, GPPractitioners, GPDetails, GPPopulations


<<<<<<< Updated upstream
from catalog.models import GPPractices, GPPractitioners, GPDetails, GPPopulations


=======
# Create your tests here.
>>>>>>> Stashed changes
class DashboardFrontendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.practice = GPPractices.objects.create(
<<<<<<< Updated upstream
            practice_code="20002",
            name="Riverbank Health Centre",
            list_size=3200,
            address="45 Riverside Road",
            postcode="AB10 1AA",
            telephone="01382555123",
            health_board="NHS Grampian",
            latitude=57.1497,
            longitude=-2.0943,
        )

        cls.doctor = GPPractitioners.objects.create(
            medical_council_number="GMC002",
            forename="James",
            surname="MacLeod",
            sex="Male",
=======
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
>>>>>>> Stashed changes
        )

        GPDetails.objects.create(
            gp_code=cls.doctor,
            practice=cls.practice,
<<<<<<< Updated upstream
            designation="Salaried GP",
=======
            designation="GP Partner",
>>>>>>> Stashed changes
        )

        GPPopulations.objects.create(
            practice=cls.practice,
            sex="Female",
<<<<<<< Updated upstream
            ages00to04=150,
            ages05to09=180,
            ages10to14=170,
            ages15to19=160,
            ages20to24=210,
=======
            ages00to04=400,
>>>>>>> Stashed changes
        )

        GPPopulations.objects.create(
            practice=cls.practice,
            sex="Male",
<<<<<<< Updated upstream
            ages00to04=140,
            ages05to09=175,
            ages10to14=165,
            ages15to19=155,
            ages20to24=205,
=======
            ages00to04=400,
>>>>>>> Stashed changes
        )

    def test_dashboard_page_loads(self):
        response = self.client.get("/tables/practices")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table/dashboard.html")
        self.assertContains(response, "GP Practice Dashboard")
<<<<<<< Updated upstream
        self.assertContains(response, "Riverbank Health Centre")
=======
        self.assertContains(response, "Alpha Medical Practice")
>>>>>>> Stashed changes

    def test_home_redirects_to_dashboard(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/tables/practices")

    def test_postcode_search_filters_results(self):
<<<<<<< Updated upstream
        response = self.client.get("/tables/practices", {"postcode": "AB10"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Riverbank Health Centre")
        self.assertContains(response, "AB10 1AA")
=======
        response = self.client.get("/tables/practices", {"postcode": "DD2"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Medical Practice")
        self.assertContains(response, "DD2 5NH")
>>>>>>> Stashed changes

    def test_patient_size_filter_loads(self):
        response = self.client.get(
            "/tables/practices/filters",
<<<<<<< Updated upstream
            {"patient_size": "2501-5000", "pagesize": "5"},
=======
            {"patient_size": "0-1000"},
>>>>>>> Stashed changes
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "table/dashboard.html")
<<<<<<< Updated upstream
        self.assertContains(response, "Riverbank Health Centre")

    def test_practice_detail_page_loads(self):
        response = self.client.get("/practices/20002/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/practice_detail.html")
        self.assertContains(response, "Riverbank Health Centre")
=======
        self.assertContains(response, "Alpha Medical Practice")

    def test_practice_detail_page_loads(self):
        response = self.client.get("/practices/10001/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/practice_detail.html")
        self.assertContains(response, "Alpha Medical Practice")
>>>>>>> Stashed changes
        self.assertContains(response, "GP Doctors")
