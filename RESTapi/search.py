#Provinces
from .models import Province,District,Subdistrict
from django.http import JsonResponse
from django.db.models import Case, When, IntegerField

def search_province_by_code(code:str):
    matched = Province.objects.filter(code__icontains=code)[0:1]
    result = list(matched.values("code", "name"))
    return JsonResponse(result, safe=False)


def search_province_by_name(name: str, max_result=8):
    matched = Province.objects.annotate(
        priority=Case(
            When(name__iexact=name, then=0),       # exact match highest priority
            When(name__istartswith=name, then=1),  # starts with next
            default=2,                             # others last
            output_field=IntegerField(),
        )
    ).filter(name__icontains=name).order_by('priority', 'name')[:max_result]

    result = list(matched.values("code", "name"))
    return JsonResponse(result, safe=False)

def all_province():
    matched = Province.objects.all()
    result = list(matched.values("code", "name"))
    return JsonResponse(result, safe=False)


#District
def search_district_by_province_code(code:str):
    matched = District.objects.filter(province_code__icontains=code)
    result = list(matched.values("code", "name"))
    return JsonResponse(result, safe=False)

def search_district_by_code(code:str):
    matched = District.objects.filter(code__icontains=code)[:1]
    result = list(matched.values("code", "name"))
    return JsonResponse(result, safe=False)

def search_district_by_name(name:str,province:str,max_result=8):
    province_code = 10
    if province:
        if province.isnumeric():
                province_code = int(province)
        else :
            try:
                print(f"look for province {province}")
                province_code = Province.objects.filter(name__icontains=name)[0].code
                print(f"result province code = {province_code}")
            except:
                province_code = ""
                print("can't find province")
        matched = District.objects.filter(province_code__icontains=province_code)
        matched = matched.filter(name__icontains=name)[:max_result]
        print(matched)
    else:
        matched = District.objects.filter(name__icontains=name)[:max_result]
    result = list(matched.values("code", "name"))
    return JsonResponse(result, safe=False)


#Subdistrict
def search_subdistrict_by_code(search:str):
    try:
        matched = Subdistrict.objects.filter(code__icontains=search)[0]
        result = list(matched.values("code", "name"))
        return JsonResponse(result, safe=False)
    except:
        return JsonResponse([], safe=False)

def search_subdistrict_by_name(search:str,max_result=8):
    matched = Subdistrict.objects.filter(name__icontains=search)[:max_result]
    result = list(matched.values("code", "name"))
    return JsonResponse(result, safe=False)


def search_subdistrict_by_district(search:str,district:str,max_result=8):
    if not district.isnumeric():
        try:
            district = District.objects.filter(name__icontains=district)[0].code
        except:
            district = 0
    matched = Subdistrict.objects.filter(district_code__istartswith=district)
    print(f"search for district code :{district}")
    matched = matched.filter(name__icontains=search)[:max_result]
    result = list(matched.values("code", "name"))
    return JsonResponse(result, safe=False)

def search_subdistrict_by_province(search:str,province:str,max_result=8):
    if not province.isnumeric():
        try:
            province = Province.objects.filter(name__icontains=province)[0].code
        except:
            province = 0
    print(f"province = :{province}")
    matched = Subdistrict.objects.filter(district_code__istartswith=province)

    if search:
        matched = matched.filter(name__icontains=search)[:max_result]

    result = list(matched.values("code", "name"))
    return JsonResponse(result, safe=False)

    

