# Generated by Django 3.0.5 on 2020-06-05 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharebazaar_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='loss',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='profit',
        ),
    ]
