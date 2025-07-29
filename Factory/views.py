from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FactoryType
from .serializers import FactoryCoordinatesSerializer, FactoryTypeSerializer
from .utils import find_factory_from_code

class FactorySearchAPIView(APIView):
    def get(self, request):
        code_str = request.GET.get("area_code", "").replace("\"", "")
        factory_type = request.GET.get("type", "").replace("\"", "")

        if not code_str:
            return Response({"error": "Empty request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            code_list = [int(code.strip()) for code in code_str.split(',')]
        except ValueError as e:
            return Response({"error": "Bad request","msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            factory_data = find_factory_from_code(code_list, factory_type)
        except Exception:
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(f"request for code:{code_list} coor:{factory_type}")
        return Response(factory_data, status=status.HTTP_200_OK)


class FactoryTypeSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get("factory_type", "").replace("\"", "").strip()

        if not query:
            return Response({"error": "Missing 'type' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        if query.isdigit():
            factory_types = FactoryType.objects.filter(code=query)
        else:
            factory_types = FactoryType.objects.filter(type__icontains=query)

        serializer = FactoryTypeSerializer(factory_types[:8], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
