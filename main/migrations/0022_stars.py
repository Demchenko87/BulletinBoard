# Generated by Django 3.1.7 on 2021-03-30 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_bb_invoce'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.CharField(max_length=1, verbose_name='Звезда')),
            ],
            options={
                'verbose_name': 'Звезда',
                'verbose_name_plural': 'Звезды рейтинга',
            },
        ),
    ]