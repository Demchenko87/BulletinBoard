# Generated by Django 3.1.7 on 2021-03-24 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20210324_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='delivery1',
            field=models.BooleanField(blank=True, db_index=True, default=False, null=True, verbose_name='Новая почта'),
        ),
    ]
