# Generated by Django 3.1.7 on 2021-03-30 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20210330_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='star',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='звезда'),
        ),
    ]