from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.v1.service import Service

service = Service()


@api_view(['POST'])
def add_deals(request):
    """Обработка файла с сделками."""
    try:
        file = request.data['deals']
        decoded_file = file.read().decode()
        service.process_file(decoded_file)
        return Response(status=status.HTTP_200_OK, data={'Status': 'OK'})
    except tuple(settings.ERROR_MESSAGES.keys()) as e:
        error_message = settings.ERROR_MESSAGES[type(e)]
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'Status': 'Error',
                'Desc': error_message,
            }
        )
