# Generated by Django 3.1.7 on 2021-03-25 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20210324_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='mastercard',
            field=models.BooleanField(default=False, verbose_name='Mastercard'),
        ),
        migrations.AddField(
            model_name='bb',
            name='money',
            field=models.BooleanField(default=False, verbose_name='Наличный'),
        ),
        migrations.AddField(
            model_name='bb',
            name='visa',
            field=models.BooleanField(default=False, verbose_name='Visa'),
        ),
        migrations.AddField(
            model_name='bb',
            name='сashless',
            field=models.BooleanField(default=False, verbose_name='Безналичный'),
        ),
    ]