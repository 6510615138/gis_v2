
from RESTapi.store import findStore
from .ProvinceSearch import *
from .MapBorderLoad import *

def is_numeric(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

def search_province(request):
    search_txt = request.GET.get("search","")
    search_txt = search_txt.replace("\"","")  # remove the qoutes and space in txt 
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
    search_txt = search_txt.replace("\"","")  
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
    search_txt = search_txt.replace("\"","")  # this was to remove the qoutes and space in the search_txt  
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

    code_str = request.GET.get("code", "")
    code_str = code_str.replace("\"","")
    print(f"coordinate of code: {code_str}")

    if not code_str:
        return JsonResponse("empty request", safe=False)
    try:
        code_list = [int(code.strip()) for code in code_str.split(',')]
    except ValueError:
        return JsonResponse("bad request", safe=False)

    print(f"lst: {code_list} ({type(code_list)})")
    geojson = get_polygon_coordinates_detailed(code_list)
    return JsonResponse(geojson, safe=False)



from .Factory import find_factory_from_code
def get_factory(request):
    code_str = request.GET.get("code", "")
    code_str = code_str.replace("\"","")

    factory_type = request.GET.get("type", "")
    factory_type = factory_type.replace("\"","").lstrip("0")
    print(f"coordinate of code: {code_str} ,type : {factory_type}")
    if not code_str:
        return JsonResponse("empty request", safe=False)
    try:
        code_list = [int(code.strip()) for code in code_str.split(',')]
    except ValueError:
        return JsonResponse("bad request", safe=False)
    print(f"lst: {code_list} ({type(code_list)})")
    try:
        factories = find_factory_from_code(code_list,factory_type)
    except:
        print(f"error fetching factory from code")
        print(f"code: {code_list}, type={factory_type}")
    return JsonResponse(factories, safe=False)

from .models import FactoryType

def get_factory_type(request):
    query = request.GET.get("type", "").replace("\"", "").strip()
    if not query:
        return JsonResponse({"error": "Missing 'type' parameter."}, status=400)
    if query.isdigit():
        factory_types = FactoryType.objects.filter(code=query)
    else:
        factory_types = FactoryType.objects.filter(type__icontains=query)
    result = [
        {
            "code": ft.code,
            "type": ft.type
        } for ft in factory_types
    ][:8]

    return JsonResponse(result, safe=False)

def get_ev(request):

    #get vendot eg, evme pttvolta etc.
    vendor = request.GET.get("vendor", "").strip()

    #get position 
    #expect position in format like "13.123,100.456"
    position = request.GET.get("position", "").strip()
    lat, long = map(float, position.split(",")) 


def get_store(request):
    #request body consist of the following fields
    # - area_code
    # - store
    # - lazy
    # - coordinates


    #area_code is the code specify the area such as {10:Bangkok}
    area_code_str = request.GET.get("area_code", "")
    area_code_str = area_code_str.replace("\"","")
    print(area_code_str)

    #store_str use as a filter for query the store by store franchise name 
    #expected to be string seperated be comma in format "store1,store2,store3" such as "Makro,7-11,Lawson"
    #options for store can be as follow
    # options: [
    #         'CP'
    #         'PurePharmacy'
    #         'CentralFoodHall'
    #         'Eathai'
    #         'Healthiful'
    #         'BigCFoodPlace'
    #         '7-11'
    #         'FamilyMart'
    #         'Lawson'
    #         'Jiffy'
    #         'CJ_Express'
    #         'MaxValuTanjai'
    #         'Freshmart'
    #         'TopSmall'
    #         'Big_mini'
    #         'TescoSmall'
    #         'Villa'
    #         'CJ_Supermarket'
    #         'MaxValu'
    #         'TopSuper'
    #         'BigC_Super'
    #         'TescoSuper'
    #         'BigC_Hyper'
    #         'TescoHyper'
    #         'Makro'
    # ]
    store_str = request.GET.get("store", "")  #get "store" from request double qoutes if any.
    store_str = store_str.replace("\"","") #remove double qoutes if any.
    store_str = store_str.strip() #remove leading and trailing white spaces
    print(store_str)

    #is_lazy use as a flag indicate lazy loading machanism which return only store_id, store_type, lat, long 
    #reducing data needed to visuallize the store in large scale
    #expected to be Boolean, it can be anything(not None e.g., 0 ,"" (empty String)) or None
    is_lazy = request.GET.get("lazy", "")
    is_lazy = is_lazy.replace("\"","")
    print(is_lazy)


 
    if is_lazy:
        pass
    else:
        #coordinates use to load store up close in full detail
        #expected to be in format "{lat},{long}" such as "13.012,100.123"
        coordinates = request.GET.get("coordinates", "") 
        coordinates = coordinates.replace("\"","")
        print(coordinates)

        pass
    result = findStore(area_code = area_code_str)

    return JsonResponse(result, safe=False)