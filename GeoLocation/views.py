from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import get_polygon_coordinates_detailed
from .models import Province, District, Subdistrict
from django.db.models import Case, When, IntegerField


class ProvinceSearchByCode(APIView):
    def get(self, request):
        code = request.GET.get("code", "")
        matched = Province.objects.filter(code__icontains=code)[:1]
        result = list(matched.values("code", "name"))
        return Response(result)


class ProvinceSearchByName(APIView):
    def get(self, request):
        name = request.GET.get("name", "")
        max_result = int(request.GET.get("max_result", 8))
        matched = Province.objects.annotate(
            priority=Case(
                When(name__iexact=name, then=0),
                When(name__istartswith=name, then=1),
                default=2,
                output_field=IntegerField()
            )
        ).filter(name__icontains=name).order_by("priority", "name")[:max_result]
        result = list(matched.values("code", "name"))
        return Response(result)


class ProvinceList(APIView):
    def get(self, request):
        result = list(Province.objects.values("code", "name"))
        return Response(result)


class DistrictSearchByProvince(APIView):
    def get(self, request):
        code = request.GET.get("province_code", "")
        matched = District.objects.filter(province_code__icontains=code)
        return Response(list(matched.values("code", "name")))


class DistrictSearchByCode(APIView):
    def get(self, request):
        code = request.GET.get("code", "")
        matched = District.objects.filter(code__icontains=code)[:1]
        return Response(list(matched.values("code", "name")))


class DistrictSearchByName(APIView):
    def get(self, request):
        name = request.GET.get("name", "")
        province = request.GET.get("province", "")
        max_result = int(request.GET.get("max_result", 8))

        province_code = ""
        if province:
            if province.isnumeric():
                province_code = int(province)
            else:
                try:
                    province_code = Province.objects.filter(name__icontains=province)[0].code
                except:
                    province_code = ""

        matched = District.objects.filter(name__icontains=name)
        if province_code:
            matched = matched.filter(province_code__icontains=province_code)
        matched = matched[:max_result]

        return Response(list(matched.values("code", "name")))


class SubdistrictSearchByCode(APIView):
    def get(self, request):
        code = request.GET.get("code", "")
        try:
            matched = Subdistrict.objects.filter(code__icontains=code)[:1]
            return Response(list(matched.values("code", "name")))
        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)


class SubdistrictSearchByName(APIView):
    def get(self, request):
        name = request.GET.get("name", "")
        max_result = int(request.GET.get("max_result", 8))
        matched = Subdistrict.objects.filter(name__icontains=name)[:max_result]
        return Response(list(matched.values("code", "name")))


class SubdistrictSearchByDistrict(APIView):
    def get(self, request):
        name = request.GET.get("name", "")
        district = request.GET.get("district", "")
        max_result = int(request.GET.get("max_result", 8))

        if not district.isnumeric():
            try:
                district = District.objects.filter(name__icontains=district)[0].code
            except:
                district = 0

        matched = Subdistrict.objects.filter(district_code__istartswith=district)
        matched = matched.filter(name__icontains=name)[:max_result]
        return Response(list(matched.values("code", "name")))


class SubdistrictSearchByProvince(APIView):
    def get(self, request):
        name = request.GET.get("name", "")
        province = request.GET.get("province", "")
        max_result = int(request.GET.get("max_result", 8))

        if not province.isnumeric():
            try:
                province = Province.objects.filter(name__icontains=province)[0].code
            except:
                province = 0

        matched = Subdistrict.objects.filter(district_code__istartswith=province)
        if name:
            matched = matched.filter(name__icontains=name)[:max_result]

        return Response(list(matched.values("code", "name")))

class GetCoordinatesAPIView(APIView):
    def get(self, request):
        code_str = request.GET.get("code", "")
        code_str = code_str.replace("\"", "")
        print(f"coordinate of code: {code_str}")

        if not code_str:
            return Response({"error": "Empty request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            code_list = [int(code.strip()) for code in code_str.split(',')]
        except ValueError:
            return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

        print(f"lst: {code_list} ({type(code_list)})")
        geojson = get_polygon_coordinates_detailed(code_list)
        return Response(geojson, status=status.HTTP_200_OK)