from django.test import TestCase
from django.urls import reverse
from .models import Province, District, Subdistrict

class ViewSearchTestCase(TestCase):
    def setUp(self):
        # Provinces
        Province.objects.create(code=10, name="กรุงเทพมหานคร")
        Province.objects.create(code=12, name="นนทบุรี")

        # Districts
        District.objects.create(code=1001, name="เขตพระนคร", province_code=10)
        District.objects.create(code=1201, name="เมืองนนทบุรี", province_code=12)

        # Subdistricts
        Subdistrict.objects.create(code=100101, name="พระบรมมหาราชวัง", district_code=1001)
        Subdistrict.objects.create(code=120101, name="สวนใหญ่", district_code=1201)

    def test_search_province_by_code_view(self):
        response = self.client.get("/province", {"search": '"10"'}) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "กรุงเทพมหานคร")

    def test_search_province_by_name_view(self):
        response = self.client.get("/province", {"search": '"นนทบุรี"'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("นนทบุรี" in p["name"] for p in response.json()))

    def test_search_district_by_code_view(self):
        response = self.client.get("/district", {"search": '"1001"'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "เขตพระนคร")

    def test_search_district_by_province_code_view(self):
        response = self.client.get("/district", {"search": '"10"'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(d["code"] == 1001 for d in response.json()))

    def test_search_district_by_name_and_province_name_view(self):
        response = self.client.get("/district", {"search": '"เมือง"', "province": '"นนทบุรี"'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["code"], 1201)

    def test_search_subdistrict_by_code_view(self):
        response = self.client.get("/subdistrict", {"search": '"100101"'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "พระบรมมหาราชวัง")

    def test_search_subdistrict_by_name_view(self):
        response = self.client.get("/subdistrict", {"search": '"พระบรม"'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "พระบรมมหาราชวัง")

    def test_search_subdistrict_by_district_name_view(self):
        response = self.client.get("/subdistrict", {"search": '"พระ"', "district": '"เขตพระนคร"'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "พระบรมมหาราชวัง")

    def test_search_subdistrict_by_province_name_view(self):
        response = self.client.get("/subdistrict", {"search": '"สวน"', "province": '"นนทบุรี"'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"], "สวนใหญ่")
