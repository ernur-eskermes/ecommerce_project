# Generated by Django 3.1.5 on 2021-02-25 11:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Код купона')),
                ('valid_from', models.DateTimeField(verbose_name='Доступен С')),
                ('valid_to', models.DateTimeField(verbose_name='Доступен До')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка %')),
                ('active', models.BooleanField(verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Купон',
                'verbose_name_plural': 'Купоны',
            },
        ),
    ]