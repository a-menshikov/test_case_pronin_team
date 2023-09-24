from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.v1.service import Service

service = Service()


@api_view(['POST'])
def add_deals(request):
    """Обработка файла с сделками."""
    file = request.data['deals']
    decoded_file = file.read().decode()
    service.process_file(decoded_file)
    return Response(status=status.HTTP_200_OK, data={'Status': 'OK'})
