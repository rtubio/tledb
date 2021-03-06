# Generated by Django 2.1.5 on 2019-01-10 00:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fetcher', '0002_auto_20190110_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tle',
            name='first_line',
            field=models.CharField(max_length=69, validators=[django.core.validators.RegexValidator(code='invalid_tle_line_1', message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\s-]{69}$')], verbose_name='First line of this TLE'),
        ),
        migrations.AlterField(
            model_name='tle',
            name='second_line',
            field=models.CharField(max_length=69, validators=[django.core.validators.RegexValidator(code='invalid_tle_line_2', message="Alphanumeric or '.-_' required", regex='^[a-zA-Z0-9.\\s-]{69}$')], verbose_name='Second line of this TLE'),
        ),
    ]
