# Generated by Django 3.0.5 on 2020-06-05 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Stock Name')),
                ('buy_date', models.DateField(verbose_name='Buy Date')),
                ('sell_date', models.DateField(verbose_name='Sold Date')),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Buy Price')),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Sell Price')),
                ('profit', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Profit')),
                ('loss', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='loss')),
                ('units', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
