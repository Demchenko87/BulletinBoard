# Generated by Django 3.1.7 on 2021-03-24 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20210324_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='title',
        ),
        migrations.AddField(
            model_name='delivery',
            name='comment',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Коментарий'),
        ),
    ]