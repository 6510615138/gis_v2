
from .search import *
from .utils import *

def is_numeric(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

def search_province(request):
    search_txt = request.GET.get("search","")
    search_txt = search_txt.strip()[1:-1]  # remove the qoutes and space in txt  
    if search_txt.isnumeric():
        print(f"search Province by code : {search_txt}")
        return search_province_by_code(code=search_txt)
    print(f"search Province by name : {search_txt}")
    return search_province_by_name(name=search_txt)

def get_all_provinces(request):
    return all_province()


def search_district(request):
    province = request.GET.get("province","")
    search_txt = request.GET.get("search","")
    search_txt = search_txt.strip()[1:-1]  
    province = province.strip()[1:-1]       # remove the qoutes and space in txt  
    if search_txt.isnumeric():
        if len(search_txt) < 4 :
            print(f"search District by province_code : {search_txt}")
            return search_district_by_province_code(search_txt)
        else:
            print(f"search District by code : {search_txt}")
            return search_district_by_code(search_txt)
    else :

        print(f"search District by name : {search_txt} in {province}")
        return search_district_by_name(search_txt,province)
    

def search_subdistrict(request):
    province = request.GET.get("province","")
    district = request.GET.get("district","")
    search_txt = request.GET.get("search","")
    search_txt = search_txt.strip()[1:-1]  # this was to remove the qoutes and space in the search_txt  
    district = district.strip()[1:-1]  # this was to remove the qoutes and space in the search_txt  
    province = province.strip()[1:-1]  # this was to remove the qoutes and space in the search_txt  
    if search_txt.isnumeric():
        return search_subdistrict_by_code(search_txt)
    if district:
        return search_subdistrict_by_district(search_txt,district,8)
    if province:
        return search_subdistrict_by_province(search_txt,province,8)
    return search_subdistrict_by_name(search_txt,8)


import ast
def get_coordinates(request):
    codes = request.GET.get("code","")
    if codes == "":
        return JsonResponse("empty request",safe=False)
    try:
        lst = ast.literal_eval(codes)[1:-1]
        lst = lst.split(",")
    except:
        return JsonResponse("bad request",safe=False)

    coor_json = get_union_coordinates(lst) #codes = [10,1201,120102,...]
    return JsonResponse(coor_json,safe=False)

    