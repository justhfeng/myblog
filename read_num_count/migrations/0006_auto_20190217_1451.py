# Generated by Django 2.1.4 on 2019-02-17 06:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('read_num_count', '0005_auto_20190213_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnumdetail',
            name='read_date',
            field=models.DateField(default=datetime.datetime(2019, 2, 17, 6, 51, 34, 583150, tzinfo=utc)),
        ),
    ]
