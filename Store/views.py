from rest_framework import viewsets
from .models import Store
from .serializers import StoreSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils.store_utils import get_stores_by_province


STORE_LABEL_MAP['BigCFoodPlace'] 
STORE_LABEL_MAP = {
  'CP': 'CP Fresh Mart',
  'PurePharmacy': 'PurePharmacy',
  'CentralFoodHall': 'CentralFoodHall',
  'Eathai': 'Eathai',
  'Healthiful': 'Healthiful',
  'BigCFoodPlace': 'BigC Food Place',
  '7-11': '7-11',
  'FamilyMart': 'FamilyMart',
  'Lawson': 'Lawson 108',
  'Jiffy': 'Jiffy',
  'CJ_Express': 'CJ Express',
  'MaxValuTanjai': 'MaxValu Tanjai',
  'Freshmart': 'Freshmart',
  'TopSmall': 'Tops Daily',
  'Big_mini': 'Big C mini',
  'TescoSmall': "Lotus's Go Fresh",
  'Villa': 'Villa Market',
  'CJ_Supermarket': 'CJ Market',
  'MaxValu': 'MaxValu',
  'TopSuper': 'Tops Market',
  'BigC_Super': 'BigC Market',
  'TescoSuper': "Lotus's Market",
  'BigC_Hyper': 'BigC Supercenter',
  'TescoHyper': 'Lotus Extra',
  'Makro': 'Makro',
}

class StoreAPIView(APIView):
    def get(self, request):
        store = request.GET.get("store", "").replace("\"", "")
        area_code = request.GET.get("area_code", "").replace("\"", "")

        if not store:
            return Response({"error": "Empty request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            code_list = [int(code.strip()) for code in store.split(',')]
        except ValueError as e:
            return Response({"error": "Bad request","msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            factory_data = find_factory_from_code(code_list, factory_type)
        except Exception:
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(f"request for code:{code_list} coor:{factory_type}")
        return Response(factory_data, status=status.HTTP_200_OK)