from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F, Sum, DecimalField
from django.utils.translation import gettext_lazy as _


class OrderQuerySet(models.QuerySet):
    def annotate_total_sum(self):
        total_sum = Sum(
            F('items__quantity') * F('items__price')
        )
        return self.annotate(total_sum=total_sum, output_field=DecimalField())


class Order(models.Model):
    class Statuses(models.TextChoices):
        UNTREATED = 'UN', _('Необработанный')
        CANCELED = 'CA', _('Отмененный')
        ACCEPTED = 'AC', _('Принятый')
        PRODUCED = 'PR', _('Приготовленный')
        SHIPPED = 'SH', _('Отгруженный')
        COMPLETED = 'CO', _('Выполненный')

    class PaymentMethods(models.TextChoices):
        CARD = 'CARD', _('Картой')
        CASH = 'CASH', _('Наличные')

    payment_method = models.CharField(
        'метод оплаты',
        max_length=6,
        choices=PaymentMethods.choices,
        db_index=True
    )
    status = models.CharField(
        'статус',
        max_length=2,
        choices=Statuses.choices,
        default=Statuses.UNTREATED,
        db_index=True
    )
    comment = models.TextField(
        "комментарий",
        blank=True,
        help_text='Необязательный комментарий к заказу'
    )
    firstname = models.CharField(
        'имя',
        max_length=50
    )
    lastname = models.CharField(
        'фамилия',
        max_length=50,
    )
    phonenumber = PhoneNumberField(
        'контактный телефон',
        null=False,
        blank=False,
        db_index=True
    )
    address = models.CharField(
        'адрес',
        max_length=50,
    )

    cooking_by = models.ForeignKey(
        'Restaurant',
        verbose_name='готовится в',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    registrated_at = models.DateTimeField(
        'дата и время регистрации',
        default=timezone.now
    )
    called_at = models.DateTimeField(
        'дата и время созвона',
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        'дата и время доставки',
        blank=True,
        null=True
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.address}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    quantity = models.IntegerField(
        'количество',
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        'цена в момент заказа',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    ) 

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'элемент заказа {self.product.name}'


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"
