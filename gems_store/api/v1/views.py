from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.v1.serializers import TopCustomersSerializer
from api.v1.service import Service

service = Service()


@api_view(['POST'])
def add_deals(request):
    """Обработка файла с сделками."""
    try:
        file = request.data['deals']
        decoded_file = file.read().decode()
        service.process_file(decoded_file)
        cache.clear()
        return Response(status=status.HTTP_201_CREATED, data={'Status': 'OK'})
    except tuple(settings.PARSE_ERROR_MESSAGES.keys()) as e:
        error_message = settings.PARSE_ERROR_MESSAGES[type(e)]
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'Status': 'Error',
                'Desc': error_message,
            }
        )


@cache_page(settings.CACHE_TIME)
@api_view(['GET'])
def get_top_customers(request):
    """Получение списка покупателей."""
    response = service.get_top_customers()
    serializer = TopCustomersSerializer(data=response, many=True)
    try:
        serializer.is_valid(raise_exception=True)
        return Response(
            status=status.HTTP_200_OK,
            data={'response': serializer.data},
        )
    except ValidationError as e:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'Status': 'Error',
                'Desc': f'Что-то пошло не так. {str(e.detail[0])}',
            }
        )
