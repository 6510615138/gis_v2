from django.http import JsonResponse
from django.db.models import Case, When, IntegerField
from .models import Province, District, Subdistrict

# --- Province Search ---
def search_province_by_code(code: str):
    province = Province.objects.filter(code__icontains=code).values("code", "name")[:1]
    return JsonResponse(list(province), safe=False)

def search_province_by_name(name: str, max_result=8):
    provinces = Province.objects.annotate(
        priority=Case(
            When(name__iexact=name, then=0),
            When(name__istartswith=name, then=1),
            default=2,
            output_field=IntegerField(),
        )
    ).filter(name__icontains=name).order_by('priority', 'name')[:max_result]
    return JsonResponse(list(provinces.values("code", "name")), safe=False)

def all_province():
    provinces = Province.objects.all().values("code", "name")
    return JsonResponse(list(provinces), safe=False)

# --- District Search ---
def search_district_by_province_code(code: str):
    districts = District.objects.filter(province_code__icontains=code).values("code", "name")
    return JsonResponse(list(districts), safe=False)

def search_district_by_code(code: str):
    district = District.objects.filter(code__icontains=code).values("code", "name")[:1]
    return JsonResponse(list(district), safe=False)

def search_district_by_name(name: str, province: str, max_result=8):
    province_code = None

    if province:
        if province.isnumeric():
            province_code = int(province)
        else:
            try:
                province_code = Province.objects.filter(name__icontains=province)[0].code
            except IndexError:
                province_code = None

    if province_code:
        districts = District.objects.filter(province_code__icontains=province_code)
    else:
        districts = District.objects.all()

    districts = districts.filter(name__icontains=name)[:max_result]
    return JsonResponse(list(districts.values("code", "name")), safe=False)

# --- Subdistrict Search ---
def search_subdistrict_by_code(code: str):
    try:
        subdistrict = Subdistrict.objects.filter(code__icontains=code).values("code", "name")[:1]
        return JsonResponse(list(subdistrict), safe=False)
    except:
        return JsonResponse([], safe=False)

def search_subdistrict_by_name(search: str, max_result=8):
    subdistricts = Subdistrict.objects.filter(name__icontains=search)[:max_result]
    return JsonResponse(list(subdistricts.values("code", "name")), safe=False)

def search_subdistrict_by_district(search: str, district: str, max_result=8):
    if not district.isnumeric():
        try:
            district = District.objects.filter(name__icontains=district)[0].code
        except IndexError:
            district = 0

    subdistricts = Subdistrict.objects.filter(district_code__istartswith=district)

    if search:
        subdistricts = subdistricts.filter(name__icontains=search)[:max_result]

    return JsonResponse(list(subdistricts.values("code", "name")), safe=False)

def search_subdistrict_by_province(search: str, province: str, max_result=8):
    if not province.isnumeric():
        try:
            province = Province.objects.filter(name__icontains=province)[0].code
        except IndexError:
            province = 0

    subdistricts = Subdistrict.objects.filter(district_code__istartswith=province)

    if search:
        subdistricts = subdistricts.filter(name__icontains=search)[:max_result]

    return JsonResponse(list(subdistricts.values("code", "name")), safe=False)
