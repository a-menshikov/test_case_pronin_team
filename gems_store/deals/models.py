from django.db import models


class Customer(models.Model):
    """Модель покупателя."""

    login = models.CharField(
        max_length=128,
        verbose_name='Логин',
        unique=True,
    )

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self) -> str:
        return self.login


class Item(models.Model):
    """Модель товара."""

    name = models.CharField(
        max_length=128,
        verbose_name='Название',
        unique=True,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return self.name


class Deal(models.Model):
    """Модель сделки."""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='deals',
        verbose_name='Покупатель',
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='deals',
        verbose_name='Товар',
    )

    total = models.PositiveIntegerField(
        verbose_name='Сумма',
    )

    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    date = models.DateTimeField(
        verbose_name='Дата',
    )

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
        ordering = ['-date']

    def __str__(self) -> str:
        return f'{self.customer} - {self.item}'
