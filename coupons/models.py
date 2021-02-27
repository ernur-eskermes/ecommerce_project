from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код купона')
    valid_from = models.DateTimeField(verbose_name='Доступен С')
    valid_to = models.DateTimeField(verbose_name='Доступен До')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка %')
    active = models.BooleanField(verbose_name='Активен')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'
