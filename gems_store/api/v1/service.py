import csv
import io
from datetime import datetime

from deals.models import Customer, Deal, Item
from django.db.models import Model
from django.utils import timezone


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

    def get_unique_values(
        self,
        field_name: str,
        data: list[dict[str, str]],
    ) -> set[str]:
        """Получение множества уникальных значений ключа."""
        unique_values = set()
        for obj in data:
            unique_values.add(obj[field_name])
        return unique_values

    def process_file(self, file: str) -> None:
        """Обработка файла с сделками."""
        io_string = io.StringIO(file)

        headers = list(
            map(str.strip, io_string.readline().split(','))
        )

        parsed_data = list(csv.DictReader(io_string, fieldnames=headers))

        customers_values = self.get_unique_values('customer', parsed_data)
        items_values = self.get_unique_values('item', parsed_data)

        customers = self.__get_objects(Customer, 'login', customers_values)
        items = self.__get_objects(Item, 'name', items_values)

        objects_to_create = []

        for deal in parsed_data:
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
