# Generated by Django 3.1.7 on 2021-03-18 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='advuser',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name='Аватар'),
        ),
    ]
