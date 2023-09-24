from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.v1.service import Service
from deals.models import Customer, Item
from django.db.models import Sum

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


@api_view(['GET'])
def get_top_customers(request):
    """Получение списка покупателей."""
    top_customers = Customer.objects.annotate(
        spent_money=Sum('deals__total'),
    ).order_by('-spent_money')[:5]

    items_per_customer = Item.objects.filter(
        deals__customer__in=top_customers
    ).values_list(
        'deals__customer__login', 'name'
    ).distinct()

    response = []

    gems_lists = {obj.login: [] for obj in top_customers}
    gems_count = {}

    for i in items_per_customer:
        gems_lists[i[0]].append(i[1])
        gems_count[i[1]] = gems_count.get(i[1], 0) + 1

    for customer in top_customers:
        response.append({
            'username': customer.login,
            'spent_money': customer.spent_money,
            'gems': [i for i in gems_lists[customer.login] if gems_count[i] > 1]
        })

    return Response(status=status.HTTP_200_OK, data={'response': response})
