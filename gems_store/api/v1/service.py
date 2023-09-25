import csv
import io
from datetime import datetime

from django.conf import settings
from django.db.models import Model, Sum
from django.utils import timezone

from api.v1.exceptions import FileFormatError
from deals.models import Customer, Deal, Item


class Service:
    """Сервисный репозиторий для операций API."""

    def __get_objects(
        self,
        model: type[Model],
        field_name: str,
        values: set[str],
    ) -> dict[str, Model | None]:
        """Получение списка объектов модели с созданием несуществующих."""
        result: dict[str, Model | None] = {key: None for key in values}

        filter_value = {
            f'{field_name}__in': values,
        }
        exist_objects = model.objects.filter(**filter_value).all()

        for object in exist_objects:
            result[getattr(object, field_name)] = object

        objects_to_create = []

        for key, value in result.items():
            if not value:
                objects_to_create.append(model(**{field_name: key}))

        new_objects = model.objects.bulk_create(objects_to_create)

        for object in new_objects:
            result[getattr(object, field_name)] = object

        return result

    def __get_unique_values(
        self,
        field_name: str,
        data: list[dict[str, str]],
    ) -> set[str]:
        """Получение множества уникальных значений ключа."""
        unique_values = set()
        for obj in data:
            unique_values.add(obj[field_name])
        return unique_values

    def __validate_headers(self, headers: list[str]) -> None:
        """Проверка корректности заголовков."""
        if sorted(settings.HEADERS_LIST) != sorted(headers):
            raise FileFormatError

    def process_file(self, file: str) -> None:
        """Обработка файла со сделками."""
        io_string = io.StringIO(file)

        headers = list(
            map(str.strip, io_string.readline().split(','))
        )
        self.__validate_headers(headers)

        read_data = csv.DictReader(io_string, fieldnames=headers)
        validated_data = [deal for deal in read_data if all(deal.values())]

        customers_values = self.__get_unique_values('customer', validated_data)
        items_values = self.__get_unique_values('item', validated_data)

        customers = self.__get_objects(Customer, 'login', customers_values)
        items = self.__get_objects(Item, 'name', items_values)

        objects_to_create = []

        for deal in validated_data:
            objects_to_create.append(Deal(
                customer=customers[deal['customer']],
                item=items[deal['item']],
                total=int(deal['total']),
                quantity=int(deal['quantity']),
                date=timezone.make_aware(
                    datetime.strptime(deal['date'], '%Y-%m-%d %H:%M:%S.%f'),
                    timezone.get_current_timezone(),
                ),
            ))

        Deal.objects.bulk_create(objects_to_create, ignore_conflicts=True)

    def get_top_customers(self) -> list[dict[str, str | int | list[str]]]:
        """Получение списка топ-покупателей со списком камней."""
        top_customers = Customer.objects.annotate(
            spent_money=Sum('deals__total'),
        ).exclude(spent_money__isnull=True).order_by(
            '-spent_money',
        )[:settings.TOP_CUSTOMER_LIMIT]

        items_per_customer = Item.objects.filter(
            deals__customer__in=top_customers
        ).values_list(
            'deals__customer__login', 'name'
        ).distinct()

        customer_gems: dict[str, list[str]] = {
            obj.login: [] for obj in top_customers
        }
        customer_gems_count: dict[str, int] = {}

        for i in items_per_customer:
            customer_gems[i[0]].append(i[1])
            customer_gems_count[i[1]] = customer_gems_count.get(i[1], 0) + 1

        result = []

        for customer in top_customers:
            result.append({
                'username': customer.login,
                'spent_money': customer.spent_money,
                'gems': [i for i in customer_gems[customer.login]
                         if customer_gems_count[i] >= settings.COMMON_GEMS]
            })

        return result
