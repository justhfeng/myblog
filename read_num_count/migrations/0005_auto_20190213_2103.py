# Generated by Django 2.1.4 on 2019-02-13 13:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('read_num_count', '0004_auto_20190213_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnumdetail',
            name='read_date',
            field=models.DateField(default=datetime.datetime(2019, 2, 13, 13, 3, 54, 18548, tzinfo=utc)),
        ),
    ]
